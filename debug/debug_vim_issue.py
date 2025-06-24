#!/usr/bin/env python3
"""
Debug the vim simulation issue by testing individual components
"""

import asyncio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.pynvim_agents.raw_editor import RawNvimEditor

def test_vim_commands():
    """Test various vim commands to identify hanging issues"""
    
    test_cases = [
        {
            "name": "Simple substitution",
            "start": ["hello world"],
            "command": ":%s/hello/hi/g<CR>",
            "expected": ["hi world"]
        },
        {
            "name": "Complex regex with backticks",
            "start": ["[[1,2],[3,4,[]],[5,6,[7,8]]]"],
            "command": "`:%s/\\[\\|\\]\\|,\\[\\]//g<CR>`",
            "expected": ["12,34,,56,78"]
        },
        {
            "name": "Clean regex without backticks",
            "start": ["[[1,2],[3,4,[]],[5,6,[7,8]]]"],
            "command": ":%s/\\[\\|\\]\\|,\\[\\]//g<CR>",
            "expected": ["12,34,,56,78"]
        },
        {
            "name": "Mark operation",
            "start": ["line1", "line2"],
            "command": "ma'a",
            "expected": ["line1", "line2"]
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n=== Test {i}: {case['name']} ===")
        print(f"Command: {repr(case['command'])}")
        
        try:
            with RawNvimEditor(initial_content=case['start']) as editor:
                print(f"Initial: {editor.get_buffer_content()}")
                
                # Set vim to suppress error messages
                editor.nvim.command("set shortmess+=IacF")
                editor.nvim.command("set noerrorbells")
                editor.nvim.command("set visualbell t_vb=")
                editor.nvim.command("set report=999")
                
                print(f"Executing command...")
                editor.type_keys(case['command'])
                
                # Ensure normal mode
                try:
                    editor.type_keys("<Esc>")
                except:
                    pass
                
                result = editor.get_buffer_content()
                print(f"Result: {result}")
                print(f"Expected: {case['expected']}")
                print(f"Match: {result == case['expected']}")
                
        except Exception as e:
            print(f"ERROR: {e}")
            import traceback
            traceback.print_exc()

def test_hanging_scenario():
    """Test scenario that might cause hanging"""
    print("\n" + "="*50)
    print("TESTING POTENTIAL HANGING SCENARIO")
    print("="*50)
    
    try:
        with RawNvimEditor(initial_content=["test"]) as editor:
            print("Testing backtick command that might hang...")
            
            # This is what's being executed based on the log
            problematic_command = "`:%s/\\[\\|\\]\\|,\\[\\]//g<CR>`"
            print(f"Command: {repr(problematic_command)}")
            
            editor.type_keys(problematic_command)
            
            result = editor.get_buffer_content()
            print(f"Result: {result}")
            
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_vim_commands()
    test_hanging_scenario()