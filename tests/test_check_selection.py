import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('check_selection_test', ROOT / 'scripts/select_checks.py')
SELECT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SELECT)


class CheckSelectionTests(unittest.TestCase):
    def test_documentation_does_not_select_unrelated_runtime_suites(self):
        self.assertEqual(SELECT.select(['README.md', 'docs/example.md', SELECT.S + 'forge-teach/SKILL.md']), [])

    def test_learning_writer_selects_the_existing_owner_suite(self):
        self.assertEqual(SELECT.select([SELECT.S + 'project-learning/scripts/candidate_store.py']), ['learning'])

    def test_owner_check_infrastructure_changes_exercise_every_affected_runner(self):
        for path in ['scripts/select_checks.py', '.github/workflows/validate.yml']:
            self.assertEqual(SELECT.select([path]), sorted(SELECT.CHECKS))

    def test_terminal_and_plan_helpers_select_distinct_suites(self):
        paths = [SELECT.S + 'agent-collaboration-terminal/scripts/provider.py',
                 SELECT.S + 'codex-forge/scripts/check-plan.mjs']
        self.assertEqual(SELECT.select(paths), ['forge-plan', 'terminal'])

    def test_shared_contract_changes_include_learning_dependency(self):
        self.assertEqual(SELECT.select(['tests/test_alignment_contracts.py']), ['learning'])

    def test_native_typescript_requires_bun_without_silently_installing_it(self):
        self.assertEqual(SELECT.select([SELECT.S + 'codex-forge/scripts/orch/store.ts']), ['forge-native'])


if __name__ == '__main__':
    unittest.main()
