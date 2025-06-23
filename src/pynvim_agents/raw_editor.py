"""
Raw Nvim Editor - Simulates exact user keystrokes as if typing in nvim

This module provides a realistic nvim interface that:
1. Starts in normal mode (just like opening nvim)
2. Requires explicit mode transitions (i for insert, <Esc> for normal)
3. Simulates exact keystroke sequences a user would type
4. Provides mode awareness and validation
"""

import os
import subprocess
import tempfile
import time

import pynvim


class RawNvimEditor:
    """
    A raw nvim editor interface that simulates real user interaction
    """

    def __init__(self, initial_content: list[str] | None = None):
        """Initialize a raw nvim editor instance"""
        self.tmpdir = tempfile.mkdtemp()
        self.socket_path = os.path.join(self.tmpdir, "nvim.sock")

        # Start headless nvim process
        self.proc = subprocess.Popen(
            ["nvim", "--headless", "--listen", self.socket_path, "--noplugin"]
        )

        time.sleep(0.5)

        # Connect to nvim
        self.nvim = pynvim.attach("socket", path=self.socket_path)
        self.buffer = self.nvim.current.buffer

        # Initialize with content if provided
        if initial_content:
            self.buffer[:] = initial_content
        else:
            self.buffer[:] = [""]

        # Start in normal mode at top of file (just like opening nvim)
        self.nvim.command("normal! gg")
        self.nvim.command("set nomodified")

    def __enter__(self) -> "RawNvimEditor":
        return self

    def __exit__(self, exc_type: type, exc_val: Exception, exc_tb: object) -> None:
        self.close()

    def close(self) -> None:
        """Clean up the nvim instance"""
        try:
            self.nvim.quit()
        except Exception:
            pass
        self.proc.terminate()
        self.proc.wait(timeout=5)

    def type_keys(self, keys: str) -> None:
        """
        Type keys exactly as a user would, with proper termcode conversion

        Examples:
        - "i" -> enter insert mode
        - "Hello World" -> type text (only works in insert mode)
        - "<Esc>" -> escape to normal mode
        - "dd" -> delete line (only works in normal mode)
        """
        # Convert vim notation to actual key codes
        processed_keys = self.nvim.api.replace_termcodes(keys, True, False, True)
        self.nvim.api.feedkeys(processed_keys, "n", False)

    def get_mode(self) -> str:
        """Get current vim mode"""
        return self.nvim.api.get_mode()["mode"]

    def get_cursor_position(self) -> tuple[int, int]:
        """Get cursor position (row, col) - 1-indexed for row, 0-indexed for col"""
        return self.nvim.current.window.cursor

    def get_buffer_content(self) -> list[str]:
        """Get all buffer content as list of lines"""
        return self.buffer[:]

    def get_line(self, line_num: int) -> str:
        """Get specific line (1-indexed)"""
        return self.buffer[line_num - 1]

    def get_current_line(self) -> str:
        """Get the line where cursor is currently positioned"""
        row, _ = self.get_cursor_position()
        return self.buffer[row - 1]

    def assert_mode(self, expected_mode: str) -> None:
        """Assert we're in the expected mode"""
        current_mode = self.get_mode()
        if current_mode != expected_mode:
            raise AssertionError(
                f"Expected mode '{expected_mode}', but in mode '{current_mode}'"
            )

    def assert_cursor_at(self, row: int, col: int) -> None:
        """Assert cursor is at expected position"""
        actual_row, actual_col = self.get_cursor_position()
        if (actual_row, actual_col) != (row, col):
            raise AssertionError(
                f"Expected cursor at ({row}, {col}), but at ({actual_row}, {actual_col})"
            )

    def assert_line_content(self, line_num: int, expected: str) -> None:
        """Assert line has expected content"""
        actual = self.get_line(line_num)
        if actual != expected:
            raise AssertionError(
                f"Line {line_num}: expected '{expected}', got '{actual}'"
            )
