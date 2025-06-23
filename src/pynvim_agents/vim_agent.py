"""
Vim Agent - An LLM-powered agent that can edit text using vim commands

This module provides an intelligent agent that can receive text editing instructions
and execute them using realistic vim keystrokes through the RawNvimEditor interface.
"""

import time
from typing import Any

from .raw_editor import RawNvimEditor


class VimAgentState:
    """Represents the current state of the vim editing session"""

    def __init__(
        self, buffer_content: list[str], cursor_position: tuple[int, int], mode: str
    ):
        self.buffer_content = buffer_content
        self.cursor_position = cursor_position
        self.mode = mode
        self.timestamp = time.time()

    def to_dict(self) -> dict[str, Any]:
        """Convert state to dictionary for serialization"""
        return {
            "buffer_content": self.buffer_content,
            "cursor_position": self.cursor_position,
            "mode": self.mode,
            "timestamp": self.timestamp,
            "line_count": len(self.buffer_content),
            "current_line": (
                self.buffer_content[self.cursor_position[0] - 1]
                if self.buffer_content
                else ""
            ),
        }


class VimEditCommand:
    """Represents a vim editing command with metadata"""

    def __init__(
        self, keystrokes: str, description: str, expected_result: str | None = None
    ):
        self.keystrokes = keystrokes
        self.description = description
        self.expected_result = expected_result
        self.timestamp = time.time()

    def to_dict(self) -> dict[str, Any]:
        """Convert command to dictionary for logging"""
        return {
            "keystrokes": self.keystrokes,
            "description": self.description,
            "expected_result": self.expected_result,
            "timestamp": self.timestamp,
        }


