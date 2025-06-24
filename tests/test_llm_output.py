#!/usr/bin/env python3
"""
Test script to simulate LLM output and see what causes mark errors
"""

import re
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.pynvim_agents.raw_editor import RawNvimEditor

def extract_solution_from_response(response_text: str) -> str:
    """Extract the vim keystroke sequence from LLM response (same as in solver)"""
    # Look for "Solution:" followed by the keystroke sequence
    solution_match = re.search(r'Solution:\s*([^\n]+)', response_text)
    if solution_match:
        return solution_match.group(1).strip()
    
    # Fallback: look for content between backticks or brackets
    backtick_match = re.search(r'`([^`]+)`', response_text)
    if backtick_match:
        return backtick_match.group(1).strip()
        
    # If no clear pattern, return the first line that looks like vim commands
    lines = response_text.split('\n')
    for line in lines:
        line = line.strip()
        if line and not line.startswith(('Explanation:', 'Keystrokes:', 'Step')):
            return line
            
    return ""

def test_problematic_sequences():
    """Test sequences that might cause mark errors"""
    
    # Common problematic sequences from LLM outputs
    test_sequences = [
        ":%s/\\[\\[/\\[/g<CR>:%s/\\]\\]/\\]/g<CR>:%s/,\\[\\]/,/g<CR>",
        ":s/hello/world/g<CR>",
        "ma'a",  # This could cause mark issues
        "'a'b",  # Mark operations that might fail
        "qa...q",  # Macro recording
        "<C-a>",  # Control commands
        "Solution: :%s/pattern/replacement/g<CR>",  # Text that includes "Solution:"
    ]
    
    for i, sequence in enumerate(test_sequences, 1):
        print(f"\n=== Test {i}: {sequence[:50]}{'...' if len(sequence) > 50 else ''} ===")
        try:
            with RawNvimEditor(initial_content=["test content"]) as editor:
                print(f"Initial: {editor.get_buffer_content()}")
                print(f"Executing: {repr(sequence)}")
                editor.type_keys(sequence)
                print(f"Result: {editor.get_buffer_content()}")
        except Exception as e:
            print(f"Error: {e}")

def test_extraction():
    """Test the extraction function with various LLM response formats"""
    
    sample_responses = [
        """Solution: :%s/\\[\\[/[/g<CR>:%s/\\]\\]/]/g<CR>
Keystrokes: 25
Explanation: Replace nested brackets""",
        
        """Here's my solution:
`:%s/hello/world/g<CR>`
This will replace all instances.""",
        
        """I would use this command sequence:
:%s/pattern/replacement/g<CR>
Keystrokes: 15""",
        
        """The vim keystrokes are: ma'ajdd'a
This sets a mark and deletes a line."""
    ]
    
    print("\n" + "="*60)
    print("TESTING EXTRACTION FUNCTION")
    print("="*60)
    
    for i, response in enumerate(sample_responses, 1):
        extracted = extract_solution_from_response(response)
        print(f"\nResponse {i}:")
        print(f"Input: {repr(response[:100])}...")
        print(f"Extracted: {repr(extracted)}")
        
        # Test the extracted sequence
        try:
            with RawNvimEditor(initial_content=["test line"]) as editor:
                editor.type_keys(extracted)
                print(f"Execution: Success")
        except Exception as e:
            print(f"Execution: Error - {e}")

if __name__ == "__main__":
    test_problematic_sequences()
    test_extraction()