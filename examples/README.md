# Examples

This directory contains practical examples of using PyNvim Agents for realistic vim automation and testing.

## Files

- **`raw_editor_demo.py`** - Simple demonstration of the RawNvimEditor interface
- **`realistic_workflows.py`** - Complex real-world editing workflows  
- **`comprehensive_example.py`** - Full feature demonstration with buffer manipulation

## Running Examples

```bash
# Run the raw editor demo
python examples/raw_editor_demo.py

# Run realistic workflows (may be slow)
python examples/realistic_workflows.py

# Run comprehensive example
python examples/comprehensive_example.py
```

## Example Categories

### Basic Usage (`raw_editor_demo.py`)
- Mode transitions (normal ↔ insert)
- Simple text editing
- Keystroke equivalence demonstration

### Realistic Workflows (`realistic_workflows.py`)
- Python function development
- Configuration file editing
- Debugging sessions
- Complex refactoring

### Comprehensive Demo (`comprehensive_example.py`)
- Buffer manipulation
- Advanced vim operations
- Multi-step editing workflows
- Direct buffer access vs keystroke simulation

## Key Patterns

### Exact Keystroke Simulation
```python
with RawNvimEditor() as nvim:
    nvim.type_keys("i")           # Insert mode
    nvim.type_keys("Hello")       # Type text
    nvim.type_keys("<Esc>")       # Normal mode
    nvim.type_keys("0cw")         # Navigate and change word
    nvim.type_keys("Hi<Esc>")     # Replace and exit
```

### Realistic Development Workflow
```python
# Write a Python function
nvim.type_keys("idef greet(name):<Enter>")
nvim.type_keys("    return f'Hello, {name}!'<Esc>")

# Add docstring
nvim.type_keys("ggO")  # First line, open above
nvim.type_keys('"""Greeting function."""<Esc>')
```

### Complex Editing Operations
```python
# Search and replace workflow
nvim.type_keys("/old_text<Enter>")  # Search
nvim.type_keys("cw")                # Change word
nvim.type_keys("new_text<Esc>")     # Replace
nvim.type_keys("n.")                # Next occurrence, repeat
```

These examples demonstrate how PyNvim Agents can be used for:
- Training AI models on vim usage
- Automating repetitive editing tasks
- Testing vim configurations and plugins
- Creating realistic vim demonstrations