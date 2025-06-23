#!/usr/bin/env python3
"""
Realistic Nvim Usage Examples

This file demonstrates how to use the RawNvimEditor exactly like a real nvim session.
Every keystroke shown here is exactly what a user would type in real nvim.
"""

from pynvim_agents import RawNvimEditor


def example_1_basic_file_editing():
    """Example 1: Basic file editing - Create a simple config file"""
    print("=== Example 1: Creating a config file ===")

    with RawNvimEditor() as nvim:
        print("User opens nvim (starts in normal mode)")
        print(f"Mode: {nvim.get_mode()}, Cursor: {nvim.get_cursor_position()}")

        # User starts typing immediately by pressing 'i'
        print("\nUser presses 'i' to enter insert mode and types config:")
        nvim.type_keys("i")  # Enter insert mode
        nvim.type_keys("# Configuration file")
        nvim.type_keys("<Enter>")
        nvim.type_keys("host = localhost")
        nvim.type_keys("<Enter>")
        nvim.type_keys("port = 8080")
        nvim.type_keys("<Enter>")
        nvim.type_keys("debug = true")

        print("Current content:")
        for i, line in enumerate(nvim.get_buffer_content(), 1):
            print(f"  {i}: {line}")

        # User exits insert mode
        print("\nUser presses <Esc> to return to normal mode")
        nvim.type_keys("<Esc>")
        print(f"Mode: {nvim.get_mode()}")

        # User goes back to edit port number
        print("\nUser wants to change port number:")
        print("- Types 'gg' to go to top of file")
        nvim.type_keys("gg")

        print("- Types '2j' to go down 2 lines")
        nvim.type_keys("2j")
        print(f"  Cursor now at: {nvim.get_cursor_position()}")

        print("- Types 'f8' to find the '8' in '8080'")
        nvim.type_keys("f8")

        print("- Types 'cw' to change the word (enters insert mode)")
        nvim.type_keys("cw")
        print(f"  Mode: {nvim.get_mode()}")

        print("- Types '3000' for new port")
        nvim.type_keys("3000")

        print("- Presses <Esc> to return to normal mode")
        nvim.type_keys("<Esc>")

        print("\nFinal content:")
        for i, line in enumerate(nvim.get_buffer_content(), 1):
            print(f"  {i}: {line}")


def example_2_python_function():
    """Example 2: Writing a Python function with realistic editing"""
    print("\n=== Example 2: Writing Python function ===")

    with RawNvimEditor() as nvim:
        print("User writes a Python function from scratch:")

        # Start writing function
        nvim.type_keys("i")  # Insert mode
        nvim.type_keys("def calculate_area(radius):")
        nvim.type_keys("<Enter>")
        nvim.type_keys("    return 3.14 * radius * radius")
        nvim.type_keys("<Esc>")  # Back to normal

        print("Initial function:")
        for i, line in enumerate(nvim.get_buffer_content(), 1):
            print(f"  {i}: {line}")

        print("\nUser realizes they want to import math module:")
        print("- Types 'gg' to go to top")
        nvim.type_keys("gg")

        print("- Types 'O' to open line above and enter insert mode")
        nvim.type_keys("O")

        print("- Types import statement")
        nvim.type_keys("import math")
        nvim.type_keys("<Esc>")

        print("\nUser wants to use math.pi instead of 3.14:")
        print("- Types 'j' to go to function definition")
        nvim.type_keys("j")

        print("- Types 'j' to go to return statement")
        nvim.type_keys("j")

        print("- Types 'f3' to find '3.14'")
        nvim.type_keys("f3")

        print("- Types 'cw' to change '3.14' to 'math.pi'")
        nvim.type_keys("cw")
        nvim.type_keys("math.pi")
        nvim.type_keys("<Esc>")

        print("\nUser adds docstring:")
        print("- Types 'k' to go up to function definition")
        nvim.type_keys("k")

        print("- Types 'A' to go to end of line and enter insert mode")
        nvim.type_keys("A")

        print("- Adds docstring")
        nvim.type_keys("<Enter>")
        nvim.type_keys('    """Calculate area of circle given radius."""')
        nvim.type_keys("<Esc>")

        print("\nFinal function:")
        for i, line in enumerate(nvim.get_buffer_content(), 1):
            print(f"  {i}: {line}")


def example_3_realistic_debugging_session():
    """Example 3: Debugging a Python script - realistic editing workflow"""
    print("\n=== Example 3: Debugging Session ===")

    # Start with buggy code
    buggy_code = [
        "def divide_numbers(a, b):",
        "    result = a / b",
        "    return result",
        "",
        "print(divide_numbers(10, 0))",
    ]

    with RawNvimEditor(buggy_code) as nvim:
        print("User has buggy code with division by zero:")
        for i, line in enumerate(nvim.get_buffer_content(), 1):
            print(f"  {i}: {line}")

        print("\nUser wants to add error checking:")
        print("- Types 'gg' to go to top")
        nvim.type_keys("gg")

        print("- Types 'j' to go to function body")
        nvim.type_keys("j")

        print("- Types 'O' to add line above and enter insert mode")
        nvim.type_keys("O")

        print("- Types error check")
        nvim.type_keys("    if b == 0:")
        nvim.type_keys("<Enter>")
        nvim.type_keys('        return "Error: Division by zero"')
        nvim.type_keys("<Esc>")

        print("\nUser wants to test with different values:")
        print("- Types 'G' to go to last line")
        nvim.type_keys("G")

        print("- Types 'f0' to find the '0' in the print statement")
        nvim.type_keys("f0")

        print("- Types 'r' to replace single character")
        nvim.type_keys("r")
        nvim.type_keys("2")  # Replace 0 with 2

        print("\nUser adds more test cases:")
        print("- Types 'A' to go to end of line and enter insert mode")
        nvim.type_keys("A")

        nvim.type_keys("<Enter>")
        nvim.type_keys("print(divide_numbers(10, 0))  # Test error case")
        nvim.type_keys("<Enter>")
        nvim.type_keys("print(divide_numbers(15, 3))  # Test normal case")
        nvim.type_keys("<Esc>")

        print("\nFinal debugged code:")
        for i, line in enumerate(nvim.get_buffer_content(), 1):
            print(f"  {i}: {line}")


