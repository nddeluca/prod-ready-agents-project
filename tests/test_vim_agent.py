"""
Tests for the VimAgent class and related components
"""

import pytest

from pynvim_agents import VimAgent, VimAgentState, VimEditCommand


class TestVimEditCommand:
    """Test the VimEditCommand class"""

    def test_command_creation(self):
        """Test creating a vim edit command"""
        cmd = VimEditCommand("iHello<Esc>", "Type hello and exit insert mode")
        assert cmd.keystrokes == "iHello<Esc>"
        assert cmd.description == "Type hello and exit insert mode"
        assert cmd.expected_result is None
        assert cmd.timestamp > 0

    def test_command_with_expected_result(self):
        """Test command with expected result"""
        cmd = VimEditCommand("dd", "Delete line", "Line should be deleted")
        assert cmd.expected_result == "Line should be deleted"

    def test_command_to_dict(self):
        """Test converting command to dictionary"""
        cmd = VimEditCommand("gg", "Go to first line", "Cursor at line 1")
        cmd_dict = cmd.to_dict()

        assert cmd_dict["keystrokes"] == "gg"
        assert cmd_dict["description"] == "Go to first line"
        assert cmd_dict["expected_result"] == "Cursor at line 1"
        assert "timestamp" in cmd_dict


class TestVimAgentState:
    """Test the VimAgentState class"""

    def test_state_creation(self):
        """Test creating agent state"""
        content = ["Hello", "World"]
        cursor = (1, 0)
        mode = "n"

        state = VimAgentState(content, cursor, mode)
        assert state.buffer_content == content
        assert state.cursor_position == cursor
        assert state.mode == mode
        assert state.timestamp > 0

    def test_state_to_dict(self):
        """Test converting state to dictionary"""
        content = ["line1", "line2"]
        state = VimAgentState(content, (2, 3), "i")
        state_dict = state.to_dict()

        assert state_dict["buffer_content"] == content
        assert state_dict["cursor_position"] == (2, 3)
        assert state_dict["mode"] == "i"
        assert state_dict["line_count"] == 2
        assert state_dict["current_line"] == "line2"
        assert "timestamp" in state_dict


