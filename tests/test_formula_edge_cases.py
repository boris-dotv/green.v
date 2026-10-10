#!/usr/bin/env python3
"""Edge-case tests for formula.calculate_from_expression and find_formula_for_query."""

import math
import unittest

from formula import (
    calculate_from_expression,
    find_formula_for_query,
    get_financial_formulas,
)


class TestCalculateFromExpression(unittest.TestCase):
    def test_simple_arithmetic(self):
        self.assertEqual(calculate_from_expression("2 + 3 * 4", {}), 14.0)

    def test_parentheses(self):
        self.assertEqual(calculate_from_expression("(2 + 3) * 4", {}), 20.0)

    def test_variable_substitution(self):
        result = calculate_from_expression("A / B", {"A": 10.0, "B": 4.0})
        self.assertEqual(result, 2.5)

    def test_longest_variable_name_wins(self):
        # "AB" must not be partially replaced by "A"
        result = calculate_from_expression("AB / A", {"A": 2.0, "AB": 8.0})
        self.assertEqual(result, 4.0)

    def test_word_boundary_prevents_substring_replacement(self):
        # "A" must not be substituted inside "ABC" when only "A" is provided
        result = calculate_from_expression("ABC", {"A": 5.0})
        self.assertTrue(math.isnan(result))

    def test_unknown_variable_returns_nan(self):
        result = calculate_from_expression("A + B", {"A": 1.0})
        self.assertTrue(math.isnan(result))

    def test_division_by_zero_literal_returns_nan(self):
        result = calculate_from_expression("10 / 0", {})
        self.assertTrue(math.isnan(result))

    def test_division_by_zero_variable_returns_nan(self):
        result = calculate_from_expression("A / B", {"A": 10.0, "B": 0.0})
        self.assertTrue(math.isnan(result))

    def test_negative_numbers(self):
        result = calculate_from_expression("-A + 5", {"A": 3.0})
        self.assertEqual(result, 2.0)

    def test_function_call_is_rejected(self):
        result = calculate_from_expression("__import__('os')", {})
        self.assertTrue(math.isnan(result))

    def test_values_dict_not_mutated(self):
        values = {"A": 1.0, "B": 2.0}
        calculate_from_expression("A + B", values)
        self.assertEqual(values, {"A": 1.0, "B": 2.0})

    def test_empty_expression_returns_nan(self):
        result = calculate_from_expression("", {})
        self.assertTrue(math.isnan(result))


class TestFindFormulaForQuery(unittest.TestCase):
    def test_known_formula_found(self):
        name, expr, variables = find_formula_for_query("executive_director_ratio")
        self.assertEqual(name, "executive_director_ratio")
        self.assertIsNotNone(expr)
        self.assertIn("Count of Executive Directors", variables)

    def test_unknown_formula_returns_none_tuple(self):
        self.assertEqual(
            find_formula_for_query("totally_unknown_metric_xyz"),
            (None, None, None),
        )

    def test_query_normalisation_handles_spaces_and_dashes(self):
        name, _, _ = find_formula_for_query("executive director ratio")
        self.assertEqual(name, "executive_director_ratio")


class TestGetFinancialFormulas(unittest.TestCase):
    def test_cache_returns_same_object(self):
        self.assertIs(get_financial_formulas(), get_financial_formulas())

    def test_every_entry_is_name_expression_pair(self):
        for name, expression in get_financial_formulas():
            self.assertIsInstance(name, str)
            self.assertIsInstance(expression, str)
            self.assertTrue(name)
            self.assertTrue(expression)


if __name__ == "__main__":
    unittest.main()
