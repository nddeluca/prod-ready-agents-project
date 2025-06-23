#!/usr/bin/env python3
"""
Vim Agent Demo - Shows how an LLM can use the VimAgent for interactive text editing

This demonstrates the iterative workflow where an LLM agent:
1. Receives the current buffer state
2. Decides what editing action to take
3. Executes vim commands
4. Receives feedback and continues
"""

from pynvim_agents import VimAgent


def demo_basic_editing():
    """Demo 1: Basic text editing workflow"""
    print("=== Demo 1: Basic Text Editing ===\n")

    with VimAgent() as agent:
        # Show initial state
        print("Initial state:")
        print(agent.format_state_for_llm())
        print("\n" + "=" * 50 + "\n")

        # Step 1: Enter insert mode and add some text
        result = agent.execute_command("i", "Enter insert mode")
        print("After entering insert mode:")
        print(agent.format_state_for_llm())
        print(f"Command result: {result['message']}")
        print("\n" + "=" * 50 + "\n")

        # Step 2: Type some content
        result = agent.execute_command("Hello, World!", "Type greeting text")
        print("After typing text:")
        print(agent.format_state_for_llm())
        print(f"Command result: {result['message']}")
        print("\n" + "=" * 50 + "\n")

        # Step 3: Add a new line
        result = agent.execute_command("<Enter>", "Create new line")
        print("After adding new line:")
        print(agent.format_state_for_llm())
        print("\n" + "=" * 50 + "\n")

        # Step 4: Add more content
        result = agent.execute_command("This is line 2", "Type second line")
        print("After typing second line:")
        print(agent.format_state_for_llm())
        print("\n" + "=" * 50 + "\n")

        # Step 5: Return to normal mode
        result = agent.execute_command("<Esc>", "Return to normal mode")
        print("After returning to normal mode:")
        print(agent.format_state_for_llm())
        print(f"Command result: {result['message']}")


def demo_editing_workflow():
    """Demo 2: More complex editing workflow"""
    print("\n\n=== Demo 2: Complex Editing Workflow ===\n")

    # Start with some initial content
    initial_content = [
        "def calculate_area(radius):",
        "    return 3.14 * radius * radius",
        "",
        "# TODO: Add error checking",
    ]

    with VimAgent(initial_content) as agent:
        print("Starting with Python code:")
        print(agent.format_state_for_llm())
        print("\n" + "=" * 50 + "\n")

        # Task: Import math module at the top
        commands = [
            {"keystrokes": "gg", "description": "Go to first line"},
            {"keystrokes": "O", "description": "Open line above and enter insert mode"},
            {"keystrokes": "import math", "description": "Add import statement"},
            {"keystrokes": "<Esc>", "description": "Return to normal mode"},
        ]

        print("Executing: Add import statement at top")
        agent.execute_commands(commands)
        print("After adding import:")
        print(agent.format_state_for_llm())
        print("\n" + "=" * 50 + "\n")

        # Task: Replace 3.14 with math.pi
        commands = [
            {"keystrokes": "/3.14<Enter>", "description": "Search for 3.14"},
            {"keystrokes": "cw", "description": "Change word"},
            {"keystrokes": "math.pi", "description": "Replace with math.pi"},
            {"keystrokes": "<Esc>", "description": "Return to normal mode"},
        ]

        print("Executing: Replace 3.14 with math.pi")
        agent.execute_commands(commands)
        print("After replacing constant:")
        print(agent.format_state_for_llm())
        print("\n" + "=" * 50 + "\n")

        # Task: Add error checking
        commands = [
            {"keystrokes": "G", "description": "Go to last line"},
            {
                "keystrokes": "O",
                "description": "Open line above TODO and enter insert mode",
            },
            {
                "keystrokes": "if radius < 0:",
                "description": "Add error check condition",
            },
            {"keystrokes": "<Enter>", "description": "New line"},
            {
                "keystrokes": "    raise ValueError('Radius cannot be negative')",
                "description": "Add error message",
            },
            {"keystrokes": "<Esc>", "description": "Return to normal mode"},
        ]

        print("Executing: Add error checking")
        agent.execute_commands(commands)
        print("After adding error checking:")
        print(agent.format_state_for_llm())
        print("\n" + "=" * 50 + "\n")

        # Show final session summary
        summary = agent.get_editing_session_summary()
        print(f"Session completed with {summary['total_commands']} commands")
        print(f"Final buffer has {summary['current_state']['line_count']} lines")


