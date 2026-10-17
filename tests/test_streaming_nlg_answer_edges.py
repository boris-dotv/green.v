#!/usr/bin/env python3
"""Tests for StreamingNLG.generate_answer formatting edge cases.

Pins the current verified behaviour of the pure generate_answer method for
degenerate function results (empty dict, None values, nested dicts, lists).
No network or heavy dependencies are used.
"""

import unittest

from enhanced_core.streaming_nlg import StreamingNLG


class TestGenerateAnswerEdges(unittest.TestCase):
    def setUp(self):
        self.nlg = StreamingNLG("http://example.invalid", "key")

    def test_empty_dict_returns_string(self):
        answer = self.nlg.generate_answer("query", {})
        self.assertIsInstance(answer, str)

    def test_none_value_does_not_raise(self):
        answer = self.nlg.generate_answer("query", {"company_name": None})
        self.assertIsInstance(answer, str)

    def test_nested_dict_does_not_raise(self):
        result = {"company_name": "ZA Bank", "meta": {"a": 1}}
        answer = self.nlg.generate_answer("query", result)
        self.assertIsInstance(answer, str)

    def test_list_value_does_not_raise(self):
        result = {"company_name": "ZA Bank", "tags": [1, 2, 3]}
        answer = self.nlg.generate_answer("query", result)
        self.assertIsInstance(answer, str)

    def test_plain_string_result(self):
        answer = self.nlg.generate_answer("query", "plain")
        self.assertIsInstance(answer, str)


if __name__ == "__main__":
    unittest.main()
