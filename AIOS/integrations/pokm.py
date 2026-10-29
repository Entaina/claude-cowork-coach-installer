#!/usr/bin/env python3
"""pOKM: the user's map of documents. Standard library only; no model calls.

Never writes in the user's folders. Its state lives in the coach folder:
pokm/.estado/alcance.json (what is mapped and at which level) and
pokm/.estado/inventario.json (snapshot of what was already processed).

Levels per folder or file, inherited by everything below it:
  indice  folder in the general map plus an index; its documents are opened and described
  mapa    folder only described in pokm/mapa.md; its documents are not opened
  fuera   excluded; never opened or described
A folder under a base without any rule is "sin decidir" and is not mapped.
"""
import argparse
from datetime import datetime
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import time
import zipfile
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[2]
STATE = ROOT / 'pokm' / '.estado'
SCOPE = STATE / 'alcance.json'
SNAPSHOT = STATE / 'inventario.json'
LEVELS = ('indice', 'mapa', 'fuera')
KINDS = {
    'documento': {'.docx', '.doc', '.odt', '.rtf', '.pages'},
    'hoja': {'.xlsx', '.xls', '.ods', '.csv', '.numbers'},
    'presentación': {'.pptx', '.ppt', '.odp', '.key'},
    'pdf': {'.pdf'},
    'texto': {'.md', '.txt'},
    'google': {'.gdoc', '.gsheet', '.gslides', '.gform', '.gdraw', '.gsite', '.gmap'},
    'imagen': {'.jpg', '.jpeg', '.png', '.gif', '.heic', '.webp', '.tif', '.tiff', '.svg'},
    'vídeo': {'.mp4', '.mov', '.avi', '.mkv', '.m4v'},
    'audio': {'.mp3', '.m4a', '.wav', '.aac'},
    'comprimido': {'.zip', '.rar', '.7z'},
}
HIDDEN = re.compile(r'^(\.|~\$|desktop\.ini$|Thumbs\.db$|Icon\r?$)', re.I)


class Fallo(Exception):
    """Visible error; nothing has been written."""


def now():
    return datetime.now().strftime('%Y-%m-%d %H:%M')


def kind(name):
    ext = os.path.splitext(name)[1].lower()
    return next((k for k, exts in KINDS.items() if ext in exts), 'otro')


def human(size):
    for unit in ('B', 'KB', 'MB', 'GB'):
        if size < 1024:
            return f'{size:.0f} {unit}'
        size /= 1024
    return f'{size:.1f} TB'


def norm(path):
    return os.path.normcase(os.path.abspath(os.path.expanduser(str(path))))


def inside(path, folder):
    path, folder = norm(path), norm(folder)
    return path == folder or path.startswith(folder.rstrip(os.sep) + os.sep)


