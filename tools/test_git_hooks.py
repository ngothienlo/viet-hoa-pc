"""Kiểm tra hook trong .githooks/ bằng repo tạm. Không đụng repo này.

    python tools/test_git_hooks.py
"""

from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

HOOKS = Path(__file__).resolve().parents[1] / ".githooks"


def git(cwd: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, encoding="utf-8")


class GitHooksTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        self.remote = root / "remote.git"
        self.repo = root / "work"
        git(root, "init", "-q", "--bare", "-b", "main", str(self.remote))
        git(root, "init", "-q", "-b", "main", str(self.repo))
        for key, value in (
            ("user.name", "Test"),
            ("user.email", "test@example.com"),
            ("core.hooksPath", HOOKS.as_posix()),
            ("commit.gpgsign", "false"),
        ):
            git(self.repo, "config", key, value)
        git(self.repo, "remote", "add", "origin", str(self.remote))
        # Commit đầu tiên của repo tạm phải bỏ qua hook, vì nó nằm trên main.
        self.write("readme.txt", "start")
        git(self.repo, "add", ".")
        self.assertEqual(git(self.repo, "commit", "-q", "--no-verify", "-m", "start").returncode, 0)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write(self, name: str, text: str) -> None:
        (self.repo / name).write_text(text, encoding="utf-8")

    def commit(self, message: str) -> subprocess.CompletedProcess:
        self.write(f"{message}.txt", message)
        git(self.repo, "add", ".")
        return git(self.repo, "commit", "-q", "-m", message)

    def test_commit_on_protected_branches_is_refused(self) -> None:
        for branch in ("main", "master", "staging"):
            with self.subTest(branch=branch):
                git(self.repo, "switch", "-q", "-C", branch)
                result = self.commit(f"direct-{branch}")
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(branch, result.stderr)

    def test_commit_on_work_branch_passes(self) -> None:
        for branch in ("feature/x", "fix/y", "docs/z", "mainline"):
            with self.subTest(branch=branch):
                git(self.repo, "switch", "-q", "-c", branch, "main")
                self.assertEqual(self.commit(branch.replace("/", "-")).returncode, 0)

    def test_local_merge_into_main_is_refused(self) -> None:
        git(self.repo, "switch", "-q", "-c", "feature/x")
        self.commit("feature")
        git(self.repo, "switch", "-q", "main")
        result = git(self.repo, "merge", "--no-ff", "-m", "merge", "feature/x")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("main", result.stderr)

    def test_push_to_protected_branch_is_refused(self) -> None:
        git(self.repo, "switch", "-q", "-c", "feature/x")
        self.commit("feature")
        self.assertEqual(git(self.repo, "push", "-q", "origin", "feature/x").returncode, 0)
        for branch in ("main", "master", "staging"):
            with self.subTest(branch=branch):
                result = git(self.repo, "push", "-q", "origin", f"feature/x:{branch}")
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(branch, result.stderr)
        self.assertNotEqual(git(self.remote, "rev-parse", "--verify", "-q", "refs/heads/master").returncode, 0)


if __name__ == "__main__":
    unittest.main()
