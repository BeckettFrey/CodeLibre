# File: tests/unit/test_git_helpers.py
import pytest
from gitclaude.utils.git_helpers import sanitize_commit_message, is_valid_commit_message

@pytest.mark.parametrize("raw,sanitized", [
    ("Fix: Refactor 💥 tests", "fix: refactor  tests"),
    ("Refactor123: logic()", "refactor123: logic"),
    ("Add 🧪 test-case 🚀", "add  testcase "),
    ("fix/bug: #42", "fixbug: 42"),
    ("", "")
])

def test_sanitize_commit_message(raw, sanitized):
    assert sanitize_commit_message(raw) == sanitized

@pytest.mark.parametrize("msg,expected", [
    ("fix: correct typo", True),
    ("", False),
    ("...", False),
    ("refactor: logic update", True),
    ("   ", False),
])

def test_is_valid_commit_message(msg, expected):
    assert is_valid_commit_message(msg) == expected