class VimAgent:
    """
    An intelligent agent that can edit text using vim commands

    This agent maintains a vim editing session and can execute commands
    while providing feedback about the current state of the buffer.
    """

    def __init__(self, initial_content: list[str] | None = None):
        """Initialize the vim agent with optional starting content"""
        self.editor = RawNvimEditor(initial_content)
        self.command_history: list[VimEditCommand] = []
        self.state_history: list[VimAgentState] = []
        self.active = True

        # Record initial state
        self._record_current_state()

    def __enter__(self) -> "VimAgent":
        return self

    def __exit__(self, exc_type: type, exc_val: Exception, exc_tb: object) -> None:
        self.close()

    def close(self) -> None:
        """Close the vim editing session"""
        if self.active:
            self.editor.close()
            self.active = False

    def get_current_state(self) -> VimAgentState:
        """Get the current state of the editor"""
        if not self.active:
            raise RuntimeError("Agent is not active")

        return VimAgentState(
            buffer_content=self.editor.get_buffer_content(),
            cursor_position=self.editor.get_cursor_position(),
            mode=self.editor.get_mode(),
        )

    def _record_current_state(self) -> None:
        """Record the current state in history"""
        state = self.get_current_state()
        self.state_history.append(state)

    def execute_command(self, keystrokes: str, description: str = "") -> dict[str, Any]:
        """
        Execute a vim command and return the resulting state

        Args:
            keystrokes: The vim keystrokes to execute (e.g., "iHello<Esc>", "dd", "gg")
            description: Human-readable description of what this command does

        Returns:
            Dictionary containing the new state and command result
        """
        if not self.active:
            raise RuntimeError("Agent is not active")

        # Record command
        command = VimEditCommand(keystrokes, description)
        self.command_history.append(command)

        try:
            # Execute the keystrokes
            self.editor.type_keys(keystrokes)

            # Record new state
            self._record_current_state()
            current_state = self.get_current_state()

            return {
                "success": True,
                "command": command.to_dict(),
                "state": current_state.to_dict(),
                "message": f"Executed: {description or keystrokes}",
            }

        except Exception as e:
            return {
                "success": False,
                "command": command.to_dict(),
                "error": str(e),
                "message": f"Failed to execute: {description or keystrokes}",
            }

    def execute_commands(
        self, commands: list[str | dict[str, str]]
    ) -> list[dict[str, Any]]:
        """
        Execute multiple vim commands in sequence

        Args:
            commands: List of commands, either as strings or dicts with 'keystrokes' and 'description'

        Returns:
            List of results from each command execution
        """
        results = []

        for cmd in commands:
            if isinstance(cmd, str):
                result = self.execute_command(cmd)
            else:
                keystrokes = cmd.get("keystrokes", "")
                description = cmd.get("description", "")
                result = self.execute_command(keystrokes, description)

            results.append(result)

            # Stop executing if a command failed
            if not result["success"]:
                break

        return results

    def get_buffer_summary(self) -> dict[str, Any]:
        """Get a comprehensive summary of the current buffer state"""
        if not self.active:
            raise RuntimeError("Agent is not active")

        state = self.get_current_state()
        content = state.buffer_content

        return {
            "line_count": len(content),
            "mode": state.mode,
            "cursor_position": state.cursor_position,
            "current_line_number": state.cursor_position[0],
            "current_column": state.cursor_position[1],
            "current_line_content": (
                content[state.cursor_position[0] - 1] if content else ""
            ),
            "buffer_content": content,
            "is_empty": len(content) == 1 and content[0] == "",
            "total_characters": sum(len(line) for line in content),
        }

    def get_context_window(
        self, lines_before: int = 3, lines_after: int = 3
    ) -> dict[str, Any]:
        """
        Get a context window around the current cursor position

        Args:
            lines_before: Number of lines to show before cursor
            lines_after: Number of lines to show after cursor

        Returns:
            Dictionary with context information
        """
        if not self.active:
            raise RuntimeError("Agent is not active")

        state = self.get_current_state()
        content = state.buffer_content
        cursor_row = state.cursor_position[0]

        # Calculate window bounds
        start_line = max(1, cursor_row - lines_before)
        end_line = min(len(content), cursor_row + lines_after)

        context_lines = []
        for i in range(start_line, end_line + 1):
            line_content = content[i - 1] if i <= len(content) else ""
            is_cursor_line = i == cursor_row

            context_lines.append(
                {
                    "line_number": i,
                    "content": line_content,
                    "is_cursor_line": is_cursor_line,
                    "cursor_column": (
                        state.cursor_position[1] if is_cursor_line else None
                    ),
                }
            )

        return {
            "cursor_position": state.cursor_position,
            "mode": state.mode,
            "context_lines": context_lines,
            "window_start": start_line,
            "window_end": end_line,
            "total_lines": len(content),
        }

    def suggest_next_actions(self) -> list[str]:
        """
        Suggest possible next actions based on current state

        Returns:
            List of suggested vim commands with descriptions
        """
        state = self.get_current_state()
        suggestions = []

        if state.mode == "n":  # Normal mode
            suggestions.extend(
                [
                    "i - Enter insert mode at cursor",
                    "A - Enter insert mode at end of line",
                    "o - Open new line below and enter insert mode",
                    "O - Open new line above and enter insert mode",
                    "dd - Delete current line",
                    "yy - Yank (copy) current line",
                    "p - Paste below cursor",
                    "gg - Go to first line",
                    "G - Go to last line",
                    "/text - Search for 'text'",
                    ":%s/old/new/g - Replace all 'old' with 'new'",
                ]
            )
        elif state.mode == "i":  # Insert mode
            suggestions.extend(
                [
                    "<Esc> - Return to normal mode",
                    "Type text to insert at cursor",
                    "<Enter> - Create new line",
                    "<BS> - Backspace",
                    "<C-w> - Delete word backwards",
                ]
            )
        elif state.mode == "v":  # Visual mode
            suggestions.extend(
                [
                    "d - Delete selection",
                    "y - Yank (copy) selection",
                    "<Esc> - Return to normal mode",
                    "c - Change (delete and enter insert mode)",
                ]
            )

        return suggestions

    def get_editing_session_summary(self) -> dict[str, Any]:
        """Get a summary of the entire editing session"""
        return {
            "total_commands": len(self.command_history),
            "current_state": self.get_current_state().to_dict(),
            "command_history": [cmd.to_dict() for cmd in self.command_history],
            "state_changes": len(self.state_history),
            "session_duration": time.time()
            - (self.state_history[0].timestamp if self.state_history else time.time()),
        }

    def format_state_for_llm(self, include_suggestions: bool = True) -> str:
        """
        Format current state in a way that's easy for an LLM to understand

        Args:
            include_suggestions: Whether to include suggested next actions

        Returns:
            Formatted string representation of current state
        """
        if not self.active:
            return "Editor session is not active"

        context = self.get_context_window()
        summary = self.get_buffer_summary()

        # Build the formatted output
        output_lines = []
        output_lines.append("=== VIM EDITOR STATE ===")
        output_lines.append(f"Mode: {summary['mode']}")
        output_lines.append(
            f"Cursor: Line {summary['current_line_number']}, Column {summary['current_column']}"
        )
        output_lines.append(f"Total Lines: {summary['line_count']}")
        output_lines.append(f"Total Characters: {summary['total_characters']}")
        output_lines.append("")

        output_lines.append("=== BUFFER CONTEXT ===")
        for line_info in context["context_lines"]:
            line_num = line_info["line_number"]
            content = line_info["content"]
            marker = " ► " if line_info["is_cursor_line"] else "   "

            # Show cursor position on current line
            if line_info["is_cursor_line"] and line_info["cursor_column"] is not None:
                cursor_pos = line_info["cursor_column"]
                if cursor_pos < len(content):
                    content = content[:cursor_pos] + "│" + content[cursor_pos:]
                else:
                    content += "│"

            output_lines.append(f"{marker}{line_num:3d}: {content}")

        if include_suggestions:
            output_lines.append("")
            output_lines.append("=== SUGGESTED ACTIONS ===")
            for suggestion in self.suggest_next_actions()[:5]:  # Limit to top 5
                output_lines.append(f"  • {suggestion}")

        return "\n".join(output_lines)
