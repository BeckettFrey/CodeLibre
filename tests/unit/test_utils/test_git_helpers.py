import pytest
import subprocess
from unittest.mock import patch, MagicMock
from codelibre.utils.git_helpers import (
    get_staged_diff,
    sanitize_commit_message,
    run_git_command,
    unstage_all_changes,
    safe_git_commit
)
from codelibre.exceptions import SanitizationError, GitCommandError


class TestGetStagedDiff:
    """Test get_staged_diff function."""
    
    @patch('subprocess.run')
    def test_get_staged_diff_success(self, mock_run):
        """Test successful diff retrieval."""
        mock_result = MagicMock()
        mock_result.stdout = "diff --git a/file.py b/file.py\n+added line\n"
        mock_run.return_value = mock_result
        
        result = get_staged_diff()
        
        mock_run.assert_called_once_with(
            ["git", "diff", "--cached"], 
            capture_output=True, 
            text=True
        )
        assert result == "diff --git a/file.py b/file.py\n+added line"
    
    @patch('subprocess.run')
    def test_get_staged_diff_empty(self, mock_run):
        """Test empty diff (no staged changes)."""
        mock_result = MagicMock()
        mock_result.stdout = "   \n  \n"
        mock_run.return_value = mock_result
        
        result = get_staged_diff()
        assert result == ""


class TestSanitizeCommitMessage:
    """Test sanitize_commit_message function."""
    
    def test_valid_conventional_commit(self):
        """Test valid conventional commit format."""
        result = sanitize_commit_message("feat: add user authentication")
        assert result == "feat: add user authentication"
    
    def test_fix_commit(self):
        """Test fix commit format."""
        result = sanitize_commit_message("fix: resolve memory leak in data processor")
        assert result == "fix: resolve memory leak in data processor"
    
    def test_message_with_numbers(self):
        """Test message with numbers."""
        result = sanitize_commit_message("Update API v2.1.0 endpoint")
        assert result == "update api v2.1.0 endpoint"
    
    def test_message_with_special_chars_removed(self):
        """Test that special characters are removed."""
        result = sanitize_commit_message("Add New Feature!!! @#$%^&*()")
        assert result == "add new feature"
    
    def test_message_with_underscores_and_slashes(self):
        """Test that underscores and slashes are preserved."""
        result = sanitize_commit_message("fix: update src/utils/helper_functions.py")
        assert result == "fix: update src/utils/helper_functions.py"
    
    def test_multiple_spaces_collapsed(self):
        """Test that multiple spaces are collapsed to single spaces."""
        result = sanitize_commit_message("fix:    update     user    login")
        assert result == "fix: update user login"
    
    def test_empty_string_raises_error(self):
        """Test that empty string raises SanitizationError."""
        with pytest.raises(SanitizationError, match="Commit message cannot be empty"):
            sanitize_commit_message("")
    
    def test_whitespace_only_raises_error(self):
        """Test that whitespace-only string raises SanitizationError."""
        with pytest.raises(SanitizationError, match="Commit message cannot be empty"):
            sanitize_commit_message("   \n\t  ")
    
    def test_non_string_input_raises_error(self):
        """Test that non-string input raises SanitizationError."""
        with pytest.raises(SanitizationError, match="Commit message must be a string"):
            sanitize_commit_message(None)
        
        with pytest.raises(SanitizationError, match="Commit message must be a string"):
            sanitize_commit_message(123)
    
    def test_no_letters_raises_error(self):
        """Test that message with no letters raises SanitizationError."""
        with pytest.raises(SanitizationError, match="Commit message must contain at least one letter"):
            sanitize_commit_message("123456789")
    
    def test_no_valid_chars_after_sanitization(self):
        """Test message with no valid characters after sanitization."""
        with pytest.raises(SanitizationError, match="Commit message contains no valid characters"):
            sanitize_commit_message("!@#$%^&*()")
    
    def test_message_too_long_raises_error(self):
        """Test that overly long message raises SanitizationError."""
        long_message = "a" * 501
        with pytest.raises(SanitizationError, match="Commit message too long after sanitization"):
            sanitize_commit_message(long_message)
    
    def test_message_at_length_limit(self):
        """Test message at the length limit passes."""
        limit_message = "a" * 500
        result = sanitize_commit_message(limit_message)
        assert result == limit_message


