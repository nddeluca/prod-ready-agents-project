import os
import subprocess
import tempfile
import time

import pynvim
import pytest


class TestPynvimBuffer:

    def send_keys(self, nvim_instance, keys):
        """Helper to send keys with proper termcode replacement"""
        nvim_instance.api.feedkeys(
            nvim_instance.api.replace_termcodes(keys, True, False, True), "n", False
        )

    @pytest.fixture(scope="function")
    def nvim_instance(self):
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

    @pytest.fixture
    def buffer(self, nvim_instance):
        buf = nvim_instance.current.buffer
        buf[:] = [""]
        nvim_instance.command("normal! gg")
        nvim_instance.command("set nomodified")
        return buf

    def test_buffer_initialization_empty(self, buffer):
        assert len(buffer) == 1
        assert buffer[0] == ""

    def test_buffer_initialization_with_text(self, buffer):
        initial_text = ["Hello, World!", "This is line 2", "Line 3 here"]
        buffer[:] = initial_text

        assert len(buffer) == 3
        assert buffer[0] == "Hello, World!"
        assert buffer[1] == "This is line 2"
        assert buffer[2] == "Line 3 here"

    def test_buffer_initialization_single_line(self, buffer):
        buffer[:] = ["Single line of text"]

        assert len(buffer) == 1
        assert buffer[0] == "Single line of text"

    def test_buffer_multiline_string_split(self, buffer):
        text = "Line 1\nLine 2\nLine 3"
        buffer[:] = text.split("\n")

        assert len(buffer) == 3
        assert buffer[0] == "Line 1"
        assert buffer[1] == "Line 2"
        assert buffer[2] == "Line 3"

    def test_normal_mode_basic_movement(self, nvim_instance, buffer):
        buffer[:] = ["First line", "Second line", "Third line"]

        nvim_instance.command("normal! gg")
        row, col = nvim_instance.current.window.cursor
        assert row == 1
        assert col == 0

    def test_normal_mode_line_navigation(self, nvim_instance, buffer):
        buffer[:] = ["Line 1", "Line 2", "Line 3", "Line 4"]

        nvim_instance.command("normal! gg")
        nvim_instance.command("normal! j")
        row, col = nvim_instance.current.window.cursor
        assert row == 2

        nvim_instance.command("normal! j")
        row, col = nvim_instance.current.window.cursor
        assert row == 3

    def test_normal_mode_character_navigation(self, nvim_instance, buffer):
        buffer[:] = ["Hello World"]

        nvim_instance.command("normal! gg0")
        nvim_instance.command("normal! l")
        row, col = nvim_instance.current.window.cursor
        assert row == 1
        assert col == 1

        nvim_instance.command("normal! 4l")
        row, col = nvim_instance.current.window.cursor
        assert col == 5

    def test_normal_mode_word_movement(self, nvim_instance, buffer):
        buffer[:] = ["Hello world this is a test"]

        nvim_instance.command("normal! gg0")
        nvim_instance.command("normal! w")
        row, col = nvim_instance.current.window.cursor
        assert col == 6

        nvim_instance.command("normal! w")
        row, col = nvim_instance.current.window.cursor
        assert col == 12

    def test_normal_mode_end_of_line(self, nvim_instance, buffer):
        buffer[:] = ["Hello World"]

        nvim_instance.command("normal! gg")
        nvim_instance.command("normal! $")
        row, col = nvim_instance.current.window.cursor
        assert col == 10

    def test_normal_mode_beginning_of_line(self, nvim_instance, buffer):
        buffer[:] = ["  Hello World"]

        nvim_instance.command("normal! gg$")
        nvim_instance.command("normal! 0")
        row, col = nvim_instance.current.window.cursor
        assert col == 0

        nvim_instance.command("normal! ^")
        row, col = nvim_instance.current.window.cursor
        assert col == 2

    def test_insert_mode_basic_insertion(self, nvim_instance, buffer):
        buffer[:] = [""]
        nvim_instance.command("normal! gg")
        nvim_instance.command("startinsert")
        nvim_instance.input("Hello")
        nvim_instance.command("stopinsert")

        assert buffer[0] == "Hello"

    def test_insert_mode_append(self, nvim_instance, buffer):
        buffer[:] = ["Hello"]
        nvim_instance.command("normal! gg$")
        nvim_instance.command("startinsert!")
        nvim_instance.input(" World")
        nvim_instance.command("stopinsert")

        assert buffer[0] == "Hello World"

    def test_insert_mode_new_line(self, nvim_instance, buffer):
        buffer[:] = ["First line"]
        nvim_instance.command("normal! gg$")
        nvim_instance.command("normal! oSecond line")
        nvim_instance.command("stopinsert")

        assert len(buffer) == 2
        assert buffer[0] == "First line"
        assert buffer[1] == "Second line"

    def test_insert_mode_new_line_above(self, nvim_instance, buffer):
        buffer[:] = ["Second line"]
        nvim_instance.command("normal! gg")
        nvim_instance.command("normal! OFirst line")
        nvim_instance.command("stopinsert")

        assert len(buffer) == 2
        assert buffer[0] == "First line"
        assert buffer[1] == "Second line"

    def test_insert_mode_enter_key(self, nvim_instance, buffer):
        buffer[:] = [""]
        nvim_instance.command("normal! gg")
        nvim_instance.command("startinsert")
        nvim_instance.input("Line 1")
        self.send_keys(nvim_instance, "<CR>")
        nvim_instance.input("Line 2")
        nvim_instance.command("stopinsert")

        assert len(buffer) == 2
        assert buffer[0] == "Line 1"
        assert buffer[1] == "Line 2"

    def test_insert_mode_backspace(self, nvim_instance, buffer):
        buffer[:] = [""]
        nvim_instance.command("normal! gg")
        nvim_instance.command("startinsert")
        nvim_instance.input("Hello World")
        self.send_keys(nvim_instance, "<BS><BS><BS><BS><BS>")
        nvim_instance.command("stopinsert")

        assert buffer[0] == "Hello "

    def test_ctrl_combinations_undo(self, nvim_instance, buffer):
        buffer[:] = ["Original text"]
        nvim_instance.command("normal! gg$")
        nvim_instance.command("startinsert!")
        nvim_instance.input(" added")
        nvim_instance.command("stopinsert")

        assert buffer[0] == "Original text added"

        nvim_instance.command("undo")
        assert buffer[0] == "Original text"

    def test_ctrl_combinations_word_deletion(self, nvim_instance, buffer):
        buffer[:] = [""]
        nvim_instance.command("normal! gg")
        nvim_instance.command("startinsert")
        nvim_instance.input("Hello World Test")
        self.send_keys(nvim_instance, "<C-w>")
        nvim_instance.command("stopinsert")

        assert buffer[0] == "Hello World "

    def test_ctrl_combinations_line_deletion(self, nvim_instance, buffer):
        buffer[:] = [""]
        nvim_instance.command("normal! gg")
        nvim_instance.command("startinsert")
        nvim_instance.input("This will be deleted")
        self.send_keys(nvim_instance, "<C-u>")
        nvim_instance.input("New text")
        nvim_instance.command("stopinsert")

        assert buffer[0] == "New text"

    def test_ctrl_combinations_escape_alternative(self, nvim_instance, buffer):
        buffer[:] = [""]
        nvim_instance.command("normal! gg")
        nvim_instance.command("startinsert")
        nvim_instance.input("Insert mode")
        self.send_keys(nvim_instance, "<C-[>")

        mode = nvim_instance.api.get_mode()["mode"]
        assert mode == "n"

    def test_visual_mode_selection(self, nvim_instance, buffer):
        buffer[:] = ["Hello World Test"]
        nvim_instance.command("normal! gg0")
        nvim_instance.command("normal! v4l")

        mode = nvim_instance.api.get_mode()["mode"]
        assert mode == "v"

    def test_delete_operations(self, nvim_instance, buffer):
        buffer[:] = ["Hello World", "Second line"]
        nvim_instance.command("normal! gg")
        nvim_instance.command("normal! dw")

        assert buffer[0] == "World"

    def test_yank_and_paste(self, nvim_instance, buffer):
        buffer[:] = ["Hello World", "Second line"]
        nvim_instance.command("normal! gg")
        nvim_instance.command("normal! yw")
        nvim_instance.command("normal! j0")
        nvim_instance.command("normal! p")

        assert buffer[1] == "SHello econd line"

    def test_search_functionality(self, nvim_instance, buffer):
        buffer[:] = ["Hello World", "World Peace", "Peace and Love"]
        nvim_instance.command("normal! gg")
        self.send_keys(nvim_instance, "/World<CR>")

        row, col = nvim_instance.current.window.cursor
        assert row == 1
        assert col == 6

    def test_replace_mode(self, nvim_instance, buffer):
        buffer[:] = ["Hello World"]
        nvim_instance.command("normal! gg")
        self.send_keys(nvim_instance, "RHi<Esc>")

        assert buffer[0] == "Hillo World"

    def test_buffer_modification_tracking(self, nvim_instance, buffer):
        buffer[:] = ["Original"]
        nvim_instance.command("set nomodified")
        modified_before = nvim_instance.current.buffer.options["modified"]

        nvim_instance.command("normal! gg$")
        self.send_keys(nvim_instance, "a text<Esc>")

        modified_after = nvim_instance.current.buffer.options["modified"]

        assert not modified_before
        assert modified_after

    def test_buffer_content_retrieval_all_lines(self, buffer):
        test_content = ["Line 1", "Line 2", "Line 3", "Line 4"]
        buffer[:] = test_content

        retrieved_content = buffer[:]
        assert retrieved_content == test_content

    def test_buffer_content_retrieval_slice(self, buffer):
        test_content = ["Line 1", "Line 2", "Line 3", "Line 4", "Line 5"]
        buffer[:] = test_content

        middle_lines = buffer[1:4]
        assert middle_lines == ["Line 2", "Line 3", "Line 4"]

    def test_buffer_content_retrieval_single_line(self, buffer):
        test_content = ["First", "Second", "Third"]
        buffer[:] = test_content

        assert buffer[0] == "First"
        assert buffer[1] == "Second"
        assert buffer[2] == "Third"

    def test_buffer_line_count(self, buffer):
        buffer[:] = ["Line 1", "Line 2", "Line 3"]
        assert len(buffer) == 3

    def test_buffer_empty_line_handling(self, buffer):
        buffer[:] = ["Line 1", "", "Line 3"]
        assert len(buffer) == 3
        assert buffer[1] == ""

    def test_complex_keystroke_sequence(self, nvim_instance, buffer):
        buffer[:] = ["function hello() {", "  return 'world';", "}"]

        nvim_instance.command("normal! gg")
        self.send_keys(nvim_instance, "f(aname<Esc>")
        self.send_keys(nvim_instance, "jA // comment<Esc>")

        assert buffer[0] == "function hello(name) {"
        assert buffer[1] == "  return 'world'; // comment"

    def test_tab_and_indentation(self, nvim_instance, buffer):
        buffer[:] = [""]
        nvim_instance.command("normal! gg")
        self.send_keys(nvim_instance, "i<Tab>indented<Esc>")

        assert buffer[0].startswith("\t") or buffer[0].startswith("    ")
        assert "indented" in buffer[0]

    def test_special_characters_input(self, nvim_instance, buffer):
        buffer[:] = [""]
        nvim_instance.command("normal! gg")
        nvim_instance.command("startinsert")
        nvim_instance.input("Special: !@#$%^&*()")
        nvim_instance.command("stopinsert")

        assert buffer[0] == "Special: !@#$%^&*()"

    def test_unicode_input(self, nvim_instance, buffer):
        buffer[:] = [""]
        nvim_instance.command("normal! gg")
        nvim_instance.command("startinsert")
        nvim_instance.input("Unicode: αβγ δεζ")
        nvim_instance.command("stopinsert")

        assert buffer[0] == "Unicode: αβγ δεζ"

    def test_multiple_cursors_simulation(self, nvim_instance, buffer):
        buffer[:] = ["line one", "line two", "line three"]

        self.send_keys(nvim_instance, "ggA modified1<Esc>")
        self.send_keys(nvim_instance, "jA modified2<Esc>")
        self.send_keys(nvim_instance, "jA modified3<Esc>")

        assert buffer[0] == "line one modified1"
        assert buffer[1] == "line two modified2"
        assert buffer[2] == "line three modified3"

    def test_buffer_line_replacement(self, buffer):
        buffer[:] = ["Original line 1", "Original line 2", "Original line 3"]
        buffer[1] = "Replaced line 2"

        assert buffer[0] == "Original line 1"
        assert buffer[1] == "Replaced line 2"
        assert buffer[2] == "Original line 3"

    def test_buffer_line_insertion(self, buffer):
        buffer[:] = ["Line 1", "Line 3"]
        buffer.append("Line 2", 1)

        assert len(buffer) == 3
        assert buffer[0] == "Line 1"
        assert buffer[1] == "Line 2"
        assert buffer[2] == "Line 3"

    def test_buffer_line_deletion(self, buffer):
        buffer[:] = ["Line 1", "Line 2", "Line 3", "Line 4"]
        del buffer[1:3]

        assert len(buffer) == 2
        assert buffer[0] == "Line 1"
        assert buffer[1] == "Line 4"

    def test_macro_recording_simulation(self, nvim_instance, buffer):
        buffer[:] = ["test", "test", "test"]

        self.send_keys(nvim_instance, "ggA123<Esc>")
        self.send_keys(nvim_instance, "jA123<Esc>")
        self.send_keys(nvim_instance, "jA123<Esc>")

        for i in range(3):
            assert buffer[i] == "test123"

    def test_advanced_search_and_replace(self, nvim_instance, buffer):
        buffer[:] = ["Hello world", "Hello universe", "Hello everyone"]

        nvim_instance.command("%s/Hello/Hi/g")

        assert buffer[0] == "Hi world"
        assert buffer[1] == "Hi universe"
        assert buffer[2] == "Hi everyone"
