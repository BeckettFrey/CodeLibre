COMMIT_TEMPLATE = """
Analyze this code change and write a concise, conventional commit message.

Instructions:
- Use a conventional prefix: refactor, chore, fix, feat, docs, style, test, perf
- Summary must be a single line under 50 characters
- Optionally include a few bullet points for key details
- Only characters allowed in summary: a-z, 0-9, space, .,  and :
- Ex.:
  - added: unit tests for new feature
  - chore: fixed bug in user authentication flow
  - refactor: improved code readability

Code changes:
{diff}
"""

SYSTEM_PROMPT = """
You are a helpful assistant that responds to each message independently.
You have no memory of previous messages in this conversation.
Treat each incoming message as a standalone query.
Keep your responses concise and focused only on the current message.
"""

CHARACTER_LIMIT = 8000  # Limit for anthropic API input