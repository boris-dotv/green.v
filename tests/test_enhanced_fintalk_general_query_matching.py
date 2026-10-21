"""Tests for EnhancedFinTalkAI._handle_general_query company matching branches.

Constructs the instance via __new__ and injects fake collaborators so no
heavy dependencies (pandas, OSWorld, enhanced_core) are imported.
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

from enhanced_fintalk import EnhancedFinTalkAI  # noqa: E402


class _FakeRegistry:
    def __init__(self, result):
        self._result = result
        self.calls = []

    def execute(self, name, params):
        self.calls.append((name, params))
        return self._result


class _FakeNLG:
    def __init__(self, answer="nlg-answer"):
        self.answer = answer
        self.calls = []

    def generate_answer(self, query, data):
        self.calls.append((query, data))
        return self.answer


def _make(registry_result, nlg_answer="nlg-answer"):
    obj = EnhancedFinTalkAI.__new__(EnhancedFinTalkAI)
    obj.function_registry = _FakeRegistry(registry_result)
    obj.nlg = _FakeNLG(nlg_answer)
    return obj


class TestHandleGeneralQueryMatching(unittest.TestCase):
    def test_za_bank_matches_and_uses_nlg(self):
        obj = _make({"name": "ZA Bank"}, nlg_answer="ZA info")
        out = obj._handle_general_query("Tell me about ZA Bank")
        self.assertEqual(out, "ZA info")
        self.assertEqual(
            obj.function_registry.calls,
            [("get_company_info", {"company_name": "ZA Bank"})],
        )
        self.assertEqual(obj.nlg.calls, [("Tell me about ZA Bank", {"name": "ZA Bank"})])

    def test_welab_matches(self):
        obj = _make({"name": "WeLab Bank"}, nlg_answer="welab info")
        out = obj._handle_general_query("WeLab details")
        self.assertEqual(out, "welab info")
        self.assertEqual(
            obj.function_registry.calls,
            [("get_company_info", {"company_name": "WeLab Bank"})],
        )

    def test_matching_is_case_insensitive(self):
        obj = _make({"name": "ZA Bank"}, nlg_answer="ok")
        out = obj._handle_general_query("ZA BANK employees")
        self.assertEqual(out, "ok")
        self.assertEqual(
            obj.function_registry.calls,
            [("get_company_info", {"company_name": "ZA Bank"})],
        )

    def test_fintalk_returns_static_description_without_registry(self):
        obj = _make({"error": "unused"})
        out = obj._handle_general_query("What is FinTalk?")
        self.assertIn("FinTalk.AI", out)
        self.assertEqual(obj.function_registry.calls, [])
        self.assertEqual(obj.nlg.calls, [])

    def test_unknown_company_returns_guidance(self):
        obj = _make({"error": "unused"})
        out = obj._handle_general_query("Tell me about SomeOther Bank")
        self.assertIn("请指定你想查询的公司名称", out)
        self.assertIn("SomeOther Bank", out)
        self.assertEqual(obj.function_registry.calls, [])

    def test_registry_error_returns_friendly_message(self):
        obj = _make({"error": "db down"})
        out = obj._handle_general_query("ZA Bank details")
        self.assertIn("抱歉", out)
        self.assertIn("db down", out)
        self.assertEqual(obj.nlg.calls, [])


if __name__ == "__main__":
    unittest.main()
