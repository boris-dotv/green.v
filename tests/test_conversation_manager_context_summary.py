#!/usr/bin/env python3
"""Tests for ConversationManager.get_context_summary.

get_context_summary joins 'Last company' and 'Entities' with '; ' and
returns the literal 'No context' when both are empty. These tests pin
that observable contract so a future refactor cannot silently change
the summary string that is fed into prompts.
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from enhanced_core.conversation_manager import ConversationManager  # noqa: E402


class TestGetContextSummary(unittest.TestCase):
    def test_empty_manager_returns_no_context(self):
        cm = ConversationManager()
        self.assertEqual(cm.get_context_summary(), "No context")

    def test_only_entities_set_omits_last_company(self):
        cm = ConversationManager()
        cm.context["entities"] = ["ZA Bank", "Mox Bank"]
        self.assertEqual(cm.get_context_summary(), "Entities: ZA Bank, Mox Bank")

    def test_only_last_company_set(self):
        cm = ConversationManager()
        cm.context["last_company"] = "ZA Bank"
        self.assertEqual(cm.get_context_summary(), "Last company: ZA Bank")

    def test_both_set_joined_with_semicolon(self):
        cm = ConversationManager()
        cm.context["last_company"] = "ZA Bank"
        cm.context["entities"] = ["ZA Bank"]
        self.assertEqual(
            cm.get_context_summary(),
            "Last company: ZA Bank; Entities: ZA Bank",
        )

    def test_add_turn_populates_summary(self):
        cm = ConversationManager()
        cm.add_turn("What is ZA Bank's employee size?", "answer")
        self.assertEqual(
            cm.get_context_summary(),
            "Last company: ZA Bank; Entities: ZA Bank",
        )

    def test_clear_resets_summary_to_no_context(self):
        cm = ConversationManager()
        cm.add_turn("ZA Bank", "a")
        cm.clear()
        self.assertEqual(cm.get_context_summary(), "No context")


if __name__ == "__main__":
    unittest.main()
