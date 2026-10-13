#!/usr/bin/env python3
"""Tests for formula.calculate_from_expression operator support.

Pins which binary operators the public entry point accepts: only the ones in
_SAFE_BINOPS (+, -, *, /, **) may produce a number, everything else must fall
through to the ValueError branch and return NaN. This guards the AST security
boundary against a future widening of _SAFE_BINOPS.
"""

import math
import unittest

from formula import calculate_from_expression


class TestSupportedOperators(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(calculate_from_expression("A + B", {"A": 1.0, "B": 2.0}), 3.0)

    def test_subtraction(self):
        self.assertEqual(calculate_from_expression("A - B", {"A": 5.0, "B": 2.0}), 3.0)

    def test_multiplication(self):
        self.assertEqual(calculate_from_expression("A * B", {"A": 3.0, "B": 4.0}), 12.0)

    def test_division(self):
        self.assertEqual(calculate_from_expression("A / B", {"A": 9.0, "B": 3.0}), 3.0)

    def test_power_is_supported(self):
        # ast.Pow is in _SAFE_BINOPS, so '**' evaluates normally.
        self.assertEqual(calculate_from_expression("A ** B", {"A": 2.0, "B": 3.0}), 8.0)

    def test_unary_plus_is_supported(self):
        self.assertEqual(calculate_from_expression("+A + B", {"A": 1.0, "B": 2.0}), 3.0)


class TestUnsupportedOperators(unittest.TestCase):
    def _assert_nan(self, expression, values):
        result = calculate_from_expression(expression, values)
        self.assertTrue(math.isnan(result), f"expected NaN for {expression!r}, got {result!r}")

    def test_modulo_yields_nan(self):
        self._assert_nan("A % B", {"A": 7.0, "B": 3.0})

    def test_floor_division_yields_nan(self):
        self._assert_nan("A // B", {"A": 7.0, "B": 3.0})

    def test_bitwise_and_yields_nan(self):
        self._assert_nan("A & B", {"A": 6.0, "B": 3.0})

    def test_bitwise_or_yields_nan(self):
        self._assert_nan("A | B", {"A": 6.0, "B": 3.0})

    def test_bitwise_xor_yields_nan(self):
        self._assert_nan("A ^ B", {"A": 6.0, "B": 3.0})

    def test_left_shift_yields_nan(self):
        self._assert_nan("A << B", {"A": 1.0, "B": 2.0})

    def test_right_shift_yields_nan(self):
        self._assert_nan("A >> B", {"A": 8.0, "B": 2.0})

    def test_bitwise_invert_yields_nan(self):
        # ast.Invert is not in _SAFE_UNARYOPS.
        self._assert_nan("~A", {"A": 1.0})

    def test_boolean_not_yields_nan(self):
        # ast.Not is not in _SAFE_UNARYOPS.
        self._assert_nan("not A", {"A": 1.0})


if __name__ == "__main__":
    unittest.main()
