"""Tests for EnhancedFinTalkAI._handle_task_query with None/empty input.

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
    def __init__(self):
        self.calls = []

    def execute(self, name, params):
        self.calls.append((name, params))
        return {"error": "unused"}


class _FakeNLG:
    def __init__(self):
        self.calls = []

    def generate_answer(self, query, data):
        self.calls.append((query, data))
        return "nlg-answer"


def _make(func_call, general_answer=None):
    obj = EnhancedFinTalkAI.__new__(EnhancedFinTalkAI)
    obj.function_registry = _FakeRegistry()
    obj.nlg = _FakeNLG()
    obj._extract_function_call = lambda q: func_call
    obj._handle_general_query = lambda q: general_answer
    return obj


class TestHandleTaskQueryNoneInput(unittest.TestCase):
    def test_none_query_no_func_call_uses_general_fallback(self):
        obj = _make(None, general_answer="general answer")
        out = obj._handle_task_query(None, False)
        self.assertEqual(out, "general answer")
        self.assertEqual(obj.function_registry.calls, [])
        self.assertEqual(obj.nlg.calls, [])

    def test_none_query_no_func_call_empty_general_returns_default(self):
        obj = _make(None, general_answer=None)
        out = obj._handle_task_query(None, False)
        self.assertEqual(out, "抱歉，我无法处理您的查询。")
        self.assertEqual(obj.function_registry.calls, [])

    def test_empty_query_no_func_call_empty_general_returns_default(self):
        obj = _make(None, general_answer="")
        out = obj._handle_task_query("", False)
        self.assertEqual(out, "抱歉，我无法处理您的查询。")


if __name__ == "__main__":
    unittest.main()
