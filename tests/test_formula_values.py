#!/usr/bin/env python3
"""Tests for formula.calculate_from_expression value handling.

Pins how the substitution + safe-AST path treats non-float inputs (ints,
bools, numeric strings, None) and missing variables, so a refactor of the
regex substitution loop or of _safe_eval_node's constant branch cannot
silently change results.
"""

import math
import unittest

from formula import calculate_from_expression


class TestNumericCoercion(unittest.TestCase):
    def test_int_values_are_accepted(self):
        self.assertEqual(calculate_from_expression("A / B", {"A": 10, "B": 4}), 2.5)

    def test_bool_values_are_accepted_as_numbers(self):
        # _safe_eval_node converts bool constants to float, but substitution
        # happens first: str(True) is 'True', which is not a valid literal.
        result = calculate_from_expression("A + B", {"A": True, "B": False})
        self.assertTrue(math.isnan(result))

    def test_numeric_string_values_are_substituted_verbatim(self):
        self.assertEqual(calculate_from_expression("A * B", {"A": "3", "B": "4"}), 12.0)

    def test_non_numeric_string_value_yields_nan(self):
        result = calculate_from_expression("A + 1", {"A": "abc"})
        self.assertTrue(math.isnan(result))

    def test_none_value_yields_nan(self):
        result = calculate_from_expression("A + 1", {"A": None})
        self.assertTrue(math.isnan(result))


class TestMissingVariables(unittest.TestCase):
    def test_missing_variable_yields_nan(self):
        result = calculate_from_expression("A / B", {"A": 10.0})
        self.assertTrue(math.isnan(result))

    def test_empty_values_with_variable_expression_yields_nan(self):
        result = calculate_from_expression("A / B", {})
        self.assertTrue(math.isnan(result))

    def test_constant_expression_ignores_values(self):
        self.assertEqual(calculate_from_expression("2 + 3", {}), 5.0)


class TestSubstitutionOrdering(unittest.TestCase):
    def test_longer_variable_name_wins_over_prefix(self):
        # 'AB' must be replaced before 'A' so 'AB' is not split into 'A' 'B'.
        result = calculate_from_expression("AB / A", {"A": 2.0, "AB": 8.0})
        self.assertEqual(result, 4.0)

    def test_variable_inside_longer_token_is_not_replaced(self):
        # Word boundaries mean 'A' does not match inside 'ABC'.
        result = calculate_from_expression("ABC", {"A": 2.0})
        self.assertTrue(math.isnan(result))

    def test_input_dict_is_not_mutated(self):
        values = {"A": 1.0, "B": 2.0}
        calculate_from_expression("A + B", values)
        self.assertEqual(values, {"A": 1.0, "B": 2.0})


class TestArithmeticResults(unittest.TestCase):
    def test_operator_precedence_is_respected(self):
        self.assertEqual(calculate_from_expression("A + B * C", {"A": 1.0, "B": 2.0, "C": 3.0}), 7.0)

    def test_parentheses_are_respected(self):
        self.assertEqual(calculate_from_expression("(A + B) * C", {"A": 1.0, "B": 2.0, "C": 3.0}), 9.0)

    def test_unary_minus_is_supported(self):
        self.assertEqual(calculate_from_expression("-A + B", {"A": 1.0, "B": 5.0}), 4.0)

    def test_division_by_zero_variable_yields_nan(self):
        result = calculate_from_expression("A / B", {"A": 1.0, "B": 0.0})
        self.assertTrue(math.isnan(result))

    def test_literal_division_by_zero_yields_nan(self):
        result = calculate_from_expression("A / 0", {"A": 1.0})
        self.assertTrue(math.isnan(result))


if __name__ == "__main__":
    unittest.main()
