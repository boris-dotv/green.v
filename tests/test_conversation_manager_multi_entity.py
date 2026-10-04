import unittest

from enhanced_core.conversation_manager import ConversationManager


class TestMultiEntityExtraction(unittest.TestCase):
    def setUp(self):
        self.cm = ConversationManager()

    def test_only_first_matching_company_is_recorded(self):
        # "ZA Bank" is first in the companies list, so it wins even though
        # "Mox Bank" also appears in the query.
        self.cm.add_turn("Compare Mox Bank and ZA Bank", "ok")
        self.assertEqual(self.cm.context["last_company"], "ZA Bank")
        self.assertEqual(self.cm.context["entities"], ["ZA Bank"])

    def test_entities_never_hold_two_companies_in_one_turn(self):
        self.cm.add_turn("ZA Bank vs WeLab Bank", "ok")
        self.assertEqual(len(self.cm.context["entities"]), 1)

    def test_later_turn_can_add_a_second_company(self):
        self.cm.add_turn("ZA Bank overview", "ok")
        self.cm.add_turn("WeLab Bank overview", "ok")
        self.assertEqual(self.cm.context["last_company"], "WeLab Bank")
        self.assertEqual(self.cm.context["entities"], ["ZA Bank", "WeLab Bank"])

    def test_repeated_company_is_not_duplicated(self):
        self.cm.add_turn("ZA Bank overview", "ok")
        self.cm.add_turn("ZA Bank again", "ok")
        self.assertEqual(self.cm.context["entities"], ["ZA Bank"])

    def test_query_without_known_company_leaves_entities_untouched(self):
        self.cm.add_turn("ZA Bank overview", "ok")
        self.cm.add_turn("Tell me about the market", "ok")
        self.assertEqual(self.cm.context["entities"], ["ZA Bank"])
        self.assertEqual(self.cm.context["last_company"], "ZA Bank")

    def test_company_match_is_case_insensitive(self):
        self.cm.add_turn("tell me about za bank", "ok")
        self.assertEqual(self.cm.context["last_company"], "ZA Bank")
        self.assertEqual(self.cm.context["entities"], ["ZA Bank"])


if __name__ == "__main__":
    unittest.main()
