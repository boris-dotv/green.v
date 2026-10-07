#!/usr/bin/env python3
"""Non-tty fallback tests for run.main.

When stdin is not a tty (piped input, CI, cron) main() must not block on
input(): it defaults the choice to "0" and exits the loop immediately
without dispatching any handler. These tests pin that guard so a refactor
of the menu loop cannot reintroduce a hang in non-interactive runs.
"""

import io
import unittest
from unittest import mock

import run


class _NonTtyStdin(io.StringIO):
    """StringIO that reports itself as not a tty."""

    def isatty(self):
        return False


class TestNonTtyFallback(unittest.TestCase):
    def _run_main(self, stdin_text=""):
        fake_stdin = _NonTtyStdin(stdin_text)
        with mock.patch.object(run.sys, "stdin", fake_stdin), \
                mock.patch.object(run, "print_banner"), \
                mock.patch.object(run, "print_menu"), \
                mock.patch.object(run, "run_demo") as demo, \
                mock.patch.object(run, "run_test") as test, \
                mock.patch.object(run, "run_main") as main_handler:
            run.main()
        return demo, test, main_handler

    def test_non_tty_exits_without_dispatch(self):
        demo, test, main_handler = self._run_main()
        demo.assert_not_called()
        test.assert_not_called()
        main_handler.assert_not_called()

    def test_non_tty_ignores_pending_input(self):
        demo, test, main_handler = self._run_main("1\n")
        demo.assert_not_called()
        test.assert_not_called()
        main_handler.assert_not_called()

    def test_non_tty_does_not_consume_stdin(self):
        fake_stdin = _NonTtyStdin("1\n")
        with mock.patch.object(run.sys, "stdin", fake_stdin), \
                mock.patch.object(run, "print_banner"), \
                mock.patch.object(run, "print_menu"):
            run.main()
        self.assertEqual(fake_stdin.read(), "1\n")

    def test_non_tty_prints_menu_once(self):
        with mock.patch.object(run.sys, "stdin", _NonTtyStdin()), \
                mock.patch.object(run, "print_banner") as banner, \
                mock.patch.object(run, "print_menu") as menu:
            run.main()
        banner.assert_called_once()
        menu.assert_called_once()


if __name__ == "__main__":
    unittest.main()
