#!/usr/bin/env python3
"""Tests for the interactive menu validation in run.py.

run.py only needs the standard library plus python-dotenv (already a
project dependency), and the run_* handlers are patched so no demo,
network or API code is executed.
"""

import io
import sys
import unittest
from contextlib import redirect_stdout
from unittest import mock

import run


class _FakeStdin(io.StringIO):
    def __init__(self, text, isatty=True):
        super().__init__(text)
        self._isatty = isatty

    def isatty(self):
        return self._isatty


class TestMenuValidation(unittest.TestCase):
    def _run_main(self, stdin_text, isatty=True):
        fake_stdin = _FakeStdin(stdin_text, isatty=isatty)
        with mock.patch.object(sys, "stdin", fake_stdin), \
                mock.patch.object(run, "run_demo") as demo, \
                mock.patch.object(run, "run_test") as test, \
                mock.patch.object(run, "run_main") as main_fn, \
                redirect_stdout(io.StringIO()) as out:
            run.main()
        return out.getvalue(), demo, test, main_fn

    def test_choice_one_runs_demo(self):
        _, demo, test, main_fn = self._run_main("1\n")
        demo.assert_called_once_with()
        test.assert_not_called()
        main_fn.assert_not_called()

    def test_choice_two_runs_test(self):
        _, demo, test, main_fn = self._run_main("2\n")
        test.assert_called_once_with()
        demo.assert_not_called()
        main_fn.assert_not_called()

    def test_choice_three_runs_main(self):
        _, demo, test, main_fn = self._run_main("3\n")
        main_fn.assert_called_once_with()
        demo.assert_not_called()
        test.assert_not_called()

    def test_choice_zero_exits_without_running_anything(self):
        _, demo, test, main_fn = self._run_main("0\n")
        demo.assert_not_called()
        test.assert_not_called()
        main_fn.assert_not_called()

    def test_empty_input_defaults_to_exit(self):
        _, demo, test, main_fn = self._run_main("\n")
        demo.assert_not_called()
        test.assert_not_called()
        main_fn.assert_not_called()

    def test_non_digit_input_is_rejected_then_retried(self):
        out, demo, _, _ = self._run_main("abc\n1\n")
        self.assertIn("\u274c \u65e0\u6548\u9009\u62e9: abc", out)
        demo.assert_called_once_with()

    def test_out_of_range_digit_is_rejected_then_retried(self):
        out, demo, _, _ = self._run_main("9\n1\n")
        self.assertIn("\u274c \u65e0\u6548\u9009\u62e9: 9", out)
        demo.assert_called_once_with()

    def test_non_tty_stdin_defaults_to_exit(self):
        _, demo, test, main_fn = self._run_main("1\n", isatty=False)
        demo.assert_not_called()
        test.assert_not_called()
        main_fn.assert_not_called()


if __name__ == "__main__":
    unittest.main()
