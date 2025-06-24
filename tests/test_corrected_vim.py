#!/usr/bin/env python3
"""
Test corrected vim commands
"""

from src.pynvim_agents.raw_editor import RawNvimEditor

def test_corrected_command():
    """Test the corrected command without backticks"""
    
    start_text = "[[1,2],[3,4,[]],[5,6,[7,8]]]"
    expected_text = "[1,2,3,4,5,6,7,8]"
    
    # The corrected command (no backticks)
    command = ":%s/\\[\\|\\]\\|,\\[\\]//g<CR>"
    
    print("Testing corrected command:")
    print(f"Start: {start_text}")
    print(f"Command: {repr(command)}")
    print(f"Expected: {expected_text}")
    
    try:
        with RawNvimEditor(initial_content=[start_text]) as editor:
            # Set vim to suppress error messages
            editor.nvim.command("set shortmess+=IacF")
            editor.nvim.command("set noerrorbells")
            editor.nvim.command("set visualbell t_vb=")
            editor.nvim.command("set report=999")
            
            editor.type_keys(command)
            
            # Ensure normal mode
            try:
                editor.type_keys("<Esc>")
            except:
                pass
            
            result = editor.get_buffer_content()
            print(f"Result: {result}")
            
            # Clean up result for comparison
            result_clean = [line for line in result if line.strip()]
            expected_clean = [expected_text]
            
            print(f"Match: {result_clean == expected_clean}")
            
            return 1 if result_clean == expected_clean else 0
            
    except Exception as e:
        print(f"Error: {e}")
        return 0

if __name__ == "__main__":
    score = test_corrected_command()
    print(f"Final score: {score}")