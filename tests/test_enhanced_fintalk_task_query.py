"""Tests for EnhancedFinTalkAI._handle_task_query branches.

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


def _make(registry_result, func_call, general_answer=None, nlg_answer="nlg-answer"):
    obj = EnhancedFinTalkAI.__new__(EnhancedFinTalkAI)
    obj.function_registry = _FakeRegistry(registry_result)
    obj.nlg = _FakeNLG(nlg_answer)
    obj._extract_function_call = lambda q: func_call
    obj._handle_general_query = lambda q: general_answer
    return obj


class TestHandleTaskQuery(unittest.TestCase):
    def test_function_call_success_uses_nlg(self):
        func_call = {"function_name": "get_company_info", "parameters": {"company_name": "ZA Bank"}}
        obj = _make({"name": "ZA Bank"}, func_call, nlg_answer="ZA info")
        out = obj._handle_task_query("ZA Bank details", False)
        self.assertEqual(out, "ZA info")
        self.assertEqual(
            obj.function_registry.calls,
            [("get_company_info", {"company_name": "ZA Bank"})],
        )
        self.assertEqual(obj.nlg.calls, [("ZA Bank details", {"name": "ZA Bank"})])

    def test_function_call_missing_parameters_defaults_to_empty(self):
        func_call = {"function_name": "list_companies"}
        obj = _make({"rows": []}, func_call, nlg_answer="listed")
        out = obj._handle_task_query("list companies", False)
        self.assertEqual(out, "listed")
        self.assertEqual(obj.function_registry.calls, [("list_companies", {})])

    def test_function_call_error_returns_friendly_message(self):
        func_call = {"function_name": "get_company_info", "parameters": {}}
        obj = _make({"error": "db down"}, func_call)
        out = obj._handle_task_query("ZA Bank details", False)
        self.assertIn("抱歉", out)
        self.assertIn("db down", out)
        self.assertEqual(obj.nlg.calls, [])

    def test_no_function_call_falls_back_to_general_query(self):
        obj = _make({"error": "unused"}, None, general_answer="general answer")
        out = obj._handle_task_query("some query", False)
        self.assertEqual(out, "general answer")
        self.assertEqual(obj.function_registry.calls, [])

    def test_no_function_call_and_empty_general_returns_default(self):
        obj = _make({"error": "unused"}, None, general_answer=None)
        out = obj._handle_task_query("some query", False)
        self.assertEqual(out, "抱歉，我无法处理您的查询。")


if __name__ == "__main__":
    unittest.main()
