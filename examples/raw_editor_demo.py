#!/usr/bin/env python3
"""
Simple Raw Nvim Example - Shows the key improvements for realistic editing
"""

from pynvim_agents import RawNvimEditor


def demonstrate_raw_editing():
    """Show how this interface improves over basic pynvim"""

    print("=== Raw Nvim Interface Demo ===\n")

    with RawNvimEditor() as nvim:
        print("✅ Key Improvements:")
        print("1. Starts in normal mode (like real nvim)")
        print("2. Requires explicit mode transitions")
        print("3. Exact keystroke simulation")
        print("4. Mode awareness and validation")
        print()

        # Show realistic workflow
        print("📝 Realistic Workflow Example:")
        print("User wants to write 'Hello, World!' then edit it")
        print()

        print("Step 1: Press 'i' to enter insert mode")
        nvim.type_keys("i")
        print(f"   Mode: {nvim.get_mode()} (insert mode)")

        print("Step 2: Type the text")
        nvim.type_keys("Hello, World!")
        print(f"   Content: {nvim.get_buffer_content()}")

        print("Step 3: Press <Esc> to return to normal mode")
        nvim.type_keys("<Esc>")
        print(f"   Mode: {nvim.get_mode()} (normal mode)")

        print("Step 4: Navigate and edit (go to start, change 'Hello' to 'Hi')")
        nvim.type_keys("0")  # Beginning of line
        nvim.type_keys("cw")  # Change word (enters insert mode automatically)
        print(f"   Mode after 'cw': {nvim.get_mode()} (insert mode)")
        nvim.type_keys("Hi")  # New text
        nvim.type_keys("<Esc>")  # Back to normal
        print(f"   Final content: {nvim.get_buffer_content()}")
        print(f"   Final mode: {nvim.get_mode()}")

        print()
        print("🔄 Mode Transitions Demonstrated:")
        print("   normal → insert (via 'i')")
        print("   insert → normal (via '<Esc>')")
        print("   normal → insert (via 'cw')")
        print("   insert → normal (via '<Esc>')")


def show_keystroke_equivalence():
    """Show that keystrokes match exactly what user would type"""

    print("\n=== Keystroke Equivalence ===\n")

    keystroke_examples = [
        ("i", "Enter insert mode"),
        ("Hello", "Type 'Hello' (only works in insert mode)"),
        ("<Esc>", "Return to normal mode"),
        ("dd", "Delete line (only works in normal mode)"),
        ("u", "Undo (only works in normal mode)"),
        ("o", "Open line below and enter insert mode"),
        ("A", "Go to end of line and enter insert mode"),
        ("/pattern<Enter>", "Search for pattern"),
        ("yy", "Yank (copy) current line"),
        ("p", "Paste"),
    ]

    print("Every keystroke in this interface matches real nvim:")
    for keys, description in keystroke_examples:
        print(f"  '{keys}' → {description}")

    print("\n💡 Usage Pattern:")
    print("   nvim.type_keys('i')           # Just like typing 'i' in real nvim")
    print("   nvim.type_keys('Hello')       # Just like typing 'Hello'")
    print("   nvim.type_keys('<Esc>')       # Just like pressing Escape")
    print("   nvim.type_keys('dd')          # Just like typing 'dd'")


def compare_approaches():
    """Compare this approach with the test suite approach"""

    print("\n=== Comparison with Test Suite ===\n")

    print("🧪 Test Suite Approach (test_pynvim_buffer.py):")
    print("   - Tests specific nvim functionality")
    print("   - Uses helper methods like send_keys()")
    print("   - Mixes nvim.command(), nvim.input(), nvim.feedkeys()")
    print("   - Focus: Comprehensive testing")
    print()

    print("🖥️  Raw Editor Approach (this interface):")
    print("   - Simulates real user interaction")
    print("   - Only uses type_keys() for everything")
    print("   - Exact keystroke equivalence")
    print("   - Focus: Realistic usage patterns")
    print()

    print("✅ Best Use Cases:")
    print("   Test Suite: When you need to test specific nvim features")
    print("   Raw Editor: When you want to simulate a real user typing")


if __name__ == "__main__":
    demonstrate_raw_editing()
    show_keystroke_equivalence()
    compare_approaches()
