# GitClaude/tests/graph/nodes.py

import os
from anthropic import Anthropic
from .state import ChatState
from dotenv import load_dotenv
from config import SYSTEM_PROMPT

load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("Anthropic API key not found. Please set it in the .env file.")

def process_query(state: ChatState) -> ChatState:
    client = Anthropic(api_key=api_key)

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": state.current_message}
        ]
    )

    state.response = message.content[0].text
    return state
