#!/usr/bin/env python3
"""Local Claude Code adapter. No model calls, global scan, or third-party packages.

The registered JSONL format is internal to Claude Code (tested with 2.1.286).
Unknown/missing records reduce coverage; this is never a complete history API.
"""
import argparse
from datetime import date, datetime, timedelta, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import sys
import tempfile
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

ROOT = Path(__file__).resolve().parents[2]
STATE = Path('.claude/coach-local')
MANIFEST = STATE / 'managed.json'
DEFAULT_TIMEZONE = 'Europe/Madrid'
# ME.md line written by the installer interview, e.g. "Zona horaria: America/Mexico_City".
TIMEZONE_LINE = re.compile(r'^[ \t]*(?:[-*][ \t]+)?\**Zona horaria\**[ \t]*:\**[ \t]*`?([A-Za-z0-9_+\-]+(?:/[A-Za-z0-9_+\-]+)*)`?', re.M)
MAX_LINE = 8 * 1024 * 1024
MAX_BYTES = 32 * 1024 * 1024
MAX_MESSAGES = 1000
MAX_TEXT = 64000


class Refusal(ValueError):
    """A conflict must be resolved before any installation write."""


def encoded(value):
    return json.dumps(value, ensure_ascii=False, indent=2) + '\n'


def digest(value):
    return hashlib.sha256(value.encode('utf-8')).hexdigest()


def instant(value):
    if not isinstance(value, str):
        raise ValueError('Timestamp must be a string')
    parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if parsed.tzinfo is None:
        raise ValueError('Timestamp without timezone')
    return parsed


def local_path(root, relative):
    """Reject symlink destinations, including their existing parent directories."""
    path = root / relative
    for part in [path, *path.parents]:
        if part == root:
            break
        if part.is_symlink():
            raise Refusal(f'Enlace de sistema no admitido: {relative}')
    if path.exists() and not path.is_file():
        raise Refusal(f'El destino no es un archivo: {relative}')
    return path


def load_object(path):
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise Refusal(f'JSON no legible: {path.name}') from exc
    if not isinstance(data, dict):
        raise Refusal(f'El JSON debe ser un objeto: {path.name}')
    return data


