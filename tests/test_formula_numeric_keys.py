#!/usr/bin/env python3
"""Tests for formula.calculate_from_expression with numeric-looking keys.

The substitution loop builds a single regex alternation over the variable
names, so a key that looks like a number (e.g. '1' or '2.5') is substituted
just like any other key. These tests pin that behaviour using only the pure
public function.
"""

import math
import unittest

from formula import calculate_from_expression


class TestNumericLookingKeys(unittest.TestCase):
    def test_integer_like_key_substitutes(self):
        # '1' is a key, so it must be replaced by its value.
        self.assertEqual(
            calculate_from_expression("1 + 1", {"1": 10.0}), 20.0
        )

    def test_float_like_key_substitutes(self):
        self.assertEqual(
            calculate_from_expression("2.5 * 2", {"2.5": 4.0}), 8.0
        )

    def test_numeric_key_alone(self):
        self.assertEqual(calculate_from_expression("1", {"1": 7.0}), 7.0)

    def test_numeric_key_does_not_touch_other_literals(self):
        # Only '1' is a key; the literal '2' must stay a literal.
        self.assertEqual(
            calculate_from_expression("1 + 2", {"1": 5.0}), 7.0
        )

    def test_numeric_key_with_letters_yields_nan(self):
        # '1A' is not a key and '1' must not partially substitute it.
        self.assertTrue(
            math.isnan(calculate_from_expression("1A", {"1": 3.0}))
        )

    def test_numeric_key_inside_parentheses(self):
        self.assertEqual(
            calculate_from_expression("(1 + 1) * 2", {"1": 3.0}), 12.0
        )

    def test_numeric_key_negative_value(self):
        self.assertEqual(
            calculate_from_expression("1 * 3", {"1": -2.0}), -6.0
        )

    def test_numeric_key_absent_yields_nan(self):
        # No keys at all, so the bare literal expression still evaluates.
        self.assertEqual(calculate_from_expression("1 + 2", {}), 3.0)


if __name__ == "__main__":
    unittest.main()
