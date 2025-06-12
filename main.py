# main.py
from utils.git_helpers import get_staged_diff, confirm_and_commit, sanitize_commit_message, is_valid_commit_message
from graph.graph import create_stateless_chat
from config import COMMIT_TEMPLATE, CHARACTER_LIMIT

def build_commit_prompt(diff: str) -> str:
    return COMMIT_TEMPLATE.format(diff=diff)

def generate_commit_message():
    diff = get_staged_diff()

    if not diff:
        print("❗ No staged changes to commit.")
        return
    
    if len(diff) > 10000:
        print(f"❗ Staged changes are too large to process (over {CHARACTER_LIMIT} characters).")
        return

    print("🔍 Analyzing staged changes...")
    prompt = build_commit_prompt(diff)
    chat_app = create_stateless_chat()
    result = chat_app.invoke({"current_message": prompt})

    raw_commit_msg = result['response'].strip()

    commit_msg = sanitize_commit_message(raw_commit_msg)
    print("\n🧼 Sanitized Commit Message:\n" + "-"*40)
    print(commit_msg)

    if not is_valid_commit_message(commit_msg):
        print("❌ Generated commit message is invalid. Aborting.")
        return

    confirm = input("\n❓ Proceed with this commit message? (y/n): ").strip().lower()
    if confirm != "y":
        print("❌ Commit canceled.")
        return

    confirm_and_commit(commit_msg)
    print("✅ Commit successful")

if __name__ == "__main__":
    generate_commit_message()
