#!/usr/bin/env python3
"""
Debug the extraction issue
"""

import re

def extract_solution_from_response(response_text: str) -> str:
    """Extract the vim keystroke sequence from LLM response"""
    print(f"DEBUG: Full response text:")
    print(repr(response_text))
    print("-" * 40)
    
    # Look for "Solution:" followed by the keystroke sequence
    solution_match = re.search(r'Solution:\s*([^\n]+)', response_text)
    if solution_match:
        candidate = solution_match.group(1).strip()
        print(f"DEBUG: Found Solution: {repr(candidate)}")
        return candidate
    
    # Look for content between backticks 
    backtick_match = re.search(r'`([^`]+)`', response_text)
    if backtick_match:
        candidate = backtick_match.group(1).strip()
        print(f"DEBUG: Found backticks: {repr(candidate)}")
        return candidate
        
    return ""

# Test with the actual problematic output
test_response = "`:%s/\\[\\|\\]\\|,\\[\\]//g<CR>`"
print("Testing extraction with:")
print(repr(test_response))
print()

result = extract_solution_from_response(test_response)
print(f"Final result: {repr(result)}")