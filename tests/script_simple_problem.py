#!/usr/bin/env python3
"""
Test with a simpler problem to verify the fixes work
"""

import asyncio
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from vimgolf_solver import VimGolfSolver, VimGolfProblem

async def test_simple_problem():
    """Test with a very simple problem"""
    
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ Error: OPENAI_API_KEY environment variable not set")
        return
    
    # Create a simple test problem
    simple_problem = VimGolfProblem(
        id="test_simple",
        title="Simple word replacement",
        description="Replace 'hello' with 'world'",
        start_text="hello there",
        end_text="world there"
    )
    
    solver = VimGolfSolver()
    
    # Replace one problem with our simple one for testing
    solver.problems = [simple_problem]
    
    print("Testing with simple problem...")
    results = await solver.solve_all_problems()
    solver.print_summary(results)

if __name__ == "__main__":
    asyncio.run(test_simple_problem())