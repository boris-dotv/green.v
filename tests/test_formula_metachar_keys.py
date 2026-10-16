#!/usr/bin/env python3
"""Tests for formula.calculate_from_expression with regex-metacharacter keys.

The substitution loop builds a regex from the variable names via re.escape,
so keys containing '.', '+', '(', ')' or '*' must be treated literally and
must not be interpreted as regex syntax. These tests pin that behaviour.
"""

import math
import unittest

from formula import calculate_from_expression


class TestMetacharacterKeys(unittest.TestCase):
    def test_dot_in_key_is_literal(self):
        # 'A.B' must match literally, not as 'A<any>B'.
        self.assertEqual(
            calculate_from_expression("A.B / 2", {"A.B": 10.0}), 5.0
        )

    def test_dot_key_does_not_match_other_char(self):
        # 'AXB' should not be substituted by the key 'A.B'.
        self.assertTrue(
            math.isnan(calculate_from_expression("AXB", {"A.B": 10.0}))
        )

    def test_plus_in_key_is_literal(self):
        self.assertEqual(
            calculate_from_expression("A+B * 3", {"A+B": 2.0}), 6.0
        )

    def test_parentheses_in_key_are_literal(self):
        self.assertEqual(
            calculate_from_expression("(A) * 4", {"(A)": 3.0}), 12.0
        )

    def test_star_in_key_is_literal(self):
        self.assertEqual(
            calculate_from_expression("A*B + 1", {"A*B": 4.0}), 5.0
        )

    def test_longest_metachar_key_wins(self):
        # 'A.B' is longer than 'A', so it must win at position 0.
        self.assertEqual(
            calculate_from_expression("A.B", {"A": 1.0, "A.B": 7.0}), 7.0
        )

    def test_metachar_key_inside_larger_expression(self):
        self.assertEqual(
            calculate_from_expression(
                "(A.B - C) / C", {"A.B": 100.0, "C": 80.0}
            ),
            0.25,
        )


if __name__ == "__main__":
    unittest.main()
