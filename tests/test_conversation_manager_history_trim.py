#!/usr/bin/env python3
"""Tests for ConversationManager history trimming.

history is a deque(maxlen=max_history), so appending more turns than
the cap silently drops the oldest ones while context keeps tracking the
newest turn. These tests pin that observable contract so a future
refactor to a plain list cannot silently grow memory or change the
output of get_history_text.
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from enhanced_core.conversation_manager import ConversationManager  # noqa: E402


class TestHistoryTrimming(unittest.TestCase):
    def test_history_is_capped_at_max_history(self):
        cm = ConversationManager(max_history=3)
        for i in range(5):
            cm.add_turn(f"q{i}", f"a{i}")
        self.assertEqual(len(cm.history), 3)

    def test_oldest_turns_are_dropped(self):
        cm = ConversationManager(max_history=3)
        for i in range(5):
            cm.add_turn(f"q{i}", f"a{i}")
        users = [turn.user for turn in cm.history]
        self.assertEqual(users, ["q2", "q3", "q4"])

    def test_get_history_text_reflects_trimmed_window(self):
        cm = ConversationManager(max_history=2)
        for i in range(4):
            cm.add_turn(f"q{i}", f"a{i}")
        text = cm.get_history_text(n_turns=10)
        self.assertNotIn("q0", text)
        self.assertNotIn("q1", text)
        self.assertIn("q2", text)
        self.assertIn("q3", text)

    def test_context_tracks_latest_turn_after_trimming(self):
        cm = ConversationManager(max_history=2)
        cm.add_turn("What is ZA Bank's employee size?", "answer")
        cm.add_turn("How about WeLab Bank?", "answer2")
        cm.add_turn("And Mox Bank?", "answer3")
        self.assertEqual(cm.context["last_company"], "Mox Bank")
        self.assertEqual(cm.context["last_user_query"], "And Mox Bank?")

    def test_entities_accumulate_beyond_history_cap(self):
        cm = ConversationManager(max_history=1)
        cm.add_turn("ZA Bank", "a")
        cm.add_turn("WeLab Bank", "b")
        self.assertEqual(len(cm.history), 1)
        self.assertEqual(cm.context["entities"], ["ZA Bank", "WeLab Bank"])

    def test_stats_total_turns_matches_trimmed_history(self):
        cm = ConversationManager(max_history=2)
        for i in range(6):
            cm.add_turn(f"q{i}", f"a{i}")
        self.assertEqual(cm.get_stats()["total_turns"], 2)

    def test_clear_resets_history_and_context(self):
        cm = ConversationManager(max_history=3)
        cm.add_turn("ZA Bank", "a")
        cm.clear()
        self.assertEqual(len(cm.history), 0)
        self.assertIsNone(cm.context["last_company"])
        self.assertEqual(cm.context["entities"], [])


if __name__ == "__main__":
    unittest.main()
