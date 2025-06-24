#!/usr/bin/env python3
"""
Test the improved extraction function
"""

import re

def _looks_like_vim_command(text: str) -> bool:
    """Check if text looks like a vim command sequence"""
    if not text:
        return False
        
    # Skip descriptive text
    if any(text.lower().startswith(phrase) for phrase in [
        'the vim keystrokes are:', 'i would use', 'here\'s', 'this will',
        'explanation:', 'keystrokes:', 'step', 'first', 'then', 'next'
    ]):
        return False
        
    # Check for vim command patterns
    vim_patterns = [
        r'^:',           # Ex commands (:s, :g, etc)
        r'^[0-9]*[a-zA-Z]',  # Normal mode commands (dd, yy, etc)
        r'<[A-Z][a-z]*>',    # Special keys (<Esc>, <CR>, etc)
        r'[ijaoIO]',         # Insert mode commands
        r'[/?]',             # Search commands
        r'[\'"`]',           # Marks, registers
    ]
    
    return any(re.search(pattern, text) for pattern in vim_patterns)

def extract_solution_from_response(response_text: str) -> str:
    """Extract the vim keystroke sequence from LLM response"""
    # Look for "Solution:" followed by the keystroke sequence
    solution_match = re.search(r'Solution:\s*([^\n]+)', response_text)
    if solution_match:
        candidate = solution_match.group(1).strip()
        if _looks_like_vim_command(candidate):
            return candidate
    
    # Look for content between backticks 
    backtick_match = re.search(r'`([^`]+)`', response_text)
    if backtick_match:
        candidate = backtick_match.group(1).strip()
        if _looks_like_vim_command(candidate):
            return candidate
            
    # Look for lines that start with vim command patterns
    lines = response_text.split('\n')
    for line in lines:
        line = line.strip()
        if line and _looks_like_vim_command(line):
            return line
            
    return ""

def test_extraction():
    """Test the improved extraction function"""
    
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
This sets a mark and deletes a line.""",
        
        """Solution: This is a complex problem
:%s/old/new/g<CR>
Keystrokes: 12""",
        
        """Step 1: First we need to...
Step 2: Then we...
dd
Explanation: Delete the line"""
    ]
    
    print("TESTING IMPROVED EXTRACTION FUNCTION")
    print("="*60)
    
    for i, response in enumerate(sample_responses, 1):
        extracted = extract_solution_from_response(response)
        print(f"\nResponse {i}:")
        print(f"Input: {repr(response)}")
        print(f"Extracted: {repr(extracted)}")
        print(f"Is vim command: {_looks_like_vim_command(extracted)}")

if __name__ == "__main__":
    test_extraction()