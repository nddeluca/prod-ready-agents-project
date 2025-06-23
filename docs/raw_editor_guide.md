# Raw Nvim Interface - Realistic Editor Simulation

This module provides a raw nvim interface that exactly mimics real user interaction with nvim, including proper mode transitions and keystroke equivalence.

## Key Features

### ✅ **Realistic Behavior**
- **Starts in normal mode** (just like opening nvim)
- **Requires explicit mode transitions** (`i` for insert, `<Esc>` for normal)
- **Exact keystroke equivalence** - every key sequence matches what a user would type
- **Mode awareness** - validates modes and cursor positions

### 🔄 **Proper Mode Transitions**
```python
with RawNvimEditor() as nvim:
    # Starts in normal mode
    assert nvim.get_mode() == "n"
    
    # Enter insert mode like a real user
    nvim.type_keys("i")
    assert nvim.get_mode() == "i"
    
    # Type text (only works in insert mode)
    nvim.type_keys("Hello, World!")
    
    # Return to normal mode
    nvim.type_keys("<Esc>")
    assert nvim.get_mode() == "n"
```

### ⌨️ **Exact Keystroke Simulation**
Every keystroke matches real nvim behavior:

| Keystroke | Real Nvim | This Interface | Description |
|-----------|-----------|----------------|-------------|
| `i` | Enter insert mode | `nvim.type_keys("i")` | Insert at cursor |
| `A` | End of line + insert | `nvim.type_keys("A")` | Append at line end |
| `o` | New line below + insert | `nvim.type_keys("o")` | Open line below |
| `<Esc>` | Return to normal | `nvim.type_keys("<Esc>")` | Exit insert mode |
| `dd` | Delete line | `nvim.type_keys("dd")` | Delete current line |
| `cw` | Change word | `nvim.type_keys("cw")` | Delete word + insert |
| `/text<Enter>` | Search | `nvim.type_keys("/text<Enter>")` | Search for pattern |

## Files

- **`raw_nvim_interface.py`** - Main interface class
- **`test_raw_nvim_interface.py`** - Test cases showing realistic workflows
- **`simple_raw_example.py`** - Simple demonstration
- **`realistic_nvim_usage.py`** - Complex real-world examples

## Basic Usage

```python
from raw_nvim_interface import RawNvimEditor

# Create editor (starts in normal mode)
with RawNvimEditor() as nvim:
    # Type exactly like in real nvim
    nvim.type_keys("i")                    # Enter insert mode
    nvim.type_keys("Hello, World!")       # Type text
    nvim.type_keys("<Esc>")               # Return to normal mode
    nvim.type_keys("0")                   # Go to beginning of line
    nvim.type_keys("cw")                  # Change word (enters insert mode)
    nvim.type_keys("Hi")                  # Type replacement
    nvim.type_keys("<Esc>")               # Back to normal mode
    
    # Get results
    content = nvim.get_buffer_content()   # ["Hi, World!"]
    mode = nvim.get_mode()                # "n" (normal mode)
    cursor = nvim.get_cursor_position()   # (row, col)
```

## Realistic Workflows

### Writing a Python Function
```python
with RawNvimEditor() as nvim:
    # Write function signature
    nvim.type_keys("i")
    nvim.type_keys("def greet(name):")
    nvim.type_keys("<Enter>")
    nvim.type_keys("    return f'Hello, {name}!'")
    nvim.type_keys("<Esc>")
    
    # Add docstring above
    nvim.type_keys("gg")      # Go to first line
    nvim.type_keys("O")       # Open line above, enter insert mode
    nvim.type_keys('"""Simple greeting function."""')
    nvim.type_keys("<Esc>")
```

### Editing Existing Code
```python
# Start with existing code
code = ["def hello():", "    pass"]
with RawNvimEditor(code) as nvim:
    # Add parameter to function
    nvim.type_keys("gg")      # First line
    nvim.type_keys("f)")      # Find closing paren
    nvim.type_keys("i")       # Insert before )
    nvim.type_keys("name")    # Add parameter
    nvim.type_keys("<Esc>")   # Back to normal
    
    # Replace 'pass' with return statement
    nvim.type_keys("j")       # Down to second line
    nvim.type_keys("w")       # Move to 'pass'
    nvim.type_keys("cw")      # Change word (enters insert mode)
    nvim.type_keys("return f'Hello, {name}!'")
    nvim.type_keys("<Esc>")
```

## Advanced Features

### Mode Validation
```python
with RawNvimEditor() as nvim:
    nvim.assert_mode("n")           # Ensure we're in normal mode
    nvim.type_keys("i")
    nvim.assert_mode("i")           # Ensure we're in insert mode
    nvim.assert_cursor_at(1, 0)     # Validate cursor position
```

### Content Validation
```python
with RawNvimEditor() as nvim:
    nvim.type_keys("iHello<Esc>")
    nvim.assert_line_content(1, "Hello")    # Check line content
    assert nvim.get_current_line() == "Hello"
```

## Comparison with Test Suite

| Aspect | Test Suite | Raw Interface |
|--------|------------|---------------|
| **Purpose** | Test nvim functionality | Simulate real user interaction |
| **API** | Mixed (`command()`, `input()`, `feedkeys()`) | Single (`type_keys()`) |
| **Mode Handling** | Explicit commands | Natural transitions |
| **Use Case** | Comprehensive testing | User behavior simulation |
| **Realism** | High functionality coverage | Exact keystroke equivalence |

## Running Examples

```bash
# Simple demonstration
uv run python simple_raw_example.py

# Comprehensive examples (may be slow)
uv run python realistic_nvim_usage.py

# Run tests
uv run pytest test_raw_nvim_interface.py -v
```

## Key Benefits

1. **🎯 Exact User Simulation** - Every keystroke matches real nvim
2. **🔄 Natural Mode Transitions** - No artificial mode switching
3. **✅ Realistic Validation** - Test like a real user would interact
4. **📝 Clear Intent** - Code reads like actual vim commands
5. **🐛 Better Debugging** - Easy to understand what user "typed"

## When to Use

**Use Raw Interface When:**
- Simulating real user interaction
- Testing user workflows
- Training AI models on vim usage
- Creating vim tutorials/demos
- Need exact keystroke equivalence

**Use Test Suite When:**
- Testing specific nvim features
- Need comprehensive functionality coverage
- Performance testing
- Edge case validation

This interface bridges the gap between programmatic nvim control and realistic user simulation, making it perfect for applications that need to replicate actual vim usage patterns.