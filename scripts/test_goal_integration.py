#!/usr/bin/env python3
"""离线合成行为回归：两个无 R03 依赖的 owner 及包安装前镜像。"""
from __future__ import annotations
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / 'scripts/goal_shadow_bridge.py'
INSTALLER = ROOT / 'scripts/install_goal_patch.py'
UPSTREAM = ROOT / 'governance/control-plane/pi-goal-upstream.v1.json'


def subject():
    spec = importlib.util.spec_from_file_location('goal_installer_subject', INSTALLER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def install_fixture(root: Path) -> Path:
    """只用两文件的合成上游包，不依赖外部 npm cache 或安装器自身的 digest 函数。"""
    package = root / '.pi/npm/node_modules/pi-goal-x'
    package.mkdir(parents=True)
    original = b'original\n'
    patched = b'patched\n'
    manifest = b'{"name":"pi-goal-x","version":"0.31.9","license":"MIT"}\n'
    emit(package / 'package.json', manifest)
    emit(package / 'README.md', original)
    control = root / 'governance/control-plane'
    control.mkdir(parents=True)
    patch = b'--- a/README.md\n+++ b/README.md\n@@ -1 +1 @@\n-original\n+patched\n'
    emit(control / 'review.patch', patch)
    def contract_digest(body):
        rows = [
            {'path': 'README.md', 'bytes': len(body), 'sha256': digest(body)},
            {'path': 'package.json', 'bytes': len(manifest), 'sha256': digest(manifest)},
        ]
        return digest(json.dumps(rows, sort_keys=True, separators=(',', ':')).encode())
    emit(control / 'pi-goal-upstream.v1.json', {
        'package': 'npm:pi-goal-x@0.31.9', 'patch_file': 'governance/control-plane/review.patch',
        'patch_sha256': digest(patch), 'upstream_files': 2,
        'upstream_tree_sha256': contract_digest(original),
        'patched_files': 2, 'patched_tree_sha256': contract_digest(patched),
    })
    emit(root / '.pi/settings.json', {'packages': ['npm:pi-goal-x@0.31.9']})
    (root / '.gitignore').write_text('.pi/npm/\n')
    subprocess.run(['git', 'init', '-q', str(root)], check=True, capture_output=True)
    return package


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def emit(path: Path, value) -> bytes:
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    raw = value if isinstance(value, bytes) else (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode()
    path.write_bytes(raw)
    path.chmod(0o600)
    return raw


class PairFixture:
    def __init__(self, root: Path, name: str):
        self.root = root / name
        self.root.mkdir(mode=0o700)
        self.repo = self.root / 'repository'; self.repo.mkdir(mode=0o700)
        self.runtime = self.root / 'runtime'; self.runtime.mkdir(mode=0o700)
        self.shadow = self.root / 'shadow'; self.shadow.mkdir(mode=0o700)
        self.restores = self.root / 'restores'; self.restores.mkdir(mode=0o700)
        self.cp = self.runtime / 'checkpoints/latest.json'
        self.idx = self.repo / 'research/artifacts/candidates/index.json'
        self.artifact = self.repo / 'research/artifacts/candidates/argument.txt'
        self.binding = {'problem_id': f'problem:{name}', 'problem_contract_sha256': digest(f'contract:{name}'.encode()),
                        'statement_sha256': digest(f'statement:{name}'.encode())}
        evidence = emit(self.artifact, f'合成研究源：{name}；并非证明。\n'.encode())
        cp = {**self.binding, 'schema_version': '1.0.0', 'sequence': 9,
              'state_vector': {'claim_boundary': 'candidate_only'},
              'artifact_manifest': {'locator': self.artifact.relative_to(self.repo).as_posix(),
                                    'files': 1, 'bytes': len(evidence), 'sha256': digest(evidence)}}
        cp['integrity'] = {'commit_marker': 'OPEN-PROBLEM-CHECKPOINT-COMMIT-V1',
                           'payload_sha256': digest(json.dumps(cp, sort_keys=True, separators=(',', ':'), allow_nan=False).encode())}
        self.cp_bytes = emit(self.cp, cp)
        self.idx_bytes = emit(self.idx, {**self.binding, 'schema_version': 'sealed-candidate-pair-index.v1',
                                        'sequence': 9, 'candidate_only': True, 'claim_ceiling': 'candidate_only',
                                        'latest_checkpoint': 'runtime/checkpoints/latest.json'})
        self.config = self.root / 'config.json'
        emit(self.config, {'schema_version': 'sealed-pair-shadow.v1', **self.binding,
                           'repository_root': str(self.repo), 'runtime_root': str(self.runtime),
                           'checkpoint': str(self.cp), 'index': str(self.idx),
                           'shadow_root': str(self.shadow), 'restore_root': str(self.restores)})

    def call(self, *arguments, config=None):
        return subprocess.run([sys.executable, '-I', '-S', '-B', str(CLI), '--config', str(config or self.config),
                               '--expected-config-sha256', digest((config or self.config).read_bytes()), *arguments],
                              env={'PATH': '/usr/bin:/bin', 'PYTHONDONTWRITEBYTECODE': '1'},
                              text=True, capture_output=True, timeout=48)


class GoalIntegrationTests(unittest.TestCase):
    def test_two_different_identities_roundtrip_and_owner_boundaries(self):
        with tempfile.TemporaryDirectory(prefix='goal-pair-') as tmp:
            for label in ('elliptic-example', 'graph-example'):
                f = PairFixture(Path(tmp), label)
                before = (f.cp.read_bytes(), f.idx.read_bytes())
                saved = f.call('save', 's1')
                self.assertEqual(saved.returncode, 0, saved.stderr)
                self.assertTrue(json.loads(saved.stdout)['candidate_only'])
                self.assertEqual(f.call('save', 's1').returncode, 0)
                restored = f.call('restore', 's1', 'fresh')
                self.assertEqual(restored.returncode, 0, restored.stderr)
                self.assertEqual((f.restores / 'fresh/checkpoint.json').read_bytes(), before[0])
                self.assertEqual((f.restores / 'fresh/index.json').read_bytes(), before[1])
                self.assertEqual((f.cp.read_bytes(), f.idx.read_bytes()), before)
                self.assertNotEqual(f.call('restore', 's1', 'fresh').returncode, 0)
                (f.restores / 'alias').symlink_to(f.restores / 'fresh')
                self.assertNotEqual(f.call('restore', 's1', 'alias').returncode, 0)

    def test_mixed_identity_corrupt_owner_and_manifest_and_untrusted_profile_reject(self):
        with tempfile.TemporaryDirectory(prefix='goal-negative-') as tmp:
            f = PairFixture(Path(tmp), 'one')
            cp, idx = f.cp_bytes, f.idx_bytes
            changed = json.loads(idx); changed['problem_id'] = 'problem:two'
            emit(f.idx, changed); self.assertNotEqual(f.call('save', 'bad').returncode, 0)
            emit(f.idx, idx)
            changed = json.loads(cp); changed['sequence'] += 1
            emit(f.cp, changed); self.assertNotEqual(f.call('save', 'bad').returncode, 0)
            emit(f.cp, cp)
            emit(f.artifact, b'drift'); self.assertNotEqual(f.call('save', 'bad').returncode, 0)
            self.assertFalse((f.shadow / 'snapshots.sqlite').exists())
            emit(f.artifact, f'合成研究源：one；并非证明。\n'.encode())
            changed = json.loads(f.config.read_bytes()); changed['schema_version'] = 'unsupported-legacy-profile.v1'
            bad = f.root / 'bad-config.json'; emit(bad, changed)
            self.assertNotEqual(f.call('save', 'bad', config=bad).returncode, 0)
            self.assertFalse((f.shadow / 'snapshots.sqlite').exists())

    def test_config_drift_and_import_shadow_fail_before_publish(self):
        with tempfile.TemporaryDirectory(prefix='goal-import-') as tmp:
            f = PairFixture(Path(tmp), 'isolation')
            alternate = f.root / 'poison'; alternate.mkdir(mode=0o700)
            marker = alternate / 'UNTRUSTED-IMPORT-RAN'
            emit(alternate / 'argparse.py',
                 f'from pathlib import Path\nPath({str(marker)!r}).write_text("BAD")\nraise RuntimeError("untrusted import")\n'.encode())
            for name in ('goal_shadow_bridge.py', 'goal_snapshot_store.py'):
                shutil.copy2(ROOT / 'scripts' / name, alternate / name)
            frozen = digest(f.config.read_bytes())
            config = json.loads(f.config.read_text()); config['problem_id'] = 'problem:drift'
            emit(f.config, config)
            command = [sys.executable, '-I', '-S', '-B', str(alternate / CLI.name), '--config', str(f.config),
                       '--expected-config-sha256', frozen, 'save', 'blocked']
            env = {'PATH': '/usr/bin:/bin', 'PYTHONPATH': str(alternate)}
            run = subprocess.run(command, cwd=alternate, capture_output=True, text=True, timeout=48, env=env)
            self.assertNotEqual(run.returncode, 0)
            self.assertIn('命令入口冻结配置与 Python 配置不一致', run.stderr)
            self.assertFalse((f.shadow / 'snapshots.sqlite').exists())
            emit(f.config, {**config, 'problem_id': f.binding['problem_id']})
            command[command.index(frozen)] = digest(f.config.read_bytes())
            isolated = subprocess.run(command, cwd=alternate, capture_output=True, text=True, timeout=48, env=env)
            self.assertEqual(isolated.returncode, 0, isolated.stderr)
            self.assertFalse(marker.exists(), '同目录恶意模块必须从未执行')
            self.assertTrue(json.loads(isolated.stdout)['candidate_only'])
            counterfactual = subprocess.run([sys.executable, '-B', *command[4:]], cwd=alternate,
                                            capture_output=True, text=True, timeout=15, env=env)
            self.assertNotEqual(counterfactual.returncode, 0)
            self.assertTrue(marker.exists(), '非隔离运行必须对同一缺陷敏感')

    def test_installer_rejects_unknown_image_without_overwrite(self):
        with tempfile.TemporaryDirectory(prefix='goal-install-') as tmp:
            repo = Path(tmp)
            package = install_fixture(repo)
            changed = emit(package / 'README.md', b'unknown-owner-edit\n')
            with self.assertRaisesRegex(ValueError, 'unknown Goal package preimage'):
                subject().install(repo, True)
            result = subprocess.run([sys.executable, str(INSTALLER), '--project-root', '.', '--apply'],
                                    cwd=repo, text=True, capture_output=True, timeout=15)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('BLOCK', result.stderr)
            self.assertEqual((package / 'README.md').read_bytes(), changed)
            self.assertFalse(list((repo / '.pi/npm').glob('.goal-patch-upstream-*')))
            self.assertTrue(UPSTREAM.is_file())

    def test_installer_accepts_documented_relative_root_and_rejects_symlink_alias(self):
        with tempfile.TemporaryDirectory(prefix='goal-install-relative-') as tmp:
            repo = Path(tmp) / 'repository'; repo.mkdir()
            package = install_fixture(repo)
            command = [sys.executable, str(INSTALLER), '--project-root', '.', '--apply']
            run = subprocess.run(command, cwd=repo, text=True, capture_output=True, timeout=15)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertEqual((package / 'README.md').read_bytes(), b'patched\n')
            again = subprocess.run(command, cwd=repo, text=True, capture_output=True, timeout=15)
            self.assertEqual(again.returncode, 0, again.stderr)
            alias = repo.parent / 'alias'; alias.symlink_to(repo, target_is_directory=True)
            blocked = subprocess.run([sys.executable, str(INSTALLER), '--project-root', str(alias), '--apply'],
                                     cwd=repo, text=True, capture_output=True, timeout=15)
            self.assertNotEqual(blocked.returncode, 0, 'symlinked root must not be accepted')
            self.assertEqual((package / 'README.md').read_bytes(), b'patched\n')

    def test_package_root_permissions_reject_without_repair_on_first_install_and_recheck(self):
        with tempfile.TemporaryDirectory(prefix='goal-install-root-mode-') as tmp:
            for phase in ('upstream', 'patched'):
                with self.subTest(phase=phase):
                    repo = Path(tmp) / phase; repo.mkdir()
                    package = install_fixture(repo)
                    module = subject()
                    if phase == 'patched':
                        self.assertEqual(module.install(repo, True), 'PATCHED_VERIFIED')
                    before = {name: (package / name).read_bytes() for name in ('README.md', 'package.json')}
                    backups_before = sorted((repo / '.pi/npm').glob('.goal-patch-upstream-*'))
                    stages_before = sorted((repo / '.pi/npm').glob('.goal-patch-stage-*'))
                    package.chmod(0o777)
                    command = [sys.executable, str(INSTALLER), '--project-root', '.',
                               '--apply' if phase == 'upstream' else '--check']
                    result = subprocess.run(command, cwd=repo, text=True, capture_output=True, timeout=15)
                    self.assertNotEqual(result.returncode, 0, f'{phase}: untrusted package root was accepted')
                    self.assertIn('BLOCK (ValueError)', result.stderr)
                    with self.assertRaisesRegex(ValueError, 'Goal package member is not owner-controlled regular data'):
                        module.install(repo, phase == 'upstream')
                    self.assertEqual(package.stat().st_mode & 0o777, 0o777)
                    self.assertEqual({name: (package / name).read_bytes() for name in before}, before)
                    self.assertEqual(sorted((repo / '.pi/npm').glob('.goal-patch-upstream-*')), backups_before)
                    self.assertEqual(sorted((repo / '.pi/npm').glob('.goal-patch-stage-*')), stages_before)

    def test_install_stage_race_preserves_new_owner_bytes(self):
        with tempfile.TemporaryDirectory(prefix='goal-install-race-') as tmp:
            repo = Path(tmp); package = install_fixture(repo); canary = package / 'README.md'
            module = subject(); real_run = subprocess.run; injected = []
            def change_after_patch(argv, *args, **kwargs):
                result = real_run(argv, *args, **kwargs)
                if argv[0] == 'patch' and result.returncode == 0:
                    emit(canary, b'CONCURRENT-OWNER-EDIT\n'); injected.append(True)
                return result
            module.subprocess.run = change_after_patch
            try:
                with self.assertRaisesRegex(ValueError, 'changed|drift|preimage'):
                    module.install(repo, True)
            finally:
                module.subprocess.run = real_run
            self.assertTrue(injected, 'failure must prove injection actually happened')
            self.assertEqual(canary.read_bytes(), b'CONCURRENT-OWNER-EDIT\n')
            self.assertFalse(list((repo / '.pi/npm').glob('.goal-patch-upstream-*')))

    def test_install_second_rename_and_readback_failure_restore_previous_image(self):
        with tempfile.TemporaryDirectory(prefix='goal-install-fault-') as tmp:
            for label in ('second-rename', 'post-swap'):
                repo = Path(tmp) / label; repo.mkdir()
                package = install_fixture(repo)
                module = subject()
                if label == 'second-rename':
                    real = os.rename; injected = []
                    def fail_second(src, dst):
                        if Path(src).name.startswith('.goal-patch-stage-'):
                            injected.append(True)
                            raise OSError('synthetic second-rename failure')
                        return real(src, dst)
                    os.rename = fail_second
                    try:
                        with self.assertRaisesRegex(OSError, 'second-rename failure'):
                            module.install(repo, True)
                    finally:
                        os.rename = real
                    self.assertTrue(injected)
                else:
                    real = module.inventory; injected = []
                    def fail_readback(path):
                        if path == package and (path / 'README.md').read_bytes() == b'patched\n':
                            injected.append(True)
                            return 0, '0'*64
                        return real(path)
                    module.inventory = fail_readback
                    try:
                        with self.assertRaisesRegex(RuntimeError, 'readback|installed'):
                            module.install(repo, True)
                    finally:
                        module.inventory = real
                    self.assertTrue(injected)
                self.assertEqual((package / 'README.md').read_bytes(), b'original\n')


if __name__ == '__main__':
    unittest.main()
