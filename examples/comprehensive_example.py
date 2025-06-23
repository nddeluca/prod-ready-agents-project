#!/usr/bin/env python3
"""
Example demonstrating pynvim buffer manipulation
"""

import os
import subprocess
import tempfile
import time

import pynvim


def create_nvim_instance():
    """Create a headless neovim instance and return the connection"""
    tmpdir = tempfile.mkdtemp()
    socket_path = os.path.join(tmpdir, "nvim.sock")

    proc = subprocess.Popen(
        ["nvim", "--headless", "--listen", socket_path, "--noplugin"]
    )

    time.sleep(0.5)

    try:
        nvim = pynvim.attach("socket", path=socket_path)
        return nvim, proc
    except Exception as e:
        proc.terminate()
        raise e


def main():
    nvim, proc = create_nvim_instance()

    try:
        # Get the current buffer
        buffer = nvim.current.buffer

        print("=== PyNvim Buffer Manipulation Demo ===\n")

        # Initialize buffer with starting text
        initial_text = ["Hello, World!", "This is line 2", "Line 3 here"]
        buffer[:] = initial_text
        print("1. Initialized buffer with text:")
        for i, line in enumerate(buffer):
            print(f"   Line {i+1}: {line}")
        print()

        # Navigate to first line, first character
        nvim.command("normal! gg0")
        print("2. Moved cursor to beginning (gg0)")
        row, col = nvim.current.window.cursor
        print(f"   Cursor position: row {row}, col {col}")
        print()

        # Insert mode operations
        nvim.command("normal! gg")
        nvim.command("startinsert!")  # Insert at end of line
        nvim.input(" Modified!")
        nvim.command("stopinsert")
        print("3. Added text in insert mode:")
        print(f"   Line 1: {buffer[0]}")
        print()

        # Normal mode navigation
        nvim.command("normal! j")  # Move down one line
        nvim.command("normal! w")  # Move to next word
        row, col = nvim.current.window.cursor
        print("4. Navigated with 'j' then 'w'")
        print(f"   Cursor position: row {row}, col {col}")
        print()

        # Word deletion
        nvim.command("normal! gg")
        nvim.command("normal! dw")  # Delete first word
        print("5. Deleted first word with 'dw':")
        print(f"   Line 1: {buffer[0]}")
        print()

        # Add new line
        nvim.command("normal! gg$")  # Go to end of first line
        nvim.command("normal! o")  # Open new line below
        nvim.input("New line added via 'o' command")
        nvim.feedkeys("<Esc>", "t")
        print("6. Added new line with 'o' command:")
        for i, line in enumerate(buffer):
            print(f"   Line {i+1}: {line}")
        print()

        # Search functionality
        nvim.command("normal! gg")
        nvim.command("/line")  # Search for 'line'
        row, col = nvim.current.window.cursor
        print("7. Searched for 'line':")
        print(f"   Found at row {row}, col {col}")
        print(f"   Text: {buffer[row-1]}")
        print()

        # Control key combinations in insert mode
        nvim.command("normal! gg")
        nvim.command("startinsert!")
        nvim.input(" Additional text")
        nvim.feedkeys("<C-w>", "t")  # Delete word backwards
        nvim.input("CTRL-W test")
        nvim.command("stopinsert")
        print("8. Used CTRL-W to delete word backwards:")
        print(f"   Line 1: {buffer[0]}")
        print()

        # Buffer content retrieval
        print("9. Final buffer contents:")
        all_lines = buffer[:]
        for i, line in enumerate(all_lines):
            print(f"   Line {i+1}: {line}")
        print(f"   Buffer has {len(buffer)} lines total")
        print()

        # Direct buffer manipulation
        buffer.append("Direct buffer append", len(buffer))
        buffer[1] = "Line 2 replaced directly"
        print("10. Direct buffer manipulation:")
        for i, line in enumerate(buffer):
            print(f"    Line {i+1}: {line}")

    finally:
        nvim.quit()
        proc.terminate()
        proc.wait(timeout=5)


if __name__ == "__main__":
    main()