def write_atomic(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix='.coach-', dir=path.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as handle:
            handle.write(content)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def canonical_wrappers(root):
    """Read the package's deliberately limited, folded-block frontmatter format."""
    wrappers = {}
    catalogue = (root / 'AIOS/mapa-skills.md').read_text(encoding='utf-8')
    for path in sorted((root / 'AIOS/skills').glob('*/SKILL.md')):
        text = path.read_text(encoding='utf-8')
        header = re.match(r'\A---\n(.*?)\n---(?:\n|$)', text, re.S)
        if not header:
            raise Refusal(f'Frontmatter no reconocido: {path.parent.name}')
        name = re.search(r'^name: ([a-z0-9]+(?:-[a-z0-9]+)*)$', header[1], re.M)
        description = re.search(r'^description: >-\n((?:  [^\n]*(?:\n|$))+)', header[1], re.M)
        status = re.search(r'^  status: (active|draft|retired)$', header[1], re.M)
        if not name or not description or not status or name[1] != path.parent.name:
            raise Refusal(f'Metadatos no reconocidos: {path.parent.name}')
        if status[1] != 'active':
            continue
        if not re.search(r'^- \*\*' + re.escape(name[1]) + r'\*\*', catalogue, re.M):
            raise Refusal(f'Skill activa sin registrar: {name[1]}')
        words = ' '.join(line.strip() for line in description[1].splitlines())
        if not words or len(words) > 1024 or len(name[1]) > 64 or name[1] == 'coach-review':
            raise Refusal(f'Metadatos nativos no válidos: {name[1]}')
        relative = f'.claude/skills/{name[1]}/SKILL.md'
        wrappers[relative] = (
            f'---\nname: {name[1]}\ndescription: >-\n{description[1].rstrip()}\n---\n\n'
            'Lee completo `${CLAUDE_SKILL_DIR}/../../../AIOS/skills/'
            f'{name[1]}/SKILL.md` y ejecuta su workflow. '
            'Las rutas del canónico se resuelven desde la raíz del coach, '
            'tres niveles por encima de CLAUDE_SKILL_DIR.\n'
        )
    if not wrappers:
        raise Refusal('No hay skills canónicas activas')
    wrappers['.claude/skills/coach-review/SKILL.md'] = '''---
name: coach-review
description: Revisa el día del coach local; genera diario y propuestas de aprendizaje y proyectos en orden.
---

La raíz del coach es `${CLAUDE_SKILL_DIR}/../../..`.
Lee `AIOS/entornos-locales.md` desde esa raíz. Ejecuta el Learning System
según `AIOS/systems/learning-system.md` y después el Sistema Proyectos y Áreas
según `AIOS/systems/proyectos-y-areas.md`, para la misma fecha y sobre el mismo log.
Fecha solicitada (opcional): $ARGUMENTS. Si falta, usa hoy en la zona horaria del usuario
(línea «Zona horaria» de ME.md; Europe/Madrid si no consta).
Completa ambas fases antes de presentar sus propuestas; espera la confirmación
del usuario antes de aplicarlas. No crees ninguna programación por esta petición.
'''
    return wrappers


def hook_command(root):
    # Pin the installed module: a nested project cannot shadow the parent hook.
    # Reinstall after moving the coach to refresh this local absolute path.
    module = root.resolve() / 'AIOS/integrations/claude_code.py'
    return 'python3 ' + shlex.quote(str(module)) + ' hook'


def install(root, apply=False):
    root = root.resolve()
    files = canonical_wrappers(root)
    manifest_path = local_path(root, MANIFEST)
    previous = load_object(manifest_path) if manifest_path.exists() else {}
    old_files = previous.get('files', {})
    if not isinstance(old_files, dict) or previous.get('schema', 1) != 1:
        raise Refusal('Manifiesto de instalación incompatible')
    orphaned = sorted(set(old_files) - set(files))
    if orphaned:
        raise Refusal('Wrappers gestionados sin canónico activo; decide cómo retirarlos o conservarlos: '
                      + ', '.join(orphaned))
    for relative, content in files.items():
        path = local_path(root, relative)
        if not path.exists() and relative in old_files:
            raise Refusal(f'Wrapper gestionado eliminado; decide antes de restaurarlo: {relative}')
        if path.exists():
            existing = path.read_text(encoding='utf-8')
            if existing != content and digest(existing) != old_files.get(relative):
                raise Refusal(f'Wrapper existente personalizado o ajeno: {relative}')

    settings_path = local_path(root, '.claude/settings.json')
    settings = load_object(settings_path) if settings_path.exists() else {}
    if settings.get('disableAllHooks') is True:
        raise Refusal('Los hooks están desactivados en este proyecto; decide antes de instalar')
    hooks = settings.setdefault('hooks', {})
    if not isinstance(hooks, dict):
        raise Refusal('hooks no es un objeto')
    groups = hooks.setdefault('SessionStart', [])
    if not isinstance(groups, list):
        raise Refusal('SessionStart no es una lista')
    command = hook_command(root)
    old_command = previous.get('hook_command')
    found = False
    for group in groups:
        if not isinstance(group, dict) or not isinstance(group.get('hooks'), list):
            raise Refusal('Grupo SessionStart no reconocido')
        for hook in group['hooks']:
            if not isinstance(hook, dict):
                raise Refusal('Hook SessionStart no reconocido')
            if hook.get('type') == 'command' and (hook.get('command') == command or
                    (old_command is not None and hook.get('command') == old_command)):
                if found:
                    raise Refusal('Hook del coach duplicado; resuélvelo antes de instalar')
                matcher = group.get('matcher', '')
                try:
                    matches_all = isinstance(matcher, str) and (matcher in ('', '*') or
                        all(re.search(matcher, source) for source in ('startup', 'resume', 'clear', 'compact')))
                except re.error:
                    matches_all = False
                if not matches_all:
                    raise Refusal('El matcher del hook del coach excluye startup, resume, clear o compact; conserva y resuelve la personalización')
                if any(item.get('disabled') is True or item.get('enabled') is False
                       for item in (group, hook)) or hook.get('async') is True:
                    raise Refusal('El hook del coach está desactivado o es asíncrono; resuelve su configuración')
                timeout = hook.get('timeout', 600)
                if isinstance(timeout, bool) or not isinstance(timeout, (int, float)) or timeout <= 0:
                    raise Refusal('El timeout del hook del coach impide verificar el registro; resuelve su configuración')
                if old_command and hook['command'] == old_command:
                    hook['command'] = command
                found = True
    if not found and old_command is not None:
        raise Refusal('El hook gestionado se ha modificado o retirado; decide antes de reinstalarlo')
    if not found:
        groups.append({'hooks': [{'type': 'command', 'command': command}]})
    files['.claude/settings.json'] = encoded(settings)
    ignore_path = local_path(root, '.claude/.gitignore')
    ignore = ignore_path.read_text(encoding='utf-8') if ignore_path.exists() else ''
    if 'coach-local/' not in ignore.splitlines():
        ignore = ignore.rstrip('\n') + ('\n' if ignore else '') + 'coach-local/\n'
    files['.claude/.gitignore'] = ignore
    # Remember only managed wrappers; settings and ignore files always merge.
    hashes = dict(old_files)
    hashes.update({relative: digest(content) for relative, content in files.items()
                   if relative.startswith('.claude/skills/')})
    files[str(MANIFEST)] = encoded({'schema': 1, 'files': hashes, 'hook_command': command})
    changes = []
    for relative, content in files.items():
        path = local_path(root, relative)
        if not path.exists() or path.read_text(encoding='utf-8') != content:
            changes.append(relative)
    if apply:
        # Every destination/conflict was inspected before the first write.
        for relative in changes:
            write_atomic(root / relative, files[relative])
    return {'status': 'applied' if apply else 'preview', 'root': str(root),
            'changed': changes, 'wrappers': len(hashes), 'global_changes': False}


def record_session(root, event, now=None):
    root = root.resolve()
    if event.get('hook_event_name') != 'SessionStart':
        raise Refusal('Se esperaba SessionStart')
    sid = event.get('session_id', '')
    if not isinstance(sid, str) or not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9_-]{0,127}', sid):
        raise Refusal('ID de sesión no válido')
    cwd = Path(event.get('cwd', '')).resolve()
    transcript = Path(event.get('transcript_path', ''))
    if not event.get('cwd') or not Path(event['cwd']).is_absolute() or not cwd.is_relative_to(root):
        raise Refusal('Sesión de otra carpeta')
    if not transcript.is_absolute() or transcript.name != sid + '.jsonl' or transcript.is_symlink():
        raise Refusal('Ruta de transcripción no reconocida')
    transcript = transcript.resolve()
    path = local_path(root, STATE / 'sessions' / (sid + '.json'))
    registration = {'session_id': sid, 'cwd': str(cwd), 'transcript_path': str(transcript),
                    'registered_at': (now or datetime.now(timezone.utc)).isoformat()}
    if path.exists():
        existing = load_object(path)
        if any(existing.get(key) != registration[key] for key in ('session_id', 'transcript_path')):
            raise Refusal('La sesión registrada cambió de ID o transcripción')
        previous_cwd = Path(existing['cwd'])
        if not previous_cwd.is_absolute() or not previous_cwd.resolve().is_relative_to(root):
            raise Refusal('La sesión registrada pertenece a otra carpeta')
        instant(existing['registered_at'])
        return
    write_atomic(path, encoded(registration))


