"""
Pytest configuration and fixtures for nvim tests
"""
import os
import shutil
import tempfile
from typing import Iterator

import pytest

from src.pynvim_agents.raw_editor import RawNvimEditor


@pytest.fixture(autouse=True)
def cleanup_swap_files():
    """Automatically clean up any nvim swap files before and after each test"""
    # Clean up before test
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith((".swp", ".swo")) or file.startswith("."):
                if ".swp" in file:
                    try:
                        os.remove(os.path.join(root, file))
                    except:
                        pass
    
    yield
    
    # Clean up after test
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith((".swp", ".swo")) or file.startswith("."):
                if ".swp" in file:
                    try:
                        os.remove(os.path.join(root, file))
                    except:
                        pass


@pytest.fixture
def raw_editor() -> Iterator[RawNvimEditor]:
    """Provide a properly managed RawNvimEditor instance"""
    editor = None
    try:
        editor = RawNvimEditor()
        yield editor
    finally:
        if editor is not None:
            try:
                editor.close()
            except:
                pass


@pytest.fixture
def raw_editor_with_content() -> Iterator[RawNvimEditor]:
    """Provide a RawNvimEditor with sample content"""
    editor = None
    try:
        editor = RawNvimEditor(initial_content=["line1", "line2", "line3"])
        yield editor
    finally:
        if editor is not None:
            try:
                editor.close()
            except:
                pass
