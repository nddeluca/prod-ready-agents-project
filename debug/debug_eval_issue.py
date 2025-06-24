#!/usr/bin/env python3
"""
Debug the evaluation issue
"""

import asyncio
import time
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from vimgolf_solver import VimGolfSolver, VimGolfProblem

async def test_direct_evaluation():
    """Test evaluation directly to see what's wrong"""
    
    # Test the exact problem that's failing
    problem = VimGolfProblem(
        id="9v00669b3ff1",
        title="Rearrange array to single level",
        description="Flatten nested array structure and remove empty elements",
        start_text="[[1,2],[3,4,[]],[5,6,[7,8]]]",
        end_text="[1,2,3,4,5,6,7,8]"
    )
    
    # Test the exact command that was extracted
    command = ":%s/\\[\\|\\]\\|,\\[\\]//g<CR>"
    
    solver = VimGolfSolver()
    
    print("Testing evaluation directly...")
    print(f"Start: {problem.start_text}")
    print(f"Expected: {problem.end_text}")
    print(f"Command: {command}")
    
    start_time = time.time()
    result = await solver.evaluate_solution(problem, command)
    eval_time = time.time() - start_time
    
    print(f"Result: {result}")
    print(f"Time taken: {eval_time:.1f}s")

def test_sync_vim():
    """Test the sync vim function directly"""
    from src.pynvim_agents.raw_editor import RawNvimEditor
    
    start_text = "[[1,2],[3,4,[]],[5,6,[7,8]]]"
    command = ":%s/\\[\\|\\]\\|,\\[\\]//g<CR>"
    
    print("\nTesting sync vim directly...")
    print(f"Start: {start_text}")
    print(f"Command: {command}")
    
    start_time = time.time()
    try:
        with RawNvimEditor(initial_content=[start_text]) as editor:
            print("Editor created")
            
            # Set vim settings
            editor.nvim.command("set shortmess+=IacF")
            editor.nvim.command("set noerrorbells")
            editor.nvim.command("set visualbell t_vb=")
            editor.nvim.command("set report=999")
            print("Settings applied")
            
            # Execute command
            editor.type_keys(command)
            print("Command executed")
            
            # Get result
            result = editor.get_buffer_content()
            print(f"Result: {result}")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    
    sync_time = time.time() - start_time
    print(f"Sync time: {sync_time:.1f}s")

if __name__ == "__main__":
    test_sync_vim()
    asyncio.run(test_direct_evaluation())