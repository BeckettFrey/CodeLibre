# File: src/codelibre/config.py

# Behavioral Configuration for CodeLibre commit message generation
MAX_CHARACTERS = 45


SYSTEM_PROMPT = f"""
You are an assistant that generates commit messages for the provided code diff.

You must:
- Generate a message in the format: <prefix>: <summary>
- Prefix: fix, feat, refactor, docs, test, chore, etc.
- Summary: max {MAX_CHARACTERS} chars, only lowercase, numbers, spaces, colons, periods.

ALSO incorporate any additional user feedback given after the diff as new requirements on how to phrase or adjust the commit message.

Return ONLY the commit message. No quotes. No explanation.
"""


# Template for the initial human prompt - wrapper
BASE_TEMPLATE = "\nDiff:\n{diff}"


# Added context for iterative feedback - wrapper  
INPUT_TEMPLATE = "\nFeedback:\n{feedback}"


# Colors and styling
class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'

    