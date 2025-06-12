# commit.py

from utils.git_helpers import get_staged_diff, confirm_and_commit
from langgraph_chat.graph import create_stateless_chat
from config import COMMIT_TEMPLATE, CHARACTER_LIMIT

def build_commit_prompt(diff: str) -> str:
    return COMMIT_TEMPLATE.format(diff=diff)

def generate_commit_message():
    diff = get_staged_diff()

    if not diff:
        print("❗ No staged changes to commit.")
        return

    if len(diff) > CHARACTER_LIMIT:
        print("❗ Staged changes are too large to process (over 10,000 characters).")
        return

    print("🔍 Analyzing staged changes...")
    prompt = build_commit_prompt(diff)
    chat_app = create_stateless_chat()
    result = chat_app.invoke({"current_message": prompt})
    commit_msg = result['response'].strip()

    print("\nSuggested Commit Message:\n" + "-"*40)
    print(commit_msg)
    print("-"*40)

    confirm = input("\n❓ Proceed with this commit message? (y/n): ")
    if confirm != "y":
        print("❌ Commit canceled.")
        return

    confirm_and_commit(commit_msg)
    print("✅ Commit successful")

if __name__ == "__main__":
    generate_commit_message()
