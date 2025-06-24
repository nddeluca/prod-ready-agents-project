#!/usr/bin/env python3
"""
Test extraction issues - some problems show empty backticks
"""

import asyncio
import os
from vimgolf_solver import VimGolfSolver

async def test_single_problem_extraction():
    """Test extraction on one of the failing problems"""
    
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ Error: OPENAI_API_KEY environment variable not set")
        return
    
    solver = VimGolfSolver()
    
    # Test the "Remove adjacent duplicates" problem that showed empty extraction
    problem = None
    for p in solver.problems:
        if "Remove adjacent duplicates" in p.title:
            problem = p
            break
    
    if not problem:
        print("Problem not found")
        return
        
    print(f"Testing problem: {problem.title}")
    print(f"Description: {problem.description}")
    print(f"Start: {problem.start_text}")
    print(f"Expected: {problem.end_text}")
    
    # Get LLM response
    prompt = solver.create_prompt(problem)
    print(f"\nPrompt length: {len(prompt)} chars")
    
    try:
        response = await solver.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a Vim expert who excels at solving VimGolf challenges with minimal keystrokes."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=1000
        )
        
        response_text = response.choices[0].message.content
        print(f"\nFull LLM Response:")
        print("="*50)
        print(response_text)
        print("="*50)
        
        # Test extraction
        extracted = solver.extract_solution_from_response(response_text)
        print(f"\nExtracted: {repr(extracted)}")
        print(f"Length: {len(extracted)}")
        
        if extracted:
            keystrokes = solver.count_keystrokes(extracted)
            print(f"Keystroke count: {keystrokes}")
        else:
            print("❌ No keystrokes extracted!")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_single_problem_extraction())