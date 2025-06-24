#!/usr/bin/env python3
"""
Test concurrent nvim instances to identify hanging
"""

import asyncio
import time
from src.pynvim_agents.raw_editor import RawNvimEditor

async def test_single_nvim():
    """Test a single nvim instance"""
    print("Testing single nvim instance...")
    start = time.time()
    
    try:
        with RawNvimEditor(initial_content=["test"]) as editor:
            editor.type_keys("iHello<Esc>")
            result = editor.get_buffer_content()
            print(f"Single nvim result: {result}")
    except Exception as e:
        print(f"Single nvim error: {e}")
    
    duration = time.time() - start
    print(f"Single nvim took: {duration:.1f}s")

async def test_concurrent_nvim():
    """Test multiple concurrent nvim instances"""
    print("\nTesting 5 concurrent nvim instances...")
    start = time.time()
    
    async def run_nvim_task(task_id):
        try:
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(None, run_nvim_sync, task_id)
            return result
        except Exception as e:
            return f"Task {task_id} error: {e}"
    
    def run_nvim_sync(task_id):
        try:
            with RawNvimEditor(initial_content=[f"task {task_id}"]) as editor:
                editor.type_keys(f"A - done<Esc>")
                result = editor.get_buffer_content()
                return f"Task {task_id}: {result}"
        except Exception as e:
            return f"Task {task_id} sync error: {e}"
    
    # Run 5 concurrent tasks
    tasks = [run_nvim_task(i) for i in range(5)]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    duration = time.time() - start
    print(f"Concurrent nvim took: {duration:.1f}s")
    
    for result in results:
        print(f"  {result}")

async def test_extraction_edge_cases():
    """Test extraction with problematic responses"""
    from vimgolf_solver import VimGolfSolver
    
    solver = VimGolfSolver()
    
    # Test cases that might cause empty extraction
    test_cases = [
        "`",  # Just backticks
        "``",  # Empty backticks
        "Solution: `", # Incomplete backticks
        "```vim\n:%s/test/TEST/g\n```", # Code block format
        "Here's the solution:\n\n`:%s/a/b/g`", # Proper format
        "Solution: The keystrokes are complex", # No actual keystrokes
    ]
    
    print("\nTesting extraction edge cases:")
    for i, case in enumerate(test_cases):
        extracted = solver.extract_solution_from_response(case)
        print(f"  {i+1}. Input: {repr(case[:30])}{'...' if len(case) > 30 else ''}")
        print(f"     Output: {repr(extracted)}")

if __name__ == "__main__":
    asyncio.run(test_single_nvim())
    asyncio.run(test_concurrent_nvim())
    asyncio.run(test_extraction_edge_cases())