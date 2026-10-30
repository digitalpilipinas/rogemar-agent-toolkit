"""Skill footprints, tag vocabulary and catalog fixes stay declared and checked."""
import importlib.util
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / 'plugins/rogemar-agent-toolkit/skills'
spec = importlib.util.spec_from_file_location('routing_catalog', ROOT / 'scripts/routing_catalog.py')
routing = importlib.util.module_from_spec(spec)
spec.loader.exec_module(routing)

# Backticked project-root paths: dot-directories, docs/ and GATES.md.
PATH_LITERAL = re.compile(r'`((?:\.[A-Za-z][\w.-]*|docs)/[^`\s]*|GATES\.md)`')
# Harness and tool configuration that projects own; skills mention them but do not create them.
NOT_TOOLKIT_FOOTPRINTS = ('.agents/skills/', '.claude/', '.cursor/', '.gemini/', '.github/',
                          '.vercel/', '.vscode/', '.wrangler/')
PINNED_TAGS = {
    'android', 'architecture', 'cloudflare', 'concurrency', 'convex', 'e2e', 'expo',
    'formal-verification', 'ios', 'netlify', 'react-native', 'shadcn', 'statechart',
    'supabase', 'swift', 'swift-concurrency', 'swift-testing', 'swiftdata', 'swiftui',
    'typescript', 'vercel', 'verification-drift', 'web', 'xcode-performance'}


def covered(literal, declared):
    """A literal is covered by a declared path, its parent folder, or project-owned config."""
    for path in declared:
        stem = re.split(r'[<*]', path)[0]  # `verify-<app>/` covers `verify-*/` and concrete names
        if literal.startswith(stem) or path.startswith(literal.rstrip('/') + '/'):
            return True
    return (literal + '/').startswith(NOT_TOOLKIT_FOOTPRINTS)


def undeclared(texts, declared):
    return sorted({m for text in texts for m in PATH_LITERAL.findall(text) if not covered(m, declared)})


class FootprintTests(unittest.TestCase):
    index = json.loads((SKILLS / 'workflow-orchestrator/references/skill-routing.json').read_text())

    def test_every_project_path_in_skill_text_is_declared(self):
        declared = [entry['path'] for entry in self.index['footprints']]
        texts = [path.read_text(errors='ignore') for path in SKILLS.rglob('*.md')]
        self.assertEqual(undeclared(texts, declared), [])

    def test_lint_catches_an_undeclared_path(self):
        declared = [entry['path'] for entry in self.index['footprints']]
        self.assertEqual(undeclared(['Write results to `.toolkit-cache/run.json`.'], declared),
                         ['.toolkit-cache/run.json'])
        self.assertEqual(undeclared(['See `docs/quality/findings.md`.'], declared), [])

    def test_invalid_footprints_are_rejected(self):
        good = dict(path='.agent-map/', access='write', tracking='ignored', **{'class': 'generated-cache'})
        routing.validate_footprint(good)
        for bad in [dict(good, path='../outside/'), dict(good, path='/abs'), dict(good, access='delete'),
                    dict(good, tracking='sometimes'), dict(good, **{'class': 'misc'}),
                    dict(good, gitignore='maybe'), dict(good, extra=True)]:
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                routing.validate_footprint(bad)

    def test_tag_vocabulary_is_pinned_and_used_tags_are_declared(self):
        self.assertEqual(set(self.index['task_tags']), PINNED_TAGS)
        used = {tag for route in self.index['skills'].values() for tag in route.get('task_tags_any', [])}
        self.assertLessEqual(used, PINNED_TAGS)
        for tag, entry in self.index['task_tags'].items():
            for marker in entry['markers']:
                self.assertFalse(Path(marker['glob']).is_absolute() or '..' in Path(marker['glob']).parts, tag)

    def test_tagged_skills_accept_every_technology_their_trigger_names(self):
        # A tag list narrower than the trigger blocks legitimate routing (for example a
        # React Native release task and mobile-release-manager).
        for name, route in self.index['skills'].items():
            tags = set(route.get('task_tags_any', []))
            if not tags or route.get('kind') != 'vendored':
                continue
            trigger = route['trigger'].lower()
            for tag in PINNED_TAGS:
                if self.index['task_tags'][tag]['markers'] and re.search(r'\b' + re.escape(tag.replace('-', ' ')) + r'\b', trigger):
                    with self.subTest(skill=name, tag=tag):
                        self.assertIn(tag, tags)

    def test_argent_routes_use_the_upstream_e2e_names(self):
        skills = self.index['skills']
        self.assertIn('argent-create-e2e', skills)
        self.assertIn('argent-qa-e2e', skills)
        self.assertNotIn('argent-create-flow', skills)
        self.assertNotIn('argent-qa-flows', skills)

    def test_appllama_is_tracked_for_drift(self):
        imported = json.loads((ROOT / 'catalog/imported-sources.json').read_text())
        self.assertIn('Appllama/appllama-skills', {s['repository'] for s in imported['sources']})


if __name__ == '__main__':
    unittest.main()
