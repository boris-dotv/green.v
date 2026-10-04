#!/usr/bin/env python3
"""Tests for ConversationManager.add_turn entity extraction.

add_turn records the user query and assistant answer, then scans the
query for known company names and stores them in context['entities'],
setting context['last_company'] to the first match. Queries without a
known company name must not add entities. These tests pin that
contract so a refactor of the extraction cannot silently break the
context that feeds prompts.
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from enhanced_core.conversation_manager import ConversationManager  # noqa: E402


class TestEntityExtraction(unittest.TestCase):
    def test_query_without_known_company_adds_no_entities(self):
        cm = ConversationManager()
        cm.add_turn("How many employees are there?", "100")
        self.assertEqual(cm.context.get("entities", []), [])
        self.assertIsNone(cm.context.get("last_company"))

    def test_known_company_is_recorded_as_entity(self):
        cm = ConversationManager()
        cm.add_turn("Tell me about ZA Bank", "ZA Bank has 500 employees")
        self.assertIn("ZA Bank", cm.context.get("entities", []))
        self.assertEqual(cm.context.get("last_company"), "ZA Bank")

    def test_entities_accumulate_across_turns(self):
        cm = ConversationManager()
        cm.add_turn("Tell me about ZA Bank", "ok")
        cm.add_turn("And WeLab Bank?", "ok")
        entities = cm.context.get("entities", [])
        self.assertIn("ZA Bank", entities)
        self.assertIn("WeLab Bank", entities)

    def test_last_company_updates_to_most_recent_match(self):
        cm = ConversationManager()
        cm.add_turn("Tell me about ZA Bank", "ok")
        cm.add_turn("And WeLab Bank?", "ok")
        self.assertEqual(cm.context.get("last_company"), "WeLab Bank")

    def test_turn_is_recorded_in_history(self):
        cm = ConversationManager()
        cm.add_turn("q", "a")
        self.assertEqual(len(cm.history), 1)
        turn = list(cm.history)[0]
        self.assertEqual(turn.user, "q")
        self.assertEqual(turn.assistant, "a")

    def test_clear_resets_entities_and_last_company(self):
        cm = ConversationManager()
        cm.add_turn("Tell me about ZA Bank", "ok")
        cm.clear()
        self.assertEqual(cm.context.get("entities", []), [])
        self.assertIsNone(cm.context.get("last_company"))


if __name__ == "__main__":
    unittest.main()
