#!/usr/bin/env python3
"""
Debug the empty backtick extraction issue
"""

import asyncio
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from vimgolf_solver import VimGolfSolver

async def test_problematic_problems():
    """Test the specific problems showing empty backticks"""
    
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ Error: OPENAI_API_KEY environment variable not set")
        return
    
    solver = VimGolfSolver()
    
    # Test the problems that showed empty backticks in the log
    problem_names = [
        "Change class fields from camel case to snake case",
        "Remove adjacent duplicates", 
        "Reordering properties",
        "YAML to dotenv",
        "Create json from a .env file"
    ]
    
    for problem_name in problem_names:
        problem = None
        for p in solver.problems:
            if problem_name in p.title:
                problem = p
                break
        
        if not problem:
            print(f"❌ Problem not found: {problem_name}")
            continue
            
        print(f"\n{'='*60}")
        print(f"Testing: {problem.title}")
        print(f"{'='*60}")
        
        try:
            # Get LLM response
            response = await solver.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a Vim expert who excels at solving VimGolf challenges with minimal keystrokes."},
                    {"role": "user", "content": solver.create_prompt(problem)}
                ],
                temperature=0.1,
                max_tokens=1000
            )
            
            response_text = response.choices[0].message.content
            print(f"Full response (first 500 chars):")
            print(response_text[:500])
            print("\n" + "-"*40)
            
            # Test extraction step by step
            print("Testing extraction...")
            
            # Check for Solution: pattern
            import re
            solution_match = re.search(r'Solution:\s*([^\n]+)', response_text)
            if solution_match:
                candidate = solution_match.group(1).strip()
                print(f"Solution line found: {repr(candidate)}")
                candidate = solver._clean_backticks(candidate)
                print(f"After cleaning: {repr(candidate)}")
                if candidate and solver._looks_like_vim_command(candidate):
                    print(f"✅ Valid vim command: {repr(candidate)}")
                else:
                    print(f"❌ Not a valid vim command")
            
            # Check for backticks
            backtick_match = re.search(r'`([^`\n]+)`', response_text)
            if backtick_match:
                candidate = backtick_match.group(1).strip()
                print(f"Backtick content found: {repr(candidate)}")
                if candidate and solver._looks_like_vim_command(candidate):
                    print(f"✅ Valid vim command from backticks: {repr(candidate)}")
                else:
                    print(f"❌ Not a valid vim command from backticks")
            
            # Final extraction
            extracted = solver.extract_solution_from_response(response_text)
            print(f"Final extracted: {repr(extracted)}")
            
            if not extracted:
                print("❌ EMPTY EXTRACTION - This is the problem!")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            
        print()

if __name__ == "__main__":
    asyncio.run(test_problematic_problems())