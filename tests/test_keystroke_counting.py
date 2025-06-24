#!/usr/bin/env python3
"""
Test the keystroke counting functionality
"""

import re

def count_keystrokes(keystroke_sequence: str) -> int:
    """
    Count the number of actual keystrokes in a vim command sequence.
    This accounts for special key notations like <CR>, <Esc>, etc.
    """
    if not keystroke_sequence:
        return 0
        
    # Count the sequence
    temp_sequence = keystroke_sequence
    keystroke_count = 0
    
    # Handle special key patterns
    special_key_patterns = [
        r'<CR>|<Enter>|<Return>',
        r'<Esc>|<Escape>',
        r'<Tab>|<S-Tab>',
        r'<BS>|<Backspace>',
        r'<Del>|<Delete>',
        r'<Up>|<Down>|<Left>|<Right>',
        r'<C-[a-zA-Z0-9]>',
        r'<S-[a-zA-Z]>',
        r'<A-[a-zA-Z]>',
        r'<F[0-9]+>',
        r'<Home>|<End>',
        r'<PageUp>|<PageDown>',
        r'<Insert>'
    ]
    
    # Replace each special key pattern with a placeholder and count
    for pattern in special_key_patterns:
        matches = re.findall(pattern, temp_sequence, re.IGNORECASE)
        keystroke_count += len(matches)
        temp_sequence = re.sub(pattern, '', temp_sequence, flags=re.IGNORECASE)
    
    # Count remaining regular characters
    keystroke_count += len(temp_sequence)
    
    return keystroke_count

# Test cases
test_cases = [
    (":%s/hello/world/<CR>", "Simple substitution"),
    ("dd", "Delete line"),
    (":%s/\\[\\|\\]\\|,\\[\\]//g<CR>", "Complex regex"),
    ("iHello<Esc>", "Insert mode"),
    ("ma'ajdd'a", "Mark operations"),
    ("<C-a>", "Ctrl command"),
    ("gg<S-v>G", "Visual select all"),
    ("", "Empty command"),
]

print("Testing keystroke counting:")
print("="*50)

total_keystrokes = 0
for command, description in test_cases:
    count = count_keystrokes(command)
    total_keystrokes += count
    print(f"{description:20} | {command:25} | {count:2} keystrokes")

print("="*50)
print(f"Total keystrokes across all test cases: {total_keystrokes}")