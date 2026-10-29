"""Behavior tests for the pOKM helper on synthetic folders; no model involved."""
import argparse
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import time
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True


def docx(path, *paragraphs):
    body = ''.join(f'<w:p><w:r><w:t>{p}</w:t></w:r></w:p>' for p in paragraphs)
    with zipfile.ZipFile(path, 'w') as z:
        z.writestr('word/document.xml', '<w:document xmlns:w="http://schemas.openxmlformats.org/'
                   f'wordprocessingml/2006/main"><w:body>{body}</w:body></w:document>')


def xlsx(path, rows):
    ns = 'xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"'
    strings, xml_rows = [], []
    for row in rows:
        cells = []
        for value in row:
            if isinstance(value, str):
                strings.append(value)
                cells.append(f'<c t="s"><v>{len(strings) - 1}</v></c>')
            else:
                cells.append(f'<c><v>{value}</v></c>')
        xml_rows.append('<row>' + ''.join(cells) + '</row>')
    with zipfile.ZipFile(path, 'w') as z:
        z.writestr('xl/workbook.xml', f'<workbook {ns}><sheets><sheet name="Tarifa"/></sheets></workbook>')
        z.writestr('xl/sharedStrings.xml', f'<sst {ns}>' + ''.join(f'<si><t>{s}</t></si>' for s in strings) + '</sst>')
        z.writestr('xl/worksheets/sheet1.xml', f'<worksheet {ns}><sheetData>{"".join(xml_rows)}</sheetData></worksheet>')


def pptx(path, *slides):
    ns = 'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"'
    with zipfile.ZipFile(path, 'w') as z:
        for i, text in enumerate(slides, 1):
            z.writestr(f'ppt/slides/slide{i}.xml', f'<p:sld xmlns:p="x" {ns}><a:t>{text}</a:t></p:sld>')


def snapshot(folder):
    return {str(p.relative_to(folder)): (p.stat().st_size, p.stat().st_mtime_ns, p.read_bytes())
            for p in Path(folder).rglob('*') if p.is_file()}


