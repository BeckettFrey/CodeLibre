from utils.git_helpers import get_staged_diff, confirm_and_commit, sanitize_commit_message, is_valid_commit_message
from graph.graph import create_stateless_chat
from config import COMMIT_TEMPLATE, CHARACTER_LIMIT

def build_commit_prompt(diff: str) -> str:
    return COMMIT_TEMPLATE.format(diff=diff)

def main():
    try:
        diff = get_staged_diff()

        if not diff:
            print("❗ No staged changes to commit.")
            return

        commit_msg = sanitize_commit_message(diff)

        if len(commit_msg) > CHARACTER_LIMIT:
            print(f"❗❗❗ (over {CHARACTER_LIMIT} characters) ❗❗❗")
            return

        if not is_valid_commit_message(commit_msg):
            print("❌ Agent Error: Invalid commit message format")
            return

        print("🔍 Analyzing staged changes...")
        prompt = build_commit_prompt(diff)
        chat_app = create_stateless_chat()

        result = chat_app.invoke({"current_message": prompt})
        raw_commit_msg = result['response'].strip()
        commit_msg = sanitize_commit_message(raw_commit_msg)
        confirm_and_commit(commit_msg)

    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