def example_4_complex_refactoring():
    """Example 4: Complex refactoring - realistic multi-step editing"""
    print("\n=== Example 4: Complex Refactoring ===")

    # Start with a class that needs refactoring
    original_code = [
        "class Calculator:",
        "    def add(self, a, b):",
        "        return a + b",
        "    def subtract(self, a, b):",
        "        return a - b",
    ]

    with RawNvimEditor(original_code) as nvim:
        print("User wants to refactor Calculator class:")
        for i, line in enumerate(nvim.get_buffer_content(), 1):
            print(f"  {i}: {line}")

        print("\nStep 1: Add constructor")
        print("- Types 'gg' then 'j' to go to line after class definition")
        nvim.type_keys("ggj")

        print("- Types 'O' to add line above and enter insert mode")
        nvim.type_keys("O")

        print("- Types constructor")
        nvim.type_keys("    def __init__(self):")
        nvim.type_keys("<Enter>")
        nvim.type_keys("        self.history = []")
        nvim.type_keys("<Esc>")

        print("\nStep 2: Modify add method to track history")
        print("- Types '/add<Enter>' to search for add method")
        nvim.type_keys("/add<Enter>")

        print("- Types 'j' to go to return line")
        nvim.type_keys("j")

        print("- Types 'O' to add line above return")
        nvim.type_keys("O")

        print("- Types history tracking")
        nvim.type_keys("        result = a + b")
        nvim.type_keys("<Enter>")
        nvim.type_keys("        self.history.append(f'Added {a} + {b} = {result}')")
        nvim.type_keys("<Esc>")

        print("- Types 'j' to go to return line")
        nvim.type_keys("j")

        print("- Types 'cw' to change 'return a + b' to 'return result'")
        nvim.type_keys("cw")
        nvim.type_keys("return result")
        nvim.type_keys("<Esc>")

        print("\nStep 3: Add method to get history")
        print("- Types 'G' to go to end of file")
        nvim.type_keys("G")

        print("- Types 'o' to add new line below")
        nvim.type_keys("o")

        print("- Types new method")
        nvim.type_keys("<Enter>")
        nvim.type_keys("    def get_history(self):")
        nvim.type_keys("<Enter>")
        nvim.type_keys("        return self.history")
        nvim.type_keys("<Esc>")

        print("\nFinal refactored code:")
        for i, line in enumerate(nvim.get_buffer_content(), 1):
            print(f"  {i}: {line}")


def demonstrate_keystroke_sequences():
    """Show various keystroke patterns that mimic real user behavior"""
    print("\n=== Common Keystroke Patterns ===")

    with RawNvimEditor() as nvim:
        print("Pattern 1: Quick line editing")
        print("User types: 'iHello World<Esc>0cwGoodbye<Esc>'")
        print("Breakdown:")
        print("  i          - Enter insert mode")
        print("  Hello World - Type text")
        print("  <Esc>      - Exit insert mode")
        print("  0          - Go to beginning of line")
        print("  cw         - Change word (deletes 'Hello' and enters insert)")
        print("  Goodbye    - Type replacement")
        print("  <Esc>      - Exit insert mode")

        nvim.type_keys("iHello World<Esc>0cwGoodbye<Esc>")
        print(f"Result: '{nvim.get_line(1)}'")

        print("\nPattern 2: Multi-line editing")
        print("User types: 'oSecond line<Esc>OFirst line<Esc>'")
        print("Breakdown:")
        print("  o          - Open line below, enter insert mode")
        print("  Second line - Type text")
        print("  <Esc>      - Exit insert mode")
        print("  O          - Open line above, enter insert mode")
        print("  First line - Type text")
        print("  <Esc>      - Exit insert mode")

        nvim.type_keys("oSecond line<Esc>OFirst line<Esc>")
        print("Result:")
        for i, line in enumerate(nvim.get_buffer_content(), 1):
            print(f"  {i}: {line}")

        print("\nPattern 3: Search and replace")
        print("User types: '/Goodbye<Enter>cwHello<Esc>'")
        print("Breakdown:")
        print("  /Goodbye<Enter> - Search for 'Goodbye'")
        print("  cw              - Change word")
        print("  Hello           - Type replacement")
        print("  <Esc>           - Exit insert mode")

        nvim.type_keys("/Goodbye<Enter>cwHello<Esc>")
        print("Result:")
        for i, line in enumerate(nvim.get_buffer_content(), 1):
            print(f"  {i}: {line}")


if __name__ == "__main__":
    example_1_basic_file_editing()
    example_2_python_function()
    example_3_realistic_debugging_session()
    example_4_complex_refactoring()
    demonstrate_keystroke_sequences()
