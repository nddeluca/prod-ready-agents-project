#!/usr/bin/env python3
"""
Development setup script for PyNvim Agents

This script helps set up the development environment and verifies everything works.
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd, description):
    """Run a command and print the result"""
    print(f"\n🔄 {description}")
    print(f"Running: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=Path(__file__).parent)
        if result.returncode == 0:
            print("✅ Success!")
            if result.stdout.strip():
                print(f"Output: {result.stdout.strip()}")
        else:
            print("❌ Failed!")
            print(f"Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False
    return True


def main():
    """Set up development environment"""
    print("🚀 PyNvim Agents Development Setup")
    print("=" * 50)

    # Check Python version

    print(f"✅ Python {sys.version}")

    # Check if we're in the right directory
    if not Path("pyproject.toml").exists():
        print("❌ Please run this script from the project root directory")
        return False

    # Install package in development mode
    if not run_command("uv sync", "Installing dependencies"):
        return False

    # Install package in editable mode
    if not run_command("uv run pip install -e .", "Installing package in development mode"):
        return False

    # Test imports
    if not run_command('uv run python -c "from pynvim_agents import RawNvimEditor; print(\'Import successful!\')"', "Testing package import"):
        return False

    # Run a simple test
    if not run_command("uv run pytest tests/test_raw_editor.py::TestRawNvimInterface::test_basic_insert_workflow -v", "Running basic test"):
        return False

    # Run example
    if not run_command("uv run python examples/raw_editor_demo.py > /dev/null 2>&1", "Testing example"):
        return False

    print("\n🎉 Development setup complete!")
    print("\n📋 Next steps:")
    print("  • Run all tests: uv run pytest")
    print("  • Run examples: uv run python examples/raw_editor_demo.py")
    print("  • Format code: uv run black src tests examples")
    print("  • Check types: uv run mypy src")
    print("  • View docs: open docs/raw_editor_guide.md")

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