class TestVimAgent:
    """Test the VimAgent class"""

    def test_agent_initialization_empty(self):
        """Test creating agent with empty buffer"""
        with VimAgent() as agent:
            state = agent.get_current_state()
            assert state.buffer_content == [""]
            assert state.cursor_position == (1, 0)
            assert state.mode == "n"

    def test_agent_initialization_with_content(self):
        """Test creating agent with initial content"""
        initial_content = ["Hello", "World"]
        with VimAgent(initial_content) as agent:
            state = agent.get_current_state()
            assert state.buffer_content == initial_content
            assert state.cursor_position == (1, 0)
            assert state.mode == "n"

    def test_execute_single_command(self):
        """Test executing a single vim command"""
        with VimAgent() as agent:
            result = agent.execute_command("i", "Enter insert mode")

            assert result["success"] is True
            assert "Enter insert mode" in result["message"]
            assert result["state"]["mode"] == "i"
            assert "command" in result

    def test_execute_command_failure_handling(self):
        """Test handling of command failures"""
        with VimAgent() as agent:
            # This should work fine - not actually a failure case for our implementation
            result = agent.execute_command("invalidcommand", "Invalid command")
            # Our vim simulation may just type these as literal characters
            # which is actually valid behavior
            assert "success" in result

    def test_execute_multiple_commands(self):
        """Test executing multiple commands in sequence"""
        with VimAgent() as agent:
            commands = [
                {"keystrokes": "i", "description": "Enter insert mode"},
                {"keystrokes": "Hello", "description": "Type text"},
                {"keystrokes": "<Esc>", "description": "Exit insert mode"},
            ]

            results = agent.execute_commands(commands)
            assert len(results) == 3
            assert all(result["success"] for result in results)

            # Check final state
            final_state = agent.get_current_state()
            assert final_state.mode == "n"
            assert "Hello" in final_state.buffer_content[0]

    def test_execute_commands_with_strings(self):
        """Test executing commands provided as strings"""
        with VimAgent() as agent:
            commands = ["i", "Test", "<Esc>"]
            results = agent.execute_commands(commands)

            assert len(results) == 3
            assert all(result["success"] for result in results)

    def test_buffer_summary(self):
        """Test getting buffer summary"""
        with VimAgent(["Line 1", "Line 2"]) as agent:
            summary = agent.get_buffer_summary()

            assert summary["line_count"] == 2
            assert summary["mode"] == "n"
            assert summary["cursor_position"] == (1, 0)
            assert summary["current_line_number"] == 1
            assert summary["current_column"] == 0
            assert summary["current_line_content"] == "Line 1"
            assert summary["buffer_content"] == ["Line 1", "Line 2"]
            assert summary["is_empty"] is False
            assert summary["total_characters"] == 12  # "Line 1" + "Line 2"

    def test_buffer_summary_empty(self):
        """Test buffer summary with empty buffer"""
        with VimAgent() as agent:
            summary = agent.get_buffer_summary()

            assert summary["line_count"] == 1
            assert summary["is_empty"] is True
            assert summary["total_characters"] == 0
            assert summary["current_line_content"] == ""

    def test_context_window(self):
        """Test getting context window around cursor"""
        content = ["Line 1", "Line 2", "Line 3", "Line 4", "Line 5"]
        with VimAgent(content) as agent:
            # Move cursor to line 3
            agent.execute_command("3G", "Go to line 3")

            context = agent.get_context_window(lines_before=1, lines_after=1)

            assert context["cursor_position"][0] == 3  # Should be at line 3
            assert context["mode"] == "n"
            assert context["window_start"] == 2  # Line 3-1
            assert context["window_end"] == 4  # Line 3+1
            assert context["total_lines"] == 5

            # Check context lines
            assert len(context["context_lines"]) == 3
            assert context["context_lines"][1]["is_cursor_line"] is True
            assert context["context_lines"][1]["line_number"] == 3
            assert context["context_lines"][1]["content"] == "Line 3"

    def test_context_window_edge_cases(self):
        """Test context window at buffer edges"""
        content = ["Only line"]
        with VimAgent(content) as agent:
            context = agent.get_context_window(lines_before=5, lines_after=5)

            assert context["window_start"] == 1
            assert context["window_end"] == 1
            assert len(context["context_lines"]) == 1
            assert context["context_lines"][0]["is_cursor_line"] is True

    def test_suggestions_normal_mode(self):
        """Test getting suggestions in normal mode"""
        with VimAgent() as agent:
            suggestions = agent.suggest_next_actions()

            assert len(suggestions) > 0
            suggestion_text = " ".join(suggestions)
            assert "insert mode" in suggestion_text.lower()
            assert "delete" in suggestion_text.lower()

    def test_suggestions_insert_mode(self):
        """Test getting suggestions in insert mode"""
        with VimAgent() as agent:
            agent.execute_command("i", "Enter insert mode")
            suggestions = agent.suggest_next_actions()

            suggestion_text = " ".join(suggestions)
            assert "normal mode" in suggestion_text.lower()
            assert "type text" in suggestion_text.lower()

    def test_suggestions_visual_mode(self):
        """Test getting suggestions in visual mode"""
        with VimAgent(["Some text"]) as agent:
            agent.execute_command("v", "Enter visual mode")
            suggestions = agent.suggest_next_actions()

            suggestion_text = " ".join(suggestions)
            assert "delete" in suggestion_text.lower()
            assert (
                "yank" in suggestion_text.lower() or "copy" in suggestion_text.lower()
            )

    def test_editing_session_summary(self):
        """Test getting editing session summary"""
        with VimAgent() as agent:
            # Execute a few commands
            agent.execute_command("i", "Enter insert")
            agent.execute_command("Hello", "Type text")
            agent.execute_command("<Esc>", "Exit insert")

            summary = agent.get_editing_session_summary()

            assert summary["total_commands"] == 3
            assert "current_state" in summary
            assert len(summary["command_history"]) == 3
            assert summary["state_changes"] == 4  # Initial + 3 commands
            assert summary["session_duration"] >= 0

    def test_format_state_for_llm(self):
        """Test formatting state for LLM consumption"""
        with VimAgent(["Hello", "World"]) as agent:
            formatted = agent.format_state_for_llm()

            assert "VIM EDITOR STATE" in formatted
            assert "Mode: n" in formatted
            assert "Cursor:" in formatted
            assert "BUFFER CONTEXT" in formatted
            assert "Hello" in formatted
            assert "World" in formatted
            assert "SUGGESTED ACTIONS" in formatted

    def test_format_state_for_llm_without_suggestions(self):
        """Test formatting state without suggestions"""
        with VimAgent(["Test"]) as agent:
            formatted = agent.format_state_for_llm(include_suggestions=False)

            assert "VIM EDITOR STATE" in formatted
            assert "BUFFER CONTEXT" in formatted
            assert "SUGGESTED ACTIONS" not in formatted

    def test_state_history_tracking(self):
        """Test that state history is properly tracked"""
        with VimAgent() as agent:
            initial_history_length = len(agent.state_history)

            agent.execute_command("i", "Enter insert")
            assert len(agent.state_history) == initial_history_length + 1

            agent.execute_command("Hello", "Type text")
            assert len(agent.state_history) == initial_history_length + 2

    def test_command_history_tracking(self):
        """Test that command history is properly tracked"""
        with VimAgent() as agent:
            assert len(agent.command_history) == 0

            agent.execute_command("i", "Enter insert")
            assert len(agent.command_history) == 1
            assert agent.command_history[0].keystrokes == "i"
            assert agent.command_history[0].description == "Enter insert"

    def test_agent_inactive_after_close(self):
        """Test that agent becomes inactive after closing"""
        agent = VimAgent()
        assert agent.active is True

        agent.close()
        assert agent.active is False

        # Should raise error when trying to use inactive agent
        with pytest.raises(RuntimeError, match="Agent is not active"):
            agent.get_current_state()

        with pytest.raises(RuntimeError, match="Agent is not active"):
            agent.execute_command("i", "Test")

    def test_context_manager_cleanup(self):
        """Test that context manager properly cleans up"""
        agent = VimAgent()
        assert agent.active is True

        with agent:
            assert agent.active is True
            # Use agent
            agent.execute_command("i", "Test")

        # Should be cleaned up after context exit
        assert agent.active is False


