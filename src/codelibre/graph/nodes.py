# File: src/codelibre/graph/nodes.py
import os
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_anthropic import ChatAnthropic
from codelibre.config import Colors
from codelibre.graph.state import ChatState
from codelibre.exceptions import ExitRequestedException, CodeLibreEnvironmentError



load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    raise CodeLibreEnvironmentError(message="ANTHROPIC_API_KEY undefined")

default_model = os.getenv("DEFAULT_MODEL")
if not default_model:
    raise CodeLibreEnvironmentError(message="DEFAULT_MODEL undefined")

default_token_limit = os.getenv("DEFAULT_TOKEN_LIMIT")
if not default_token_limit:
    raise CodeLibreEnvironmentError(message="DEFAULT_TOKEN_LIMIT undefined")
else:
    default_token_limit = int(default_token_limit)


llm = ChatAnthropic(
    model=default_model,
    anthropic_api_key=api_key,
    max_tokens=500,
    temperature=0.7
)


def truncate_messages(state: ChatState) -> ChatState:
    """
    TODO: Implement message truncation logic.
    For now, this is a placeholder that does nothing.
    """
    return state


def add_input(state: ChatState) -> ChatState:
    """
    Node to handle user queries.
    Adds human follow-up input if present, then runs the next LLM step with full memory context.
    Each input is treated as a new message in the chain (maintaining conversation context).
    """
    prompt = ""
    while not prompt:
        try:
            # Create a visually prominent input prompt
            input_text = (
                f"\n{Colors.CYAN}{Colors.BOLD} INPUT REQUIRED {Colors.RESET}\n"
                f"{Colors.DIM}{Colors.BOLD}→ Respond (or 'y' to continue, 'n' to exit): {Colors.RESET}"
            )
            prompt = input(input_text).strip()
            
            if prompt.lower() in ['y', 'yes']:
                print(f"{Colors.GREEN}✓ Continuing...{Colors.RESET}")
                return ChatState(
                    messages=state.messages,
                    system_prompt=state.system_prompt,
                    reiterate=False
                )
            elif prompt.lower() in ['n', 'no', 'exit', 'quit']:
                raise ExitRequestedException("User requested exit")
            elif prompt:
                state.reiterate = True
                break
        except (EOFError, KeyboardInterrupt):
            print(f"\n{Colors.RED}✗ Interrupted by user{Colors.RESET}")
            raise ExitRequestedException("User interrupted")

    state.messages.append(HumanMessage(content="Feedback: " + prompt))
    state.response = ""  # reset response for new query
    return ChatState(
        messages=state.messages,
        system_prompt=state.system_prompt,
        response=state.response,
        reiterate=True  # indicate we need to ask LLM again
    )


def update_conversation_history(state: ChatState) -> ChatState:
    """
    Updates the conversation history with the AI response if one exists.
    This should be called before asking for new input to maintain context.
    """
    if state.response and state.response.strip():
        # Only add AI message if it's not already the last message
        if not state.messages or not isinstance(state.messages[-1], AIMessage):
            state.messages.append(AIMessage(content=state.response))
    
    return ChatState(
        messages=state.messages,
        system_prompt=state.system_prompt,
        response=state.response,
        reiterate=state.reiterate
    )


def ask(state: ChatState) -> ChatState:
    """
    Calls the LLM with the current conversation state,
    ensuring the system prompt is passed only at the top level.
    Includes retry logic for API overload errors.
    """
    import time
    from anthropic import APIStatusError

    # Prepare full prompt: system message + conversation history
    messages = []
    if state.system_prompt:
        # Initialize with system prompt if not found in context
        if not any(isinstance(msg, SystemMessage) for msg in state.messages):
            messages.append(SystemMessage(content=state.system_prompt))

    messages.extend(state.messages)  # the actual conversation history

    # Retry logic for API overload
    max_retries = 3
    base_delay = 2  # seconds
    
    for attempt in range(max_retries):
        try:
            print(f"\nscs{Colors.BLUE}🤖 Asking AI...{Colors.RESET}")
            response = llm.invoke(messages)
            
            if not response or not getattr(response, "content", "").strip():
                raise ValueError("LLM returned an empty response")
            
            print(f"{Colors.GREEN} ✓ AI response{Colors.RESET}")
            return ChatState(
                messages=state.messages,
                system_prompt=state.system_prompt,
                response=response.content,
                reiterate=False 
            )
            
        except APIStatusError as e:
            error_details = getattr(e, 'body', {}) or {}
            error_type = error_details.get('error', {}).get('type', 'unknown')
            
            if error_type == 'overloaded_error' and attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)  # exponential backoff
                print(f"{Colors.CYAN}⚠️  API is overloaded. Retrying in {delay} seconds... (attempt {attempt + 1}/{max_retries}){Colors.RESET}")
                time.sleep(delay)
                continue
            else:
                raise
        except Exception as e:
            print(f"{Colors.RED}✗ Unexpected error: {str(e)}{Colors.RESET}")
            raise
    
    # This should never be reached, but just in case
    raise RuntimeError("Max retries exceeded for API calls")