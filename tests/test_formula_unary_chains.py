#!/usr/bin/env python3
"""Tests for formula.calculate_from_expression nested unary operators.

Pins how chained unary operators (ast.UAdd / ast.USub) are folded: the AST
nests them, so '--A' is USub(USub(A)) and must evaluate to A, while '-+A'
must evaluate to -A. A refactor of the _SAFE_UNARYOPS branch could silently
change this, so the behaviour is pinned here at the public entry point.
"""

import math
import unittest

from formula import calculate_from_expression


class TestUnaryChains(unittest.TestCase):
    def test_double_negation_returns_original_value(self):
        self.assertEqual(calculate_from_expression("--A", {"A": 3.0}), 3.0)

    def test_negation_of_unary_plus_returns_negated_value(self):
        self.assertEqual(calculate_from_expression("-+A", {"A": 3.0}), -3.0)

    def test_unary_plus_of_negation_returns_negated_value(self):
        self.assertEqual(calculate_from_expression("+ -A", {"A": 3.0}), -3.0)

    def test_triple_negation_returns_negated_value(self):
        self.assertEqual(calculate_from_expression("---A", {"A": 3.0}), -3.0)

    def test_double_negation_inside_expression(self):
        self.assertEqual(calculate_from_expression("--A + B", {"A": 3.0, "B": 1.0}), 4.0)

    def test_double_negation_of_parenthesised_expression(self):
        self.assertEqual(calculate_from_expression("--(A + B)", {"A": 1.0, "B": 2.0}), 3.0)

    def test_double_negation_of_literal(self):
        self.assertEqual(calculate_from_expression("--5", {}), 5.0)

    def test_unary_chain_with_unsupported_operator_yields_nan(self):
        result = calculate_from_expression("--A % B", {"A": 4.0, "B": 3.0})
        self.assertTrue(math.isnan(result))

    def test_unary_chain_on_missing_variable_yields_nan(self):
        result = calculate_from_expression("--A", {})
        self.assertTrue(math.isnan(result))


if __name__ == "__main__":
    unittest.main()
