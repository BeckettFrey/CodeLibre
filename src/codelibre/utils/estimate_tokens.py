# File: src/codelibre/utils/estimate_tokens.py
import re


def estimate_anthropic_tokens(messages):
    """
    Rough estimator for Anthropic-style tokens in a list of messages.
    Each message should be a SystemMessage, HumanMessage, etc.
    Counts roughly: 1 token ≈ 4 characters (average English).
    Adds small overhead per message.
    """
    text = ""
    for m in messages:
        if isinstance(m, str):
            text += m
        else:
            text += m.content

    # Approx 1 token = 4 chars (safe high estimate)
    approx_tokens = len(re.sub(r"\s+", " ", text)) / 4
    approx_tokens += len(messages) * 4

    return int(approx_tokens)