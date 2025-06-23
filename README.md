# PyNvim Agents

Production-ready tools for programmatic Neovim control and automation. This package provides comprehensive utilities for testing, automating, and simulating real user interaction with Neovim through pynvim.

## Features

### 🤖 **LLM Agent Interface (NEW!)**
- **Intelligent text editing** - LLMs can send natural language instructions
- **Iterative workflow** - Agent executes commands and provides state feedback
- **Command history tracking** - Full session logging and analysis
- **Context-aware suggestions** - Smart recommendations based on current state

### Raw Editor Interface
- **Exact keystroke simulation** - Every key sequence matches what a user would type
- **Realistic mode transitions** - Starts in normal mode, requires explicit `i`/`<Esc>` transitions  
- **Natural vim workflow** - Perfect for simulating real user behavior

### Comprehensive Testing Suite
- **80 comprehensive tests** covering all major nvim operations and agent functionality
- **Buffer manipulation** - Initialize, edit, retrieve content
- **Mode operations** - Normal, insert, visual, replace modes
- **Advanced features** - Search, yank/paste, control key combinations
- **Agent testing** - Full coverage of LLM integration patterns

### Production Ready
- Full test coverage with pytest
- Type hints and modern Python practices
- Comprehensive documentation and examples
- Easy installation and setup

## Quick Start

### Installation

```bash
# Install the package
pip install pynvim-agents

# Install with development dependencies  
pip install pynvim-agents[dev]
```

### Basic Usage

#### 🤖 LLM Agent Interface (Intelligent Editing)

```python
from pynvim_agents import VimAgent

# LLM-powered editing with natural language instructions
with VimAgent() as agent:
    # Agent receives current state and executes commands
    result = agent.execute_command("i", "Enter insert mode")
    result = agent.execute_command("def hello():", "Define function")
    result = agent.execute_command("<Esc>", "Exit insert mode")
    
    # Get formatted state for LLM consumption
    state = agent.format_state_for_llm()
    print(state)  # Shows buffer, cursor position, mode, suggestions
    
    # Execute multiple commands at once
    commands = [
        {"keystrokes": "o", "description": "New line"},
        {"keystrokes": "    return 'Hello!'", "description": "Add return"},
        {"keystrokes": "<Esc>", "description": "Exit insert"}
    ]
    results = agent.execute_commands(commands)
```

#### Raw Editor Interface (Realistic User Simulation)

```python
from pynvim_agents import RawNvimEditor

# Simulate exactly what a user would type
with RawNvimEditor() as nvim:
    # Start in normal mode (like real nvim)
    nvim.type_keys("i")                    # Enter insert mode
    nvim.type_keys("Hello, World!")       # Type text
    nvim.type_keys("<Esc>")               # Return to normal mode
    nvim.type_keys("0cw")                 # Go to start, change word
    nvim.type_keys("Hi<Esc>")             # Type replacement, exit insert
    
    content = nvim.get_buffer_content()   # ["Hi, World!"]
    mode = nvim.get_mode()                # "n" (normal mode)
```

## 🚀 LLM Integration

### With OpenAI API

```python
import openai
from pynvim_agents import VimAgent

class OpenAIVimEditor:
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)
        self.agent = VimAgent()
    
    def execute_task(self, task: str):
        # Get current state
        state = self.agent.format_state_for_llm()
        
        # Ask LLM for vim commands
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{
                "role": "user", 
                "content": f"Current vim state:\n{state}\n\nTask: {task}\n\nGenerate vim commands as JSON list."
            }]
        )
        
        # Execute LLM's commands
        commands = json.loads(response.choices[0].message.content)
        return self.agent.execute_commands(commands)

# Usage
editor = OpenAIVimEditor("your-api-key")
editor.execute_task("Add error handling to this function")
```

### Interactive Demo

```bash
# Try the interactive vim agent
python examples/interactive_vim_agent.py --example

# Or run the LLM integration demos
python examples/llm_integration_example.py
```

## Project Structure

```
pynvim-agents/
├── src/pynvim_agents/          # Main package
│   ├── __init__.py             # Package exports
│   ├── raw_editor.py           # RawNvimEditor class
│   ├── vim_agent.py            # VimAgent for LLM integration
│   └── buffer_utils.py         # Testing utilities
├── tests/                      # Test suite
│   ├── test_raw_editor.py      # Raw editor tests
│   ├── test_vim_agent.py       # VimAgent tests
│   └── test_buffer_operations.py # Buffer operation tests
├── examples/                   # Usage examples
│   ├── vim_agent_demo.py       # VimAgent demonstrations
│   ├── interactive_vim_agent.py # Interactive CLI demo
│   └── llm_integration_example.py # LLM integration patterns
├── docs/                       # Documentation
└── pyproject.toml             # Package configuration
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test categories
pytest tests/test_raw_editor.py -v   # Raw editor tests only
```

## Development

```bash
# Install in development mode
pip install -e .[dev]

# Run tests
pytest

# Format code
black src tests examples
ruff src tests examples
```

## Requirements

- **Python 3.10+**
- **Neovim** (accessible via `nvim` command)
- **pynvim** (automatically installed)

## License

MIT License

## Acknowledgments

- Built on top of the excellent [pynvim](https://github.com/neovim/pynvim) library
