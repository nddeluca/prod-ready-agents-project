#!/usr/bin/env python3
"""
Test a single vimgolf problem to debug issues
"""

import asyncio
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from vimgolf_solver import VimGolfSolver, VimGolfProblem

async def test_single_problem():
    """Test solving a single problem to debug"""
    
    # Create a simple test problem
    test_problem = VimGolfProblem(
        id="test",
        title="Simple replacement",
        description="Replace hello with world",
        start_text="hello there",
        end_text="world there"
    )
    
    print("Testing single problem without OpenAI...")
    
    # Test the evaluation function directly with a known solution
    solver = VimGolfSolver()
    
    # Test with a simple command that should work
    test_command = ":%s/hello/world/g<CR>"
    print(f"Testing command: {test_command}")
    
    try:
        result = await solver.evaluate_solution(test_problem, test_command)
        print(f"Evaluation result: {result}")
    except Exception as e:
        print(f"Error in evaluation: {e}")
    
    # Test extraction
    mock_response = f"""Solution: {test_command}
Keystrokes: 15
Explanation: Simple substitution"""
    
    extracted = solver.extract_solution_from_response(mock_response)
    print(f"Extracted: {repr(extracted)}")

if __name__ == "__main__":
    asyncio.run(test_single_problem())