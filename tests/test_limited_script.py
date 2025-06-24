#!/usr/bin/env python3
"""
Test script with only 3 problems to identify issues
"""

import asyncio
import os
from vimgolf_solver import VimGolfSolver, VimGolfProblem

async def test_limited_problems():
    """Test with only 3 simple problems"""
    
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ Error: OPENAI_API_KEY environment variable not set")
        return
    
    # Create simple test problems
    test_problems = [
        VimGolfProblem(
            id="test1",
            title="Simple replacement",
            description="Replace hello with world",
            start_text="hello there",
            end_text="world there"
        ),
        VimGolfProblem(
            id="test2", 
            title="Add exclamation",
            description="Add exclamation mark",
            start_text="hello",
            end_text="hello!"
        ),
        VimGolfProblem(
            id="test3",
            title="Uppercase first word",
            description="Make first word uppercase",
            start_text="hello world",
            end_text="HELLO world"
        )
    ]
    
    solver = VimGolfSolver()
    solver.problems = test_problems  # Replace with our simple problems
    
    print("🧪 Testing with 3 simple problems...")
    start_time = asyncio.get_event_loop().time()
    
    try:
        results = await asyncio.wait_for(solver.solve_all_problems(), timeout=60.0)
        end_time = asyncio.get_event_loop().time()
        
        print(f"\n✅ Completed in {end_time - start_time:.1f}s")
        solver.print_summary(results)
        
    except asyncio.TimeoutError:
        print("❌ Script timed out after 60 seconds")
    except Exception as e:
        print(f"❌ Script failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_limited_problems())