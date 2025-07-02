# File: src/codelibre/cli.py
import sys
import os
from codelibre.utils.git_helpers import get_staged_diff, sanitize_commit_message, run_git_command, unstage_all_changes
from codelibre.graph.graph import build_chat_graph
from codelibre.config import BASE_TEMPLATE, SYSTEM_PROMPT
from codelibre.graph.state import ChatState
from codelibre.graph.nodes import ExitRequestedException
from langchain_core.messages import HumanMessage
from codelibre.config import Colors
from anthropic import APIStatusError
import traceback


def print_header():
    """Print a clean header for the application."""
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'─' * 50}")
    print("  🚀 Smart Git Commit Message Generator")
    print(f"{'─' * 50}{Colors.RESET}")


def print_separator():
    """Print a subtle separator line."""
    print(f"{Colors.DIM}{'─' * 30}{Colors.RESET}")


def get_user_confirmation(commit_message):
    """Enhanced user confirmation with better formatting."""
    print(f"\n{Colors.GREEN}{Colors.BOLD}📝 Proposed Commit Message:{Colors.RESET}" + f" {commit_message}")

    print_separator()
    print(f"{Colors.BOLD}What would you like to do?{Colors.RESET}")
    print(f"  {Colors.GREEN}[y]es{Colors.RESET}    → Commit now")
    print(f"  {Colors.YELLOW}[e]dit{Colors.RESET}   → Modify message")
    print(f"  {Colors.RED}[n]o{Colors.RESET}     → Cancel")
    
    while True:
        try:
            choice = input(f"\n{Colors.BOLD}Your choice (y/e/n):{Colors.RESET} ").lower().strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n{Colors.YELLOW}⚡ Cancelled{Colors.RESET}")
            return None, False
        
        if choice in ['y', 'yes', '']:  # Default to yes on enter
            return commit_message, True
        elif choice in ['n', 'no']:
            print(f"{Colors.RED}✗ Cancelled{Colors.RESET}")
            return None, False
        elif choice in ['e', 'edit']:
            print(f"\n{Colors.DIM}Current message:{Colors.RESET}")
            print(f"  {commit_message}")
            try:
                new_message = input(f"\n{Colors.BOLD}Enter your message:{Colors.RESET} ").strip()
                if new_message:
                    return new_message, True
                else:
                    print(f"{Colors.YELLOW}⚠ No changes made, keeping original{Colors.RESET}")
                    return commit_message, True
            except (EOFError, KeyboardInterrupt):
                print(f"\n{Colors.YELLOW}⚡ Edit cancelled{Colors.RESET}")
                return None, False
        else:
            print(f"{Colors.YELLOW}⚠ Please type 'y' to commit, 'e' to edit, or 'n' to cancel{Colors.RESET}")


def execute_commit(commit_message):
    """Execute git commit with enhanced feedback."""
    try:
        print(f"\n{Colors.BLUE}⚙ Committing changes...{Colors.RESET}")
        print(f"  {Colors.DIM}git commit -m \"{commit_message}\"{Colors.RESET}")
        
        result = run_git_command(["commit", "-m", commit_message])
        
        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ Successfully committed!{Colors.RESET}")
        
        if result.stdout:
            print(f"  {Colors.DIM}{result.stdout.strip()}{Colors.RESET}")
            
    except Exception as e:
        print(f"\n{Colors.RED}✗ Failed to commit: {e}{Colors.RESET}")
        sys.exit(1)


def print_usage():
    """Display usage information with better formatting."""
    print_header()
    print(f"\n{Colors.BOLD}Usage:{Colors.RESET}")
    print(f"  python main.py {Colors.CYAN}[option]{Colors.RESET}")
    
    print(f"\n{Colors.BOLD}Options:{Colors.RESET}")
    print(f"  {Colors.GREEN}--staged{Colors.RESET}      Generate message from staged changes")
    print(f"  {Colors.GREEN}--all{Colors.RESET}         Stage all files and generate message")
    print(f"  {Colors.GREEN}-e <files...>{Colors.RESET} Add specified files before generating message")
    
    print(f"\n{Colors.DIM}Examples:")
    print("  python main.py --staged")
    print("  python main.py --all")
    print(f"  python main.py -e src/main.py README.md{Colors.RESET}")
    print()


