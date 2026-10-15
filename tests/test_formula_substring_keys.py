#!/usr/bin/env python3
"""Tests for formula.calculate_from_expression with overlapping variable names.

When the values dict contains a key that is a substring of another key
(e.g. 'A' and 'AB'), the substitution loop must replace the longer name
first so that 'AB' is not corrupted into '<value>A'. These tests pin that
longest-first ordering at the public entry point.
"""

import math
import unittest

from formula import calculate_from_expression


class TestSubstringKeys(unittest.TestCase):
    def test_longer_key_wins_over_substring(self):
        result = calculate_from_expression("AB", {"A": 1.0, "AB": 5.0})
        self.assertEqual(result, 5.0)

    def test_substring_key_still_usable_alone(self):
        result = calculate_from_expression("A + 1", {"A": 1.0, "AB": 5.0})
        self.assertEqual(result, 2.0)

    def test_both_keys_in_one_expression(self):
        result = calculate_from_expression("AB + A", {"A": 1.0, "AB": 5.0})
        self.assertEqual(result, 6.0)

    def test_three_levels_of_overlap(self):
        values = {"A": 1.0, "AB": 2.0, "ABC": 3.0}
        result = calculate_from_expression("ABC + AB + A", values)
        self.assertEqual(result, 6.0)

    def test_unknown_longer_key_yields_nan(self):
        result = calculate_from_expression("AB", {"A": 1.0})
        self.assertTrue(math.isnan(result))

    def test_repeated_longer_key(self):
        result = calculate_from_expression("AB * AB", {"A": 1.0, "AB": 3.0})
        self.assertEqual(result, 9.0)


if __name__ == "__main__":
    unittest.main()