COMMAND_ENVELOPE = re.compile(
    r'\A\s*<command-message>[^<>]+</command-message>\s*'
    r'<command-name>/[^<>]+</command-name>'
    r'(?:\s*<command-args>(.*?)</command-args>)?\s*\Z', re.S
)


MECHANICAL = re.compile(
    r'^\s*(?:<(?:(?:local-command|command|bash|task-notification|system-reminder|teammate-message)[\w-]*)\b'
    r'|\[Request interrupted|This session is being continued from a previous conversation)'
)


def message_text(record):
    if any(record.get(flag) for flag in ('isMeta', 'isSidechain', 'isCompactSummary', 'isSynthetic')):
        return None
    message = record.get('message')
    if not isinstance(message, dict) or message.get('role') != record.get('type'):
        raise ValueError('Unknown message structure')
    content = message.get('content')
    if isinstance(content, str):
        text = content
    elif isinstance(content, list):
        known_blocks = {'text', 'image', 'document', 'thinking', 'redacted_thinking',
                        'tool_use', 'server_tool_use', 'tool_result', 'web_search_tool_result',
                        'web_fetch_tool_result', 'mcp_tool_use', 'mcp_tool_result', 'container_upload'}
        if any(not isinstance(block, dict) or block.get('type') not in known_blocks
               or (block.get('type') == 'text' and not isinstance(block.get('text'), str))
               for block in content):
            raise ValueError('Unknown content structure')
        if any(isinstance(block, dict) and block.get('type') == 'tool_result' for block in content):
            return None
        text = '\n'.join(block['text'] for block in content if isinstance(block, dict)
                         and block.get('type') == 'text' and isinstance(block.get('text'), str))
    else:
        raise ValueError('Unknown content structure')
    if record.get('type') == 'user':
        envelope = COMMAND_ENVELOPE.fullmatch(text)
        if envelope:
            # Native slash arguments are human input, not the expanded skill body.
            # Preserve the source metadata, but never execute the command or its args.
            text = (envelope[1] or '').strip()
    return text if text.strip() and not MECHANICAL.match(text) else None