def print_status(message, status_type="info"):
    """Print status messages with consistent formatting."""
    icons = {
        "info": f"{Colors.BLUE}ℹ",
        "success": f"{Colors.GREEN}✓",
        "warning": f"{Colors.YELLOW}⚠",
        "error": f"{Colors.RED}✗",
        "process": f"{Colors.CYAN}⚙"
    }
    
    icon = icons.get(status_type, "•")
    print(f"{icon} {message}{Colors.RESET}")


def cli():
    """Main entry point for the CodeLibre."""
    args = sys.argv[1:]

    if not args:
        print_usage()
        return

    print_header()

    # Handle command line arguments
    if args[0] == "--staged":
        print_status("Using currently staged changes", "info")
    elif args[0] == "--all":
        print_status("Staging all files...", "process")
        run_git_command(["add", "."])
        print_status("All files staged successfully", "success")
    elif args[0] == "-e":
        files = args[1:]
        if not files:
            print_status("No files specified", "error")
            print(f"  {Colors.DIM}Usage: python main.py -e <file1> <file2> ...{Colors.RESET}")
            return
        
        print_status(f"Staging specified files: {', '.join(files)}", "process")

        # Sanitize file paths before staging
        files = [sanitize_commit_message(f) for f in files]

        try:
            # Unstage any previously staged files that are not in the new list
            run_git_command(["reset", "HEAD"] + files)

            # Stage the specified files
            run_git_command(["add"] + files)

            print_status("Files staged successfully", "success")
            
        except Exception as e:
            print_status(f"Failed to stage files: {e}", "error")
            return
        
    else:
        print_status("Unknown option", "error")
        print(f"  {Colors.DIM}Run without arguments to see available options{Colors.RESET}")
        return

    try:
        print_separator()
        print_status("Analyzing staged changes...", "process")
        
        diff = get_staged_diff()
        if not diff:
            print_status("No changes staged for commit", "warning")
            print(f"  {Colors.DIM}Tip: Use 'codelibre -e <files>' or run with --all{Colors.RESET}")
            return
        
        # Build graph, create initial state with first message
        chat_app = build_chat_graph().compile()
        state = ChatState(messages=[], system_prompt=SYSTEM_PROMPT)
        state.messages.append(HumanMessage(content=BASE_TEMPLATE.format(diff=diff)))
   
        print_status("Generating commit message...", "process")
        print()
        
        # Show a subtle progress indicator
        print(f"{Colors.CYAN}", end='')
        
        final_response = ""

        # Process only 'ask' node events
        for message_chunk, metadata in chat_app.stream( 
            state,
            stream_mode="messages",
        ):
            if (message_chunk and metadata["langgraph_node"] == "ask"):
                print(message_chunk.content, end='', flush=True)
                final_response += message_chunk.content
        
        print(f"{Colors.RESET}")  # Reset color and newline
        
        if not final_response:
            print_status("Unable to generate commit message", "error")
            print(f"  {Colors.DIM}Try with different changes or check your diff{Colors.RESET}")
            return
            
        sanitized_commit_msg = sanitize_commit_message(final_response.strip())
        
        # Get user confirmation and execute if approved
        final_message, should_commit = get_user_confirmation(sanitized_commit_msg)
        
        if should_commit and final_message:
            execute_commit(final_message)
        
        print()  # Final spacing


    except ExitRequestedException:
        if args[0] != "--staged":
            unstage_all_changes()  # Ensure we unstage if user exits (except for --staged)
        print(f"\n{Colors.YELLOW}⚡ Stopped by user request{Colors.RESET}")
        sys.exit(0)

    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⚡ Interrupted (Ctrl+C){Colors.RESET}")
        sys.exit(1)

    except APIStatusError:
        print(f"\n{Colors.RED}✗ API is currently overloaded. Please try again later.{Colors.RESET}")
        print(f"  {Colors.DIM}If this persists, check your API usage limits or contact support.{Colors.RESET}")
        sys.exit(1)

    except Exception as e:
        print(f"\n{Colors.RED}✗ Something went wrong: {e}{Colors.RESET}")
        if os.getenv('DEBUG'):
            print(f"{Colors.DIM}Full error details:{Colors.RESET}")
            traceback.print_exc()
        else:
            print(f"  {Colors.DIM}Run with DEBUG=1 for more details{Colors.RESET}")
        print()


if __name__ == "__main__":
    cli()