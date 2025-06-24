#!/usr/bin/env python3
"""
Test script to debug vim command interpretation issues
"""

import asyncio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.pynvim_agents.raw_editor import RawNvimEditor

def test_simple_commands():
    """Test basic vim commands to see what's causing the mark errors"""
    print("Testing simple vim commands...")
    
    # Test 1: Simple text insertion
    print("\n=== Test 1: Simple insertion ===")
    try:
        with RawNvimEditor(initial_content=["hello world"]) as editor:
            print(f"Initial: {editor.get_buffer_content()}")
            editor.type_keys("A!")  # Append exclamation at end
            print(f"After 'A!': {editor.get_buffer_content()}")
            editor.type_keys("<Esc>")  # Back to normal mode
            print(f"Final: {editor.get_buffer_content()}")
    except Exception as e:
        print(f"Error in test 1: {e}")

    # Test 2: Common vimgolf pattern - substitute
    print("\n=== Test 2: Substitute command ===")
    try:
        with RawNvimEditor(initial_content=["hello world"]) as editor:
            print(f"Initial: {editor.get_buffer_content()}")
            editor.type_keys(":%s/world/vim/g<CR>")
            print(f"After substitute: {editor.get_buffer_content()}")
    except Exception as e:
        print(f"Error in test 2: {e}")

    # Test 3: Commands that might cause mark errors
    print("\n=== Test 3: Potentially problematic commands ===")
    try:
        with RawNvimEditor(initial_content=["line1", "line2", "line3"]) as editor:
            print(f"Initial: {editor.get_buffer_content()}")
            # This might be causing issues - test mark-related commands
            editor.type_keys("ma")  # Set mark 'a'
            editor.type_keys("j")   # Move down
            editor.type_keys("'a")  # Go to mark 'a'
            print(f"After mark operations: {editor.get_buffer_content()}")
    except Exception as e:
        print(f"Error in test 3: {e}")

    # Test 4: Test what happens with complex keystroke sequences
    print("\n=== Test 4: Complex sequence ===")
    try:
        with RawNvimEditor(initial_content=["[[1,2],[3,4,[]],[5,6,[7,8]]]"]) as editor:
            print(f"Initial: {editor.get_buffer_content()}")
            # Try a simple transformation
            editor.type_keys(":%s/\\[\\[/[/g<CR>")
            print(f"After first sub: {editor.get_buffer_content()}")
    except Exception as e:
        print(f"Error in test 4: {e}")

if __name__ == "__main__":
    test_simple_commands()