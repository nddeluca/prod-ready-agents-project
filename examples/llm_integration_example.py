#!/usr/bin/env python3
"""
LLM Integration Example - Shows how to integrate VimAgent with an actual LLM

This example demonstrates how you could integrate the VimAgent with:
1. OpenAI's API (commented out - requires API key)
2. A local LLM
3. A simulated LLM for demonstration

The pattern shows how an LLM can iteratively edit text by:
- Receiving the current buffer state
- Deciding what editing action to take
- Executing vim commands
- Receiving feedback and continuing
"""

import re

from pynvim_agents import VimAgent


class SimulatedLLM:
    """
    A simulated LLM that demonstrates how a real LLM could interact with VimAgent

    This uses simple pattern matching to simulate intelligent editing decisions.
    In practice, you'd replace this with calls to OpenAI, Anthropic, or local LLM APIs.
    """

    def __init__(self):
        self.conversation_history = []

    def analyze_task_and_generate_commands(
        self, task: str, current_state: str, context: dict
    ) -> list[dict[str, str]]:
        """
        Analyze the editing task and current state to generate vim commands

        Args:
            task: The editing task to perform (e.g., "Add error handling")
            current_state: Formatted state string from VimAgent
            context: Additional context about the buffer

        Returns:
            List of vim commands to execute
        """
        task_lower = task.lower()

        # Analyze current state
        context.get("mode", "n")
        context.get("line_count", 1)
        context.get("current_line_content", "")

        # Task-specific command generation
        if "function" in task_lower and "add" in task_lower:
            return self._generate_add_function_commands(current_state, context)
        elif "error" in task_lower and (
            "handling" in task_lower or "check" in task_lower
        ):
            return self._generate_error_handling_commands(current_state, context)
        elif "docstring" in task_lower or "documentation" in task_lower:
            return self._generate_docstring_commands(current_state, context)
        elif "import" in task_lower:
            return self._generate_import_commands(task, current_state, context)
        elif "refactor" in task_lower:
            return self._generate_refactor_commands(current_state, context)
        elif "fix" in task_lower and "indent" in task_lower:
            return self._generate_fix_indentation_commands(current_state, context)
        else:
            return self._generate_generic_commands(task, current_state, context)

    def _generate_add_function_commands(
        self, state: str, context: dict
    ) -> list[dict[str, str]]:
        """Generate commands to add a new function"""
        if context.get("line_count", 1) == 1 and not context.get(
            "current_line_content"
        ):
            # Empty buffer - start fresh
            return [
                {"keystrokes": "i", "description": "Enter insert mode"},
                {
                    "keystrokes": "def new_function():",
                    "description": "Add function definition",
                },
                {"keystrokes": "<Enter>    pass", "description": "Add function body"},
                {"keystrokes": "<Esc>", "description": "Exit insert mode"},
            ]
        else:
            # Add function at the end
            return [
                {"keystrokes": "G", "description": "Go to end of file"},
                {"keystrokes": "o", "description": "Open new line"},
                {
                    "keystrokes": "<Enter>def new_function():",
                    "description": "Add function definition",
                },
                {"keystrokes": "<Enter>    pass", "description": "Add function body"},
                {"keystrokes": "<Esc>", "description": "Exit insert mode"},
            ]

    def _generate_error_handling_commands(
        self, state: str, context: dict
    ) -> list[dict[str, str]]:
        """Generate commands to add error handling"""
        # Look for function definitions
        if "def " in state:
            return [
                {
                    "keystrokes": "/def <Enter>",
                    "description": "Find function definition",
                },
                {"keystrokes": "j", "description": "Move to function body"},
                {"keystrokes": "O", "description": "Open line above"},
                {"keystrokes": "    try:", "description": "Add try block"},
                {"keystrokes": "<Esc>", "description": "Exit insert mode"},
                {"keystrokes": "G", "description": "Go to end"},
                {"keystrokes": "O", "description": "Open line above"},
                {
                    "keystrokes": "    except Exception as e:",
                    "description": "Add except block",
                },
                {
                    "keystrokes": "<Enter>        print(f'Error: {e}')",
                    "description": "Add error handling",
                },
                {"keystrokes": "<Esc>", "description": "Exit insert mode"},
            ]
        else:
            return [
                {"keystrokes": "o", "description": "Open new line"},
                {
                    "keystrokes": "# TODO: Add error handling",
                    "description": "Add TODO comment",
                },
                {"keystrokes": "<Esc>", "description": "Exit insert mode"},
            ]

    def _generate_docstring_commands(
        self, state: str, context: dict
    ) -> list[dict[str, str]]:
        """Generate commands to add docstring"""
        return [
            {"keystrokes": "/def <Enter>", "description": "Find function definition"},
            {"keystrokes": "A", "description": "Go to end of line"},
            {"keystrokes": '<Enter>    """', "description": "Start docstring"},
            {
                "keystrokes": "<Enter>    Description of the function",
                "description": "Add description",
            },
            {"keystrokes": '<Enter>    """', "description": "End docstring"},
            {"keystrokes": "<Esc>", "description": "Exit insert mode"},
        ]

    def _generate_import_commands(
        self, task: str, state: str, context: dict
    ) -> list[dict[str, str]]:
        """Generate commands to add import statements"""
        # Extract what to import from the task
        import_match = re.search(r"import (\w+)", task)
        module = import_match.group(1) if import_match else "os"

        return [
            {"keystrokes": "gg", "description": "Go to top of file"},
            {"keystrokes": "O", "description": "Open line above"},
            {
                "keystrokes": f"import {module}",
                "description": f"Import {module} module",
            },
            {"keystrokes": "<Esc>", "description": "Exit insert mode"},
        ]

    def _generate_refactor_commands(
        self, state: str, context: dict
    ) -> list[dict[str, str]]:
        """Generate commands to refactor code"""
        return [
            {"keystrokes": "gg", "description": "Go to start"},
            {"keystrokes": "o", "description": "Open new line"},
            {"keystrokes": "# Refactored code", "description": "Add refactor comment"},
            {"keystrokes": "<Esc>", "description": "Exit insert mode"},
        ]

    def _generate_fix_indentation_commands(
        self, state: str, context: dict
    ) -> list[dict[str, str]]:
        """Generate commands to fix indentation"""
        return [
            {"keystrokes": "gg", "description": "Go to start"},
            {"keystrokes": "V", "description": "Enter line visual mode"},
            {"keystrokes": "G", "description": "Select all lines"},
            {"keystrokes": "=", "description": "Auto-indent selection"},
            {"keystrokes": "<Esc>", "description": "Exit visual mode"},
        ]

    def _generate_generic_commands(
        self, task: str, state: str, context: dict
    ) -> list[dict[str, str]]:
        """Generate generic commands for unrecognized tasks"""
        return [
            {"keystrokes": "o", "description": "Open new line"},
            {"keystrokes": f"# TODO: {task}", "description": f"Add TODO for: {task}"},
            {"keystrokes": "<Esc>", "description": "Exit insert mode"},
        ]


