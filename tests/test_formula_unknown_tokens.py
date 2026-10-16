#!/usr/bin/env python3
"""Tests for formula.calculate_from_expression with unknown longer tokens.

The substitution loop replaces only exact variable names, so a shorter key
that is a prefix of an unknown longer token must not partially substitute it.
These tests pin that behaviour using only the pure public function.
"""

import math
import unittest

from formula import calculate_from_expression


class TestUnknownLongerTokens(unittest.TestCase):
    def test_unknown_longer_token_yields_nan(self):
        # 'AX' is not a key; 'A' must not partially substitute it.
        self.assertTrue(
            math.isnan(calculate_from_expression("AX", {"A": 1.0}))
        )

    def test_known_key_embedded_in_unknown_token_yields_nan(self):
        # 'B' is known but 'XB' is not; 'B' must not be substituted inside it.
        self.assertTrue(
            math.isnan(calculate_from_expression("XB", {"B": 2.0}))
        )

    def test_unknown_token_mid_expression_yields_nan(self):
        self.assertTrue(
            math.isnan(
                calculate_from_expression("1 + AX", {"A": 1.0})
            )
        )

    def test_known_key_alone_still_evaluates(self):
        self.assertEqual(
            calculate_from_expression("A * 3", {"A": 1.0}), 3.0
        )

    def test_known_key_next_to_unknown_token_yields_nan(self):
        # 'A' alone is fine, but 'AX' is unknown, so the whole expression fails.
        self.assertTrue(
            math.isnan(
                calculate_from_expression("A + AX", {"A": 1.0})
            )
        )

    def test_empty_values_with_letters_yields_nan(self):
        self.assertTrue(
            math.isnan(calculate_from_expression("A + B", {}))
        )

    def test_unknown_token_inside_parentheses_yields_nan(self):
        self.assertTrue(
            math.isnan(
                calculate_from_expression("(AX + 1)", {"A": 1.0})
            )
        )


if __name__ == "__main__":
    unittest.main()
