# GitClaude/utils/git_helpers.py

import subprocess
import re

def get_staged_diff() -> str:
    result = subprocess.run(["git", "diff", "--cached"], capture_output=True, text=True)
    return result.stdout.strip()

def sanitize_commit_message(msg: str) -> str:
    # Allow only lowercase letters, spaces, periods, numbers and colons
    return re.sub(r"[^a-z .:0-9]", "", msg.lower())

def is_valid_commit_message(msg: str) -> bool:
    # Ensure the message is non-empty and has at least one letter
    return bool(msg and any(char.isalpha() for char in msg))

def confirm_and_commit(commit_msg: str):
    print("\n" + "-"*20 + " M " + "-"*20)
    print(commit_msg)
    print("-"*43 + "\n")

    confirm = input("❓ Proceed with this commit message? (y/n): ").strip().lower()

    if confirm == "y":
        print("\n")
        subprocess.run(["git", "commit", "-m", commit_msg])
        print("\n✅ Commit completed.")
    else:
        print("\n❌ Commit canceled.")

        

