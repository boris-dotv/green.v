#!/usr/bin/env python3
"""Tests for formula.calculate_from_expression rejection of calls and attributes.

The public entry point must reject function calls, attribute access, subscripts
and comprehensions by falling through to the ValueError branch and returning
NaN. This pins the AST security boundary at the level callers actually use.
"""

import math
import unittest

from formula import calculate_from_expression


class TestRejectedConstructs(unittest.TestCase):
    def _assert_nan(self, expression, values=None):
        result = calculate_from_expression(expression, values or {"A": 1.0, "B": 2.0})
        self.assertTrue(math.isnan(result), f"expected NaN for {expression!r}, got {result!r}")

    def test_function_call_yields_nan(self):
        self._assert_nan("abs(A)")

    def test_builtin_call_with_two_args_yields_nan(self):
        self._assert_nan("max(A, B)")

    def test_attribute_access_yields_nan(self):
        self._assert_nan("A.real")

    def test_subscript_yields_nan(self):
        self._assert_nan("A[0]")

    def test_comparison_yields_nan(self):
        self._assert_nan("A < B")

    def test_boolean_and_yields_nan(self):
        self._assert_nan("A and B")

    def test_string_literal_yields_nan(self):
        self._assert_nan("'abc'")

    def test_none_literal_yields_nan(self):
        self._assert_nan("None")

    def test_list_literal_yields_nan(self):
        self._assert_nan("[A, B]")

    def test_valid_expression_still_evaluates(self):
        self.assertEqual(calculate_from_expression("(A + B) * 2", {"A": 1.0, "B": 2.0}), 6.0)


if __name__ == "__main__":
    unittest.main()