class LLMVimEditor:
    """
    A high-level interface that combines VimAgent with an LLM

    This demonstrates how you could build an intelligent text editor
    that can understand natural language editing instructions.
    """

    def __init__(
        self, initial_content: list[str] | None = None, llm: SimulatedLLM | None = None
    ):
        self.agent = VimAgent(initial_content)
        self.llm = llm or SimulatedLLM()
        self.task_history = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """Close the editor"""
        self.agent.close()

    def execute_task(self, task: str) -> dict:
        """
        Execute a high-level editing task using the LLM

        Args:
            task: Natural language description of what to do

        Returns:
            Dictionary with task results and final state
        """
        print(f"\n🎯 Task: {task}")
        print("-" * 50)

        # Get current state
        current_state = self.agent.format_state_for_llm(include_suggestions=False)
        context = self.agent.get_buffer_summary()

        print("📍 Current state:")
        print(self.agent.format_state_for_llm(include_suggestions=False))

        # Let LLM analyze and generate commands
        print(f"\n🤖 LLM analyzing task: '{task}'")
        commands = self.llm.analyze_task_and_generate_commands(
            task, current_state, context
        )

        if not commands:
            return {
                "success": False,
                "message": "LLM couldn't generate commands for this task",
                "task": task,
                "commands_executed": 0,
            }

        print(f"🎮 LLM generated {len(commands)} commands:")
        for i, cmd in enumerate(commands, 1):
            print(f"  {i}. {cmd['description']} ({cmd['keystrokes']})")

        # Execute commands
        print("\n⚡ Executing commands...")
        results = self.agent.execute_commands(commands)

        successful_commands = sum(1 for r in results if r["success"])
        failed_commands = len(results) - successful_commands

        print(
            f"✅ Successfully executed {successful_commands}/{len(commands)} commands"
        )
        if failed_commands > 0:
            print(f"❌ {failed_commands} commands failed")

        # Show final state
        print("\n📍 Final state:")
        print(self.agent.format_state_for_llm(include_suggestions=False))

        # Record task
        task_result = {
            "success": failed_commands == 0,
            "task": task,
            "commands_generated": len(commands),
            "commands_executed": successful_commands,
            "commands_failed": failed_commands,
            "final_state": self.agent.get_buffer_summary(),
        }

        self.task_history.append(task_result)
        return task_result

    def get_task_history(self) -> list[dict]:
        """Get history of all executed tasks"""
        return self.task_history

    def show_final_code(self):
        """Show the final code with line numbers"""
        content = self.agent.get_buffer_summary()["buffer_content"]
        print(f"\n📄 Final Code ({len(content)} lines):")
        print("=" * 50)
        for i, line in enumerate(content, 1):
            print(f"{i:3d}: {line}")
        print("=" * 50)


