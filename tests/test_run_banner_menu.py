#!/usr/bin/env python3
"""Tests for run.print_banner and run.print_menu output shape."""

import io
import unittest
from contextlib import redirect_stdout

import run


class TestPrintBanner(unittest.TestCase):
    def _capture(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            run.print_banner()
        return buf.getvalue()

    def test_banner_starts_with_blank_line(self):
        out = self._capture()
        self.assertTrue(out.startswith("\n"))

    def test_banner_contains_rocket_border(self):
        out = self._capture()
        self.assertIn("\U0001f680" * 40, out)

    def test_banner_contains_title_lines(self):
        out = self._capture()
        self.assertIn("FinTalk.AI - Enhanced Financial Assistant", out)
        self.assertIn("MCP Architecture + GitHub Integration", out)

    def test_banner_has_four_lines(self):
        out = self._capture()
        lines = out.split("\n")
        # leading blank line, then 4 printed lines, then trailing empty
        self.assertEqual(lines[0], "")
        self.assertEqual(lines[1], "\U0001f680" * 40)
        self.assertEqual(lines[2], " " * 15 + "FinTalk.AI - Enhanced Financial Assistant")
        self.assertEqual(lines[3], " " * 20 + "MCP Architecture + GitHub Integration")
        self.assertEqual(lines[4], "\U0001f680" * 40)


class TestPrintMenu(unittest.TestCase):
    def _capture(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            run.print_menu()
        return buf.getvalue()

    def test_menu_contains_separator(self):
        out = self._capture()
        self.assertIn("=" * 80, out)

    def test_menu_contains_all_options(self):
        out = self._capture()
        for option in ("[1]", "[2]", "[3]", "[0]"):
            self.assertIn(option, out)

    def test_menu_ends_with_prompt(self):
        out = self._capture()
        self.assertTrue(out.endswith("\n\u8bf7\u9009\u62e9 [0-3]: "))

    def test_menu_separator_count(self):
        out = self._capture()
        self.assertEqual(out.count("=" * 80), 3)


if __name__ == "__main__":
    unittest.main()