class TestRunGitCommand:
    """Test run_git_command function."""
    
    @patch('subprocess.run')
    def test_successful_command_list_args(self, mock_run):
        """Test successful git command with list arguments."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "output"
        mock_result.stderr = ""
        mock_run.return_value = mock_result
        
        result = run_git_command(["status", "--porcelain"])
        
        mock_run.assert_called_once_with(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            timeout=30
        )
        assert result == mock_result
    
    @patch('subprocess.run')
    def test_successful_command_string_args(self, mock_run):
        """Test successful git command with string arguments."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_run.return_value = mock_result
        
        result = run_git_command("status --porcelain")
        
        mock_run.assert_called_once_with(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            timeout=30
        )
    
    def test_empty_args_raises_error(self):
        """Test that empty arguments raise GitCommandError."""
        with pytest.raises(GitCommandError, match="Git command arguments cannot be empty"):
            run_git_command([])
        
        with pytest.raises(GitCommandError, match="Git command arguments cannot be empty"):
            run_git_command("")
    
    def test_non_string_args_raise_error(self):
        """Test that non-string arguments raise GitCommandError."""
        with pytest.raises(GitCommandError, match="All git arguments must be strings"):
            run_git_command(["status", 123])
    
    def test_invalid_arg_type_raises_error(self):
        """Test that invalid argument types raise GitCommandError."""
        with pytest.raises(GitCommandError, match="Git arguments must be a list or string"):
            run_git_command(123)
    
    def test_dangerous_characters_raise_error(self):
        """Test that dangerous characters in arguments raise GitCommandError."""
        dangerous_chars = [';', '&', '|', '`', '$(']
        
        for char in dangerous_chars:
            with pytest.raises(GitCommandError, match="Potentially dangerous character"):
                run_git_command([f"status{char}rm -rf /"])
    
    @patch('subprocess.run')
    def test_git_command_failure(self, mock_run):
        """Test handling of git command failure."""
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stderr = "fatal: not a git repository"
        mock_run.return_value = mock_result
        
        with pytest.raises(GitCommandError, match="Git command failed: fatal: not a git repository"):
            run_git_command(["status"])
    
    @patch('subprocess.run')
    def test_git_command_failure_no_stderr(self, mock_run):
        """Test handling of git command failure with no stderr."""
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stderr = ""
        mock_run.return_value = mock_result
        
        with pytest.raises(GitCommandError, match="Git command failed: Unknown git error"):
            run_git_command(["status"])
    
    @patch('subprocess.run')
    def test_timeout_raises_error(self, mock_run):
        """Test that command timeout raises GitCommandError."""
        mock_run.side_effect = subprocess.TimeoutExpired(["git", "status"], 30)
        
        with pytest.raises(GitCommandError, match="Git command timed out after 30 seconds"):
            run_git_command(["status"])
    
    @patch('subprocess.run')
    def test_file_not_found_raises_error(self, mock_run):
        """Test that FileNotFoundError raises GitCommandError."""
        mock_run.side_effect = FileNotFoundError()
        
        with pytest.raises(GitCommandError, match="Git command not found - is git installed?"):
            run_git_command(["status"])
    
    @patch('subprocess.run')
    def test_unexpected_error_raises_git_command_error(self, mock_run):
        """Test that unexpected errors are wrapped in GitCommandError."""
        mock_run.side_effect = RuntimeError("Unexpected error")
        
        with pytest.raises(GitCommandError, match="Unexpected error running git command: Unexpected error"):
            run_git_command(["status"])


class TestUnstageAllChanges:
    """Test unstage_all_changes function."""
    
    @patch('codelibre.utils.git_helpers.run_git_command')
    def test_successful_unstage(self, mock_run_git):
        """Test successful unstaging of all changes."""
        result = unstage_all_changes()
        
        mock_run_git.assert_called_once_with(["reset", "HEAD"], cwd=None)
        assert result is True
    
    @patch('codelibre.utils.git_helpers.run_git_command')
    def test_unstage_with_cwd(self, mock_run_git):
        """Test unstaging with custom working directory."""
        result = unstage_all_changes(cwd="/some/path")
        
        mock_run_git.assert_called_once_with(["reset", "HEAD"], cwd="/some/path")
        assert result is True
    
    @patch('codelibre.utils.git_helpers.run_git_command')
    def test_unstage_failure(self, mock_run_git):
        """Test handling of unstage failure."""
        mock_run_git.side_effect = GitCommandError("Failed to reset")
        
        result = unstage_all_changes()
        
        assert result is False


