# File: cli.py
import subprocess
import sys

from utils.git_helpers import (
    get_staged_diff,
    confirm_and_commit,
    sanitize_commit_message,
    is_valid_commit_message
)

from graph.graph import create_stateless_chat
from config import COMMIT_TEMPLATE, CHARACTER_LIMIT


def build_commit_prompt(diff: str) -> str:
    return COMMIT_TEMPLATE.format(diff=diff)


def run_git_command(args):
    result = subprocess.run(["git"] + args, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Git error: {result.stderr.strip()}")
        sys.exit(1)


def cli():
    args = sys.argv[1:]

    if not args:
        print("\nUsage: python main.py [option]\n")
        print("  --staged         Generate message from staged changes")
        print("  --all            Stage all files and generate message")
        print("  -e <files...>    Add specified files before generating message\n")
        return

    if args[0] == "--staged":
        pass  # already staged, do nothing

    elif args[0] == "--all":
        print("🔧 Running git add for all files...")
        run_git_command(["add", "."])

    elif args[0] == "-e":
        files = args[1:]
        if not files:
            print("❗ Please provide files after -e")
            return
        print(f"🔧 Running git add for specified files: {files}")
        run_git_command(["add"] + files)

    else:
        print("❌ Invalid option.")
        return

    try:
        diff = get_staged_diff()
        if not diff:
            print("❗ No staged changes to commit.")
            return

        commit_msg = sanitize_commit_message(diff)

        if len(commit_msg) > CHARACTER_LIMIT:
            print(f"❗❗❗ Message too long (>{CHARACTER_LIMIT} characters)")
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
    cli()