class Pokm(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='pokm pruebas ')
        base = Path(self.temporary.name)
        self.coach = base / 'mi coach'
        (self.coach / 'AIOS/integrations').mkdir(parents=True)
        shutil.copy2(ROOT / 'AIOS/integrations/pokm.py', self.coach / 'AIOS/integrations/pokm.py')
        spec = importlib.util.spec_from_file_location('pokm_test', self.coach / 'AIOS/integrations/pokm.py')
        self.pokm = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.pokm)
        self.drive = base / 'Google Drive'
        self.mine = self.drive / 'Mi unidad'
        self.shared = self.drive / 'Unidades compartidas'
        for folder in ('Comercial/Tarifas', 'Comercial/Clientes/Faro', 'Dirección', 'RRHH/Nóminas', 'Fotos'):
            (self.shared / folder).mkdir(parents=True)
        (self.mine / 'Notas').mkdir(parents=True)
        xlsx(self.shared / 'Comercial/Tarifas/Tarifa 2026.xlsx', [['Ref', 'PVP'], ['HM-10', 7950]])
        docx(self.shared / 'Comercial/Clientes/Faro/Propuesta.docx', 'Propuesta Faro', 'Importe 24.610 €')
        docx(self.shared / 'Dirección/Acta.docx', 'Málaga en marzo')
        (self.shared / 'RRHH/Nóminas/nomina.txt').write_text('Salario 4120')
        (self.shared / 'Fotos/IMG_1.jpg').write_bytes(b'\xff\xd8')
        (self.mine / 'Notas/ideas.md').write_text('Ideas')
        (self.shared / 'Comercial/Seguimiento.gdoc').write_text(json.dumps({'url': 'https://docs.google.com/document/d/X/edit'}))
        (self.shared / 'Comercial/~$Propuesta.docx').write_bytes(b'lock')

    def tearDown(self):
        self.temporary.cleanup()

    def run_cmd(self, *argv):
        out = io.StringIO()
        with patch.object(sys, 'argv', ['pokm.py', *map(str, argv)]), contextlib.redirect_stdout(out), \
                contextlib.redirect_stderr(io.StringIO()):
            try:
                self.pokm.main()
            except SystemExit as exc:
                if exc.code:
                    raise AssertionError(f'pokm.py {argv} -> {exc.code}')
        return out.getvalue()

    def activate(self):
        self.run_cmd('alcance', 'activar', self.mine, self.shared)
        self.run_cmd('alcance', 'poner', self.shared / 'Comercial', '--nivel', 'indice')
        self.run_cmd('alcance', 'poner', self.shared / 'Dirección', '--nivel', 'mapa')
        self.run_cmd('alcance', 'poner', self.shared / 'RRHH', '--nivel', 'fuera', '--motivo', 'datos de personas')
        self.run_cmd('alcance', 'poner', self.shared / 'Fotos', '--nivel', 'fuera', '--motivo', 'fotos')
        self.run_cmd('alcance', 'poner', self.mine / 'Notas', '--nivel', 'indice')
        self.run_cmd('marcar', '--todo')

    def test_never_writes_in_user_folders(self):
        before = snapshot(self.drive)
        self.run_cmd('inventario', self.drive)
        self.activate()
        (self.shared / 'Comercial/nuevo.docx').write_bytes(b'x')
        before = snapshot(self.drive)
        self.run_cmd('cambios')
        self.run_cmd('texto', self.shared / 'Comercial/Clientes/Faro/Propuesta.docx')
        self.run_cmd('marcar', '--sin-lectura')
        self.assertEqual(before, snapshot(self.drive))
        self.assertTrue((self.coach / 'pokm/.estado/alcance.json').is_file())
        self.assertTrue((self.coach / 'pokm/.estado/inventario.json').is_file())

    def test_inventory_summarises_without_saving(self):
        out = self.run_cmd('inventario', self.drive)
        self.assertIn('Comercial', out)
        self.assertIn('archivos', out)
        self.assertNotIn('~$', out)
        self.assertFalse((self.coach / 'pokm').exists())

    def test_scope_inherits_and_excludes(self):
        self.activate()
        scope = self.pokm.load_scope()
        level = self.pokm.level
        self.assertEqual(level(scope, self.shared / 'Comercial/Clientes/Faro/Propuesta.docx'), 'indice')
        self.assertEqual(level(scope, self.shared / 'Dirección/Acta.docx'), 'mapa')
        self.assertEqual(level(scope, self.shared / 'RRHH/Nóminas/nomina.txt'), 'fuera')
        self.assertIsNone(level(scope, self.mine / 'Otra'))
        self.assertEqual(level(scope, Path(self.temporary.name) / 'fuera de las bases'), 'fuera')
        snap = json.loads((self.coach / 'pokm/.estado/inventario.json').read_text())
        paths = ' '.join(snap['archivos'])
        self.assertIn('Propuesta.docx', paths)
        self.assertIn('Acta.docx', paths)
        self.assertNotIn('nomina', paths)
        self.assertNotIn('IMG_1', paths)
        self.assertNotIn('~$', paths)

    def test_rules_need_a_base_and_exclusions_need_a_reason(self):
        self.run_cmd('alcance', 'activar', self.shared)
        with self.assertRaises(AssertionError):
            self.run_cmd('alcance', 'poner', self.mine / 'Notas', '--nivel', 'indice')
        with self.assertRaises(AssertionError):
            self.run_cmd('alcance', 'poner', self.shared / 'RRHH', '--nivel', 'fuera')

    def test_changes_by_level_and_undecided_reported_once(self):
        self.activate()
        self.assertIn('0 cambios', self.run_cmd('cambios'))
        docx(self.shared / 'Comercial/Clientes/Faro/Contrato.docx', 'Vence en 2027')
        (self.shared / 'Comercial/Clientes/Sierra').mkdir()
        docx(self.shared / 'Comercial/Clientes/Sierra/Propuesta Sierra.docx', 'Jaca')
        time.sleep(0.01)
        xlsx(self.shared / 'Comercial/Tarifas/Tarifa 2026.xlsx', [['Ref', 'PVP'], ['HM-10', 8100]])
        os.utime(self.shared / 'Comercial/Tarifas/Tarifa 2026.xlsx', (time.time() + 60, time.time() + 60))
        (self.shared / 'Comercial/Clientes/Faro/Propuesta.docx').unlink()
        docx(self.shared / 'Dirección/Acta octubre.docx', 'Marta sustituye a Iván')
        (self.shared / 'Legal').mkdir()
        (self.shared / 'Legal/demanda.txt').write_text('confidencial')
        (self.shared / 'RRHH/Nóminas/otra.txt').write_text('Salario')
        out = self.run_cmd('cambios')
        lines = [line.split('\t') for line in out.splitlines()[1:]]
        by_state = {}
        for line in lines:
            by_state.setdefault(line[0], []).append(line)
        new = {Path(line[-1]).name: line[1] for line in by_state['NUEVO']}
        self.assertEqual(new, {'Contrato.docx': 'indice', 'Propuesta Sierra.docx': 'indice', 'Acta octubre.docx': 'mapa'})
        self.assertEqual([Path(l[-1]).name for l in by_state['MODIFICADO']], ['Tarifa 2026.xlsx'])
        self.assertEqual([Path(l[-1]).name for l in by_state['BORRADO']], ['Propuesta.docx'])
        self.assertEqual([Path(l[-1]).name for l in by_state['SIN-DECIDIR']], ['Legal'])
        self.assertNotIn('otra.txt', out)
        self.assertNotIn('demanda', out)
        self.run_cmd('marcar', '--sin-lectura')
        out = self.run_cmd('cambios')
        self.assertNotIn('SIN-DECIDIR', out)
        self.assertNotIn('Acta octubre', out)
        self.assertNotIn('BORRADO', out)
        self.assertIn('Contrato.docx', out)
        self.run_cmd('marcar', self.shared / 'Comercial/Clientes/Faro/Contrato.docx',
                     self.shared / 'Comercial/Clientes/Sierra/Propuesta Sierra.docx',
                     self.shared / 'Comercial/Tarifas/Tarifa 2026.xlsx')
        self.assertIn('0 cambios', self.run_cmd('cambios'))

    def test_leaving_the_scope_is_not_a_deletion(self):
        self.activate()
        self.run_cmd('alcance', 'poner', self.shared / 'Comercial/Clientes', '--nivel', 'fuera', '--motivo', 'clientes')
        out = self.run_cmd('cambios')
        self.assertIn('SALE', out)
        self.assertIn('Propuesta.docx', out)
        self.assertNotIn('BORRADO', out)
        self.run_cmd('marcar', '--sin-lectura')
        snap = json.loads((self.coach / 'pokm/.estado/inventario.json').read_text())
        self.assertFalse(any('Clientes' in p for p in snap['archivos']))

    def test_limit_per_pass(self):
        self.activate()
        for i in range(7):
            docx(self.shared / f'Comercial/doc{i}.docx', f'Documento {i}')
        out = self.run_cmd('cambios', '--limite', '3')
        self.assertEqual(sum(line.startswith('NUEVO') for line in out.splitlines()), 3)
        self.assertIn('PENDIENTE\t4 documentos más', out)

    def test_limit_serves_modified_and_known_folders_first(self):
        self.activate()
        (self.shared / 'Comercial/Lote').mkdir()
        for i in range(5):
            docx(self.shared / f'Comercial/Lote/oferta{i}.docx', f'Oferta {i}')
        docx(self.shared / 'Comercial/Clientes/Faro/Adenda.docx', 'Preaviso 90 días')
        xlsx(self.shared / 'Comercial/Tarifas/Tarifa 2026.xlsx', [['Ref', 'PVP'], ['HM-10', 8100]])
        os.utime(self.shared / 'Comercial/Tarifas/Tarifa 2026.xlsx', (time.time() + 60, time.time() + 60))
        out = self.run_cmd('cambios', '--limite', '2')
        shown = [line.split('\t')[-1] for line in out.splitlines() if line.startswith(('NUEVO', 'MODIFICADO'))]
        self.assertEqual([Path(p).name for p in shown], ['Tarifa 2026.xlsx', 'Adenda.docx'])
        self.assertIn('PENDIENTE\t5 documentos más', out)

    def test_mark_pass_marks_exactly_what_the_pass_showed(self):
        self.activate()
        for i in range(4):
            docx(self.shared / f'Comercial/doc{i}.docx', f'Documento {i}')
        (self.shared / 'Comercial/Clientes/Faro/Propuesta.docx').unlink()
        docx(self.shared / 'Dirección/Acta nueva.docx', 'Acta')
        out = self.run_cmd('cambios', '--limite', '3')
        shown = {line.split('\t')[-1] for line in out.splitlines() if line.startswith('NUEVO\tindice')}
        self.run_cmd('marcar', '--pasada', '--limite', '3')
        out = self.run_cmd('cambios', '--limite', '3')
        left = [line.split('\t')[-1] for line in out.splitlines() if line.startswith(('NUEVO', 'MODIFICADO', 'BORRADO'))]
        self.assertEqual(len(left), 1)
        self.assertNotIn(left[0], shown)
        self.assertNotIn('Acta nueva', out)
        self.assertNotIn('BORRADO', out)

    def test_timeout_never_turns_unvisited_files_into_deletions(self):
        self.activate()
        clock = iter([0, 0] + [10_000] * 1000)
        with patch.object(self.pokm.time, 'monotonic', lambda: next(clock)):
            out = self.run_cmd('cambios', '--tiempo-max', '5')
        self.assertIn('INCOMPLETO', out)
        self.assertNotIn('BORRADO', out)
        before = (self.coach / 'pokm/.estado/inventario.json').read_text()
        clock = iter([0, 0] + [10_000] * 1000)
        with patch.object(self.pokm.time, 'monotonic', lambda: next(clock)):
            self.run_cmd('marcar', '--sin-lectura', '--tiempo-max', '5')
        after = json.loads((self.coach / 'pokm/.estado/inventario.json').read_text())
        self.assertEqual(set(json.loads(before)['archivos']), set(after['archivos']))

    def test_coach_inside_a_base_is_skipped(self):
        coach_in_drive = self.mine / 'mi coach'
        shutil.copytree(self.coach, coach_in_drive)
        spec = importlib.util.spec_from_file_location('pokm_dentro', coach_in_drive / 'AIOS/integrations/pokm.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        files, _, _ = module.walk([self.mine], None, module.own_folder())
        self.assertFalse(any('mi coach' in p for p in files))

    def test_text_only_reads_inside_the_active_scope(self):
        with self.assertRaises(AssertionError):  # pOKM inactive: only the coach folder
            self.run_cmd('texto', self.shared / 'Comercial/Clientes/Faro/Propuesta.docx')
        (self.coach / 'nota.md').write_text('del coach')
        self.assertIn('del coach', self.run_cmd('texto', self.coach / 'nota.md'))
        self.activate()
        self.assertIn('Málaga', self.run_cmd('texto', self.shared / 'Dirección/Acta.docx'))
        for refused in (self.shared / 'RRHH/Nóminas/nomina.txt', self.mine / 'Notas/../../Unidades compartidas/RRHH/Nóminas/nomina.txt'):
            with self.assertRaises(AssertionError):
                self.run_cmd('texto', refused)
        (self.mine / 'Otra').mkdir()
        (self.mine / 'Otra/x.md').write_text('sin decidir')
        outside = Path(self.temporary.name) / 'fuera.txt'
        outside.write_text('secreto')
        (self.shared / 'Comercial/enlace.txt').symlink_to(outside)
        for refused in (self.mine / 'Otra/x.md', outside, self.shared / 'Comercial/enlace.txt'):
            with self.assertRaises(AssertionError):
                self.run_cmd('texto', refused)

    def test_text_extraction(self):
        self.activate()
        text = lambda path: self.run_cmd('texto', path)
        self.assertIn('Importe 24.610', text(self.shared / 'Comercial/Clientes/Faro/Propuesta.docx'))
        self.assertIn('HM-10 | 7950', text(self.shared / 'Comercial/Tarifas/Tarifa 2026.xlsx'))
        pptx(self.shared / 'Comercial/Presentación.pptx', 'Quiénes somos', 'Clientes')
        self.assertIn('[2] Clientes', text(self.shared / 'Comercial/Presentación.pptx'))
        self.assertIn('SOLO EN LÍNEA', text(self.shared / 'Comercial/Seguimiento.gdoc'))
        self.assertIn('docs.google.com', text(self.shared / 'Comercial/Seguimiento.gdoc'))
        (self.shared / 'Comercial/viejo.doc').write_bytes(b'\xd0\xcf')
        self.assertIn('Formato antiguo', text(self.shared / 'Comercial/viejo.doc'))
        (self.shared / 'Comercial/roto.docx').write_bytes(b'no es zip')
        self.assertIn('No se pudo leer', text(self.shared / 'Comercial/roto.docx'))
        (self.shared / 'Comercial/largo.md').write_text('x' * 9000)
        self.assertIn('[… recortado]', self.run_cmd('texto', self.shared / 'Comercial/largo.md', '--max', '100'))

    def test_inactive_and_deactivated(self):
        self.assertIn('sin activar', self.run_cmd('estado'))
        with self.assertRaises(AssertionError):
            self.run_cmd('cambios')
        self.activate()
        self.assertIn('activo', self.run_cmd('estado'))
        self.run_cmd('alcance', 'desactivar')
        self.assertIn('desactivado', self.run_cmd('cambios'))


if __name__ == '__main__':
    unittest.main()
