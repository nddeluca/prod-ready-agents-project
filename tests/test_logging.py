#!/usr/bin/env python3
"""
Test the logging improvements with a single problem
"""

import asyncio
import os
from vimgolf_solver import VimGolfSolver

async def test_logging():
    """Test logging with a single problem"""
    
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ Error: OPENAI_API_KEY environment variable not set")
        return
    
    solver = VimGolfSolver()
    
    # Test with just the first problem
    single_problem = solver.problems[0]
    result = await solver.solve_problem(single_problem)
    
    print("\n" + "="*60)
    print("SINGLE PROBLEM TEST RESULT")
    print("="*60)
    print(f"Problem: {result['title']}")
    print(f"Success: {result['success']}")
    if result['success']:
        print(f"Eval Score: {result['eval_score']}")
        print(f"API Time: {result.get('api_time', 0):.1f}s")
        print(f"Eval Time: {result.get('eval_time', 0):.1f}s")
        print(f"Total Time: {result.get('total_time', 0):.1f}s")
        print(f"Keystrokes: {result.get('keystroke_sequence', 'None')}")
    else:
        print(f"Error: {result.get('error', 'Unknown')}")

if __name__ == "__main__":
    asyncio.run(test_logging())