#!/usr/bin/env python3
"""Tests for formula.calculate_from_expression longest-first substitution.

The substitution loop sorts variable names by length descending and builds a
single regex alternation, so at any position the longest matching key wins.
These tests pin that behaviour for prefix keys and for keys that appear
mid-expression, using only the pure public function.
"""

import math
import unittest

from formula import calculate_from_expression


class TestPrefixKeys(unittest.TestCase):
    def test_longer_prefix_key_wins_at_start(self):
        # 'AB' must win over 'A' at position 0.
        self.assertEqual(
            calculate_from_expression("AB", {"A": 1.0, "AB": 5.0}), 5.0
        )

    def test_shorter_key_still_usable_alone(self):
        self.assertEqual(
            calculate_from_expression("A + 1", {"A": 1.0, "AB": 5.0}), 2.0
        )

    def test_longer_key_wins_mid_expression(self):
        # 'AB' appears after a space; 'A' must not consume the 'A' of 'AB'.
        self.assertEqual(
            calculate_from_expression("2 * AB", {"A": 1.0, "AB": 5.0}), 10.0
        )

    def test_both_keys_in_same_expression(self):
        self.assertEqual(
            calculate_from_expression(
                "AB - A", {"A": 1.0, "AB": 5.0}
            ),
            4.0,
        )

    def test_three_level_prefix_chain(self):
        # 'ABC' > 'AB' > 'A'; the longest must always win.
        self.assertEqual(
            calculate_from_expression(
                "ABC + AB + A", {"A": 1.0, "AB": 2.0, "ABC": 3.0}
            ),
            6.0,
        )

    def test_unknown_longer_token_yields_nan(self):
        # 'AX' is not a key, and 'A' must not partially substitute it.
        self.assertTrue(
            math.isnan(calculate_from_expression("AX", {"A": 1.0}))
        )

    def test_prefix_key_inside_parentheses(self):
        self.assertEqual(
            calculate_from_expression(
                "(AB + A) / A", {"A": 1.0, "AB": 5.0}
            ),
            6.0,
        )

    def test_negative_value_for_prefix_key(self):
        self.assertEqual(
            calculate_from_expression(
                "AB * 2", {"A": 1.0, "AB": -3.0}
            ),
            -6.0,
        )


if __name__ == "__main__":
    unittest.main()
