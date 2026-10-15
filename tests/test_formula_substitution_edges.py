#!/usr/bin/env python3
"""Edge-case tests for formula.calculate_from_expression substitution.

These pin the single-pass longest-first substitution introduced to fix
corruption of longer variable names by shorter keys, and cover keys that
contain regex metacharacters or that overlap with unknown tokens.
"""

import math
import unittest

from formula import calculate_from_expression


class TestSubstitutionEdges(unittest.TestCase):
    def test_key_with_regex_metacharacters(self):
        # A key containing a regex metacharacter must be escaped so it is
        # matched literally, not as a pattern.
        result = calculate_from_expression("A+B", {"A+B": 7.0})
        self.assertEqual(result, 7.0)

    def test_key_with_dot_is_literal(self):
        result = calculate_from_expression("A.B", {"A.B": 3.0})
        self.assertEqual(result, 3.0)

    def test_unknown_token_containing_known_key_yields_nan(self):
        # 'AB' is not a key, but 'A' is; the leftover 'B' must be detected as
        # a variable-like token and produce NaN rather than a wrong number.
        result = calculate_from_expression("AB", {"A": 1.0})
        self.assertTrue(math.isnan(result))

    def test_known_key_used_twice(self):
        result = calculate_from_expression("A + A * A", {"A": 2.0})
        self.assertEqual(result, 6.0)

    def test_empty_values_dict_leaves_expression_alone(self):
        # With no values, a bare variable name stays and must yield NaN.
        result = calculate_from_expression("A + 1", {})
        self.assertTrue(math.isnan(result))

    def test_numeric_only_expression_with_values(self):
        # Values present but expression has no variables: still evaluates.
        result = calculate_from_expression("2 + 3", {"A": 1.0})
        self.assertEqual(result, 5.0)

    def test_longest_key_wins_at_each_position(self):
        values = {"X": 1.0, "XY": 2.0, "XYZ": 4.0}
        result = calculate_from_expression("XYZ + XY + X", values)
        self.assertEqual(result, 7.0)


if __name__ == "__main__":
    unittest.main()