class TestSafeGitCommit:
    """Test safe_git_commit function."""
    
    @patch('codelibre.utils.git_helpers.run_git_command')
    def test_successful_commit(self, mock_run_git):
        """Test successful git commit."""
        # Mock status check (has changes)
        status_result = MagicMock()
        status_result.stdout = "M  file.py\n"
        
        # Mock commit command
        commit_result = MagicMock()
        commit_result.returncode = 0
        
        mock_run_git.side_effect = [status_result, commit_result]
        
        result = safe_git_commit("feat: add new feature")
        
        assert result is True
        assert mock_run_git.call_count == 2
        mock_run_git.assert_any_call(["status", "--porcelain"], cwd=None)
        mock_run_git.assert_any_call(["commit", "-m", "feat: add new feature"], cwd=None)
    
    @patch('codelibre.utils.git_helpers.run_git_command')
    def test_commit_with_cwd(self, mock_run_git):
        """Test commit with custom working directory."""
        status_result = MagicMock()
        status_result.stdout = "M  file.py\n"
        commit_result = MagicMock()
        
        mock_run_git.side_effect = [status_result, commit_result]
        
        result = safe_git_commit("fix: bug fix", cwd="/some/path")
        
        assert result is True
        mock_run_git.assert_any_call(["status", "--porcelain"], cwd="/some/path")
        mock_run_git.assert_any_call(["commit", "-m", "fix: bug fix"], cwd="/some/path")
    
    @patch('codelibre.utils.git_helpers.run_git_command')
    def test_no_changes_to_commit(self, mock_run_git):
        """Test error when no changes to commit."""
        status_result = MagicMock()
        status_result.stdout = ""  # No changes
        mock_run_git.return_value = status_result
        
        with pytest.raises(GitCommandError, match="No changes to commit"):
            safe_git_commit("feat: add feature")
    
    def test_sanitization_error_propagated(self):
        """Test that sanitization errors are propagated."""
        with pytest.raises(SanitizationError):
            safe_git_commit("")  # Empty message
    
    @patch('codelibre.utils.git_helpers.run_git_command')
    def test_git_command_error_propagated(self, mock_run_git):
        """Test that git command errors are propagated."""
        status_result = MagicMock()
        status_result.stdout = "M  file.py\n"
        
        mock_run_git.side_effect = [
            status_result,
            GitCommandError("Commit failed")
        ]
        
        with pytest.raises(GitCommandError, match="Commit failed"):
            safe_git_commit("feat: add feature")
    
    @patch('codelibre.utils.git_helpers.run_git_command')
    def test_message_sanitization_applied(self, mock_run_git):
        """Test that commit message is properly sanitized."""
        status_result = MagicMock()
        status_result.stdout = "M  file.py\n"
        commit_result = MagicMock()
        
        mock_run_git.side_effect = [status_result, commit_result]
        
        # Message with special characters that should be sanitized
        result = safe_git_commit("FEAT: Add New Feature!!! @#$%")
        
        assert result is True
        # Check that the sanitized message was used
        mock_run_git.assert_any_call(["commit", "-m", "feat: add new feature"], cwd=None)


class TestIntegration:
    """Integration tests combining multiple functions."""
    
    @patch('subprocess.run')
    @patch('codelibre.utils.git_helpers.run_git_command')
    def test_full_workflow_simulation(self, mock_run_git, mock_subprocess):
        """Test a complete workflow simulation."""
        # Mock get_staged_diff
        diff_result = MagicMock()
        diff_result.stdout = "diff --git a/file.py b/file.py\n+new line\n"
        mock_subprocess.return_value = diff_result
        
        # Mock safe_git_commit internals
        status_result = MagicMock()
        status_result.stdout = "M  file.py\n"
        commit_result = MagicMock()
        
        mock_run_git.side_effect = [status_result, commit_result]
        
        # Test the workflow
        diff = get_staged_diff()
        assert "diff --git a/file.py b/file.py" in diff
        
        commit_success = safe_git_commit("feat: add new functionality")
        assert commit_success is True


# Fixtures for common test data
@pytest.fixture
def valid_commit_messages():
    """Fixture providing valid commit messages for testing."""
    return [
        "feat: add user authentication",
        "fix: resolve memory leak",
        "docs: update README",
        "refactor: simplify API handling",
        "test: add unit tests for helpers",
        "chore: update dependencies"
    ]


@pytest.fixture
def invalid_commit_messages():
    """Fixture providing invalid commit messages for testing."""
    return [
        "",  # Empty
        "   ",  # Whitespace only
        "123456789",  # No letters
        "!@#$%^&*()",  # No valid characters
        "a" * 501,  # Too long
        None,  # Wrong type
        123,  # Wrong type
    ]


# Parametrized tests using fixtures
class TestParametrizedCommitMessages:
    """Parametrized tests for commit message validation."""
    
    def test_valid_messages_pass(self, valid_commit_messages):
        """Test that all valid messages pass sanitization."""
        for msg in valid_commit_messages:
            result = sanitize_commit_message(msg)
            assert isinstance(result, str)
            assert len(result) > 0
            assert any(c.isalpha() for c in result)
    
    def test_invalid_messages_fail(self, invalid_commit_messages):
        """Test that all invalid messages raise SanitizationError."""
        for msg in invalid_commit_messages:
            with pytest.raises(SanitizationError):
                sanitize_commit_message(msg)