#!/usr/bin/env python3
"""Focused regression tests for native provider launch construction."""

from __future__ import annotations

import contextlib
import io
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock


SKILL_DIR = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


launch = load_module("launch_terminals", SKILL_DIR / "scripts" / "launch_terminals.py")
runner = load_module("run_provider", SKILL_DIR / "scripts" / "run_provider.py")
prepare = load_module("prepare_run", SKILL_DIR / "scripts" / "prepare_run.py")
validate = load_module("validate_run", SKILL_DIR / "scripts" / "validate_run.py")


class InteractiveLaunchTests(unittest.TestCase):
    def script_for(self, provider: dict[str, object]) -> str:
        script, _ = launch.shell_script(
            provider=provider,
            workspace=Path("/tmp/worktree"),
            run_dir=Path("/tmp/run"),
            approval_policy="manual",
            fallback_visible=False,
            timeout_seconds=1800,
            manifest_mode="review",
            execution_mode="interactive",
        )
        return script

    def test_antigravity_starts_bare_cli_before_manual_prompt(self) -> None:
        script = self.script_for({
            "id": "antigravity",
            "command": "agy",
            "artifact_dir": "agy",
            "model": "gemini-3.7-flash-high",
            "effort": "high",
        })
        self.assertIn("exec agy", script)
        self.assertIn("Wait until the native CLI is ready", script)
        self.assertIn("/tmp/run/agy/prompt.md", script)
        for forbidden in (
            "--prompt-interactive",
            "--print-timeout",
            "--project",
            "--model",
            "--effort",
        ):
            self.assertNotIn(forbidden, script)

    def test_grok_starts_bare_lowercase_cli_before_manual_prompt(self) -> None:
        script = self.script_for({
            "id": "grok",
            "command": "Grok",
            "artifact_dir": "grok",
            "model": None,
            "effort": None,
        })
        self.assertIn("exec grok", script)
        self.assertIn("/tmp/run/grok/prompt.md", script)
        self.assertNotIn("--prompt-file", script)

    def test_cursor_starts_bare_agent_before_manual_prompt(self) -> None:
        script = self.script_for({
            "id": "cursor",
            "command": "agent",
            "artifact_dir": "cursor",
            "model": "claude-sonnet-5-high",
            "effort": None,
            "entry_command": "/poteto-mode",
        })
        self.assertIn("exec agent", script)
        self.assertIn("Wait until the native CLI is ready", script)
        self.assertIn("/tmp/run/cursor/prompt.md", script)
        self.assertIn("Native entry command: /poteto-mode", script)
        for forbidden in ("--print", "--model", "--force", "--approve-mcps"):
            self.assertNotIn(forbidden, script)

    def test_codex_starts_bare_cli_before_manual_prompt(self) -> None:
        script = self.script_for({
            "id": "codex",
            "command": "codex",
            "artifact_dir": "codex",
        })
        self.assertIn("exec codex", script)
        self.assertIn("Wait until the native CLI is ready", script)
        self.assertIn("/tmp/run/codex/prompt.md", script)
        self.assertNotIn("codex ", script.split("exec codex", 1)[0])
        self.assertNotIn("--prompt", script)

    def test_managed_pty_starts_bare_cursor_without_submitting_prompt(self) -> None:
        script, approval_note = launch.shell_script(
            provider={
                "id": "cursor",
                "command": "agent",
                "artifact_dir": "cursor",
                "entry_command": "/poteto-mode",
            },
            workspace=Path("/tmp/worktree"),
            run_dir=Path("/tmp/run"),
            approval_policy="manual",
            fallback_visible=True,
            timeout_seconds=1800,
            manifest_mode="implementation",
            execution_mode="managed_pty",
        )
        self.assertIn("exec agent", script)
        self.assertIn("Codex-managed PTY", script)
        self.assertIn("/tmp/run/cursor/prompt.md", script)
        self.assertIn("Native entry command: /poteto-mode", script)
        self.assertIn("Codex will submit the standalone entry command", script)
        self.assertIn("manual approvals remain visible", approval_note)

    def test_visible_terminal_receipt_uses_front_window_after_delay(self) -> None:
        completed = mock.Mock(stdout="16214\n")
        with mock.patch.object(launch.sys, "platform", "darwin"), mock.patch.object(
            launch.subprocess, "run", return_value=completed
        ) as run:
            self.assertEqual(launch.open_terminal(Path("/tmp/launch.sh")), "16214")
        applescript = run.call_args.args[0][-1]
        capture = "set terminalWindowId to id of front window"
        self.assertIn(capture, applescript)
        self.assertLess(applescript.index(capture), applescript.index("delay 1"))
        self.assertIn("return terminalWindowId as text", applescript)

    def test_hosted_antigravity_timeout_has_duration_unit_without_auto_approval(self) -> None:
        command = runner.build_command(
            {
                "id": "antigravity",
                "command": "agy",
                "artifact_dir": "agy",
                "model": "gemini-3.7-flash-high",
                "effort": "high",
            },
            workspace=Path("/tmp/worktree"),
            run_dir=Path("/tmp/run"),
            prompt="Review this patch.",
            timeout_seconds=1800,
            auto_approve=False,
        )
        timeout_index = command.index("--print-timeout")
        self.assertEqual(command[timeout_index + 1], "1800s")
        self.assertNotIn("--project", command)
        self.assertNotIn("--dangerously-skip-permissions", command)

    def test_hosted_grok_uses_prompt_file_without_auto_approval(self) -> None:
        command = runner.build_command(
            {
                "id": "grok",
                "command": "grok",
                "artifact_dir": "grok",
                "model": "grok-4.6",
                "effort": "high",
            },
            workspace=Path("/tmp/worktree"),
            run_dir=Path("/tmp/run"),
            prompt="Review this patch.",
            timeout_seconds=1200,
            auto_approve=False,
        )
        self.assertEqual(command[0], "grok")
        self.assertIn("--cwd", command)
        self.assertIn("--prompt-file", command)
        self.assertEqual(command[command.index("--prompt-file") + 1], "/tmp/run/grok/prompt.md")
        self.assertNotIn("--always-approve", command)

    def test_hosted_cursor_uses_print_mode_and_read_only_plan_boundary(self) -> None:
        command = runner.build_command(
            {
                "id": "cursor",
                "command": "agent",
                "artifact_dir": "cursor",
                "model": "claude-sonnet-5-high",
                "effort": None,
            },
            workspace=Path("/tmp/worktree"),
            run_dir=Path("/tmp/run"),
            prompt="Review this patch.",
            timeout_seconds=1800,
            auto_approve=False,
            mode="review",
        )
        self.assertEqual(command[0], "agent")
        self.assertIn("--print", command)
        self.assertEqual(command[command.index("--output-format") + 1], "text")
        self.assertEqual(command[command.index("--workspace") + 1], "/tmp/worktree")
        self.assertIn("--trust", command)
        self.assertEqual(command[command.index("--mode") + 1], "plan")
        self.assertEqual(command[command.index("--model") + 1], "claude-sonnet-5-high")
        self.assertEqual(command[-1], "Review this patch.")
        self.assertNotIn("--force", command)
        self.assertNotIn("--approve-mcps", command)

    def test_hosted_codex_uses_exec_and_stdin_prompt_marker(self) -> None:
        command = runner.build_command(
            {
                "id": "codex",
                "command": "codex",
                "artifact_dir": "codex",
                "model": "gpt-5.6-terra",
            },
            workspace=Path("/tmp/worktree"),
            run_dir=Path("/tmp/run"),
            prompt="Review this patch.",
            timeout_seconds=1800,
            auto_approve=False,
        )
        self.assertEqual(command[:4], ["codex", "exec", "--cd", "/tmp/worktree"])
        self.assertIn("--model", command)
        self.assertEqual(command[command.index("--model") + 1], "gpt-5.6-terra")
        self.assertEqual(command[-1], "-")
        self.assertNotIn("Review this patch.", command)

    def test_hosted_codex_full_auto_flag_is_explicit_only(self) -> None:
        command = runner.build_command(
            {"id": "codex", "command": "codex", "artifact_dir": "codex"},
            workspace=Path("/tmp/worktree"),
            run_dir=Path("/tmp/run"),
            prompt="Implement the bounded task.",
            timeout_seconds=1800,
            auto_approve=True,
        )
        self.assertIn("--dangerously-bypass-approvals-and-sandbox", command)

    def test_hosted_cursor_full_auto_uses_force_only_for_implementation(self) -> None:
        command = runner.build_command(
            {
                "id": "cursor",
                "command": "agent",
                "artifact_dir": "cursor",
                "model": "claude-sonnet-5-high",
                "effort": None,
            },
            workspace=Path("/tmp/worktree"),
            run_dir=Path("/tmp/run"),
            prompt="Implement the bounded change.",
            timeout_seconds=1800,
            auto_approve=True,
            mode="implementation",
        )
        self.assertIn("--force", command)
        self.assertNotIn("--mode", command)
        self.assertNotIn("--approve-mcps", command)

    def test_managed_runner_rejects_native_entry_command(self) -> None:
        with self.assertRaisesRegex(ValueError, "visible interactive"):
            runner.build_command(
                {
                    "id": "cursor",
                    "command": "agent",
                    "artifact_dir": "cursor",
                    "entry_command": "/poteto-mode",
                },
                workspace=Path("/tmp/worktree"),
                run_dir=Path("/tmp/run"),
                prompt="/poteto-mode Review this patch.",
                timeout_seconds=1800,
                auto_approve=False,
                mode="review",
            )

    def test_background_shell_uses_host_runner_without_full_auto(self) -> None:
        script, approval_note = launch.shell_script(
            provider={
                "id": "antigravity",
                "command": "agy",
                "artifact_dir": "agy",
                "model": "gemini-3.7-flash-high",
                "effort": "high",
            },
            workspace=Path("/tmp/worktree"),
            run_dir=Path("/tmp/run"),
            approval_policy="manual",
            fallback_visible=True,
            timeout_seconds=1800,
            manifest_mode="review",
            execution_mode="background",
        )
        self.assertIn("run_provider.py", script)
        self.assertIn("--approval-policy manual", script)
        self.assertIn("--fallback-visible", script)
        self.assertIn("manual approval", approval_note)

    def test_hosted_shell_adds_full_auto_only_when_explicit(self) -> None:
        script, approval_note = launch.shell_script(
            provider={
                "id": "antigravity",
                "command": "agy",
                "artifact_dir": "agy",
                "model": "gemini-3.7-flash-high",
                "effort": "high",
            },
            workspace=Path("/tmp/worktree"),
            run_dir=Path("/tmp/run"),
            approval_policy="full-auto",
            fallback_visible=True,
            timeout_seconds=1800,
            manifest_mode="review",
            execution_mode="background",
        )
        self.assertIn("--approval-policy full-auto", script)
        self.assertIn("full-auto approval", approval_note)

    def test_prompt_submission_receipt_matches_execution_mode(self) -> None:
        self.assertEqual(
            launch.prompt_submission_mode("interactive"),
            "manual_after_provider_ready",
        )
        self.assertEqual(
            launch.prompt_submission_mode("background"),
            "host_runner_at_launch",
        )
        self.assertEqual(
            launch.prompt_submission_mode("managed_pty"),
            "manual_after_provider_ready",
        )

    def test_background_manual_runner_records_visible_fallback(self) -> None:
        script, _ = launch.shell_script(
            provider={
                "id": "antigravity",
                "command": "agy",
                "artifact_dir": "agy",
                "model": None,
                "effort": None,
            },
            workspace=Path("/tmp/worktree"),
            run_dir=Path("/tmp/run"),
            approval_policy="manual",
            fallback_visible=True,
            timeout_seconds=1800,
            manifest_mode="review",
            execution_mode="background",
        )
        self.assertIn("--approval-policy manual", script)
        self.assertIn("--fallback-visible", script)
        self.assertNotIn("--dangerously-skip-permissions", script)

    def test_background_launch_is_detached_and_noninteractive(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            process = mock.Mock(pid=4312)
            with mock.patch.object(launch.subprocess, "Popen", return_value=process) as popen:
                pid = launch.launch_background(
                    Path(temporary) / "launch.sh",
                    Path(temporary) / "background.log",
                )
            self.assertEqual(pid, 4312)
            self.assertEqual(popen.call_args.args[0][0], "/bin/zsh")
            self.assertIs(popen.call_args.kwargs["stdin"], launch.subprocess.DEVNULL)
            self.assertIs(popen.call_args.kwargs["stderr"], launch.subprocess.STDOUT)
            self.assertTrue(popen.call_args.kwargs["start_new_session"])

    def test_full_auto_requires_isolated_worktree(self) -> None:
        with self.assertRaisesRegex(ValueError, "isolated-worktree"):
            launch.validate_launch_policy(
                execution="background",
                approval_policy="full-auto",
                fallback_visible=True,
                authority="allowed-paths",
            )
        launch.validate_launch_policy(
            execution="background",
            approval_policy="full-auto",
            fallback_visible=True,
            authority="isolated-worktree",
        )

    def test_manual_background_requires_visible_fallback(self) -> None:
        with self.assertRaisesRegex(ValueError, "visible fallback"):
            launch.validate_launch_policy(
                execution="background",
                approval_policy="manual",
                fallback_visible=False,
                authority="read-only",
            )

    def test_native_entry_command_rejects_noninteractive_launch(self) -> None:
        entries = [{"id": "cursor", "entry_command": "/poteto-mode"}]
        with self.assertRaisesRegex(ValueError, "managed PTY or visible interactive"):
            launch.validate_native_entry_policy(
                entries=entries,
                execution_mode="background",
            )
        launch.validate_native_entry_policy(entries=entries, execution_mode="interactive")
        launch.validate_native_entry_policy(entries=entries, execution_mode="managed_pty")

    def test_managed_pty_requires_manual_approval(self) -> None:
        with self.assertRaisesRegex(ValueError, "managed-pty requires manual approval"):
            launch.validate_launch_policy(
                execution="managed-pty",
                approval_policy="full-auto",
                fallback_visible=True,
                authority="isolated-worktree",
            )

    def test_runner_classifies_visible_attention(self) -> None:
        self.assertEqual(
            runner.attention_reason("Do you trust the contents of this project?"),
            "workspace_trust_required",
        )
        self.assertEqual(
            runner.attention_reason("Requesting permission for: bun test"),
            "approval_required",
        )
        self.assertEqual(
            runner.attention_reason("ERROR: SecItemCopyMatching failed -50"),
            "authentication_required",
        )
        self.assertEqual(
            runner.attention_reason("Approval required for this command"),
            "approval_required",
        )
        self.assertIsNone(runner.attention_reason("Analysis completed normally."))

    def test_runner_classifies_anchored_denied_permission_attention(self) -> None:
        self.assertEqual(
            runner.attention_reason(
                'Error: permission check failed for command "bun test": '
                "user denied permission to run command"
            ),
            "approval_required",
        )
        self.assertIsNone(
            runner.attention_reason('The report quotes "Requesting permission" as a prior prompt.')
        )
        self.assertIsNone(
            runner.attention_reason('The report quotes "Do you trust the contents of this project?".')
        )
        self.assertIsNone(
            runner.attention_reason(
                "```text\n"
                'Error: permission check failed for command "bun test": '
                "user denied permission to run command\n"
                "```"
            )
        )
        self.assertIsNone(
            runner.attention_reason(
                '    Error: permission check failed for command "bun test": '
                "user denied permission to run command"
            )
        )


    def test_background_runner_stops_for_manual_attention(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir = Path(temporary)
            provider_dir = run_dir / "fake"
            provider_dir.mkdir()
            (run_dir / "logs").mkdir()
            fake_provider = run_dir / "fake-provider.sh"
            fake_provider.write_text(
                "#!/bin/sh\nprintf '%s\\n' 'Requesting permission for: test command'\nsleep 10\n",
                encoding="utf-8",
            )
            os.chmod(fake_provider, 0o700)
            (run_dir / "manifest.json").write_text(json.dumps({
                "workspace": temporary,
                "authority": {"workspace": "read-only", "external": "none"},
                "providers": [{
                    "id": "fake",
                    "command": str(fake_provider),
                    "artifact_dir": "fake",
                }],
            }), encoding="utf-8")
            (provider_dir / "prompt.md").write_text("Test prompt", encoding="utf-8")
            (provider_dir / "events.jsonl").write_text("", encoding="utf-8")
            (run_dir / "owner_notice.md").write_text("# Test\n", encoding="utf-8")
            argv = [
                "run_provider.py",
                "--run", str(run_dir),
                "--provider", "fake",
                "--timeout-seconds", "5",
                "--approval-policy", "manual",
                "--fallback-visible",
            ]
            with mock.patch.object(sys, "argv", argv):
                self.assertEqual(runner.main(), 2)
            self.assertIn("state: needs_attention", (provider_dir / "status.md").read_text())
            attention = json.loads((provider_dir / "attention.json").read_text())
            self.assertEqual(attention["reason"], "approval_required")

    def test_grok_attention_records_one_visible_manual_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir = Path(temporary)
            provider_dir = run_dir / "grok"
            provider_dir.mkdir()
            (run_dir / "logs").mkdir()
            fake_provider = run_dir / "fake-grok.sh"
            fake_provider.write_text(
                "#!/bin/sh\nprintf '%s\\n' 'Do you trust this workspace?'\nsleep 10\n",
                encoding="utf-8",
            )
            os.chmod(fake_provider, 0o700)
            (run_dir / "manifest.json").write_text(json.dumps({
                "workspace": temporary,
                "authority": {"workspace": "read-only", "external": "none"},
                "providers": [{
                    "id": "grok",
                    "command": "grok",
                    "artifact_dir": "grok",
                }],
            }), encoding="utf-8")
            (provider_dir / "prompt.md").write_text("Test prompt", encoding="utf-8")
            (provider_dir / "events.jsonl").write_text("", encoding="utf-8")
            (run_dir / "owner_notice.md").write_text("# Test\n", encoding="utf-8")
            argv = [
                "run_provider.py",
                "--run", str(run_dir),
                "--provider", "grok",
                "--timeout-seconds", "5",
                "--approval-policy", "manual",
                "--fallback-visible",
            ]
            with mock.patch.object(sys, "argv", argv), mock.patch.object(
                runner, "build_command", return_value=[str(fake_provider)]
            ):
                self.assertEqual(runner.main(), 2)
            attention = json.loads((provider_dir / "attention.json").read_text())
            self.assertEqual(attention["provider"], "grok")
            self.assertEqual(attention["reason"], "workspace_trust_required")
            fallback = attention["visible_fallback_command"]
            self.assertEqual(fallback.count("--execution"), 1)
            self.assertIn("visible", fallback)
            self.assertIn("manual", fallback)


class LaunchReceiptCompatibilityTests(unittest.TestCase):
    @staticmethod
    def make_run_in_context(temporary: str, *, schema: int = 3,
                            execution: dict[str, object] | None = None,
                            authority: dict[str, str] | None = None) -> Path:
        run_dir = Path(temporary)
        provider_dir = run_dir / "fake"
        provider_dir.mkdir()
        (run_dir / "logs").mkdir()
        manifest: dict[str, object] = {
            "schema": schema,
            "run_id": "run-test",
            "workspace": temporary,
            "mode": "review",
            "providers": [{
                "id": "fake",
                "command": "fake-provider",
                "artifact_dir": "fake",
            }],
        }
        if execution is not None:
            manifest["execution"] = execution
        if authority is not None:
            manifest["authority"] = authority
        (run_dir / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        (provider_dir / "prompt.md").write_text("Test prompt", encoding="utf-8")
        (provider_dir / "status.md").write_text("state: pending\n", encoding="utf-8")
        (provider_dir / "events.jsonl").write_text("", encoding="utf-8")
        (provider_dir / "result.md").write_text("", encoding="utf-8")
        return run_dir

    def test_managed_pty_requires_a_codex_tty(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir = self.make_run_in_context(
                temporary,
                execution={"mode": "managed-pty", "approval_policy": "manual"},
                authority={"workspace": "read-only", "external": "none"},
            )
            argv = [
                "launch_terminals.py", "--run", temporary, "--provider", "fake",
                "--execution", "managed-pty", "--approval-policy", "manual",
            ]
            fake_stream = mock.Mock(isatty=mock.Mock(return_value=False))
            with mock.patch.object(sys, "argv", argv), mock.patch.object(
                launch.sys, "stdin", fake_stream
            ), mock.patch.object(launch.sys, "stdout", fake_stream):
                self.assertEqual(launch.main(), 1)
            receipt = json.loads((run_dir / "launch.json").read_text(encoding="utf-8"))
            self.assertEqual(receipt["visibility"], "codex_managed_pty")
            self.assertIn("tty=true", receipt["errors"][0])
            self.assertFalse(receipt["providers"][0]["started"])

    def test_managed_pty_replaces_launcher_in_the_same_session(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir = self.make_run_in_context(
                temporary,
                execution={"mode": "managed-pty", "approval_policy": "manual"},
                authority={"workspace": "read-only", "external": "none"},
            )
            argv = [
                "launch_terminals.py", "--run", temporary, "--provider", "fake",
                "--execution", "managed-pty", "--approval-policy", "manual",
                "--fallback-visible",
            ]
            fake_stream = mock.Mock(isatty=mock.Mock(return_value=True))
            with mock.patch.object(sys, "argv", argv), mock.patch.object(
                launch.sys, "stdin", fake_stream
            ), mock.patch.object(launch.sys, "stdout", fake_stream), mock.patch.object(
                launch.os, "execv"
            ) as execv:
                self.assertEqual(launch.main(), 0)
            receipt = json.loads((run_dir / "launch.json").read_text(encoding="utf-8"))
            record = receipt["providers"][0]
            self.assertTrue(record["started"])
            self.assertEqual(record["visibility"], "codex_managed_pty")
            self.assertEqual(record["prompt_submission"], "manual_after_provider_ready")
            execv.assert_called_once_with("/bin/zsh", ["/bin/zsh", record["script"]])

    def test_visible_fallback_preserves_prior_receipt_monitor_time_and_owner_notice(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir = self.make_run_in_context(
                temporary,
                execution={"mode": "background", "approval_policy": "manual", "fallback_visible": True},
                authority={"workspace": "read-only", "external": "none"},
            )
            first_args = [
                "launch_terminals.py", "--run", temporary, "--provider", "fake",
                "--execution", "background", "--approval-policy", "manual",
                "--fallback-visible",
            ]
            with mock.patch.object(sys, "argv", first_args), mock.patch.object(
                launch, "launch_background", return_value=4312
            ):
                self.assertEqual(launch.main(), 0)
            first = json.loads((run_dir / "launch.json").read_text(encoding="utf-8"))
            first_monitor = first["monitor_started_at"]
            prior_notice = (run_dir / "owner_notice.md").read_text(encoding="utf-8")

            fallback_args = [
                "launch_terminals.py", "--run", temporary, "--provider", "fake",
                "--execution", "visible", "--approval-policy", "manual",
            ]
            with mock.patch.object(sys, "argv", fallback_args), mock.patch.object(
                launch, "open_terminal", return_value="window-2"
            ):
                self.assertEqual(launch.main(), 0)
            receipt = json.loads((run_dir / "launch.json").read_text(encoding="utf-8"))
            self.assertEqual(receipt["monitor_started_at"], first_monitor)
            self.assertEqual(len(receipt["launch_attempts"]), 1)
            self.assertEqual(receipt["launch_attempts"][0]["mode"], "background")
            notice = (run_dir / "owner_notice.md").read_text(encoding="utf-8")
            self.assertIn(prior_notice, notice)
            self.assertIn("Execution mode: background", notice)
            self.assertIn("Execution mode: interactive", notice)

            with mock.patch.object(sys, "argv", fallback_args), mock.patch.object(
                launch, "open_terminal", return_value="window-3"
            ):
                self.assertEqual(launch.main(), 0)
            third = json.loads((run_dir / "launch.json").read_text(encoding="utf-8"))
            self.assertEqual(third["monitor_started_at"], first_monitor)
            self.assertEqual(
                [attempt["mode"] for attempt in third["launch_attempts"]],
                ["background", "visible"],
            )

    def test_owner_notice_append_preserves_interleaved_background_completion(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            notice = Path(temporary) / "owner_notice.md"
            notice.write_text("prepared evidence\n", encoding="utf-8")
            real_open = os.open
            real_write = os.write
            real_close = os.close
            injected = False

            def open_after_background_completion(path: object, flags: int, mode: int = 0o777) -> int:
                nonlocal injected
                if not injected:
                    injected = True
                    completion_fd = real_open(path, os.O_WRONLY | os.O_APPEND)
                    try:
                        real_write(completion_fd, b"background completion\n")
                    finally:
                        real_close(completion_fd)
                return real_open(path, flags, mode)

            with mock.patch.object(launch.os, "open", side_effect=open_after_background_completion):
                launch._append_owner_notice(notice, "visible fallback")

            content = notice.read_text(encoding="utf-8")
            self.assertIn("prepared evidence", content)
            self.assertIn("background completion", content)
            self.assertIn("visible fallback", content)

    def test_schema_two_unattended_keeps_visible_fallback_default(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir = self.make_run_in_context(temporary, schema=2)
            argv = [
                "launch_terminals.py", "--run", temporary, "--provider", "fake",
                "--unattended", "--dry-run",
            ]
            with mock.patch.object(sys, "argv", argv):
                self.assertEqual(launch.main(), 0)
            receipt = json.loads((run_dir / "launch.json").read_text(encoding="utf-8"))
            self.assertTrue(receipt["fallback_visible"])
            self.assertIn("--fallback-visible", receipt["providers"][0]["command_preview"])

    def test_auto_approve_rejects_explicit_approval_policy(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            self.make_run_in_context(
                temporary,
                authority={"workspace": "isolated-worktree", "external": "none"},
            )
            argv = [
                "launch_terminals.py", "--run", temporary, "--provider", "fake",
                "--auto-approve", "--approval-policy", "manual", "--dry-run",
            ]
            with mock.patch.object(sys, "argv", argv):
                with self.assertRaises(SystemExit) as error:
                    launch.main()
            self.assertEqual(error.exception.code, 2)

    def test_full_auto_shell_warns_owner_and_non_sandbox_scope(self) -> None:
        script, approval_note = launch.shell_script(
            provider={"id": "fake", "command": "fake", "artifact_dir": "fake"},
            workspace=Path("/tmp/worktree"),
            run_dir=Path("/tmp/run"),
            approval_policy="full-auto",
            fallback_visible=True,
            timeout_seconds=1800,
            manifest_mode="review",
            execution_mode="background",
        )
        self.assertIn("explicit owner authorization", script)
        self.assertIn("not bounded by allowed paths", script)
        self.assertIn("explicit owner authorization", approval_note)


class PromptAndValidationTests(unittest.TestCase):
    def test_cursor_entry_command_is_separate_from_followup_prompt(self) -> None:
        prompt = prepare.prompt_for(
            provider={
                "id": "cursor",
                "command": "agent",
                "artifact_dir": "cursor",
                "entry_command": "/poteto-mode",
            },
            workspace=Path("/tmp/worktree"),
            run_dir=Path("/tmp/run"),
            objective="Implement the bounded task",
            intent="implementation",
            mode="implementation",
            workflow="sequential",
            scope="current-worktree",
            workspace_authority="allowed-paths",
            external_authority="none",
            allowed_paths=["src"],
            excluded_paths=[".env"],
            monitor_minutes=30,
            poll_seconds=60,
            codex_roles={},
        )
        self.assertTrue(prompt.startswith("# Follow-up after standalone native mode activation"))
        self.assertNotIn("/poteto-mode", prompt)
        self.assertEqual(prepare.normalize_cursor_entry_command(" /poteto-mode "), "/poteto-mode")
        with self.assertRaisesRegex(ValueError, "only the slash-command token"):
            prepare.normalize_cursor_entry_command("/poteto-mode extra")

    def test_implementation_prompt_leads_with_task_and_defers_discovery(self) -> None:
        prompt = prepare.prompt_for(
            provider={"id": "cursor", "command": "agent", "artifact_dir": "cursor"},
            workspace=Path("/tmp/worktree"),
            run_dir=Path("/tmp/run"),
            objective="Create the bounded leaf module now.",
            intent="implementation",
            mode="implementation",
            workflow="sequential",
            scope="current-worktree",
            workspace_authority="allowed-paths",
            external_authority="none",
            allowed_paths=["src/leaf.ts", "src/integration.ts"],
            excluded_paths=["src/shared.ts", ".env"],
            monitor_minutes=30,
            poll_seconds=60,
            codex_roles={},
        )
        self.assertLess(prompt.index("Create the bounded leaf module now."), prompt.index("Run manifest"))
        self.assertIn("## Implementation-first execution", prompt)
        self.assertIn("Do not enumerate skills, plugins, MCPs", prompt)
        self.assertIn("Protected/excluded paths: src/shared.ts, .env", prompt)
        self.assertNotIn("Allowed paths: src/leaf.ts, src/integration.ts", prompt)
        self.assertNotIn("## Provider-native capability preflight", prompt)

    def test_cursor_aliases_and_verified_default_model(self) -> None:
        parser = prepare.argparse.ArgumentParser()
        self.assertEqual(prepare.canonical_provider("Cursor", parser), "cursor")
        self.assertEqual(prepare.canonical_provider("agent", parser), "cursor")
        self.assertEqual(prepare.canonical_provider("cursor-agent", parser), "cursor")
        self.assertEqual(prepare.PROVIDER_SPECS["cursor"]["command"], "agent")
        self.assertEqual(
            prepare.PROVIDER_SPECS["cursor"]["default_model"],
            "claude-sonnet-5-high",
        )
        self.assertEqual(launch.DEFAULT_TIMEOUTS["cursor"], 1800)

    def test_codex_keyword_is_case_insensitive_and_defaults_to_managed_pty(self) -> None:
        parser = prepare.argparse.ArgumentParser()
        self.assertEqual(prepare.canonical_provider("Codex", parser), "codex")
        self.assertEqual(prepare.PROVIDER_SPECS["codex"]["command"], "codex")
        self.assertEqual(launch.INTERACTIVE_COMMANDS["codex"], "codex")
        self.assertEqual(launch.DEFAULT_TIMEOUTS["codex"], 1800)

        with tempfile.TemporaryDirectory() as temporary:
            argv = [
                "prepare_run.py",
                "--workspace", temporary,
                "--objective", "Review the bounded task",
                "--provider", "Codex",
                "--mode", "review",
            ]
            with mock.patch.object(sys, "argv", argv), contextlib.redirect_stdout(io.StringIO()) as output:
                self.assertEqual(prepare.main(), 0)
            run_dir = Path(output.getvalue().strip())
            manifest = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["execution"]["mode"], "managed-pty")
            self.assertEqual(manifest["providers"][0]["id"], "codex")
            self.assertTrue((run_dir / "codex" / "prompt.md").exists())
            self.assertIn("Codex CLI process is separate", (run_dir / "codex" / "prompt.md").read_text(encoding="utf-8"))

    def test_external_authority_none_removes_blanket_capability_authorization(self) -> None:
        prompt = prepare.prompt_for(
            provider={"id": "fake", "command": "fake", "artifact_dir": "fake"},
            workspace=Path("/tmp/worktree"),
            run_dir=Path("/tmp/run"),
            objective="Review this worktree",
            intent="review",
            mode="review",
            workflow="parallel",
            scope="current-worktree",
            workspace_authority="read-only",
            external_authority="none",
            allowed_paths=["src"],
            excluded_paths=[".env"],
            monitor_minutes=30,
            poll_seconds=60,
            codex_roles={},
        )
        self.assertIn("External authority is **none**", prompt)
        self.assertIn("report any required external check or action as not run", prompt)
        self.assertNotIn("user explicitly authorizes you to use all relevant skills", prompt)
        self.assertIn("## Provider-native capability preflight", prompt)
        self.assertIn("Skills and callable tools are separate discovery surfaces", prompt)
        self.assertIn("Do not search an external marketplace", prompt)
        self.assertIn("named tools and procedural suggestions as non-exhaustive", prompt)
        self.assertIn("exercise provider-native judgment", prompt)
        self.assertIn("Capability discovery never expands those boundaries", prompt)
        self.assertIn("administrative records only", prompt)
        self.assertNotIn("## Review contract", prompt)

    def test_antigravity_review_prompt_routes_exact_quality_skills(self) -> None:
        contract = prepare.review_contract_for("antigravity", "code")
        self.assertIn("$code-review-and-quality", contract)
        self.assertIn("code-review-and-quality/SKILL.md", contract)
        self.assertIn("$code-review-tests", contract)
        self.assertIn("Do not invoke CodeRabbit", contract)
        self.assertIn("Finding key", contract)

    def test_grok_review_prompt_has_security_focus_without_nested_coderabbit(self) -> None:
        contract = prepare.review_contract_for("grok", "code")
        self.assertIn("security, privacy, trust boundaries", contract)
        self.assertIn("code-review-tests/SKILL.md", contract)
        self.assertIn("Do not invoke CodeRabbit", contract)
        self.assertNotIn("$code-review-and-quality", contract)

    def test_cursor_review_prompt_has_independent_pragmatic_focus(self) -> None:
        contract = prepare.review_contract_for("cursor", "code")
        self.assertIn("pragmatic codebase-navigation", contract)
        self.assertIn("developer ergonomics", contract)
        self.assertIn("Preserve an independent perspective", contract)
        self.assertIn("Do not invoke CodeRabbit", contract)

    def test_review_contract_is_opt_in(self) -> None:
        self.assertEqual(prepare.review_contract_for("antigravity", "none"), "")

    def test_selected_review_profile_is_independent_of_implementation_mode(self) -> None:
        prompt = prepare.prompt_for(
            provider={"id": "antigravity", "command": "agy", "artifact_dir": "agy"},
            workspace=Path("/tmp/worktree"),
            run_dir=Path("/tmp/run"),
            objective="Review this worktree and implement validated fixes",
            intent="code review and implementation",
            mode="implementation",
            workflow="parallel",
            scope="current-worktree",
            workspace_authority="read-only",
            external_authority="none",
            allowed_paths=["src"],
            excluded_paths=[".env"],
            monitor_minutes=30,
            poll_seconds=60,
            codex_roles={},
            review_profile="code",
        )
        self.assertIn("## Review contract", prompt)
        self.assertIn("$code-review-and-quality", prompt)
        self.assertIn("Edit or execute only within the authorized workspace", prompt)

    def test_validator_exits_nonzero_for_incomplete_states(self) -> None:
        for state in (
            "completed_with_warnings",
            "incomplete",
            "needs_attention",
            "failed",
            "timed_out",
            "cancelled",
        ):
            with self.subTest(state=state), tempfile.TemporaryDirectory() as temporary:
                run_dir = Path(temporary)
                provider_dir = run_dir / "fake"
                provider_dir.mkdir()
                (run_dir / "manifest.json").write_text(json.dumps({
                    "run_id": "run-test",
                    "workspace": temporary,
                    "mode": "review",
                    "providers": [{"id": "fake", "artifact_dir": "fake", "command": "fake"}],
                }), encoding="utf-8")
                timestamp = "2026-08-23T00:00:00+00:00"
                (provider_dir / "status.md").write_text(
                    f"state: {state}\nphase: done\nstarted_at: {timestamp}\n"
                    f"updated_at: {timestamp}\ncompleted_at: {timestamp}\n",
                    encoding="utf-8",
                )
                (provider_dir / "result.md").write_text("# Result\n", encoding="utf-8")
                (provider_dir / "events.jsonl").write_text("", encoding="utf-8")
                argv = ["validate_run.py", "--run", temporary]
                with mock.patch.object(sys, "argv", argv), contextlib.redirect_stdout(io.StringIO()):
                    self.assertNotEqual(validate.main(), 0)


if __name__ == "__main__":
    unittest.main()
