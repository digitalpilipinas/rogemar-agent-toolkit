#!/usr/bin/env python3
"""Fixture-based tests for project-learning initialization, hooks, and storage."""

from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
INITIALIZER = SKILL_ROOT / "scripts/initialize_project.py"
STORE = SKILL_ROOT / "scripts/candidate_store.py"
VALIDATOR = SKILL_ROOT / "scripts/validate_project.py"


def run_command(*args: str, cwd: Path, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [*args],
        cwd=cwd,
        check=check,
        capture_output=True,
        text=True,
        timeout=15,
    )


def message(role: str, text: str) -> dict:
    content_type = "input_text" if role == "user" else "output_text"
    return {
        "type": "response_item",
        "payload": {
            "type": "message",
            "role": role,
            "content": [{"type": content_type, "text": text}],
        },
    }


class ProjectLearningTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="project-learning-test-")
        self.root = Path(self.temp.name) / "repo"
        self.root.mkdir()
        run_command("git", "init", "-q", cwd=self.root)
        (self.root / "AGENTS.md").write_text("# Existing instructions\n", encoding="utf-8")
        (self.root / ".gitignore").write_text("existing-local-file\n", encoding="utf-8")
        hooks_dir = self.root / ".codex"
        hooks_dir.mkdir()
        (hooks_dir / "hooks.json").write_text(
            json.dumps(
                {
                    "hooks": {
                        "Stop": [
                            {
                                "hooks": [
                                    {
                                        "type": "command",
                                        "command": "python3 existing-stop.py",
                                        "timeout": 5,
                                    }
                                ]
                            }
                        ]
                    }
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def initialize(self) -> dict:
        result = run_command(
            "python3", "-I", str(INITIALIZER), "--root", str(self.root), cwd=self.root
        )
        return json.loads(result.stdout)

    def store(self, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        return run_command("python3", "-I", str(STORE), *args, cwd=self.root, check=check)

    def capture_request(
        self,
        index: int,
        *,
        lesson: str | None = None,
        milestone: bool = False,
        session: str | None = None,
        turn: str | None = None,
    ) -> Path:
        state_dir = self.root / ".codex/project-learning/state"
        state_dir.mkdir(parents=True, exist_ok=True)
        path = state_dir / f"request-{index}.json"
        path.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "session_id": session or f"session-{index}",
                    "turn_id": turn or f"turn-{index}",
                    "lesson": lesson or f"Durable lesson number {index}",
                    "applies_when": f"Condition {index} is present",
                    "does_not_apply_when": f"Condition {index} is absent",
                    "evidence_level": "verified",
                    "evidence": [
                        {
                            "kind": "test",
                            "reference": f"test-command-{index}",
                            "summary": f"Verification established outcome {index}",
                        }
                    ],
                    "milestone": milestone,
                    "source_project": None,
                    "source_lesson_id": None,
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        return path

    def run_hook(
        self,
        user_text: str,
        assistant_text: str,
        *,
        permission_mode: str = "default",
        stop_hook_active: bool = False,
        session: str = "session-hook",
        turn: str = "turn-hook",
    ) -> subprocess.CompletedProcess[str]:
        transcript = self.root / ".codex/project-learning/state/transcript-fixture.jsonl"
        records = [
            {"type": "event_msg", "payload": {"type": "task_started"}},
            message("developer", "ignored"),
            message("user", user_text),
            {
                "type": "response_item",
                "payload": {"type": "reasoning", "summary": ["must remain ignored"]},
            },
            message("assistant", assistant_text),
            {
                "type": "response_item",
                "payload": {"type": "custom_tool_call_output", "output": "ignored"},
            },
        ]
        transcript.write_text(
            "".join(json.dumps(record) + "\n" for record in records), encoding="utf-8"
        )
        payload = {
            "cwd": str(self.root),
            "hook_event_name": "Stop",
            "last_assistant_message": assistant_text,
            "model": "test-model",
            "permission_mode": permission_mode,
            "session_id": session,
            "stop_hook_active": stop_hook_active,
            "transcript_path": str(transcript),
            "turn_id": turn,
        }
        hook = self.root / ".codex/hooks/project-learning-stop.py"
        return subprocess.run(
            ["python3", "-I", str(hook)],
            cwd=self.root,
            input=json.dumps(payload),
            capture_output=True,
            text=True,
            check=True,
            timeout=10,
        )

    def test_initializer_is_idempotent_and_preserves_existing_hook(self) -> None:
        check_result = run_command(
            "python3",
            "-I",
            str(INITIALIZER),
            "--check",
            "--root",
            str(self.root),
            cwd=self.root,
        )
        self.assertIn("would add Stop hook", check_result.stdout)
        self.initialize()
        hooks = json.loads((self.root / ".codex/hooks.json").read_text(encoding="utf-8"))
        encoded = json.dumps(hooks)
        self.assertIn("python3 existing-stop.py", encoded)
        self.assertIn("project-learning-stop.py", encoded)
        second = self.initialize()
        self.assertTrue(all(item.startswith("unchanged:") for item in second["results"]))
        self.assertEqual((self.root / "AGENTS.md").read_text().count("BEGIN PROJECT LEARNING"), 1)

    def test_hook_queues_signal_without_blocking_and_skips_guarded_modes(self) -> None:
        self.initialize()
        allowed = self.run_hook(
            "We want this rule going forward instead of the previous approach.",
            "Implemented the correction and verified the tests passed.",
        )
        self.assertEqual(allowed.stdout, "")
        queue_path = self.root / ".codex/project-learning/state/queue/session-hook-turn-hook.json"
        queued = json.loads(queue_path.read_text(encoding="utf-8"))
        self.assertEqual(queued["event_type"], "turn_signal")
        self.assertEqual(queued["session_id"], "session-hook")
        self.assertEqual(queued["turn_id"], "turn-hook")
        self.assertIn("correction", queued["signals"])
        self.assertIn("durable-rule", queued["signals"])

        active = self.run_hook(
            "We want this rule going forward.",
            "The fix was verified.",
            stop_hook_active=True,
        )
        self.assertEqual(active.stdout, "")
        plan = self.run_hook(
            "We want this rule going forward.",
            "The plan is verified.",
            permission_mode="plan",
        )
        self.assertEqual(plan.stdout, "")
        opted_out = self.run_hook(
            "For this task, do not learn or remember anything.",
            "Implemented and verified.",
        )
        self.assertEqual(opted_out.stdout, "")
        trivial = self.run_hook("What is two plus two?", "Four.")
        self.assertEqual(trivial.stdout, "")

    def test_disabled_processed_and_malformed_hooks_fail_open(self) -> None:
        self.initialize()
        run_command(
            "python3",
            "-I",
            str(INITIALIZER),
            "--root",
            str(self.root),
            "--set-enabled",
            "false",
            cwd=self.root,
        )
        disabled = self.run_hook(
            "We want this rule going forward.",
            "The correction was implemented and verified.",
        )
        self.assertEqual(disabled.stdout, "")
        run_command(
            "python3",
            "-I",
            str(INITIALIZER),
            "--root",
            str(self.root),
            "--set-enabled",
            "true",
            cwd=self.root,
        )
        marker = self.root / ".codex/project-learning/state/session-hook-turn-hook.json"
        marker.write_text('{"schema_version":1,"outcome":"no_candidate"}\n')
        processed = self.run_hook(
            "We want this rule going forward.",
            "The correction was implemented and verified.",
        )
        self.assertEqual(processed.stdout, "")
        hook = self.root / ".codex/hooks/project-learning-stop.py"
        malformed = subprocess.run(
            ["python3", "-I", str(hook)],
            cwd=self.root,
            input="not-json",
            capture_output=True,
            text=True,
            check=True,
            timeout=10,
        )
        self.assertEqual(malformed.stdout, "")

    def test_capture_deduplicates_and_is_idempotent(self) -> None:
        self.initialize()
        product = self.root / "product.txt"
        product.write_text("unchanged\n", encoding="utf-8")
        first_request = self.capture_request(1, lesson="Keep one durable implementation boundary")
        first = json.loads(
            self.store("capture", "--root", str(self.root), "--request", str(first_request)).stdout
        )
        self.assertEqual(first["event_type"], "captured")
        repeated = json.loads(
            self.store("capture", "--root", str(self.root), "--request", str(first_request)).stdout
        )
        self.assertTrue(repeated["idempotent"])
        second_request = self.capture_request(
            2, lesson="Keep one durable implementation boundary"
        )
        second_request_data = json.loads(second_request.read_text())
        second_request_data["applies_when"] = "Condition 1 is present"
        second_request_data["does_not_apply_when"] = "Condition 1 is absent"
        second_request.write_text(json.dumps(second_request_data) + "\n")
        reinforced = json.loads(
            self.store("capture", "--root", str(self.root), "--request", str(second_request)).stdout
        )
        self.assertEqual(reinforced["event_type"], "reinforced")
        self.assertEqual(first["candidate_id"], reinforced["candidate_id"])
        self.assertEqual(product.read_text(encoding="utf-8"), "unchanged\n")

    def test_fifth_candidate_and_milestone_each_cue_once(self) -> None:
        self.initialize()
        results = []
        for index in range(1, 7):
            request = self.capture_request(index)
            results.append(
                json.loads(
                    self.store(
                        "capture", "--root", str(self.root), "--request", str(request)
                    ).stdout
                )
            )
        self.assertFalse(results[3]["review_due"])
        self.assertTrue(results[4]["review_due"])
        self.assertFalse(results[5]["review_due"])
        milestone = self.capture_request(20, milestone=True)
        milestone_result = json.loads(
            self.store("capture", "--root", str(self.root), "--request", str(milestone)).stdout
        )
        self.assertTrue(milestone_result["review_due"])
        repeated = json.loads(
            self.store("capture", "--root", str(self.root), "--request", str(milestone)).stdout
        )
        self.assertFalse(repeated["review_due"])

    def test_sensitive_and_raw_transcript_fields_are_rejected(self) -> None:
        self.initialize()
        request = self.capture_request(1)
        data = json.loads(request.read_text())
        data["raw_transcript"] = "conversation text"
        request.write_text(json.dumps(data) + "\n")
        result = self.store(
            "capture", "--root", str(self.root), "--request", str(request), check=False
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("forbidden field", result.stderr)

    def test_promotion_requires_approval_and_writes_ledger_only_after_request(self) -> None:
        self.initialize()
        request = self.capture_request(1)
        captured = json.loads(
            self.store("capture", "--root", str(self.root), "--request", str(request)).stdout
        )
        ledger = self.root / "docs/project-learning/lessons.md"
        before = ledger.read_text(encoding="utf-8")
        listed = json.loads(
            self.store("list", "--root", str(self.root), "--status", "pending").stdout
        )
        self.assertEqual(listed["count"], 1)
        self.assertEqual(ledger.read_text(encoding="utf-8"), before)

        promotion_path = self.root / ".codex/project-learning/state/promotion.json"
        promotion_path.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "candidate_id": captured["candidate_id"],
                    "status": "Accepted",
                    "lesson": "Approved durable lesson",
                    "applies_when": "The verified condition is present",
                    "does_not_apply_when": "The verified condition is absent",
                    "evidence_strength": "verified",
                    "cross_project": "Evaluate",
                    "approved_by": "user",
                    "supersedes": None,
                }
            )
            + "\n",
            encoding="utf-8",
        )
        promoted = json.loads(
            self.store(
                "promote", "--root", str(self.root), "--request", str(promotion_path)
            ).stdout
        )
        self.assertEqual(promoted["status"], "promoted")
        self.assertIn("Approved durable lesson", ledger.read_text(encoding="utf-8"))

    def test_full_project_validator_accepts_initialized_project(self) -> None:
        self.initialize()
        result = run_command(
            "python3", "-I", str(VALIDATOR), "--root", str(self.root), cwd=self.root
        )
        report = json.loads(result.stdout)
        self.assertTrue(report["valid"])
        self.assertEqual(report["candidate_events"], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
