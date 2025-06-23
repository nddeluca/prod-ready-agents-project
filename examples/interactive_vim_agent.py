#!/usr/bin/env python3
"""
Interactive Vim Agent - A simple interactive demo showing how an LLM could use the VimAgent

This provides a command-line interface where you can:
1. Give editing instructions in natural language
2. Execute vim commands directly
3. See the buffer state after each operation
4. Get suggestions for next actions

Usage:
    python interactive_vim_agent.py
"""

import json
import sys

from pynvim_agents import VimAgent


class InteractiveVimAgent:
    """Interactive wrapper around VimAgent for demo purposes"""

    def __init__(self, initial_content: list[str] | None = None):
        self.agent = VimAgent(initial_content)
        self.running = True

    def show_help(self):
        """Show available commands"""
        help_text = """
=== Interactive Vim Agent Commands ===

1. Direct vim commands:
   > i                    (enter insert mode)
   > Hello World<Esc>     (type text and exit insert mode)
   > dd                   (delete line)
   > gg                   (go to first line)
   > /search<Enter>       (search for text)

2. Special commands:
   :state                 (show current state)
   :context               (show context window)
   :summary               (show buffer summary)
   :history               (show command history)
   :suggestions           (show suggested next actions)
   :help                  (show this help)
   :quit                  (exit the agent)

3. Multi-step commands (JSON format):
   [{"keystrokes": "i", "description": "enter insert"}, {"keystrokes": "hello", "description": "type"}]

4. Natural language (simulated LLM responses):
   Just type what you want to do, like:
   "Add a function definition"
   "Fix the indentation"
   "Delete the current line"
"""
        print(help_text)

    def show_state(self):
        """Show current editor state"""
        print("\n" + "=" * 60)
        print(self.agent.format_state_for_llm())
        print("=" * 60 + "\n")

    def show_context(self):
        """Show context window around cursor"""
        context = self.agent.get_context_window()
        print(f"\nContext (lines {context['window_start']}-{context['window_end']}):")
        print("-" * 40)
        for line_info in context["context_lines"]:
            marker = " ► " if line_info["is_cursor_line"] else "   "
            print(f"{marker}{line_info['line_number']:3d}: {line_info['content']}")
        print("-" * 40)

    def show_summary(self):
        """Show buffer summary"""
        summary = self.agent.get_buffer_summary()
        print("\nBuffer Summary:")
        print(f"  Lines: {summary['line_count']}")
        print(f"  Mode: {summary['mode']}")
        print(
            f"  Cursor: Line {summary['current_line_number']}, Column {summary['current_column']}"
        )
        print(f"  Characters: {summary['total_characters']}")
        print(f"  Current line: '{summary['current_line_content']}'")

    def show_history(self):
        """Show command history"""
        session = self.agent.get_editing_session_summary()
        print(f"\nCommand History ({session['total_commands']} commands):")
        for i, cmd in enumerate(session["command_history"][-10:], 1):  # Show last 10
            print(f"  {i:2d}. {cmd['keystrokes']:15s} - {cmd['description']}")

    def show_suggestions(self):
        """Show suggested next actions"""
        suggestions = self.agent.suggest_next_actions()
        print("\nSuggested Actions:")
        for i, suggestion in enumerate(suggestions[:8], 1):  # Show top 8
            print(f"  {i}. {suggestion}")

    def simulate_llm_response(self, user_input: str):
        """Simulate how an LLM might respond to natural language editing requests"""
        user_lower = user_input.lower()

        # Simple pattern matching to simulate LLM understanding
        if "function" in user_lower and "add" in user_lower:
            return [
                {"keystrokes": "o", "description": "Open new line"},
                {
                    "keystrokes": "def new_function():",
                    "description": "Add function definition",
                },
                {"keystrokes": "<Enter>    pass", "description": "Add function body"},
                {"keystrokes": "<Esc>", "description": "Exit insert mode"},
            ]
        elif "delete" in user_lower and (
            "line" in user_lower or "current" in user_lower
        ):
            return [{"keystrokes": "dd", "description": "Delete current line"}]
        elif "indent" in user_lower or "fix indent" in user_lower:
            return [{"keystrokes": ">>", "description": "Indent current line"}]
        elif "save" in user_lower:
            return [{"keystrokes": ":w<Enter>", "description": "Save file (simulated)"}]
        elif "undo" in user_lower:
            return [{"keystrokes": "u", "description": "Undo last change"}]
        elif "search" in user_lower:
            return [{"keystrokes": "/TODO<Enter>", "description": "Search for TODO"}]
        elif "replace" in user_lower:
            return [
                {
                    "keystrokes": ":%s/old/new/g<Enter>",
                    "description": "Replace all 'old' with 'new'",
                }
            ]
        else:
            print(
                f"🤖 Simulated LLM: I'm not sure how to '{user_input}'. Try a vim command or use :help"
            )
            return None

    def execute_command(self, command: str):
        """Execute a single vim command"""
        try:
            result = self.agent.execute_command(command)
            if result["success"]:
                print(f"✅ {result['message']}")
            else:
                print(f"❌ {result['message']}")
                if "error" in result:
                    print(f"   Error: {result['error']}")
            return result["success"]
        except Exception as e:
            print(f"❌ Error executing command: {e}")
            return False

    def execute_command_list(self, commands: list[dict]):
        """Execute a list of commands"""
        print(f"🤖 Executing {len(commands)} commands:")
        for i, cmd in enumerate(commands, 1):
            keystrokes = cmd.get("keystrokes", "")
            description = cmd.get("description", "")
            print(f"  {i}. {description}")

            if not self.execute_command(keystrokes):
                print("   ⚠️  Stopping execution due to error")
                break

    def process_input(self, user_input: str):
        """Process user input and execute appropriate action"""
        user_input = user_input.strip()

        if not user_input:
            return

        # Handle special commands
        if user_input.startswith(":"):
            command = user_input[1:].lower()
            if command == "quit" or command == "q":
                self.running = False
                print("👋 Goodbye!")
            elif command == "help" or command == "h":
                self.show_help()
            elif command == "state":
                self.show_state()
            elif command == "context":
                self.show_context()
            elif command == "summary":
                self.show_summary()
            elif command == "history":
                self.show_history()
            elif command == "suggestions":
                self.show_suggestions()
            else:
                print(f"Unknown command: {command}. Use :help for available commands.")
            return

        # Handle JSON command lists
        if user_input.startswith("[") and user_input.endswith("]"):
            try:
                commands = json.loads(user_input)
                self.execute_command_list(commands)
                return
            except json.JSONDecodeError:
                print("❌ Invalid JSON format")
                return

        # Check if it looks like a vim command
        vim_indicators = [
            "<",
            ">",
            "gg",
            "dd",
            "yy",
            "/",
            ":",
            "i",
            "a",
            "o",
            "O",
            "u",
            "p",
        ]
        if (
            any(indicator in user_input for indicator in vim_indicators)
            or len(user_input.split()) == 1
        ):
            # Treat as direct vim command
            self.execute_command(user_input)
        else:
            # Treat as natural language and simulate LLM response
            print(f"🤖 Simulated LLM interpreting: '{user_input}'")
            commands = self.simulate_llm_response(user_input)
            if commands:
                self.execute_command_list(commands)

    def run(self):
        """Run the interactive session"""
        print("🚀 Interactive Vim Agent Started!")
        print("Type :help for commands, :quit to exit")

        # Show initial state
        self.show_state()

        while self.running:
            try:
                user_input = input("\nvim-agent> ").strip()
                if user_input:
                    self.process_input(user_input)

                    # Show updated state after each command (unless it was a query command)
                    if not user_input.startswith(":") or user_input.startswith(
                        ":state"
                    ):
                        self.show_context()

            except KeyboardInterrupt:
                print("\n👋 Exiting...")
                self.running = False
            except EOFError:
                print("\n👋 Exiting...")
                self.running = False

        # Cleanup
        self.agent.close()


def main():
    """Main entry point"""
    print("=" * 60)
    print("   INTERACTIVE VIM AGENT - LLM Text Editing Demo")
    print("=" * 60)

    # Check if user wants to start with content
    if len(sys.argv) > 1 and sys.argv[1] == "--example":
        initial_content = [
            "# Example Python code",
            "def hello():",
            "print('Hello, World!')",  # Intentionally bad indentation
            "",
            "# TODO: Add more functions",
        ]
        print("Starting with example Python code...")
    else:
        initial_content = None
        print("Starting with empty buffer...")

    # Run the interactive agent
    interactive_agent = InteractiveVimAgent(initial_content)
    try:
        interactive_agent.run()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        interactive_agent.agent.close()


if __name__ == "__main__":
    main()
