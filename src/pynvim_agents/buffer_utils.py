"""
Buffer utilities for comprehensive pynvim testing

This module provides utilities for testing nvim buffer operations including:
- Buffer initialization and manipulation
- Normal mode operations (navigation, editing)
- Insert mode operations
- Control key combinations
- Visual mode operations
- Advanced editing patterns
"""

import os
import subprocess
import tempfile
import time
from collections.abc import Generator
from typing import Any

import pynvim

try:
    import pytest  # type: ignore
except ImportError:
    pytest = None  # type: ignore


class NvimBufferTester:
    """
    Comprehensive testing utilities for pynvim buffer operations
    """

    def __init__(self) -> None:
        """Initialize the buffer tester"""
        pass

    def send_keys(self, nvim_instance: Any, keys: str) -> None:
        """Helper to send keys with proper termcode replacement"""
        nvim_instance.api.feedkeys(
            nvim_instance.api.replace_termcodes(keys, True, False, True), "n", False
        )

    def nvim_instance(self) -> Generator[Any, None, None]:
        """Create a clean nvim instance for testing"""
        with tempfile.TemporaryDirectory() as tmpdir:
            socket_path = os.path.join(tmpdir, "nvim.sock")

            proc = subprocess.Popen(
                ["nvim", "--headless", "--listen", socket_path, "--noplugin"]
            )

            time.sleep(0.5)

            try:
                nvim = pynvim.attach("socket", path=socket_path)
                nvim.command("set nomodified")
                yield nvim
            finally:
                try:
                    nvim.quit()
                except Exception:
                    pass
                proc.terminate()
                proc.wait(timeout=5)

    def buffer(self, nvim_instance: Any) -> Any:
        """Create a clean buffer for testing"""
        buf = nvim_instance.current.buffer
        buf[:] = [""]
        nvim_instance.command("normal! gg")
        nvim_instance.command("set nomodified")
        return buf


class NvimTestUtils:
    """
    Standalone utilities for nvim testing without pytest fixtures
    """

    @staticmethod
    def create_nvim_instance(
        initial_content: list[str] | None = None,
    ) -> tuple[Any, Any, Any]:
        """Create a standalone nvim instance for testing"""
        tmpdir = tempfile.mkdtemp()
        socket_path = os.path.join(tmpdir, "nvim.sock")

        proc = subprocess.Popen(
            ["nvim", "--headless", "--listen", socket_path, "--noplugin"]
        )

        time.sleep(0.5)

        try:
            nvim = pynvim.attach("socket", path=socket_path)
            buffer = nvim.current.buffer

            if initial_content:
                buffer[:] = initial_content
            else:
                buffer[:] = [""]

            nvim.command("normal! gg")
            nvim.command("set nomodified")

            return nvim, buffer, proc
        except Exception as e:
            proc.terminate()
            raise e

    @staticmethod
    def cleanup_nvim_instance(nvim: Any, proc: Any) -> None:
        """Clean up a nvim instance"""
        try:
            nvim.quit()
        except Exception:
            pass
        proc.terminate()
        proc.wait(timeout=5)

    @staticmethod
    def send_keys(nvim_instance: Any, keys: str) -> None:
        """Send keys with proper termcode replacement"""
        nvim_instance.api.feedkeys(
            nvim_instance.api.replace_termcodes(keys, True, False, True), "n", False
        )
