#!/usr/bin/env python3
"""Tests for QueryArbitrator history interpolation in the prompt.

_build_arbitration_prompt interpolates history verbatim into the
'Context:' line and falls back to 'No history' only when history is
falsy. These tests pin that observable contract (multi-line history is
preserved, braces are not treated as format fields, empty string and
None both fall back) so a future refactor of the f-string cannot
silently drop or mangle conversation context.
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from enhanced_core.arbitrator import QueryArbitrator  # noqa: E402


class RecordingLLM:
    """Fake llm_caller that records calls and returns a fixed reply."""

    def __init__(self, reply="A"):
        self.reply = reply
        self.calls = []

    def __call__(self, prompt, temperature=0.1):
        self.calls.append({"prompt": prompt, "temperature": temperature})
        return self.reply


def _prompt_for(history):
    llm = RecordingLLM()
    QueryArbitrator(llm).arbitrate("q", history=history)
    assert len(llm.calls) == 1
    return llm.calls[0]["prompt"]


class TestHistoryInterpolation(unittest.TestCase):
    def test_default_history_used_when_omitted(self):
        llm = RecordingLLM()
        QueryArbitrator(llm).arbitrate("q")
        self.assertIn("No history", llm.calls[0]["prompt"])

    def test_empty_string_history_falls_back_to_default(self):
        prompt = _prompt_for("")
        self.assertIn("No history", prompt)

    def test_none_history_falls_back_to_default(self):
        prompt = _prompt_for(None)
        self.assertIn("No history", prompt)

    def test_single_line_history_is_interpolated(self):
        prompt = _prompt_for("user: hi")
        self.assertIn("user: hi", prompt)
        self.assertNotIn("No history", prompt)

    def test_multi_line_history_is_preserved(self):
        history = "user: hi\nassistant: hello\nuser: how many?"
        prompt = _prompt_for(history)
        self.assertIn(history, prompt)

    def test_history_with_braces_is_not_reformatted(self):
        history = "prior {turn} with {braces}"
        prompt = _prompt_for(history)
        self.assertIn("prior {turn} with {braces}", prompt)

    def test_query_is_still_interpolated_alongside_history(self):
        llm = RecordingLLM()
        QueryArbitrator(llm).arbitrate("unique-marker-query", history="prior-turn")
        prompt = llm.calls[0]["prompt"]
        self.assertIn("unique-marker-query", prompt)
        self.assertIn("prior-turn", prompt)


if __name__ == "__main__":
    unittest.main()
