# File: src/codelibre/utils/git_helpers.py
import subprocess
import re
from codelibre.config import Colors
from codelibre.exceptions import SanitizationError, GitCommandError
import shlex
from typing import List, Union


def get_staged_diff() -> str:
    result = subprocess.run(["git", "diff", "--cached"], capture_output=True, text=True)
    return result.stdout.strip()

def sanitize_commit_message(msg: str) -> str:
    """
    Sanitizes the commit message by allowing only lowercase letters,
    spaces, periods, numbers and colons. Ensures it's non-empty and has at least one letter.
    """
    if not isinstance(msg, str):
        raise SanitizationError("Commit message must be a string")
    
    # Handle empty or whitespace-only input
    if not msg.strip():
        raise SanitizationError("Commit message cannot be empty")
    
    # Sanitize the message
    sanitized_msg = re.sub(r"[^a-z .:_/0-9]", "", msg.lower()).strip()
    
    # Collapse multiple spaces into single spaces
    sanitized_msg = re.sub(r'\s+', ' ', sanitized_msg)
    
    # Validate the sanitized message
    if not sanitized_msg:
        raise SanitizationError("Commit message contains no valid characters")
    
    if not any(char.isalpha() for char in sanitized_msg):
        raise SanitizationError("Commit message must contain at least one letter")
    
    # Check for reasonable length limits
    if len(sanitized_msg) > 500:  # Reasonable upper limit
        raise SanitizationError("Commit message too long after sanitization")
    
    return sanitized_msg


def run_git_command(args: Union[List[str], str], cwd: str = None) -> subprocess.CompletedProcess:
    """
    Execute git command with comprehensive error handling and security measures.
    
    Args:
        args: Git command arguments (list or string)
        cwd: Working directory for the command
        
    Returns:
        CompletedProcess object with stdout, stderr, and returncode
        
    Raises:
        GitCommandError: When git command fails or validation fails
    """
    # Input validation
    if not args:
        raise GitCommandError(message="Git command arguments cannot be empty")
    
    # Handle string input by splitting safely
    if isinstance(args, str):
        args = shlex.split(args)
    
    # Ensure args is a list
    if not isinstance(args, list):
        raise GitCommandError(message="Git arguments must be a list or string")
    
    # Security: Validate that all arguments are strings and safe
    safe_args = []
    for arg in args:
        if not isinstance(arg, str):
            raise GitCommandError(message=f"All git arguments must be strings, got {type(arg)}")
        
        # Basic security check - no shell injection attempts
        if any(dangerous in arg for dangerous in [';', '&', '|', '`', '$(']):
            raise GitCommandError(message=f"Potentially dangerous character in git argument: {arg}")
        
        safe_args.append(arg)
    
    # Construct full command
    full_command = ["git"] + safe_args
    
    try:
        # Execute with timeout to prevent hanging
        result = subprocess.run(
            full_command,
            capture_output=True,
            text=True,
            timeout=30,  # 30 second timeout
        )
        
        # Handle git command failure
        if result.returncode != 0:
            error_msg = result.stderr.strip() if result.stderr else "Unknown git error"
            print(f"\n{Colors.RED}✗ Git Error{Colors.RESET}")
            print(f"  Command: {' '.join(full_command)}")
            print(f"  {error_msg}")
            print(f"{Colors.DIM}  Run with DEBUG=1 for more details{Colors.RESET}")
            
            raise GitCommandError(
                message=f"Git command failed: {error_msg}"
            )
        
        return result
        
    except subprocess.TimeoutExpired:
        raise GitCommandError("Git command timed out after 30 seconds")
    except FileNotFoundError:
        raise GitCommandError("Git command not found - is git installed?")
    except Exception as e:
        raise GitCommandError(f"Unexpected error running git command: {str(e)}")


def unstage_all_changes(cwd: str = None) -> bool:
    """
    Unstage all changes in the current git repository.
    """
    try:
        run_git_command(["reset", "HEAD"], cwd=cwd)
        print(f"{Colors.GREEN}✓ Successfully unstaged all changes{Colors.RESET}")
        return True
    except GitCommandError as e:
        print(f"{Colors.RED}✗ Failed to unstage changes: {str(e)}{Colors.RESET}")
        return False


def safe_git_commit(message: str, cwd: str = None) -> bool:
    """
    Safely create a git commit with sanitized message.
    
    Args:
        message: Commit message to sanitize and use
        cwd: Working directory for git operations
        
    Returns:
        True if commit was successful
        
    Raises:
        SanitizationError: If message sanitization fails
        GitCommandError: If git operations fail
    """
    try:
        # Sanitize the commit message
        clean_message = sanitize_commit_message(message)
        
        # Check if there are changes to commit
        status_result = run_git_command(["status", "--porcelain"], cwd=cwd)
        if not status_result.stdout.strip():
            raise GitCommandError("No changes to commit")
        
        # Create the commit
        run_git_command(["commit", "-m", clean_message], cwd=cwd)
        
        print(f"✓ Successfully committed: {clean_message}")
        return True
        
    except (SanitizationError, GitCommandError) as e:
        print(f"{Colors.RED}✗ Commit failed: {str(e)}{Colors.RESET}")
        raise


# Example usage and testing
if __name__ == "__main__":
    # Test cases
    test_messages = [
        "fix: update user authentication",
        "Add New Feature!!! @#$%",
        "",
        "   ",
        "123456789",
        "fix user login bug",
        "a" * 600,  # Too long
        None,  # Wrong type
    ]
    
    for msg in test_messages:
        try:
            if msg is None:
                print("Testing None input...")
                result = sanitize_commit_message(msg)
            else:
                print(f"Testing: '{msg}'")
                result = sanitize_commit_message(msg)
            print(f"  ✓ Result: '{result}'")
        except Exception as e:
            print(f"  ✗ Error: {e}")
        print()

        

