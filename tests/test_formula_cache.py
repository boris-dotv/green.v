#!/usr/bin/env python3
"""Tests for formula.get_financial_formulas caching and entry shape.

Pins the module-level cache contract: the first call builds the list, later
calls return the very same object, and every entry is a (name, expression)
2-tuple with non-empty parts. find_formula_for_query depends on this shape.
"""

import unittest

import formula
from formula import get_financial_formulas


class TestFormulaCache(unittest.TestCase):
    def setUp(self):
        # Reset the module cache so each test starts from a known state.
        formula._FORMULA_CACHE = None

    def tearDown(self):
        formula._FORMULA_CACHE = None

    def test_first_call_populates_cache(self):
        self.assertIsNone(formula._FORMULA_CACHE)
        formulas = get_financial_formulas()
        self.assertIsNotNone(formula._FORMULA_CACHE)
        self.assertIs(formulas, formula._FORMULA_CACHE)

    def test_second_call_returns_same_object(self):
        first = get_financial_formulas()
        second = get_financial_formulas()
        self.assertIs(first, second)

    def test_cached_result_is_reused_after_mutation(self):
        formulas = get_financial_formulas()
        formulas.append(("sentinel", "1"))
        self.assertIn(("sentinel", "1"), get_financial_formulas())

    def test_entries_are_two_tuples_of_non_empty_strings(self):
        formulas = get_financial_formulas()
        self.assertTrue(formulas)
        for entry in formulas:
            self.assertIsInstance(entry, tuple)
            self.assertEqual(len(entry), 2)
            name, expression = entry
            self.assertIsInstance(name, str)
            self.assertIsInstance(expression, str)
            self.assertTrue(name.strip())
            self.assertTrue(expression.strip())

    def test_known_formula_is_present(self):
        names = [name for name, _ in get_financial_formulas()]
        self.assertIn("debt_to_equity_ratio", names)
        self.assertIn("executive_director_ratio", names)

    def test_rebuild_after_cache_reset_is_equal(self):
        first = list(get_financial_formulas())
        formula._FORMULA_CACHE = None
        second = list(get_financial_formulas())
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
