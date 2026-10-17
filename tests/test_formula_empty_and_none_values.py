#!/usr/bin/env python3
"""Tests for formula.calculate_from_expression degenerate value inputs.

Covers the empty values dict (no substitution regex is built), None values
(str(None) -> 'None' leaves letters -> NaN), and zero values (division-by-zero
pre-check). Uses only the pure public function.
"""

import math
import unittest

from formula import calculate_from_expression


class TestEmptyValues(unittest.TestCase):
    def test_empty_values_pure_arithmetic(self):
        self.assertEqual(calculate_from_expression("1 + 2 * 3", {}), 7.0)

    def test_empty_values_with_variable_returns_nan(self):
        result = calculate_from_expression("A / B", {})
        self.assertTrue(math.isnan(result))

    def test_empty_values_parentheses(self):
        self.assertEqual(calculate_from_expression("(4 + 6) / 2", {}), 5.0)


class TestNoneValues(unittest.TestCase):
    def test_none_value_yields_nan(self):
        # str(None) == 'None' leaves letters behind -> NaN
        result = calculate_from_expression("A / B", {"A": None, "B": 2.0})
        self.assertTrue(math.isnan(result))

    def test_none_value_alone_yields_nan(self):
        result = calculate_from_expression("A", {"A": None})
        self.assertTrue(math.isnan(result))


class TestZeroValues(unittest.TestCase):
    def test_zero_numerator_ok(self):
        self.assertEqual(calculate_from_expression("A / B", {"A": 0, "B": 4.0}), 0.0)

    def test_zero_denominator_yields_nan(self):
        result = calculate_from_expression("A / B", {"A": 5.0, "B": 0})
        self.assertTrue(math.isnan(result))

    def test_zero_literal_denominator_yields_nan(self):
        result = calculate_from_expression("A / 0", {"A": 5.0})
        self.assertTrue(math.isnan(result))


if __name__ == "__main__":
    unittest.main()
