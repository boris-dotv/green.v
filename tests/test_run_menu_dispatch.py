#!/usr/bin/env python3
"""Dispatch tests for run.main's interactive menu loop.

main() reads a choice from stdin, validates it, and dispatches to one of the
run_* handlers before breaking out of the loop. These tests patch the
handlers and feed choices through a fake stdin so no demo, network or heavy
dependency code is executed.
"""

import io
import unittest
from unittest import mock

import run


class _FakeStdin(io.StringIO):
    """StringIO that reports itself as a tty so main() reads from it."""

    def isatty(self):
        return True


class TestMainDispatch(unittest.TestCase):
    def _run_main(self, choice_text):
        fake_stdin = _FakeStdin(choice_text)
        with mock.patch.object(run.sys, "stdin", fake_stdin), \
                mock.patch.object(run, "print_banner"), \
                mock.patch.object(run, "print_menu"), \
                mock.patch.object(run, "run_demo") as demo, \
                mock.patch.object(run, "run_test") as test, \
                mock.patch.object(run, "run_main") as main_handler:
            run.main()
        return demo, test, main_handler

    def test_choice_one_dispatches_to_run_demo(self):
        demo, test, main_handler = self._run_main("1\n")
        demo.assert_called_once()
        test.assert_not_called()
        main_handler.assert_not_called()

    def test_choice_two_dispatches_to_run_test(self):
        demo, test, main_handler = self._run_main("2\n")
        test.assert_called_once()
        demo.assert_not_called()
        main_handler.assert_not_called()

    def test_choice_three_dispatches_to_run_main(self):
        demo, test, main_handler = self._run_main("3\n")
        main_handler.assert_called_once()
        demo.assert_not_called()
        test.assert_not_called()

    def test_choice_zero_exits_without_dispatch(self):
        demo, test, main_handler = self._run_main("0\n")
        demo.assert_not_called()
        test.assert_not_called()
        main_handler.assert_not_called()

    def test_invalid_choice_reprompts_then_dispatches(self):
        demo, test, main_handler = self._run_main("9\n1\n")
        demo.assert_called_once()
        test.assert_not_called()
        main_handler.assert_not_called()

    def test_non_digit_choice_reprompts_then_exits(self):
        demo, test, main_handler = self._run_main("abc\n0\n")
        demo.assert_not_called()
        test.assert_not_called()
        main_handler.assert_not_called()

    def test_empty_input_defaults_to_exit(self):
        demo, test, main_handler = self._run_main("\n")
        demo.assert_not_called()
        test.assert_not_called()
        main_handler.assert_not_called()


if __name__ == "__main__":
    unittest.main()