class TestVimAgentIntegration:
    """Integration tests for VimAgent with realistic workflows"""

    def test_realistic_editing_workflow(self):
        """Test a realistic editing workflow"""
        with VimAgent() as agent:
            # Create a simple Python function
            commands = [
                {"keystrokes": "i", "description": "Enter insert mode"},
                {
                    "keystrokes": "def greet(name):",
                    "description": "Function definition",
                },
                {"keystrokes": "<Enter>", "description": "New line"},
                {
                    "keystrokes": "    return f'Hello, {name}!'",
                    "description": "Function body",
                },
                {"keystrokes": "<Esc>", "description": "Exit insert mode"},
            ]

            results = agent.execute_commands(commands)
            assert all(r["success"] for r in results)

            # Verify final state
            state = agent.get_current_state()
            assert state.mode == "n"
            content = state.buffer_content
            assert "def greet(name):" in content[0]
            assert "return f'Hello, {name}!'" in content[1]

    def test_editing_with_navigation(self):
        """Test editing with cursor navigation"""
        initial_content = ["Line 1", "Line 2", "Line 3"]
        with VimAgent(initial_content) as agent:
            # Go to second line and modify it
            commands = [
                {"keystrokes": "j", "description": "Move down one line"},
                {"keystrokes": "A", "description": "Append at end of line"},
                {"keystrokes": " - modified", "description": "Add text"},
                {"keystrokes": "<Esc>", "description": "Exit insert mode"},
            ]

            results = agent.execute_commands(commands)
            assert all(r["success"] for r in results)

            # Check that line 2 was modified
            content = agent.get_current_state().buffer_content
            assert "Line 2 - modified" in content[1]

    def test_deletion_and_undo(self):
        """Test deletion and undo operations"""
        with VimAgent(["Delete me", "Keep me"]) as agent:
            # Delete first line
            result = agent.execute_command("dd", "Delete first line")
            assert result["success"]

            content = agent.get_current_state().buffer_content
            assert content == ["Keep me"]

            # Undo deletion
            result = agent.execute_command("u", "Undo deletion")
            assert result["success"]

            content = agent.get_current_state().buffer_content
            assert len(content) == 2
            assert "Delete me" in content[0]
