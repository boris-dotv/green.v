#!/usr/bin/env python3
"""Tests for formula.calculate_from_expression nested parens and blank input.

Pins two edge cases at the public entry point: deeply nested or redundant
parentheses must evaluate normally, and blank/whitespace-only expressions
must return NaN (ast.parse raises SyntaxError, caught by the caller) rather
than raising out of the function.
"""

import math
import unittest

from formula import calculate_from_expression


class TestNestedParentheses(unittest.TestCase):
    def test_redundant_parentheses_around_variable(self):
        self.assertEqual(calculate_from_expression("((A))", {"A": 3.0}), 3.0)

    def test_deeply_nested_expression(self):
        expr = "((((A + B)))) * (((C)))"
        result = calculate_from_expression(expr, {"A": 1.0, "B": 2.0, "C": 4.0})
        self.assertEqual(result, 12.0)

    def test_nested_parentheses_with_negation(self):
        self.assertEqual(calculate_from_expression("-((A - B))", {"A": 1.0, "B": 4.0}), 3.0)

    def test_unbalanced_parentheses_yield_nan(self):
        result = calculate_from_expression("((A + B)", {"A": 1.0, "B": 2.0})
        self.assertTrue(math.isnan(result))


class TestBlankExpressions(unittest.TestCase):
    def test_empty_string_yields_nan(self):
        self.assertTrue(math.isnan(calculate_from_expression("", {"A": 1.0})))

    def test_whitespace_only_yields_nan(self):
        self.assertTrue(math.isnan(calculate_from_expression("   ", {"A": 1.0})))

    def test_newline_only_yields_nan(self):
        self.assertTrue(math.isnan(calculate_from_expression("\n\t", {"A": 1.0})))

    def test_expression_with_only_parentheses_yields_nan(self):
        self.assertTrue(math.isnan(calculate_from_expression("()", {"A": 1.0})))


if __name__ == "__main__":
    unittest.main()