def read_json(path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise Fallo(f'No se puede leer {path.name}: {exc}') from exc


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix='.pokm-', dir=path.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as handle:
            json.dump(data, handle, ensure_ascii=False, indent=1)
            handle.write('\n')
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def load_scope(required=True):
    scope = read_json(SCOPE, None)
    if scope is None:
        if required:
            raise Fallo('El pOKM no está activado: no hay pokm/.estado/alcance.json')
        return None
    if not isinstance(scope.get('bases'), list) or not isinstance(scope.get('reglas'), dict):
        raise Fallo('alcance.json no tiene el formato esperado')
    return scope


def level(scope, path):
    """Longest rule wins; inside a base without a rule means undecided (None)."""
    best, best_len = None, -1
    for rule, data in scope['reglas'].items():
        if inside(path, rule) and len(norm(rule)) > best_len:
            best, best_len = data['nivel'], len(norm(rule))
    if best is None and not any(inside(path, base) for base in scope['bases']):
        return 'fuera'
    return best


def walk(folders, deadline=None, skip=()):
    """Yield files (metadata only) and report visited folders; never opens files."""
    visited, files, complete = set(), {}, True
    for folder in folders:
        stack = [norm(folder)]
        while stack:
            if deadline and time.monotonic() > deadline:
                complete = False
                break
            current = stack.pop()
            if any(inside(current, s) for s in skip):
                continue
            try:
                entries = sorted(os.scandir(current), key=lambda e: e.name)
            except OSError:
                continue
            for entry in entries:
                if HIDDEN.match(entry.name):
                    continue
                try:
                    if entry.is_symlink():
                        continue
                    if entry.is_dir():
                        stack.append(norm(entry.path))
                    elif entry.is_file():
                        st = entry.stat()
                        files[norm(entry.path)] = {
                            'bytes': st.st_size,
                            'mtime': int(st.st_mtime),
                            'tipo': kind(entry.name),
                        }
                except OSError:
                    continue
            visited.add(current)
        if not complete:
            break
    return files, visited, complete


def own_folder():
    return [norm(ROOT)]


# --- inventario -----------------------------------------------------------

def cmd_inventario(args):
    deadline = time.monotonic() + args.tiempo_max if args.tiempo_max else None
    files, _, complete = walk(args.carpetas, deadline, own_folder())
    groups = {}
    for path, data in files.items():
        base = next(norm(c) for c in args.carpetas if inside(path, c))
        parts = os.path.relpath(os.path.dirname(path), base).split(os.sep)
        parts = [] if parts == ['.'] else parts
        for depth in range(0, min(len(parts), args.niveles) + 1):
            key = (base, os.sep.join(parts[:depth]))
            group = groups.setdefault(key, {'n': 0, 'bytes': 0, 'ultimo': 0, 'tipos': {}})
            group['n'] += 1
            group['bytes'] += data['bytes']
            group['ultimo'] = max(group['ultimo'], data['mtime'])
            group['tipos'][data['tipo']] = group['tipos'].get(data['tipo'], 0) + 1
    for (base, rel), group in sorted(groups.items()):
        depth = 0 if not rel else rel.count(os.sep) + 1
        types = ', '.join(f'{k} {v}' for k, v in sorted(group['tipos'].items(), key=lambda x: -x[1]))
        last = datetime.fromtimestamp(group['ultimo']).strftime('%Y-%m-%d')
        print(f"{'  ' * depth}{rel or base} — {group['n']} archivos, {human(group['bytes'])}, "
              f"último cambio {last} ({types})")
    if not complete:
        print('INCOMPLETO: se agotó el tiempo; el resumen solo cubre lo recorrido.')


# --- alcance --------------------------------------------------------------

def cmd_alcance(args):
    if args.accion == 'activar':
        if not args.rutas:
            raise Fallo('Indica al menos una carpeta base')
        missing = [r for r in args.rutas if not os.path.isdir(r)]
        if missing:
            raise Fallo('No existe o no es carpeta: ' + ', '.join(missing))
        scope = load_scope(required=False) or {'activo': True, 'bases': [], 'reglas': {}, 'creado': now()}
        scope['activo'] = True
        for base in args.rutas:
            if norm(base) not in scope['bases']:
                scope['bases'].append(norm(base))
        write_json(SCOPE, scope)
        print('Activado. Bases: ' + '; '.join(scope['bases']))
        return
    scope = load_scope()
    if args.accion == 'ver':
        print(f"Activo: {'sí' if scope.get('activo') else 'no'}")
        for base in scope['bases']:
            print(f'BASE\t{base}')
        for rule, data in sorted(scope['reglas'].items()):
            reason = f"\t{data['motivo']}" if data.get('motivo') else ''
            print(f"{data['nivel'].upper()}\t{rule}{reason}")
        return
    if args.accion == 'desactivar':
        scope['activo'] = False
        write_json(SCOPE, scope)
        print('Desactivado: la revisión diaria deja de mantener el mapa. pokm/ se conserva.')
        return
    if not args.rutas:
        raise Fallo('Indica la carpeta o el archivo')
    for target in args.rutas:
        if not any(inside(target, base) for base in scope['bases']):
            raise Fallo(f'Fuera de las bases del pOKM: {target}')
        if args.accion == 'poner':
            if args.nivel not in LEVELS:
                raise Fallo('Nivel: indice, mapa o fuera')
            if args.nivel == 'fuera' and not args.motivo:
                raise Fallo('«fuera» necesita --motivo')
            scope['reglas'][norm(target)] = {'nivel': args.nivel, 'motivo': args.motivo or '', 'fecha': now()}
        elif args.accion == 'quitar':
            scope['reglas'].pop(norm(target), None)
    write_json(SCOPE, scope)
    print(f"Hecho: {args.accion} {', '.join(args.rutas)}")


# --- cambios y marcar -----------------------------------------------------

def container(scope, folder):
    """An undecided folder that only holds decided ones (e.g. «Unidades compartidas»)."""
    return any(inside(rule, folder) and norm(rule) != norm(folder) for rule in scope['reglas'])


def current_state(scope, seconds):
    deadline = time.monotonic() + seconds if seconds else None
    files, visited, complete = walk(scope['bases'], deadline, own_folder())
    in_scope = {}
    for path, data in files.items():
        lvl = level(scope, path)
        if lvl in ('indice', 'mapa'):
            in_scope[path] = dict(data, nivel=lvl)
    # Report only the topmost undecided item: a folder or loose file whose parent is a
    # base or a container. Everything below an undecided folder stays out with it.
    undecided = set()
    for item in list(visited) + list(files):
        if norm(item) in scope['bases'] or level(scope, item) is not None:
            continue
        if os.path.isdir(item) and container(scope, item):
            continue
        parent = os.path.dirname(item)
        if parent in scope['bases'] or (level(scope, parent) is None and container(scope, parent)):
            undecided.add(item)
    return in_scope, visited, complete, sorted(undecided)


def diff(scope, snapshot, seconds):
    current, visited, complete, undecided = current_state(scope, seconds)
    before = snapshot.get('archivos', {})
    changes = []
    for path, data in current.items():
        old = before.get(path)
        if old is None:
            changes.append(('NUEVO', path, data))
        elif (old['bytes'], old['mtime']) != (data['bytes'], data['mtime']):
            changes.append(('MODIFICADO', path, data))
    for path, old in before.items():
        if path in current:
            continue
        # Not seen: deleted only if its folder was listed in full (a timeout is not a
        # deletion). If the file still exists, it left the scope: it is removed from the
        # map just the same, but must not be described again.
        folder = os.path.dirname(path)
        if folder in visited or not os.path.isdir(folder):
            changes.append(('SALE' if os.path.exists(path) else 'BORRADO', path, old))
    new_undecided = [f for f in undecided if f not in snapshot.get('avisadas', [])]
    return changes, current, complete, new_undecided


def cmd_cambios(args):
    scope = load_scope()
    if not scope.get('activo'):
        print('pOKM desactivado: no hay nada que mantener.')
        return
    snapshot = read_json(SNAPSHOT, {'archivos': {}})
    changes, _, complete, undecided = diff(scope, snapshot, args.tiempo_max)
    reading = [c for c in changes if c[0] in ('NUEVO', 'MODIFICADO') and c[2].get('nivel') == 'indice']
    # Within the per-pass limit: modified first, then new files in folders already mapped,
    # then folders that are new as a whole (a bulk drop must not crowd out an addendum).
    known = {os.path.dirname(p) for p in snapshot.get('archivos', {})}
    reading.sort(key=lambda c: (c[0] != 'MODIFICADO', os.path.dirname(c[1]) not in known, c[1]))
    others = [c for c in changes if c not in reading]
    shown = reading[:args.limite]
    later = len(reading) - len(shown)
    print(f"Desde {snapshot.get('fecha', 'la activación')}: {len(changes)} cambios "
          f"({len(reading)} para leer, {len(others)} sin lectura); {len(undecided)} sin decidir")
    for state, path, data in shown + others:
        stamp = datetime.fromtimestamp(data['mtime']).strftime('%Y-%m-%d %H:%M')
        print(f"{state}\t{data.get('nivel', '-')}\t{data['tipo']}\t{stamp}\t{human(data['bytes'])}\t{path}")
    for folder in undecided:
        print(f'SIN-DECIDIR\t-\tcarpeta\t-\t-\t{folder}')
    if later:
        print(f'PENDIENTE\t{later} documentos más para leer: quedan para la próxima pasada.')
    if not complete:
        print('INCOMPLETO\tse agotó el tiempo: lo no recorrido no cuenta como borrado y sigue en la próxima pasada.')


def cmd_marcar(args):
    scope = load_scope()
    snapshot = read_json(SNAPSHOT, {'archivos': {}, 'avisadas': []})
    snapshot.setdefault('avisadas', [])
    files = snapshot.setdefault('archivos', {})
    if args.todo or args.sin_lectura or args.pasada:
        changes, current, complete, undecided = diff(scope, snapshot, args.tiempo_max)
        reading = [c for c in changes if c[0] in ('NUEVO', 'MODIFICADO') and c[2].get('nivel') == 'indice']
        known = {os.path.dirname(p) for p in files}
        reading.sort(key=lambda c: (c[0] != 'MODIFICADO', os.path.dirname(c[1]) not in known, c[1]))
        this_pass = {c[1] for c in reading[:args.limite]} if args.pasada else set()
        for state, path, data in changes:
            if (args.sin_lectura or args.pasada) and state in ('NUEVO', 'MODIFICADO') and \
                    data.get('nivel') == 'indice' and path not in this_pass:
                continue
            if state in ('BORRADO', 'SALE'):
                files.pop(path, None)
            else:
                files[path] = {k: data[k] for k in ('bytes', 'mtime', 'tipo', 'nivel')}
        snapshot['avisadas'] = sorted(set(snapshot['avisadas']) | set(undecided))
        if not complete:
            print('INCOMPLETO: solo se marca lo recorrido; el resto sigue pendiente.')
    for target in args.rutas:
        path = norm(target)
        if not os.path.exists(path):
            files.pop(path, None)
            continue
        if not os.path.isfile(path):
            raise Fallo(f'No es un archivo: {target}')
        lvl = level(scope, path)
        if lvl not in ('indice', 'mapa'):
            files.pop(path, None)
            continue
        st = os.stat(path)
        files[path] = {'bytes': st.st_size, 'mtime': int(st.st_mtime), 'tipo': kind(path), 'nivel': lvl}
    snapshot['fecha'] = now()
    write_json(SNAPSHOT, snapshot)
    print(f"Foto actualizada: {len(files)} archivos dentro del pOKM.")


# --- estado ---------------------------------------------------------------

def cmd_estado(args):
    scope = load_scope(required=False)
    if scope is None:
        print('pOKM: sin activar.')
        return
    snapshot = read_json(SNAPSHOT, {'archivos': {}})
    print(f"pOKM: {'activo' if scope.get('activo') else 'desactivado'}; "
          f"{len(scope['bases'])} bases, {len(scope['reglas'])} reglas, "
          f"{len(snapshot.get('archivos', {}))} archivos en la foto del {snapshot.get('fecha', '—')}.")


# --- texto ----------------------------------------------------------------

def xml_text(data, tag):
    root = ElementTree.fromstring(data)
    return [node.text or '' for node in root.iter() if node.tag.endswith(tag)]


def text_docx(z):
    root = ElementTree.fromstring(z.read('word/document.xml'))
    out = []
    for paragraph in root.iter():
        if paragraph.tag.endswith('}p'):
            line = ''.join(n.text or '' for n in paragraph.iter() if n.tag.endswith('}t'))
            if line.strip():
                out.append(line)
    return '\n'.join(out)


def text_pptx(z):
    slides = sorted((n for n in z.namelist() if re.match(r'ppt/slides/slide\d+\.xml$', n)),
                    key=lambda n: int(re.findall(r'\d+', n)[-1]))
    return '\n'.join(f'[{i}] ' + ' · '.join(t for t in xml_text(z.read(n), '}t') if t.strip())
                     for i, n in enumerate(slides, 1))


def text_xlsx(z):
    names = z.namelist()
    shared = []
    if 'xl/sharedStrings.xml' in names:
        root = ElementTree.fromstring(z.read('xl/sharedStrings.xml'))
        for item in root:
            if item.tag.endswith('}si'):
                shared.append(''.join(n.text or '' for n in item.iter() if n.tag.endswith('}t')))
    sheets = [s.get('name') for s in ElementTree.fromstring(z.read('xl/workbook.xml')).iter()
              if s.tag.endswith('}sheet')]
    paths = sorted((n for n in names if re.match(r'xl/worksheets/sheet\d+\.xml$', n)),
                   key=lambda n: int(re.findall(r'\d+', n)[-1]))
    out = []
    for i, name in enumerate(paths):
        out.append(f'## {sheets[i] if i < len(sheets) else name}')
        for row in ElementTree.fromstring(z.read(name)).iter():
            if not row.tag.endswith('}row'):
                continue
            cells = []
            for cell in row:
                value = next((n.text for n in cell.iter() if n.tag.endswith('}v') or n.tag.endswith('}t')), '') or ''
                if cell.get('t') == 's' and value.isdigit() and int(value) < len(shared):
                    value = shared[int(value)]
                cells.append(value)
            out.append(' | '.join(cells))
    return '\n'.join(out)


def text_odf(z):
    return '\n'.join(t for t in xml_text(z.read('content.xml'), '}p') if t.strip())


def readable(path):
    """Only the coach folder and what the active pOKM maps («indice» or «mapa»).

    The app lets this program run without asking; it must not become a way to read any
    file on the computer, nor to open what the user excluded.
    """
    real = os.path.realpath(path)  # a link inside a base must not reach outside it
    if inside(path, ROOT) and inside(real, os.path.realpath(ROOT)):
        return None
    scope = load_scope(required=False)
    if not scope or not scope.get('activo'):
        return 'El pOKM no está activo: este programa solo lee la carpeta del coach.'
    if not any(inside(real, os.path.realpath(base)) for base in scope['bases']):
        return 'Fuera de las carpetas del pOKM: no se lee.'
    lvl = level(scope, path)
    if lvl == 'fuera':
        return ('Está fuera del pOKM: no se lee. Si el usuario quiere, que lo abra él o que lo saque '
                'de «fuera» en el mapa.')
    if lvl is None:
        return 'Está sin decidir en el pOKM: no se lee hasta que el usuario decida su nivel.'
    return None


def cmd_texto(args):
    path = args.archivo
    ext = os.path.splitext(path)[1].lower()
    if not os.path.isfile(path):
        raise Fallo(f'No existe: {path}')
    refusal = readable(path)
    if refusal:
        raise Fallo(refusal + ' Fuera del alcance, pídele permiso para leerlo con la app.')
    try:
        if ext in KINDS['google']:
            data = json.loads(Path(path).read_text(encoding='utf-8'))
            link = data.get('url') or data.get('doc_id') or '(sin enlace)'
            out = f'SOLO EN LÍNEA: el contenido no está en el ordenador. Enlace: {link}'
        elif ext == '.pdf':
            tool = shutil.which('pdftotext')
            if tool:
                out = subprocess.run([tool, '-layout', path, '-'], capture_output=True, text=True,
                                     timeout=60).stdout
            else:
                out = 'PDF: léelo con el lector de PDF de la app; aquí no hay extractor.'
        elif ext in ('.docx', '.pptx', '.xlsx', '.odt', '.ods', '.odp'):
            with zipfile.ZipFile(path) as z:
                out = {'.docx': text_docx, '.pptx': text_pptx, '.xlsx': text_xlsx}.get(ext, text_odf)(z)
        elif ext in ('.md', '.txt', '.csv'):
            out = Path(path).read_text(encoding='utf-8', errors='replace')
        elif ext in ('.doc', '.xls', '.ppt'):
            out = f'Formato antiguo ({ext}): no se extrae texto. Descríbelo por su nombre y su carpeta.'
        else:
            out = f'Formato {ext or "sin extensión"}: no se extrae texto.'
    except (zipfile.BadZipFile, KeyError, ElementTree.ParseError, OSError, ValueError,
            subprocess.SubprocessError) as exc:
        out = f'No se pudo leer ({type(exc).__name__}). Descríbelo por su nombre y su carpeta.'
    print(out[:args.max] + ('\n[… recortado]' if len(out) > args.max else ''))


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest='command', required=True)
    p = commands.add_parser('estado', help='¿Está activo? Bases, reglas y última foto')
    p = commands.add_parser('inventario', help='Resumen por carpetas sin abrir archivos; no guarda nada')
    p.add_argument('carpetas', nargs='+')
    p.add_argument('--niveles', type=int, default=2)
    p.add_argument('--tiempo-max', type=int, default=300, help='segundos; 0 sin límite')
    p = commands.add_parser('alcance', help='activar, ver, poner, quitar o desactivar')
    p.add_argument('accion', choices=['activar', 'ver', 'poner', 'quitar', 'desactivar'])
    p.add_argument('rutas', nargs='*')
    p.add_argument('--nivel', choices=LEVELS)
    p.add_argument('--motivo')
    p = commands.add_parser('cambios', help='Nuevo, modificado, borrado, fuera del alcance y sin decidir desde la última foto')
    p.add_argument('--limite', type=int, default=30, help='máximo de documentos para leer en esta pasada')
    p.add_argument('--tiempo-max', type=int, default=300)
    p = commands.add_parser('marcar', help='Actualiza la foto con lo ya procesado')
    p.add_argument('rutas', nargs='*')
    p.add_argument('--todo', action='store_true', help='todo lo que hay dentro del alcance')
    p.add_argument('--sin-lectura', action='store_true', help='borrados, nivel mapa y carpetas sin decidir')
    p.add_argument('--pasada', action='store_true',
                   help='lo de --sin-lectura más los documentos que dio «cambios» con el mismo --limite, ya procesados')
    p.add_argument('--limite', type=int, default=30)
    p.add_argument('--tiempo-max', type=int, default=300)
    p = commands.add_parser('texto', help='Texto de Word, Excel, PowerPoint, OpenDocument, texto y accesos de Google')
    p.add_argument('archivo')
    p.add_argument('--max', type=int, default=4000)
    args = parser.parse_args()
    handler = {'estado': cmd_estado, 'inventario': cmd_inventario, 'alcance': cmd_alcance,
               'cambios': cmd_cambios, 'marcar': cmd_marcar, 'texto': cmd_texto}[args.command]
    try:
        handler(args)
    except Fallo as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        sys.exit(2)


if __name__ == '__main__':
    main()
