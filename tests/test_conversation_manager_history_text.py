#!/usr/bin/env python3
"""Tests for ConversationManager.get_history_text.

get_history_text formats the most recent turns as 'User: ...' lines with an
optional 'Assistant: ...' line, joined by newlines. Note that it slices with
list(self.history)[-n_turns:], so n_turns=0 returns the whole history rather
than an empty string. These tests pin that observable behaviour.
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from enhanced_core.conversation_manager import ConversationManager  # noqa: E402


class TestGetHistoryText(unittest.TestCase):
    def test_empty_history_returns_empty_string(self):
        cm = ConversationManager()
        self.assertEqual(cm.get_history_text(), "")

    def test_single_turn_with_assistant(self):
        cm = ConversationManager()
        cm.add_turn("How many employees?", "100 employees")
        self.assertEqual(
            cm.get_history_text(),
            "User: How many employees?\nAssistant: 100 employees",
        )

    def test_empty_assistant_line_is_omitted(self):
        cm = ConversationManager()
        cm.add_turn("How many employees?", "")
        self.assertEqual(cm.get_history_text(), "User: How many employees?")

    def test_multiple_turns_joined_by_newline(self):
        cm = ConversationManager()
        cm.add_turn("q1", "a1")
        cm.add_turn("q2", "a2")
        self.assertEqual(
            cm.get_history_text(),
            "User: q1\nAssistant: a1\nUser: q2\nAssistant: a2",
        )

    def test_n_turns_limits_to_most_recent(self):
        cm = ConversationManager()
        cm.add_turn("q1", "a1")
        cm.add_turn("q2", "a2")
        cm.add_turn("q3", "a3")
        self.assertEqual(
            cm.get_history_text(n_turns=2),
            "User: q2\nAssistant: a2\nUser: q3\nAssistant: a3",
        )

    def test_n_turns_zero_returns_full_history(self):
        cm = ConversationManager()
        cm.add_turn("q1", "a1")
        cm.add_turn("q2", "a2")
        self.assertEqual(
            cm.get_history_text(n_turns=0),
            "User: q1\nAssistant: a1\nUser: q2\nAssistant: a2",
        )

    def test_n_turns_larger_than_history(self):
        cm = ConversationManager()
        cm.add_turn("q1", "a1")
        self.assertEqual(
            cm.get_history_text(n_turns=99),
            "User: q1\nAssistant: a1",
        )

    def test_clear_empties_history_text(self):
        cm = ConversationManager()
        cm.add_turn("q1", "a1")
        cm.clear()
        self.assertEqual(cm.get_history_text(), "")


if __name__ == "__main__":
    unittest.main()
