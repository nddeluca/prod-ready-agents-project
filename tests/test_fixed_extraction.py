#!/usr/bin/env python3
"""
Test the fixed extraction logic
"""

import re

def _clean_backticks(text: str) -> str:
    """Remove surrounding backticks from text"""
    text = text.strip()
    if text.startswith('`') and text.endswith('`'):
        return text[1:-1].strip()
    return text

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
    # Look for "Solution:" followed by the keystroke sequence on the same line
    solution_match = re.search(r'Solution:\s*([^\n]+)', response_text)
    if solution_match:
        candidate = solution_match.group(1).strip()
        # Skip if it's just code block markers
        if candidate in ['```', '```vim', '```viml']:
            pass  # Continue to other extraction methods
        else:
            candidate = _clean_backticks(candidate)
            if candidate and _looks_like_vim_command(candidate):
                return candidate
    
    # Look for content in code blocks
    code_block_match = re.search(r'```(?:vim|viml)?\n([^`]+)\n```', response_text, re.MULTILINE)
    if code_block_match:
        candidate = code_block_match.group(1).strip()
        if candidate and _looks_like_vim_command(candidate):
            return candidate
    
    # Look for content between single backticks (not code blocks)
    # Match single-line backtick content only
    backtick_match = re.search(r'`([^`\n]+)`', response_text)
    if backtick_match:
        candidate = backtick_match.group(1).strip()
        if candidate and _looks_like_vim_command(candidate):
            return candidate
            
    # Look for lines that start with vim command patterns
    lines = response_text.split('\n')
    for line in lines:
        line = line.strip()
        # Skip empty lines and code block markers
        if not line or line.startswith('```'):
            continue
        # Remove surrounding backticks if present
        line = _clean_backticks(line)
        if line and _looks_like_vim_command(line):
            return line
            
    return ""

# Test the problematic case
problematic_response = r"""Solution: 
```
ggO{<Esc>:%s/\(.*\)=\(.*\)/  "\1": "\2",/<CR>ggddG$xO}<Esc>
```

Keystrokes: 45

Explanation:

1. `gg`: Go to the first line.
2. `O`: Open a new line above the current line and enter insert mode."""

print("Testing problematic response:")
print("Input:", repr(problematic_response[:100]) + "...")
result = extract_solution_from_response(problematic_response)
print("Extracted:", repr(result))
print("Length:", len(result))
print("Is valid vim command:", _looks_like_vim_command(result))

# Test other cases
test_cases = [
    'Solution: `:%s/test/TEST/g<CR>`',  # Inline backticks
    'Solution: ```',  # Just code block marker
    '```vim\ndd\n```',  # Code block
    'Solution: \n```\ndd\n```',  # Solution with code block
]

print("\nTesting other cases:")
for i, case in enumerate(test_cases, 1):
    result = extract_solution_from_response(case)
    print(f"{i}. Input: {repr(case)}")
    print(f"   Result: {repr(result)}")
    print()