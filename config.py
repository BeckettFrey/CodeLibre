COMMIT_TEMPLATE = """ Generate a commit message for the code diff below in the format: 
<prefix>: <summary>

Rules:
- Use prefix: fix, feat, refactor, docs, test, chore, etc.
- Summary: max 20 chars, lowercase, numbers, spaces, colons, periods only 
- Return only the commit message

Code diff: {diff} """

SYSTEM_PROMPT = "Return only the commit message. No quotes. No explanation."

CHARACTER_LIMIT = 8000  # Limit for efficient anthropic API input