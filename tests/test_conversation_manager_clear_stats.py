#!/usr/bin/env python3
"""Tests for ConversationManager.clear and get_stats."""

import unittest

from enhanced_core.conversation_manager import ConversationManager


CONTEXT_KEYS = {
    "last_company",
    "last_query_type",
    "entities",
    "last_query",
    "last_sql",
    "last_assistant",
    "last_user_query",
    "last_query_time",
    "last_company_mention_time",
}


class TestClear(unittest.TestCase):
    def test_clear_empties_history(self):
        cm = ConversationManager()
        cm.add_turn("How many employees at ZA Bank?", "About 500", query_type="query")
        self.assertEqual(len(cm.history), 1)
        cm.clear()
        self.assertEqual(len(cm.history), 0)

    def test_clear_resets_all_context_keys(self):
        cm = ConversationManager()
        cm.add_turn("Tell me about Mox Bank", "Mox Bank is a virtual bank")
        cm.context["last_sql"] = "SELECT 1"
        cm.context["last_assistant"] = "stale"
        cm.clear()
        self.assertEqual(set(cm.context.keys()), CONTEXT_KEYS)
        for key in CONTEXT_KEYS:
            value = cm.context[key]
            if key == "entities":
                self.assertEqual(value, [])
            else:
                self.assertIsNone(value)

    def test_clear_resets_slots(self):
        cm = ConversationManager()
        cm.slots["company"] = "ZA Bank"
        cm.clear()
        self.assertEqual(cm.slots, {})

    def test_clear_returns_self_for_chaining(self):
        cm = ConversationManager()
        self.assertIs(cm.clear(), cm)

    def test_clear_is_idempotent(self):
        cm = ConversationManager()
        cm.clear()
        cm.clear()
        self.assertEqual(len(cm.history), 0)
        self.assertEqual(cm.context["entities"], [])
        self.assertEqual(cm.slots, {})

    def test_add_turn_after_clear_starts_fresh(self):
        cm = ConversationManager()
        cm.add_turn("ZA Bank employees?", "500")
        cm.clear()
        cm.add_turn("What about Mox Bank?", "300")
        self.assertEqual(len(cm.history), 1)
        self.assertEqual(cm.context["last_company"], "Mox Bank")
        self.assertEqual(cm.context["entities"], ["Mox Bank"])


class TestGetStats(unittest.TestCase):
    def test_stats_on_fresh_manager(self):
        cm = ConversationManager()
        stats = cm.get_stats()
        self.assertEqual(stats["total_turns"], 0)
        self.assertIsNone(stats["last_company"])
        self.assertEqual(stats["entities_count"], 0)
        self.assertEqual(stats["slots_count"], 0)

    def test_stats_counts_turns_and_entities(self):
        cm = ConversationManager()
        cm.add_turn("ZA Bank employees?", "500")
        cm.add_turn("WeLab Bank employees?", "400")
        stats = cm.get_stats()
        self.assertEqual(stats["total_turns"], 2)
        self.assertEqual(stats["last_company"], "WeLab Bank")
        self.assertEqual(stats["entities_count"], 2)

    def test_stats_counts_slots(self):
        cm = ConversationManager()
        cm.slots["company"] = "ZA Bank"
        cm.slots["metric"] = "employees"
        self.assertEqual(cm.get_stats()["slots_count"], 2)

    def test_stats_after_clear(self):
        cm = ConversationManager()
        cm.add_turn("ZA Bank employees?", "500")
        cm.slots["company"] = "ZA Bank"
        cm.clear()
        stats = cm.get_stats()
        self.assertEqual(stats["total_turns"], 0)
        self.assertIsNone(stats["last_company"])
        self.assertEqual(stats["entities_count"], 0)
        self.assertEqual(stats["slots_count"], 0)

    def test_stats_respects_max_history(self):
        cm = ConversationManager(max_history=2)
        for i in range(5):
            cm.add_turn(f"query {i}", f"answer {i}")
        self.assertEqual(cm.get_stats()["total_turns"], 2)


if __name__ == "__main__":
    unittest.main()