def bounded_lines(handle, on_error):
    """Read a snapshot's final window; retain real byte offsets, not guessed lines."""
    size = os.fstat(handle.fileno()).st_size
    start = max(0, size - MAX_BYTES)
    number = 0 if start == 0 else None

    def chunk():
        remaining = size - handle.tell()
        return handle.readline(min(MAX_LINE + 1, remaining)) if remaining > 0 else b''

    if start:
        on_error('transcript_tail_window', None, start)
        handle.seek(start - 1)
        if handle.read(1) != b'\n':
            # Discard the unknown first fragment in bounded chunks, even if huge.
            while True:
                raw = chunk()
                if not raw or raw.endswith(b'\n'):
                    break
    while handle.tell() < size:
        offset = handle.tell()
        raw = chunk()
        if not raw:
            break
        if number is not None:
            number += 1
        if len(raw) > MAX_LINE:
            on_error('transcript_line_size_limit', number, offset)
            while raw and not raw.endswith(b'\n'):
                raw = chunk()
            continue
        yield raw, number, offset


def user_timezone(root, explicit=None):
    """Explicit --tz first, then the ME.md line, then the pre-2.3.0 default."""
    if explicit:
        try:
            return ZoneInfo(explicit), explicit, 'argument'
        except (ZoneInfoNotFoundError, ValueError):
            raise ValueError('Zona horaria desconocida: ' + explicit)
    try:
        match = TIMEZONE_LINE.search((root / 'ME.md').read_text(encoding='utf-8'))
    except (OSError, UnicodeDecodeError):
        match = None
    if match:
        try:
            return ZoneInfo(match[1]), match[1], 'ME.md'
        except (ZoneInfoNotFoundError, ValueError):
            pass
    return ZoneInfo(DEFAULT_TIMEZONE), DEFAULT_TIMEZONE, 'default'


