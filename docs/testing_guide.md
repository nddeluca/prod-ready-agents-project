# PyNvim Buffer Manipulation Test Suite

This directory contains a comprehensive test suite for using pynvim to manipulate Neovim buffers with keyboard input simulation.

## Files

- `test_pynvim_buffer.py` - Main test suite with 41 comprehensive tests
- `pynvim_example.py` - Demonstration script showing real-world usage
- `pyproject.toml` - Updated with pynvim and pytest dependencies

## Test Coverage

### Buffer Initialization
- Empty buffer creation
- Buffer initialization with text content
- Single line and multiline text handling

### Normal Mode Operations
- Basic cursor movement (h, j, k, l)
- Line navigation (gg, G, j, k)
- Character navigation (l, h, 0, $, ^)
- Word movement (w, b, e)
- Line beginning/end navigation

### Insert Mode Operations
- Basic text insertion (i, a, o, O)
- Text input and modification
- Enter key handling for new lines
- Backspace functionality

### Control Key Combinations
- Ctrl-W (delete word backwards)
- Ctrl-U (delete line)
- Ctrl-[ (escape alternative)
- Undo operations

### Advanced Operations
- Visual mode selection
- Delete operations (dw, dd)
- Yank and paste (y, p)
- Search functionality (/)
- Replace mode (R)
- Tab and indentation
- Special character input
- Unicode text support

### Buffer Content Manipulation
- Direct buffer content retrieval
- Line slicing and indexing
- Buffer modification tracking
- Line replacement, insertion, and deletion
- Search and replace operations

## Key Features Tested

1. **Headless Neovim Integration**: Tests spawn headless nvim instances
2. **Socket Communication**: Uses Unix sockets for nvim communication
3. **Proper Cleanup**: Ensures nvim processes are terminated after tests
4. **State Isolation**: Each test gets a fresh nvim instance
5. **Raw Keystroke Simulation**: Tests actual vim key sequences
6. **Buffer State Validation**: Verifies buffer contents after operations

## Running Tests

```bash
# Run all tests (41 tests, all passing)
uv run pytest test_pynvim_buffer.py -v

# Run specific test categories
uv run pytest test_pynvim_buffer.py -k "insert_mode" -v
uv run pytest test_pynvim_buffer.py -k "normal_mode" -v
uv run pytest test_pynvim_buffer.py -k "buffer_content" -v

# Run demonstration
uv run python pynvim_example.py
```

## Test Results

✅ **All 41 tests passing** - The test suite is fully functional and covers comprehensive pynvim buffer manipulation scenarios.

## Test Architecture

The test suite uses pytest fixtures to:
- Create isolated nvim instances for each test
- Provide clean buffer states
- Handle proper cleanup of processes
- Ensure test independence

Key components:
- `nvim_instance` fixture: Creates headless nvim with socket communication
- `buffer` fixture: Provides clean buffer for each test
- **Critical**: `send_keys()` helper using `replace_termcodes()` for proper vim key sequence handling
- Mix of `nvim.command()`, `nvim.input()`, and `nvim.api.feedkeys()` for different operations

## Usage Patterns Demonstrated

1. **Basic Setup**:
   ```python
   nvim = pynvim.attach("socket", path=socket_path)
   buffer = nvim.current.buffer
   ```

2. **Buffer Initialization**:
   ```python
   buffer[:] = ["Line 1", "Line 2", "Line 3"]
   ```

3. **Normal Mode Commands**:
   ```python
   nvim.command("normal! gg")  # Go to first line
   nvim.command("normal! w")   # Move word forward
   ```

4. **Insert Mode Operations**:
   ```python
   nvim.command("startinsert")
   nvim.input("Hello World")
   nvim.command("stopinsert")
   ```

5. **Key Combinations** (Critical - Use replace_termcodes):
   ```python
   def send_keys(self, nvim_instance, keys):
       """Helper to send keys with proper termcode replacement"""
       nvim_instance.api.feedkeys(nvim_instance.api.replace_termcodes(keys, True, False, True), "n", False)
   
   # Usage:
   self.send_keys(nvim_instance, "<C-w>")   # Ctrl-W
   self.send_keys(nvim_instance, "<Esc>")   # Escape
   self.send_keys(nvim_instance, "<BS>")    # Backspace
   ```

This test suite provides a solid foundation for any application that needs to programmatically control Neovim buffers with realistic keyboard input simulation.