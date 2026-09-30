#!/usr/bin/env python3
"""Tests for the RejectionDetector prompt template contract.

These pin the observable prompt built in RejectionDetector.should_accept:
- the ACCEPT/REJECT scope keyword lists are present,
- the query is interpolated exactly once and verbatim,
- the decision instruction and trailing 'Decision:' marker are present,
- llm_caller is invoked with temperature=0.1.
"""

import logging
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from enhanced_core.rejection_detector import RejectionDetector  # noqa: E402


class RecordingLLM:
    """Fake llm_caller that records prompts and returns a fixed reply."""

    def __init__(self, reply="1"):
        self.reply = reply
        self.calls = []

    def __call__(self, prompt, temperature=0.1):
        self.calls.append({"prompt": prompt, "temperature": temperature})
        return self.reply


class TestPromptTemplate(unittest.TestCase):
    def setUp(self):
        logging.disable(logging.CRITICAL)

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def _prompt_for(self, query):
        llm = RecordingLLM()
        RejectionDetector(llm).should_accept(query)
        self.assertEqual(len(llm.calls), 1)
        return llm.calls[0]

    def test_temperature_is_point_one(self):
        call = self._prompt_for("What is the employee count of ZA Bank?")
        self.assertEqual(call["temperature"], 0.1)

    def test_accept_scope_keywords_present(self):
        prompt = self._prompt_for("hello")["prompt"]
        for keyword in (
            "ACCEPT these types of queries",
            "companies",
            "management",
            "shareholders",
            "employees",
            "Financial metrics and ratios",
            "Data comparisons and analysis",
            "Formula calculations",
            "Related follow-up questions",
            "Greetings",
            "Thank you messages",
            "Goodbye messages",
        ):
            self.assertIn(keyword, prompt)

    def test_reject_scope_keywords_present(self):
        prompt = self._prompt_for("hello")["prompt"]
        for keyword in (
            "REJECT these types of queries",
            "Unrelated topics",
            "Nonsense or gibberish",
            "Offensive content",
        ):
            self.assertIn(keyword, prompt)

    def test_output_instruction_present(self):
        prompt = self._prompt_for("hello")["prompt"]
        self.assertIn("Output ONLY: 1 (accept) or 0 (reject)", prompt)
        self.assertTrue(prompt.rstrip().endswith("Decision:"))

    def test_query_interpolated_verbatim(self):
        query = "Compare {shareholder} concentration\nbetween ZA Bank and WeLab Bank"
        prompt = self._prompt_for(query)["prompt"]
        self.assertIn(f"Query: {query}", prompt)

    def test_query_appears_exactly_once(self):
        query = "unique-marker-query-12345"
        prompt = self._prompt_for(query)["prompt"]
        self.assertEqual(prompt.count(query), 1)

    def test_empty_query_still_builds_prompt(self):
        prompt = self._prompt_for("")["prompt"]
        self.assertIn("Query: ", prompt)
        self.assertTrue(prompt.rstrip().endswith("Decision:"))


if __name__ == "__main__":
    unittest.main()
