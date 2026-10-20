"""Tests for EnhancedFinTalkAI._handle_small_talk and _handle_knowledge_query.

Constructs the instance via __new__ and patches the module-level llm_caller
so no network or heavy dependencies are needed.
"""
import sys
import types
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# Stub heavy modules that enhanced_fintalk imports at module load time.
for _name in (
    "enhanced_core",
    "formula",
    "OSWorld",
    "OSWorld.docker_osworld_adapter",
):
    if _name not in sys.modules:
        sys.modules[_name] = types.ModuleType(_name)

_ec = sys.modules["enhanced_core"]
for _attr in (
    "ParallelExecutor",
    "QueryRewriter",
    "QueryArbitrator",
    "RejectionDetector",
    "CorrelationChecker",
    "FinancialFunctionRegistry",
    "StreamingNLG",
    "ConversationManager",
):
    if not hasattr(_ec, _attr):
        setattr(_ec, _attr, type(_attr, (), {}))

_formula = sys.modules["formula"]
if not hasattr(_formula, "find_formula_for_query"):
    _formula.find_formula_for_query = lambda q: None
if not hasattr(_formula, "calculate_from_expression"):
    _formula.calculate_from_expression = lambda *a, **k: None

_osw = sys.modules["OSWorld.docker_osworld_adapter"]
if not hasattr(_osw, "DockerOSWorldAdapter"):
    _osw.DockerOSWorldAdapter = type("DockerOSWorldAdapter", (), {})

import enhanced_fintalk  # noqa: E402
from enhanced_fintalk import EnhancedFinTalkAI  # noqa: E402


class _Recorder:
    def __init__(self, reply="llm-reply"):
        self.reply = reply
        self.calls = []

    def __call__(self, prompt, temperature=0.3):
        self.calls.append((prompt, temperature))
        return self.reply


def _make():
    return EnhancedFinTalkAI.__new__(EnhancedFinTalkAI)


class TestHandleSmallTalk(unittest.TestCase):
    def setUp(self):
        self._orig = enhanced_fintalk.llm_caller

    def tearDown(self):
        enhanced_fintalk.llm_caller = self._orig

    def test_hello_keyword_returns_canned_response(self):
        rec = _Recorder()
        enhanced_fintalk.llm_caller = rec
        out = _make()._handle_small_talk("Hello there")
        self.assertIn("FinTalk.AI", out)
        self.assertEqual(rec.calls, [])

    def test_keyword_match_is_case_insensitive(self):
        enhanced_fintalk.llm_caller = _Recorder()
        out = _make()._handle_small_talk("THANK you")
        self.assertIn("不客气", out)

    def test_bye_keyword(self):
        enhanced_fintalk.llm_caller = _Recorder()
        out = _make()._handle_small_talk("bye")
        self.assertIn("再见", out)

    def test_unmatched_query_falls_back_to_llm(self):
        rec = _Recorder("friendly")
        enhanced_fintalk.llm_caller = rec
        out = _make()._handle_small_talk("tell me a joke")
        self.assertEqual(out, "friendly")
        self.assertEqual(len(rec.calls), 1)
        prompt, temperature = rec.calls[0]
        self.assertIn("tell me a joke", prompt)
        self.assertEqual(temperature, 0.7)


class TestHandleKnowledgeQuery(unittest.TestCase):
    def setUp(self):
        self._orig = enhanced_fintalk.llm_caller

    def tearDown(self):
        enhanced_fintalk.llm_caller = self._orig

    def test_delegates_to_llm_with_query_in_prompt(self):
        rec = _Recorder("explained")
        enhanced_fintalk.llm_caller = rec
        out = _make()._handle_knowledge_query("what is ROE?")
        self.assertEqual(out, "explained")
        self.assertEqual(len(rec.calls), 1)
        prompt, temperature = rec.calls[0]
        self.assertIn("what is ROE?", prompt)
        self.assertEqual(temperature, 0.7)

    def test_returns_llm_reply_verbatim(self):
        enhanced_fintalk.llm_caller = _Recorder("")
        self.assertEqual(_make()._handle_knowledge_query("concept"), "")


if __name__ == "__main__":
    unittest.main()
