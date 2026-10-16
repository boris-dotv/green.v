#!/usr/bin/env python3
"""Tests for formula.calculate_from_expression error paths.

Covers the explicit division-by-zero pre-check, the ZeroDivisionError
catch, and the OverflowError catch for huge exponents. All of these must
return NaN rather than raising, because callers treat NaN as 'no result'.
"""

import math
import unittest

from formula import calculate_from_expression


class TestDivisionByZero(unittest.TestCase):
    def test_literal_zero_divisor_yields_nan(self):
        self.assertTrue(math.isnan(calculate_from_expression("A / 0", {"A": 1.0})))

    def test_literal_zero_point_zero_divisor_yields_nan(self):
        self.assertTrue(
            math.isnan(calculate_from_expression("A / 0.0", {"A": 1.0}))
        )

    def test_zero_divisor_with_spaces_yields_nan(self):
        self.assertTrue(
            math.isnan(calculate_from_expression("A /   0", {"A": 1.0}))
        )

    def test_variable_divisor_that_is_zero_yields_nan(self):
        # The regex pre-check only catches literal zeros, so this exercises
        # the ZeroDivisionError branch instead.
        self.assertTrue(math.isnan(calculate_from_expression("A / B", {"A": 1.0, "B": 0.0})))

    def test_nonzero_divisor_evaluates(self):
        self.assertEqual(calculate_from_expression("A / 4", {"A": 10.0}), 2.5)

    def test_zero_numerator_is_fine(self):
        self.assertEqual(calculate_from_expression("0 / A", {"A": 4.0}), 0.0)


class TestOverflow(unittest.TestCase):
    def test_huge_exponent_yields_nan(self):
        # float ** int raises OverflowError, which is caught and mapped to NaN.
        self.assertTrue(
            math.isnan(calculate_from_expression("A ** 10000", {"A": 10.0}))
        )

    def test_moderate_exponent_evaluates(self):
        self.assertEqual(calculate_from_expression("A ** 3", {"A": 2.0}), 8.0)


if __name__ == "__main__":
    unittest.main()