def demo_llm_editing_session():
    """Demonstrate a complete LLM-powered editing session"""
    print("🚀 LLM-Powered Vim Editing Session")
    print("=" * 60)

    # Start with some basic Python code
    initial_code = ["# Simple calculator", "print(5 + 3)"]

    with LLMVimEditor(initial_code) as editor:
        # Task 1: Refactor into a function
        editor.execute_task("Add a function to calculate the sum")

        # Task 2: Add error handling
        editor.execute_task("Add error handling to the function")

        # Task 3: Add documentation
        editor.execute_task("Add docstring to the function")

        # Task 4: Add import
        editor.execute_task("Import math module")

        # Show final result
        editor.show_final_code()

        # Show task summary
        history = editor.get_task_history()
        print("\n📊 Session Summary:")
        print(f"Total tasks completed: {len(history)}")
        successful_tasks = sum(1 for task in history if task["success"])
        print(f"Successful tasks: {successful_tasks}/{len(history)}")

        total_commands = sum(task["commands_executed"] for task in history)
        print(f"Total vim commands executed: {total_commands}")


def demo_interactive_llm_session():
    """Demonstrate an interactive session with the LLM editor"""
    print("\n\n🎮 Interactive LLM Session Demo")
    print("=" * 60)

    # Simulate a conversation where user gives tasks
    tasks = [
        "Create a Python class for a simple calculator",
        "Add methods for addition and subtraction",
        "Add error handling for division by zero",
        "Add documentation to all methods",
    ]

    with LLMVimEditor() as editor:
        for i, task in enumerate(tasks, 1):
            print(f"\n👤 User Request #{i}: {task}")
            result = editor.execute_task(task)

            if result["success"]:
                print("✅ Task completed successfully!")
            else:
                print(f"❌ Task failed: {result.get('message', 'Unknown error')}")

            # Brief pause between tasks (in real usage, this would be user input)
            if i < len(tasks):
                print("\n⏸️  Press Enter to continue to next task...")
                # input()  # Uncomment for actual interactive use

        editor.show_final_code()


def demo_real_llm_integration_pattern():
    """
    Show the pattern for integrating with real LLM APIs

    This demonstrates the structure you'd use with OpenAI, Anthropic, etc.
    """
    print("\n\n🔌 Real LLM Integration Pattern")
    print("=" * 60)

    # This is the pattern you'd use with a real LLM API
    integration_example = '''
# Example integration with OpenAI API (requires openai package and API key)

import openai
from pynvim_agents import VimAgent

class OpenAIVimEditor:
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model
        self.agent = VimAgent()

    def execute_task(self, task: str):
        # Get current buffer state
        current_state = self.agent.format_state_for_llm()

        # Create prompt for LLM
        prompt = f"""
You are a vim expert. Given the current buffer state and a task, generate vim commands.

Current buffer state:
{current_state}

Task: {task}

Please respond with a JSON list of vim commands in this format:
[{{"keystrokes": "i", "description": "enter insert mode"}}, ...]

Commands:
"""

        # Call OpenAI API
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )

        # Parse response and execute commands
        try:
            commands = json.loads(response.choices[0].message.content)
            return self.agent.execute_commands(commands)
        except json.JSONDecodeError:
            return {"success": False, "error": "Invalid JSON response from LLM"}

# Usage:
# editor = OpenAIVimEditor("your-api-key")
# editor.execute_task("Add error handling to this function")
'''

    print("Here's how you'd integrate with a real LLM API:")
    print(integration_example)

    print("\n🔑 Key Integration Points:")
    print("1. Format current buffer state with agent.format_state_for_llm()")
    print("2. Send state + task to LLM API")
    print("3. Parse LLM response as JSON command list")
    print("4. Execute commands with agent.execute_commands()")
    print("5. Handle errors and provide feedback")


if __name__ == "__main__":
    demo_llm_editing_session()
    demo_interactive_llm_session()
    demo_real_llm_integration_pattern()

    print("\n" + "=" * 60)
    print("🎉 LLM Integration Examples Complete!")
    print("The VimAgent provides a powerful foundation for building")
    print("LLM-powered text editors with realistic vim command execution.")
    print("=" * 60)
