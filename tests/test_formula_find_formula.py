#!/usr/bin/env python3
"""Tests for formula.find_formula_for_query matching behaviour.

Pins the normalisation rules (lowercase, spaces and hyphens become
underscores), the (name, expression, variables) return contract, and the
(None, None, None) miss case. Also verifies that the returned expression is
actually consumable by calculate_from_expression.
"""

import unittest

from formula import calculate_from_expression, find_formula_for_query, get_financial_formulas


class TestFindFormulaMatches(unittest.TestCase):
    def test_exact_name_matches(self):
        name, expr, variables = find_formula_for_query("executive_director_ratio")
        self.assertEqual(name, "executive_director_ratio")
        self.assertIsNotNone(expr)
        self.assertIsInstance(variables, list)

    def test_uppercase_query_matches(self):
        name, _, _ = find_formula_for_query("EXECUTIVE_DIRECTOR_RATIO")
        self.assertEqual(name, "executive_director_ratio")

    def test_spaces_are_normalised_to_underscores(self):
        name, _, _ = find_formula_for_query("executive director ratio")
        self.assertEqual(name, "executive_director_ratio")

    def test_hyphens_are_normalised_to_underscores(self):
        name, _, _ = find_formula_for_query("executive-director-ratio")
        self.assertEqual(name, "executive_director_ratio")

    def test_name_embedded_in_sentence_matches(self):
        name, _, _ = find_formula_for_query(
            "can you get me the executive_director_ratio for a company?"
        )
        self.assertEqual(name, "executive_director_ratio")

    def test_unknown_query_returns_none_triple(self):
        self.assertEqual(
            find_formula_for_query("what is the weather today"), (None, None, None)
        )

    def test_empty_query_returns_none_triple(self):
        self.assertEqual(find_formula_for_query(""), (None, None, None))


class TestFindFormulaContract(unittest.TestCase):
    def test_returned_expression_is_in_formula_list(self):
        name, expr, _ = find_formula_for_query("debt_to_equity_ratio")
        self.assertIn((name, expr), get_financial_formulas())

    def test_variables_are_non_empty_strings(self):
        _, _, variables = find_formula_for_query("debt_to_equity_ratio")
        self.assertTrue(variables)
        for var in variables:
            self.assertIsInstance(var, str)
            self.assertTrue(var.strip())

    def test_variables_do_not_contain_operators(self):
        _, _, variables = find_formula_for_query("debt_to_equity_ratio")
        for var in variables:
            self.assertFalse(any(ch in var for ch in "()*/+-"))

    def test_expression_is_calculable_with_matching_values(self):
        _, expr, variables = find_formula_for_query("debt_to_equity_ratio")
        values = {var: 2.0 for var in variables}
        self.assertEqual(calculate_from_expression(expr, values), 1.0)


if __name__ == "__main__":
    unittest.main()
