import subprocess
import re

def get_staged_diff() -> str:
    result = subprocess.run(["git", "diff", "--cached"], capture_output=True, text=True)
    return sanitize_commit_message(result.stdout.strip())

def sanitize_commit_message(msg: str) -> str:
    # Allow only lowercase letters, spaces, periods, and colons
    return re.sub(r"[^a-z .:]", "", msg.lower())

def confirm_and_commit(commit_msg: str):
    print("\nSuggested Commit Message:\n" + "-"*40)
    print(commit_msg)
    print("-"*40)
    print("❓ Proceed with this commit message? (y/n): ")
    confirm = input().strip().lower()
    if confirm == "y":
        subprocess.run(["git", "commit", "-m", commit_msg])
        print("✅ Commit completed.")
    else:
        print("❌ Commit canceled.")