def demo_llm_simulation():
    """Demo 3: Simulate how an LLM would interact with the agent"""
    print("\n\n=== Demo 3: LLM Interaction Simulation ===\n")

    # Simulate LLM receiving a task: "Create a Python class for a simple calculator"
    with VimAgent() as agent:

        # LLM Decision 1: Start by entering insert mode
        print("🤖 LLM Decision: I need to create a Python class. Let me start typing.")
        agent.execute_command("i", "Enter insert mode to start typing")
        print("📍 Current state after entering insert mode:")
        print(agent.format_state_for_llm(include_suggestions=False))
        print("\n" + "-" * 40 + "\n")

        # LLM Decision 2: Type the class definition
        print("🤖 LLM Decision: I'll create a Calculator class with basic methods.")
        commands = [
            "class Calculator:",
            "<Enter>",
            "    def __init__(self):",
            "<Enter>",
            "        pass",
            "<Enter>",
            "<Enter>",
            "    def add(self, a, b):",
            "<Enter>",
            "        return a + b",
        ]

        for cmd in commands:
            agent.execute_command(cmd, f"Type: {cmd}")

        print("📍 Current state after typing class structure:")
        print(agent.format_state_for_llm(include_suggestions=False))
        print("\n" + "-" * 40 + "\n")

        # LLM Decision 3: Exit insert mode and add more methods
        print("🤖 LLM Decision: Let me exit insert mode and add more methods.")
        agent.execute_command("<Esc>", "Exit insert mode")

        # Add subtract method
        agent.execute_command("o", "Open new line below")
        agent.execute_command(
            "<Enter>    def subtract(self, a, b):", "Add subtract method"
        )
        agent.execute_command(
            "<Enter>        return a - b", "Add subtract implementation"
        )
        agent.execute_command("<Esc>", "Exit insert mode")

        print("📍 Current state after adding subtract method:")
        print(agent.format_state_for_llm(include_suggestions=False))
        print("\n" + "-" * 40 + "\n")

        # LLM Decision 4: Let me go back and improve the __init__ method
        print(
            "🤖 LLM Decision: The __init__ method should track operations. Let me improve it."
        )

        # Navigate to the pass statement and replace it
        commands = [
            {"keystrokes": "/pass<Enter>", "description": "Find the pass statement"},
            {"keystrokes": "ciw", "description": "Change inner word (replace 'pass')"},
            {"keystrokes": "self.history = []", "description": "Add history tracking"},
            {"keystrokes": "<Esc>", "description": "Exit insert mode"},
        ]

        agent.execute_commands(commands)

        print("📍 Final state after improving __init__:")
        print(agent.format_state_for_llm())
        print("\n" + "-" * 40 + "\n")

        # Show what the LLM accomplished
        buffer_summary = agent.get_buffer_summary()
        print(
            f"🎉 LLM successfully created a {buffer_summary['line_count']}-line Python class!"
        )
        print("Final code:")
        for i, line in enumerate(buffer_summary["buffer_content"], 1):
            print(f"  {i:2d}: {line}")


def demo_interactive_session():
    """Demo 4: Show how this could be used in an interactive LLM session"""
    print("\n\n=== Demo 4: Interactive Session Format ===\n")

    # This shows the format that an LLM would see in a conversation
    with VimAgent(["print('Hello')", "# TODO: Make this better"]) as agent:

        # Simulate the conversation format
        print("USER: Please improve this Python code by adding a function")
        print()
        print(
            "ASSISTANT: I'll help you improve this code. Let me first see the current state:"
        )
        print()
        print(agent.format_state_for_llm())
        print()
        print("I can see we have a simple print statement and a TODO comment.")
        print("Let me refactor this into a proper function:")
        print()

        # Show step-by-step what the LLM would do
        steps = [
            ("gg", "Go to first line"),
            ("O", "Open line above to add function definition"),
            ("def greet():", "Define function"),
            ("<Esc>", "Exit insert mode"),
            ("j", "Move to next line"),
            (">>", "Indent the print statement"),
            ("A", "Go to end of line and enter insert mode"),
            ("<BS><BS><BS><BS><BS><BS><BS><BS><BS>", "Remove 'Hello'"),
            ("return 'Hello, World!'", "Make it return a value"),
            ("<Esc>", "Exit insert mode"),
            ("G", "Go to last line"),
            ("dd", "Delete the TODO comment"),
            ("o", "Add new line"),
            ("", ""),
            ("print(greet())", "Add function call"),
            ("<Esc>", "Exit insert mode"),
        ]

        for i, (keystrokes, description) in enumerate(steps, 1):
            if keystrokes:  # Skip empty steps
                print(f"Step {i}: {description}")
                result = agent.execute_command(keystrokes, description)
                if not result["success"]:
                    print(f"  ❌ Failed: {result['message']}")
                    break
                else:
                    print(f"  ✅ {result['message']}")

            if i % 3 == 0:  # Show state every few steps
                print("\nCurrent state:")
                context = agent.get_context_window(lines_before=2, lines_after=2)
                for line_info in context["context_lines"]:
                    marker = " ► " if line_info["is_cursor_line"] else "   "
                    print(
                        f"{marker}{line_info['line_number']:2d}: {line_info['content']}"
                    )
                print()

        print("\nFinal result:")
        print(agent.format_state_for_llm(include_suggestions=False))
        print("\nThe code has been successfully refactored into a proper function!")


if __name__ == "__main__":
    demo_basic_editing()
    demo_editing_workflow()
    demo_llm_simulation()
    demo_interactive_session()

    print("\n" + "=" * 60)
    print("🎉 All demos completed successfully!")
    print("The VimAgent provides a powerful interface for LLMs to edit text")
    print("using realistic vim commands with full state feedback.")
    print("=" * 60)
