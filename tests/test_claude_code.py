"""Behavior tests for local files; real Claude CLI discovery is tested separately."""
from datetime import datetime, timezone
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location('coach_claude_code', ROOT / 'AIOS/integrations/claude_code.py')
adapter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adapter)


def snapshots(root):
    return {str(path.relative_to(root)): path.read_bytes()
            for path in root.rglob('*') if path.is_file()}


class NativeCodeIntegration(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='coach pruebas ', dir=ROOT / 'tests')
        self.base = Path(self.temporary.name)
        self.coach = self.base / 'mi coach con espacios'
        self.coach.mkdir()
        shutil.copytree(ROOT / 'AIOS', self.coach / 'AIOS', ignore=shutil.ignore_patterns('__pycache__'))
        for name in ('CLAUDE.md', 'AGENTS.md'):
            shutil.copy2(ROOT / name, self.coach / name)
        self.personal = {
            'ME.md': '# Rosa\nRegla personal.\n',
            'projects/mio.md': 'Proyecto propio\n',
            'knowledge/mio.md': 'Conocimiento privado\n',
            'areas/mia.md': 'Área propia\n',
            'episodic/logs/2026-10-06.md': 'Diario previo\n',
        }
        for relative, text in self.personal.items():
            path = self.coach / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)

    def tearDown(self):
        self.temporary.cleanup()

    def transcript(self, sid='session-1', cwd=None, registered='2026-10-06T12:00:00Z'):
        cwd = cwd or self.coach
        cwd.mkdir(parents=True, exist_ok=True)
        directory = self.base / 'native transcripts'
        directory.mkdir(exist_ok=True)
        path = directory / (sid + '.jsonl')
        event = {'hook_event_name': 'SessionStart', 'session_id': sid,
                 'cwd': str(cwd), 'transcript_path': str(path)}
        adapter.record_session(self.coach, event, adapter.instant(registered))
        return path, event

    def record(self, text='He decidido revisar el inventario', timestamp='2026-10-07T08:00:00Z',
               uuid='message-1', sid='session-1', cwd=None, role='user', **flags):
        return dict({'type': role, 'sessionId': sid, 'cwd': str(cwd or self.coach),
                     'uuid': uuid, 'timestamp': timestamp,
                     'message': {'role': role, 'content': text}}, **flags)

    def put(self, path, records):
        path.write_text(''.join(json.dumps(record) + '\n' for record in records))

    def test_preview_is_read_only_apply_idempotent_preserves_personal(self):
        before = snapshots(self.coach)
        preview = adapter.install(self.coach)
        self.assertEqual(preview['status'], 'preview')
        self.assertEqual(preview['wrappers'], 13)
        self.assertEqual(before, snapshots(self.coach))
        adapter.install(self.coach, apply=True)
        first = snapshots(self.coach)
        self.assertEqual(adapter.install(self.coach, apply=True)['changed'], [])
        self.assertEqual(first, snapshots(self.coach))
        for relative, content in before.items():
            self.assertEqual((self.coach / relative).read_bytes(), content)
        self.assertEqual((self.coach / '.claude/.gitignore').read_text(), 'coach-local/\n')

    def test_all_wrapper_conflicts_are_found_before_any_write(self):
        path = self.coach / '.claude/skills/skill-installer/SKILL.md'
        path.parent.mkdir(parents=True)
        path.write_text('Mi wrapper personalizado')
        before = snapshots(self.coach)
        with self.assertRaises(adapter.Refusal):
            adapter.install(self.coach, apply=True)
        self.assertEqual(before, snapshots(self.coach))

    def test_existing_settings_hooks_and_ignore_are_preserved(self):
        settings = {'permissions': {'allow': ['Read']}, 'env': {'MY_ENV': 'yes'},
                    'hooks': {'SessionStart': [{'matcher': 'resume', 'hooks': [
                        {'type': 'command', 'command': 'printf existing'}]}],
                              'Stop': [{'hooks': [{'type': 'command', 'command': 'printf stop'}]}]}}
        directory = self.coach / '.claude'
        directory.mkdir()
        (directory / 'settings.json').write_text(json.dumps(settings))
        (directory / '.gitignore').write_text('settings.local.json\n')
        adapter.install(self.coach, apply=True)
        updated = json.loads((directory / 'settings.json').read_text())
        self.assertEqual(updated['permissions']['allow'][0], 'Read')
        self.assertEqual(updated['permissions']['allow'][1:], adapter.permission_rules(adapter.hook_spec(self.coach), self.coach))
        self.assertEqual(updated['env'], settings['env'])
        self.assertEqual(updated['hooks']['Stop'], settings['hooks']['Stop'])
        self.assertEqual(updated['hooks']['SessionStart'][0], settings['hooks']['SessionStart'][0])
        self.assertEqual(len(updated['hooks']['SessionStart']), 2)
        self.assertEqual((directory / '.gitignore').read_text(), 'settings.local.json\ncoach-local/\n')

    def test_managed_refresh_allowed_but_manual_wrapper_edit_blocks_all_writes(self):
        adapter.install(self.coach, apply=True)
        source = self.coach / 'AIOS/skills/pulidor/SKILL.md'
        source.write_text(source.read_text().replace('Skill de postura,', 'Skill de reflexión,'))
        changed = adapter.install(self.coach, apply=True)['changed']
        self.assertIn('.claude/skills/pulidor/SKILL.md', changed)
        wrapper = self.coach / '.claude/skills/pulidor/SKILL.md'
        wrapper.write_text(wrapper.read_text() + '\nMi regla propia.\n')
        source.write_text(source.read_text().replace('Skill de reflexión,', 'Skill de revisión,'))
        before = snapshots(self.coach)
        with self.assertRaises(adapter.Refusal):
            adapter.install(self.coach, apply=True)
        self.assertEqual(before, snapshots(self.coach))

    def test_retired_managed_wrapper_blocks_reinstall_without_deleting_anything(self):
        adapter.install(self.coach, apply=True)
        canonical = self.coach / 'AIOS/skills/pulidor/SKILL.md'
        canonical.write_text(canonical.read_text().replace('  status: active', '  status: retired'))
        catalogue = self.coach / 'AIOS/mapa-skills.md'
        catalogue.write_text(''.join(line for line in catalogue.read_text().splitlines(keepends=True)
                                     if not line.startswith('- **pulidor**')))
        before = snapshots(self.coach)
        with self.assertRaisesRegex(adapter.Refusal, 'sin canónico activo'):
            adapter.install(self.coach, apply=True)
        self.assertEqual(before, snapshots(self.coach))
        self.assertTrue((self.coach / '.claude/skills/pulidor/SKILL.md').is_file())

    def test_restricted_or_disabled_managed_hook_is_reported_without_writes(self):
        adapter.install(self.coach, apply=True)
        settings_path = self.coach / '.claude/settings.json'
        initial = settings_path.read_text()
        cases = [('matcher', 'resume'), ('matcher', 'startup'), ('matcher', '['),
                 ('matcher', 'startup|resume'), ('matcher', 'startup|resume|clear'),
                 ('disableAllHooks', True), ('disabled', True), ('enabled', False),
                 ('timeout', 0), ('timeout', -1), ('async', True)]
        for field, value in cases:
            with self.subTest(field=field, value=value):
                settings = json.loads(initial)
                group = settings['hooks']['SessionStart'][-1]
                if field == 'matcher':
                    group[field] = value
                elif field == 'disableAllHooks':
                    settings[field] = value
                else:
                    group['hooks'][0][field] = value
                settings_path.write_text(adapter.encoded(settings))
                before = snapshots(self.coach)
                with self.assertRaises(adapter.Refusal):
                    adapter.install(self.coach, apply=True)
                self.assertEqual(before, snapshots(self.coach))
        settings = json.loads(initial)
        settings['hooks']['SessionStart'][-1]['matcher'] = 'startup|resume|clear|compact'
        settings_path.write_text(adapter.encoded(settings))
        before = snapshots(self.coach)
        self.assertEqual(adapter.install(self.coach, apply=True)['changed'], [])
        self.assertEqual(before, snapshots(self.coach))

    def test_malformed_settings_and_symlink_fail_before_writes(self):
        directory = self.coach / '.claude'
        directory.mkdir()
        settings = directory / 'settings.json'
        settings.write_text('{bad json')
        before = snapshots(self.coach)
        with self.assertRaises(adapter.Refusal):
            adapter.install(self.coach, apply=True)
        self.assertEqual(before, snapshots(self.coach))
        settings.unlink()
        outside = self.base / 'outside'
        outside.mkdir()
        (directory / 'skills').symlink_to(outside, target_is_directory=True)
        with self.assertRaises(adapter.Refusal):
            adapter.install(self.coach, apply=True)
        self.assertEqual(list(outside.iterdir()), [])

    def test_pinned_hook_runs_from_subdirectory_with_spaces_without_shadowing(self):
        adapter.install(self.coach, apply=True)
        nested = self.coach / 'projects/un proyecto'
        nested.mkdir()
        path = self.base / 'session-cli.jsonl'
        event = {'hook_event_name': 'SessionStart', 'session_id': 'session-cli',
                 'cwd': str(nested), 'transcript_path': str(path)}
        environment = dict(os.environ, CLAUDE_PROJECT_DIR=str(nested))
        settings = json.loads((self.coach / '.claude/settings.json').read_text())
        hook = settings['hooks']['SessionStart'][-1]['hooks'][0]
        self.assertEqual(hook['command'], sys.executable)
        self.assertIn(str(self.coach), hook['args'][0])
        command = [hook['command'], *hook['args']]
        shadow = nested / 'AIOS/integrations/claude_code.py'
        shadow.parent.mkdir(parents=True)
        shadow.write_text('raise SystemExit("Nested module must not execute")')
        completed = subprocess.run(command, cwd=nested, env=environment,
                                   input=json.dumps(event), text=True, capture_output=True)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(completed.stdout, '')
        registration = self.coach / '.claude/coach-local/sessions/session-cli.json'
        data = json.loads(registration.read_text())
        self.assertEqual(data['cwd'], str(nested))
        self.assertEqual(set(data), {'session_id', 'cwd', 'transcript_path', 'registered_at'})
        first = registration.read_bytes()
        again = subprocess.run(command, cwd=nested, env=environment,
                               input=json.dumps(event), text=True, capture_output=True)
        self.assertEqual(again.returncode, 0, again.stderr)
        self.assertEqual(registration.read_bytes(), first)
        for wrapper in (self.coach / '.claude/skills').glob('*/SKILL.md'):
            text = wrapper.read_text()
            self.assertNotIn('allowed-tools:', text)
            if wrapper.parent.name != 'coach-review':
                pointer = wrapper.parent / '../../../AIOS/skills' / wrapper.parent.name / 'SKILL.md'
                self.assertTrue(pointer.resolve().is_file())
                self.assertIn('${CLAUDE_SKILL_DIR}/../../../AIOS/skills/', text)

    def test_resume_and_cd_within_coach_keep_registration_and_recover_messages(self):
        nested = self.coach / 'projects/nested'
        sibling = self.coach / 'areas/another'
        nested.mkdir()
        sibling.mkdir()
        path, event = self.transcript(cwd=nested)
        registration = self.coach / '.claude/coach-local/sessions/session-1.json'
        original = registration.read_bytes()
        event['cwd'] = str(sibling)
        adapter.record_session(self.coach, event, adapter.instant('2026-10-07T12:00:00Z'))
        self.assertEqual(registration.read_bytes(), original)
        self.put(path, [self.record(cwd=nested, uuid='nested'),
                        self.record(cwd=sibling, uuid='sibling'),
                        self.record(cwd=self.coach, uuid='root')])
        result = adapter.history(self.coach, '2026-10-07')
        self.assertEqual({message['uuid'] for message in result['messages']}, {'nested', 'sibling', 'root'})
        self.assertEqual(result['errors'], [])
        event['cwd'] = str(self.base)
        with self.assertRaises(adapter.Refusal):
            adapter.record_session(self.coach, event)
        self.assertEqual(registration.read_bytes(), original)

    def test_deleted_wrapper_and_changed_or_deleted_hook_require_decision(self):
        adapter.install(self.coach, apply=True)
        wrapper = self.coach / '.claude/skills/pulidor/SKILL.md'
        content = wrapper.read_bytes()
        wrapper.unlink()
        before = snapshots(self.coach)
        with self.assertRaisesRegex(adapter.Refusal, 'Wrapper gestionado eliminado'):
            adapter.install(self.coach, apply=True)
        self.assertEqual(before, snapshots(self.coach))
        wrapper.write_bytes(content)
        settings_path = self.coach / '.claude/settings.json'
        initial = settings_path.read_text()
        for change in ('edit', 'delete'):
            with self.subTest(change=change):
                settings = json.loads(initial)
                group = settings['hooks']['SessionStart'][-1]
                if change == 'edit':
                    group['hooks'][0]['args'].append('--my-custom-flag')
                else:
                    group['hooks'] = []
                settings_path.write_text(adapter.encoded(settings))
                before = snapshots(self.coach)
                with self.assertRaisesRegex(adapter.Refusal, 'hook gestionado se ha modificado o retirado'):
                    adapter.install(self.coach, apply=True)
                self.assertEqual(before, snapshots(self.coach))

    def test_reinstall_after_move_refreshes_only_the_managed_hook_path(self):
        adapter.install(self.coach, apply=True)
        previous = adapter.hook_spec(self.coach)
        moved = self.base / 'coach moved with spaces'
        shutil.move(self.coach, moved)
        self.coach = moved
        updated = adapter.install(moved, apply=True)
        self.assertEqual(set(updated['changed']), {'.claude/settings.json', '.claude/coach-local/managed.json'})
        settings = json.loads((moved / '.claude/settings.json').read_text())
        hooks = settings['hooks']['SessionStart'][-1]['hooks']
        self.assertEqual(len(hooks), 1)
        self.assertEqual({key: hooks[0][key] for key in ('command', 'args')}, adapter.hook_spec(moved))
        self.assertNotEqual(hooks[0]['args'], previous['args'])
        self.assertEqual(adapter.install(moved, apply=True)['changed'], [])

    def test_upgrade_replaces_the_shell_form_hook_of_2_3_0_in_place(self):
        module = self.coach.resolve() / 'AIOS/integrations/claude_code.py'
        legacy = "python3 '" + str(module) + "' hook"
        settings = {'hooks': {'SessionStart': [
            {'hooks': [{'type': 'command', 'command': 'printf existing'}]},
            {'hooks': [{'type': 'command', 'command': legacy, 'timeout': 30}]}]}}
        (self.coach / '.claude/coach-local').mkdir(parents=True)
        (self.coach / '.claude/settings.json').write_text(adapter.encoded(settings))
        (self.coach / '.claude/coach-local/managed.json').write_text(
            adapter.encoded({'schema': 1, 'files': {}, 'hook_command': legacy}))
        adapter.install(self.coach, apply=True)
        groups = json.loads((self.coach / '.claude/settings.json').read_text())['hooks']['SessionStart']
        self.assertEqual(len(groups), 2)
        self.assertEqual(groups[0]['hooks'][0], {'type': 'command', 'command': 'printf existing'})
        self.assertEqual(groups[1]['hooks'][0], {'type': 'command', 'timeout': 30,
                                                 **adapter.hook_spec(self.coach)})
        manifest = json.loads((self.coach / '.claude/coach-local/managed.json').read_text())
        self.assertEqual(manifest['hook'], adapter.hook_spec(self.coach))
        self.assertNotIn('hook_command', manifest)
        self.assertEqual(adapter.install(self.coach, apply=True)['changed'], [])

    def activate_pokm(self, active=True):
        drive = self.base / 'Drive con espacios'
        (drive / 'Comercial').mkdir(parents=True, exist_ok=True)
        (drive / 'RRHH').mkdir(exist_ok=True)
        scope = {'activo': active, 'bases': [str(drive)],
                 'reglas': {str(drive / 'Comercial'): {'nivel': 'indice', 'motivo': ''},
                            str(drive / 'RRHH'): {'nivel': 'fuera', 'motivo': 'nóminas'}}}
        path = self.coach / 'pokm/.estado/alcance.json'
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(scope))
        return drive

    def test_coach_scripts_are_allowed_and_pokm_scope_is_managed(self):
        settings_path = self.coach / '.claude/settings.json'
        settings_path.parent.mkdir()
        settings_path.write_text(json.dumps({'permissions': {'allow': ['Bash(npm test *)'],
                                                             'deny': ['Read(./.env)'],
                                                             'additionalDirectories': ['/tmp/mio']}}))
        adapter.install(self.coach, apply=True)
        rules = adapter.permission_rules(adapter.hook_spec(self.coach), self.coach)
        self.assertTrue(any('pokm.py' in rule for rule in rules))
        self.assertTrue(any('claude_code.py history' in rule for rule in rules))
        self.assertIn(f'Bash(python3 "{self.coach.resolve() / "AIOS/integrations/pokm.py"}" *)', rules)
        self.assertTrue(all(rule.startswith(('Bash(', 'PowerShell(')) for rule in rules))
        permissions = json.loads(settings_path.read_text())['permissions']
        self.assertEqual(permissions['allow'], ['Bash(npm test *)', *rules])
        self.assertEqual(permissions['deny'], ['Read(./.env)'])
        self.assertEqual(permissions['additionalDirectories'], ['/tmp/mio'])
        drive = self.activate_pokm()
        changed = adapter.install(self.coach, apply=True)['changed']
        self.assertEqual(set(changed), {'.claude/settings.json', '.claude/coach-local/managed.json'})
        permissions = json.loads(settings_path.read_text())['permissions']
        self.assertEqual(permissions['additionalDirectories'], ['/tmp/mio', str(drive)])
        self.assertEqual(permissions['deny'], ['Read(./.env)', f'Read(/{drive / "RRHH"}/**)'])
        self.assertEqual(adapter.install(self.coach, apply=True)['changed'], [])
        self.activate_pokm(active=False)
        adapter.install(self.coach, apply=True)
        permissions = json.loads(settings_path.read_text())['permissions']
        self.assertEqual(permissions['additionalDirectories'], ['/tmp/mio'])
        self.assertEqual(permissions['deny'], ['Read(./.env)'])
        self.assertEqual(permissions['allow'], ['Bash(npm test *)', *rules])

    def test_removed_managed_permission_requires_decision(self):
        adapter.install(self.coach, apply=True)
        settings_path = self.coach / '.claude/settings.json'
        settings = json.loads(settings_path.read_text())
        settings['permissions']['allow'].pop(0)
        settings_path.write_text(adapter.encoded(settings))
        before = snapshots(self.coach)
        with self.assertRaisesRegex(adapter.Refusal, 'retiró entradas gestionadas'):
            adapter.install(self.coach, apply=True)
        self.assertEqual(before, snapshots(self.coach))

    def test_new_interpreter_replaces_only_managed_rules(self):
        adapter.install(self.coach, apply=True)
        old_rules = adapter.permission_rules(adapter.hook_spec(self.coach), self.coach)
        other = self.base / 'otro python' / 'python3'
        other.parent.mkdir()
        other.write_text('#!/bin/sh\n')
        with patch.object(adapter.sys, 'executable', str(other)):
            adapter.install(self.coach, apply=True)
            new_rules = adapter.permission_rules(adapter.hook_spec(self.coach), self.coach)
        allow = json.loads((self.coach / '.claude/settings.json').read_text())['permissions']['allow']
        self.assertEqual(sorted(allow), sorted(new_rules))
        self.assertFalse((set(old_rules) - set(new_rules)) & set(allow))
        self.assertIn(f'Bash("{other}" AIOS/integrations/pokm.py *)', allow)
        self.assertTrue(set(old_rules) - set(new_rules))

    def test_malformed_pokm_scope_fails_before_writes(self):
        path = self.coach / 'pokm/.estado/alcance.json'
        path.parent.mkdir(parents=True)
        path.write_text(json.dumps({'activo': True, 'bases': ['relativa'], 'reglas': {}}))
        before = snapshots(self.coach)
        with self.assertRaisesRegex(adapter.Refusal, 'pOKM'):
            adapter.install(self.coach, apply=True)
        self.assertEqual(before, snapshots(self.coach))

    def test_review_wrapper_runs_the_pokm_phase(self):
        wrapper = adapter.canonical_wrappers(self.coach)['.claude/skills/coach-review/SKILL.md']
        self.assertIn('pOKM', wrapper)
        self.assertIn('No crees ninguna programación', wrapper)
        self.assertIn('.claude/skills/pokm/SKILL.md', adapter.canonical_wrappers(self.coach))

    def test_unidentified_interpreter_refuses_before_writing(self):
        before = snapshots(self.coach)
        with patch.object(adapter.sys, 'executable', ''), self.assertRaisesRegex(adapter.Refusal, 'intérprete'):
            adapter.install(self.coach, apply=True)
        self.assertEqual(before, snapshots(self.coach))

    def test_long_transcript_reads_final_window_with_real_offsets(self):
        path, _ = self.transcript()
        prefix = (json.dumps({'type': 'system', 'padding': 'x' * 900}) + '\n').encode() * 12
        final = (json.dumps(self.record(text='Decisión reciente')) + '\n').encode()
        path.write_bytes(prefix + final)
        with patch.object(adapter, 'MAX_BYTES', 4096), patch.object(adapter, 'MAX_LINE', 1024):
            result = adapter.history(self.coach, '2026-10-07')
        self.assertEqual([message['text'] for message in result['messages']], ['Decisión reciente'])
        self.assertEqual(result['messages'][0]['source'], {'path': str(path), 'line': None, 'byte_offset': len(prefix)})
        self.assertEqual([error['code'] for error in result['errors']], ['transcript_tail_window'])
        self.assertEqual(result['coverage']['status'], 'partial')
        # The cut can be in a very long line; discard it in chunks and reach the recent message.
        prefix = b'x' * 12000 + b'\n'
        path.write_bytes(prefix + final)
        with patch.object(adapter, 'MAX_BYTES', 4096), patch.object(adapter, 'MAX_LINE', 1024):
            result = adapter.history(self.coach, '2026-10-07')
        self.assertEqual(result['messages'][0]['source']['byte_offset'], len(prefix))
        self.assertIsNone(result['messages'][0]['source']['line'])
        self.assertEqual([error['code'] for error in result['errors']], ['transcript_tail_window'])
        # A complete oversized line inside the window is skipped, with an exact line number.
        prefix = b'x' * 2000 + b'\n'
        path.write_bytes(prefix + final)
        with patch.object(adapter, 'MAX_BYTES', 4096), patch.object(adapter, 'MAX_LINE', 1024):
            result = adapter.history(self.coach, '2026-10-07')
        self.assertEqual(result['messages'][0]['source'], {'path': str(path), 'line': 2, 'byte_offset': len(prefix)})
        self.assertEqual([error['code'] for error in result['errors']], ['transcript_line_size_limit'])

    def test_another_project_never_registers_or_leaks(self):
        other = self.base / 'otro coach'
        other.mkdir()
        path, event = self.transcript()
        event.update(session_id='session-other', cwd=str(other),
                     transcript_path=str(self.base / 'session-other.jsonl'))
        with self.assertRaises(adapter.Refusal):
            adapter.record_session(self.coach, event)
        self.put(path, [self.record(), self.record(text='Dato ajeno', cwd=other, uuid='other'),
                        self.record(text='Otra sesión', sid='foreign', uuid='foreign')])
        # Unregistered transcript: even correct metadata must not be scanned.
        (path.parent / 'unregistered.jsonl').write_text(json.dumps(self.record(text='Oculto')))
        result = adapter.history(self.coach, '2026-10-07')
        self.assertEqual([message['text'] for message in result['messages']], ['He decidido revisar el inventario'])
        self.assertEqual({issue['code'] for issue in result['errors']}, {'cwd_mismatch', 'session_mismatch'})

    def test_registration_lower_bound_prevents_retrospective_import(self):
        path, event = self.transcript(registered='2026-10-07T09:00:00Z')
        self.put(path, [self.record(timestamp='2026-10-07T08:59:59Z'),
                        self.record(text='Nuevo', timestamp='2026-10-07T09:00:00Z', uuid='new')])
        result = adapter.history(self.coach, '2026-10-07')
        self.assertEqual([message['text'] for message in result['messages']], ['Nuevo'])
        self.assertEqual(result['coverage']['status'], 'partial')
        adapter.record_session(self.coach, event, adapter.instant('2026-10-08T09:00:00Z'))
        self.assertEqual(adapter.history(self.coach, '2026-10-07')['messages'], result['messages'])

    def test_midnight_and_dst_use_calendar_day_in_madrid(self):
        path, _ = self.transcript(registered='2026-01-01T00:00:00Z')
        records = [
            self.record(timestamp='2026-10-06T21:59:59Z', uuid='before'),
            self.record(timestamp='2026-10-06T22:00:00Z', uuid='start'),
            self.record(timestamp='2026-10-07T21:59:59Z', uuid='last'),
            self.record(timestamp='2026-10-07T22:00:00Z', uuid='after'),
            self.record(timestamp='2026-10-24T22:00:00Z', uuid='fall-start'),
            self.record(timestamp='2026-10-25T00:30:00Z', uuid='fall-first-0230'),
            self.record(timestamp='2026-10-25T01:30:00Z', uuid='fall-second-0230'),
            self.record(timestamp='2026-10-25T22:59:59Z', uuid='fall-last'),
            self.record(timestamp='2026-10-25T23:00:00Z', uuid='fall-after'),
            self.record(timestamp='2026-03-28T23:00:00Z', uuid='spring-start'),
            self.record(timestamp='2026-03-29T21:59:59Z', uuid='spring-last'),
            self.record(timestamp='2026-03-29T22:00:00Z', uuid='spring-after'),
        ]
        self.put(path, records)
        normal = adapter.history(self.coach, '2026-10-07')
        self.assertEqual([message['uuid'] for message in normal['messages']], ['start', 'last'])
        fall = adapter.history(self.coach, '2026-10-25')
        self.assertEqual([message['uuid'] for message in fall['messages']],
                         ['fall-start', 'fall-first-0230', 'fall-second-0230', 'fall-last'])
        self.assertTrue(fall['messages'][1]['timestamp'].endswith('+02:00'))
        self.assertTrue(fall['messages'][2]['timestamp'].endswith('+01:00'))
        spring = adapter.history(self.coach, '2026-03-29')
        self.assertEqual([message['uuid'] for message in spring['messages']], ['spring-start', 'spring-last'])

    def test_user_timezone_from_me_md_argument_and_fallback(self):
        path, _ = self.transcript(registered='2026-01-01T00:00:00Z')
        self.put(path, [
            self.record(timestamp='2026-10-07T05:59:59Z', uuid='before'),
            self.record(timestamp='2026-10-07T06:00:00Z', uuid='start'),
            self.record(timestamp='2026-10-08T05:59:59Z', uuid='last'),
            self.record(timestamp='2026-10-08T06:00:00Z', uuid='after'),
        ])
        me = self.coach / 'ME.md'
        me.write_text('# Rosa\n\n## Quién soy\n\nZona horaria: America/Mexico_City\n')
        mexico = adapter.history(self.coach, '2026-10-07')
        self.assertEqual((mexico['timezone'], mexico['timezone_source']), ('America/Mexico_City', 'ME.md'))
        self.assertEqual([message['uuid'] for message in mexico['messages']], ['start', 'last'])
        self.assertTrue(mexico['messages'][0]['timestamp'].endswith('-06:00'))
        me.write_text('# Rosa\n- **Zona horaria:** `America/Mexico_City`\n')
        self.assertEqual(adapter.history(self.coach, '2026-10-07')['timezone_source'], 'ME.md')
        forced = adapter.history(self.coach, '2026-10-07', 'Europe/Madrid')
        self.assertEqual((forced['timezone'], forced['timezone_source']), ('Europe/Madrid', 'argument'))
        self.assertEqual([message['uuid'] for message in forced['messages']], ['before', 'start'])
        me.write_text('# Rosa\nZona horaria: Marte/Olympus\n')
        fallback = adapter.history(self.coach, '2026-10-07')
        self.assertEqual((fallback['timezone'], fallback['timezone_source']), ('Europe/Madrid', 'default'))
        with self.assertRaises(ValueError):
            adapter.history(self.coach, '2026-10-07', 'Marte/Olympus')

    def test_without_zone_database_uses_system_local_time(self):
        # Windows without the tzdata package: no IANA zone loads, not even UTC.
        path, _ = self.transcript(registered='2026-01-01T00:00:00Z')
        self.put(path, [self.record(timestamp='2026-10-07T12:00:00Z', uuid='noon')])
        (self.coach / 'ME.md').write_text('# Rosa\nZona horaria: America/Mexico_City\n')

        def missing(name):
            raise adapter.ZoneInfoNotFoundError(name)
        with patch.object(adapter, 'ZoneInfo', missing):
            for tz in (None, 'Europe/Madrid'):
                with self.subTest(tz=tz):
                    result = adapter.history(self.coach, '2026-10-07', tz)
                    self.assertEqual(result['timezone_source'], 'system')
                    self.assertTrue(result['timezone'].startswith('sistema'))
                    self.assertEqual([message['uuid'] for message in result['messages']], ['noon'])
                    start = datetime.fromisoformat(result['interval']['start'])
                    self.assertEqual(start.utcoffset(), datetime(2026, 10, 7).astimezone().utcoffset())

    def test_malformed_missing_and_unexpected_transcripts_remain_partial(self):
        self.assertEqual(adapter.history(self.coach, '2026-10-07')['messages'], [])
        path, _ = self.transcript()
        absent = adapter.history(self.coach, '2026-10-07')
        self.assertEqual(absent['messages'], [])
        self.assertIn('transcript_unavailable', [issue['code'] for issue in absent['errors']])
        path.write_text('{bad\n[]\n' + json.dumps(self.record()) + '\n')
        result = adapter.history(self.coach, '2026-10-07')
        self.assertEqual(len(result['messages']), 1)
        self.assertEqual({issue['code'] for issue in result['errors']}, {'invalid_jsonl', 'unknown_record_format'})
        self.put(path, [self.record(timestamp='2026-10-07T10:00:00'),
                        self.record(timestamp='not-a-date', uuid='bad-date')])
        result = adapter.history(self.coach, '2026-10-07')
        self.assertEqual(result['messages'], [])
        self.assertEqual(result['coverage']['status'], 'partial')
        path.write_text('{bad\n' * 25)
        result = adapter.history(self.coach, '2026-10-07')
        self.assertEqual(len(result['errors']), 20)
        self.assertEqual(result['errors_omitted'], 5)

    def test_future_message_formats_and_bad_metadata_fail_visibly(self):
        path, _ = self.transcript()
        records = [self.record(uuid='bad-timestamp', timestamp=7),
                   self.record(uuid='bad-cwd', cwd=self.coach),
                   self.record(uuid='future-content', text={'new': 'secret'}),
                   self.record(uuid='bad-text-block', text=[{'type': 'text', 'text': 3}]),
                   {'type': 'future-message', 'message': 'secret'},
                   {'type': 'system', 'subtype': 'compact_boundary'}]
        records[1]['cwd'] = 42
        self.put(path, records)
        result = adapter.history(self.coach, '2026-10-07')
        self.assertEqual(result['messages'], [])
        self.assertEqual([error['code'] for error in result['errors']],
                         ['missing_message_metadata', 'missing_message_metadata',
                          'unknown_message_format', 'unknown_message_format', 'unknown_record_type'])
        self.assertNotIn('secret', json.dumps(result))
        registration = self.coach / '.claude/coach-local/sessions/session-1.json'
        data = json.loads(registration.read_text())
        data['registered_at'] = 42
        registration.write_text(json.dumps(data))
        malformed = adapter.history(self.coach, '2026-10-07')
        self.assertEqual(malformed['messages'], [])
        self.assertEqual(malformed['errors'][0]['code'], 'invalid_registration')
        adapter.install(self.coach, apply=True)
        wrapper = (self.coach / '.claude/skills/coach-review/SKILL.md').read_text()
        self.assertNotIn('disable-model-invocation', wrapper)

    def test_observed_cli_technical_records_do_not_create_errors_or_messages(self):
        path, _ = self.transcript()
        self.put(path, [{'type': kind, 'data': 'technical content'} for kind in
                        ('attachment', 'atis-latch', 'last-prompt', 'cost-state', 'queue-operation')]
                       + [self.record()])
        result = adapter.history(self.coach, '2026-10-07')
        self.assertEqual(result['errors'], [])
        self.assertEqual([message['uuid'] for message in result['messages']], ['message-1'])
        self.assertNotIn('technical content', json.dumps(result))

    def test_native_slash_preserves_human_arguments_but_not_expansion_or_stdout(self):
        path, _ = self.transcript()
        args = '2026-10-07\n\nHe elegido revisar el inventario. Prefiero comparaciones en tablas breves.'
        envelope = ('<command-message>coach-review</command-message>\n'
                    '<command-name>/coach-review</command-name>\n'
                    '<command-args>' + args + '</command-args>')
        empty = ('<command-message>coach-review</command-message>\n'
                 '<command-name>/coach-review</command-name>\n'
                 '<command-args></command-args>')
        self.put(path, [self.record(text=envelope, uuid='slash-human'),
                        self.record(text=envelope, uuid='slash-expansion', isMeta=True),
                        self.record(text=empty, uuid='empty-slash'),
                        self.record(text=empty.split('<command-args>')[0], uuid='no-args-slash'),
                        self.record(text='<local-command-stdout>technical output</local-command-stdout>', uuid='stdout')])
        result = adapter.history(self.coach, '2026-10-07')
        self.assertEqual(len(result['messages']), 1)
        message = result['messages'][0]
        self.assertEqual(message['text'], args)
        self.assertEqual(message['uuid'], 'slash-human')
        self.assertEqual(message['role'], 'user')
        self.assertEqual(message['timestamp'], '2026-10-07T10:00:00+02:00')
        self.assertEqual(message['source'], {'path': str(path), 'line': 1, 'byte_offset': 0})
        self.assertEqual(result['errors'], [])

    def test_mechanical_content_reasoning_tools_and_duplicates_are_excluded(self):
        path, _ = self.transcript()
        records = [self.record(), self.record(),
            self.record(text='Resumen automático', uuid='meta', isMeta=True),
            self.record(text='Subagente', uuid='side', isSidechain=True),
            self.record(text='Resumen de compactación', uuid='compact', isCompactSummary=True),
            self.record(text='<local-command-stdout>secret</local-command-stdout>', uuid='command'),
            self.record(text='<task-notification>untrusted</task-notification>', uuid='task'),
            self.record(text='[Request interrupted by user]', uuid='interrupt'),
            self.record(text='This session is being continued from a previous conversation that ran out of context.', uuid='summary'),
            self.record(text=[{'type': 'tool_result', 'content': 'private'}, {'type': 'text', 'text': 'not human'}], uuid='result'),
            self.record(text=[{'type': 'thinking', 'thinking': 'secret reasoning'},
                              {'type': 'tool_use', 'name': 'Bash', 'input': {'command': 'secret'}},
                              {'type': 'text', 'text': 'Propongo empezar por inventario'}], role='assistant', uuid='assistant'),
        ]
        self.put(path, records)
        result = adapter.history(self.coach, '2026-10-07')
        self.assertEqual([message['uuid'] for message in result['messages']], ['assistant', 'message-1'])
        self.assertEqual({message['role'] for message in result['messages']}, {'user', 'assistant'})
        text = json.dumps(result)
        for private in ('secret reasoning', 'untrusted', 'not human', 'Resumen automático'):
            self.assertNotIn(private, text)
        self.assertEqual(result['messages'][0]['source']['line'], len(records))


if __name__ == '__main__':
    unittest.main()