def history(root, day, tz=None):
    root = root.resolve()
    selected = date.fromisoformat(day)
    zone, zone_name, zone_source = user_timezone(root, tz)
    start = datetime.combine(selected, datetime.min.time(), zone)
    end = datetime.combine(selected + timedelta(days=1), datetime.min.time(), zone)
    result = {'date': day, 'timezone': zone_name, 'timezone_source': zone_source, 'root': str(root),
              'interval': {'start': start.isoformat(), 'end': end.isoformat()},
              'coverage': {'status': 'partial', 'reason': 'Solo sesiones registradas desde el alta del hook; formato JSONL interno.'},
              'sessions': [], 'messages': [], 'errors': [], 'errors_omitted': 0}

    def error(code, session=None, line=None, byte_offset=None):
        issue = {'code': code}
        if session:
            issue['session_id'] = session
        if line is not None:
            issue['line'] = line
        if byte_offset is not None:
            issue['byte_offset'] = byte_offset
        if len(result['errors']) < 20:
            result['errors'].append(issue)
        else:
            result['errors_omitted'] += 1

    registry = root / STATE / 'sessions'
    if not registry.exists():
        error('no_registered_sessions')
        return result
    if registry.is_symlink() or (root / STATE).is_symlink() or (root / '.claude').is_symlink():
        error('invalid_registry')
        return result
    seen = set()
    for registration_path in sorted(registry.glob('*.json')):
        sid = registration_path.stem
        try:
            local_path(root, registration_path.relative_to(root))
            registration = load_object(registration_path)
            cwd = Path(registration['cwd'])
            path = Path(registration['transcript_path'])
            registered = instant(registration['registered_at'])
            if (registration['session_id'] != sid or not cwd.is_absolute()
                    or not cwd.resolve().is_relative_to(root)):
                raise Refusal('Registro de otra carpeta')
            if not path.is_absolute() or path.name != sid + '.jsonl' or path.is_symlink():
                raise Refusal('Ruta de transcripción no válida')
        except (KeyError, TypeError, ValueError, OSError):
            error('invalid_registration', sid)
            continue
        if registered >= end:
            continue
        try:
            handle = path.open('rb')
        except OSError:
            error('transcript_unavailable', sid)
            continue
        result['sessions'].append(sid)
        with handle:
            report = lambda code, line, offset: error(code, sid, line, offset)
            for raw, number, byte_offset in bounded_lines(handle, report):
                try:
                    record = json.loads(raw)
                except (ValueError, UnicodeError):
                    error('invalid_jsonl', sid, number, byte_offset)
                    continue
                if not isinstance(record, dict):
                    error('unknown_record_format', sid, number, byte_offset)
                    continue
                if record.get('type') not in ('user', 'assistant'):
                    if record.get('type') not in {'system', 'progress', 'summary', 'file-history-snapshot',
                            'queue-operation', 'last-prompt', 'attachment', 'atis-latch', 'cost-state',
                            'custom-title', 'agent-name',
                            'agent-color', 'tag', 'pr-link', 'saved_hook_context', 'mode'}:
                        error('unknown_record_type', sid, number, byte_offset)
                    continue
                if record.get('sessionId') != sid:
                    error('session_mismatch', sid, number, byte_offset)
                    continue
                try:
                    message_cwd = Path(record['cwd'])
                    if not message_cwd.is_absolute() or not message_cwd.resolve().is_relative_to(root):
                        error('cwd_mismatch', sid, number, byte_offset)
                        continue
                    timestamp = instant(record['timestamp'])
                    uuid = record['uuid']
                    if not isinstance(uuid, str) or not uuid:
                        raise ValueError('UUID ausente')
                except (KeyError, TypeError, ValueError, AttributeError):
                    error('missing_message_metadata', sid, number, byte_offset)
                    continue
                if not (start <= timestamp < end) or timestamp < registered:
                    continue
                try:
                    text = message_text(record)
                except ValueError:
                    error('unknown_message_format', sid, number, byte_offset)
                    continue
                if text is None:
                    continue
                if len(text) > MAX_TEXT:
                    error('message_text_limit', sid, number, byte_offset)
                    continue
                key = (sid, uuid)
                if key in seen:
                    continue
                if len(result['messages']) >= MAX_MESSAGES:
                    error('message_count_limit', sid, number, byte_offset)
                    break
                seen.add(key)
                result['messages'].append({'session_id': sid, 'uuid': uuid,
                    'timestamp': timestamp.astimezone(zone).isoformat(), 'role': record['type'],
                    'text': text, 'source': {'path': str(path), 'line': number, 'byte_offset': byte_offset}})
    result['messages'].sort(key=lambda item: (instant(item['timestamp']), item['session_id'], item['uuid']))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    install_parser = commands.add_parser('install', help='Preview local integration; --apply writes it')
    install_parser.add_argument('--apply', action='store_true')
    commands.add_parser('hook', help='SessionStart input on stdin; metadata only')
    history_parser = commands.add_parser('history', help='Read only registered sessions')
    history_parser.add_argument('--date', required=True)
    history_parser.add_argument('--tz', help='IANA timezone; default: ME.md line, then Europe/Madrid')
    args = parser.parse_args()
    try:
        if args.command == 'install':
            print(encoded(install(ROOT, args.apply)), end='')
        elif args.command == 'hook':
            event = json.load(sys.stdin)
            if not isinstance(event, dict):
                raise Refusal('El evento no es un objeto')
            record_session(ROOT, event)
        else:
            print(encoded(history(ROOT, args.date, args.tz)), end='')
    except (Refusal, OSError, ValueError, KeyError, TypeError) as exc:
        print(encoded({'status': 'error', 'message': str(exc)}), file=sys.stderr, end='')
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
