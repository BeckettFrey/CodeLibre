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
    print("\n" + "-"*40)
    print(commit_msg)
    print("-"*40)

    print("❓ Proceed with this commit message? (y/n): ")
    confirm = input().strip().lower()
    
    if confirm == "y":
        subprocess.run(["git", "commit", "-m", commit_msg])
        print("✅ Commit completed.")
    else:
        print("❌ Commit canceled.")

        

