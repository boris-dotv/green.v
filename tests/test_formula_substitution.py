#!/usr/bin/env python3
"""Tests for variable substitution in formula.calculate_from_expression.

Pins the rules that make substitution safe and predictable:
- longest variable name wins (no partial replacement of prefixes)
- word boundaries prevent replacing substrings inside identifiers
- leftover variable-like tokens yield NaN
- division by zero yields NaN
- unsupported operators yield NaN
"""

import math
import unittest

from formula import calculate_from_expression


class TestSubstitutionOrdering(unittest.TestCase):
    def test_longest_key_replaced_first(self):
        # "A" must not clobber the prefix of "AB".
        result = calculate_from_expression("AB + A", {"A": 1.0, "AB": 10.0})
        self.assertEqual(result, 11.0)

    def test_three_keys_with_shared_prefix(self):
        result = calculate_from_expression(
            "ABC - AB - A", {"A": 1.0, "AB": 2.0, "ABC": 5.0}
        )
        self.assertEqual(result, 2.0)

    def test_word_boundary_avoids_substring_replacement(self):
        # "A" appears inside "TOTAL" but must not be substituted there.
        result = calculate_from_expression("TOTAL / A", {"A": 2.0, "TOTAL": 8.0})
        self.assertEqual(result, 4.0)


class TestSubstitutionGuards(unittest.TestCase):
    def test_leftover_variable_token_returns_nan(self):
        # "B" is not provided, so the expression still contains a letter.
        self.assertTrue(math.isnan(calculate_from_expression("A + B", {"A": 1.0})))

    def test_division_by_zero_literal_returns_nan(self):
        self.assertTrue(math.isnan(calculate_from_expression("A / 0", {"A": 1.0})))

    def test_division_by_zero_variable_returns_nan(self):
        self.assertTrue(math.isnan(calculate_from_expression("A / B", {"A": 1.0, "B": 0.0})))

    def test_empty_values_with_letters_returns_nan(self):
        self.assertTrue(math.isnan(calculate_from_expression("A + 1", {})))

    def test_pure_numeric_expression_ignores_values(self):
        self.assertEqual(calculate_from_expression("2 + 3", {"A": 99.0}), 5.0)

    def test_unsupported_operator_returns_nan(self):
        self.assertTrue(math.isnan(calculate_from_expression("A % B", {"A": 5.0, "B": 2.0})))

    def test_values_dict_is_not_mutated(self):
        values = {"A": 1.0, "B": 2.0}
        calculate_from_expression("A + B", values)
        self.assertEqual(values, {"A": 1.0, "B": 2.0})


if __name__ == "__main__":
    unittest.main()
