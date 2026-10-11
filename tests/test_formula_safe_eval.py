#!/usr/bin/env python3
"""Tests for the AST-based safe evaluator in formula.py.

These pin the rejection behaviour of _safe_eval_node: only numbers, variables,
basic arithmetic (+ - * / **) and unary +/- are allowed. Everything else must
raise ValueError so calculate_from_expression returns NaN instead of executing
arbitrary code.
"""

import ast
import math
import unittest

from formula import _safe_eval_node, calculate_from_expression


class TestSafeEvalNodeAllowed(unittest.TestCase):
    def _eval(self, expr, values=None):
        tree = ast.parse(expr, mode="eval")
        return _safe_eval_node(tree, values or {})

    def test_constant_int(self):
        self.assertEqual(self._eval("7"), 7.0)

    def test_constant_float(self):
        self.assertEqual(self._eval("2.5"), 2.5)

    def test_bool_constant_is_float(self):
        self.assertEqual(self._eval("True"), 1.0)

    def test_addition(self):
        self.assertEqual(self._eval("1 + 2"), 3.0)

    def test_subtraction(self):
        self.assertEqual(self._eval("5 - 2"), 3.0)

    def test_multiplication(self):
        self.assertEqual(self._eval("3 * 4"), 12.0)

    def test_division(self):
        self.assertEqual(self._eval("9 / 3"), 3.0)

    def test_power(self):
        self.assertEqual(self._eval("2 ** 3"), 8.0)

    def test_unary_plus(self):
        self.assertEqual(self._eval("+5"), 5.0)

    def test_unary_minus(self):
        self.assertEqual(self._eval("-5"), -5.0)

    def test_nested_parentheses(self):
        self.assertEqual(self._eval("((1 + 2) * (3 + 4))"), 21.0)


class TestSafeEvalNodeRejections(unittest.TestCase):
    def _eval(self, expr, values=None):
        tree = ast.parse(expr, mode="eval")
        return _safe_eval_node(tree, values or {})

    def test_string_constant_rejected(self):
        with self.assertRaises(ValueError):
            self._eval("'hello'")

    def test_bytes_constant_rejected(self):
        with self.assertRaises(ValueError):
            self._eval("b'hello'")

    def test_none_constant_rejected(self):
        with self.assertRaises(ValueError):
            self._eval("None")

    def test_complex_constant_rejected(self):
        with self.assertRaises(ValueError):
            self._eval("1j")

    def test_modulo_operator_rejected(self):
        with self.assertRaises(ValueError):
            self._eval("5 % 2")

    def test_floor_division_operator_rejected(self):
        with self.assertRaises(ValueError):
            self._eval("5 // 2")

    def test_bitwise_and_rejected(self):
        with self.assertRaises(ValueError):
            self._eval("5 & 2")

    def test_bitwise_or_rejected(self):
        with self.assertRaises(ValueError):
            self._eval("5 | 2")

    def test_left_shift_rejected(self):
        with self.assertRaises(ValueError):
            self._eval("5 << 2")

    def test_bitwise_invert_rejected(self):
        with self.assertRaises(ValueError):
            self._eval("~5")

    def test_boolean_not_rejected(self):
        with self.assertRaises(ValueError):
            self._eval("not 5")

    def test_function_call_rejected(self):
        with self.assertRaises(ValueError):
            self._eval("abs(-5)")

    def test_name_lookup_rejected(self):
        with self.assertRaises(ValueError):
            self._eval("foo")

    def test_comparison_rejected(self):
        with self.assertRaises(ValueError):
            self._eval("1 < 2")


class TestCalculateFromExpressionGuards(unittest.TestCase):
    def test_modulo_returns_nan(self):
        self.assertTrue(math.isnan(calculate_from_expression("5 % 2", {})))

    def test_floor_division_returns_nan(self):
        self.assertTrue(math.isnan(calculate_from_expression("5 // 2", {})))

    def test_bitwise_invert_returns_nan(self):
        self.assertTrue(math.isnan(calculate_from_expression("~5", {})))

    def test_string_literal_returns_nan(self):
        self.assertTrue(math.isnan(calculate_from_expression("'abc'", {})))

    def test_power_operator_is_allowed(self):
        self.assertEqual(calculate_from_expression("2 ** 3", {}), 8.0)

    def test_unary_minus_is_allowed(self):
        self.assertEqual(calculate_from_expression("-A", {"A": 4.0}), -4.0)


if __name__ == "__main__":
    unittest.main()
