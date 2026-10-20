"""Tests for EnhancedFinTalkAI._handle_general_query and _extract_function_call
with None/empty input.

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


class _FakeRegistry:
    def __init__(self):
        self.executed = []

    def get_functions(self):
        return [{"name": "get_company_info"}]

    def execute(self, name, params):
        self.executed.append((name, params))
        return {"data": [{"company": params.get("company_name")}]}


def _make(registry=None):
    inst = EnhancedFinTalkAI.__new__(EnhancedFinTalkAI)
    inst.function_registry = registry or _FakeRegistry()
    return inst


class TestHandleGeneralQueryNoneInput(unittest.TestCase):
    def setUp(self):
        self._orig = enhanced_fintalk.llm_caller

    def tearDown(self):
        enhanced_fintalk.llm_caller = self._orig

    def test_none_query_does_not_raise(self):
        out = _make()._handle_general_query(None)
        self.assertIn("请指定", out)

    def test_empty_query_returns_guidance(self):
        out = _make()._handle_general_query("")
        self.assertIn("请指定", out)

    def test_unknown_company_guidance_echoes_query(self):
        out = _make()._handle_general_query("some unknown bank")
        self.assertIn("some unknown bank", out)

    def test_fintalk_branch_returns_description(self):
        out = _make()._handle_general_query("What is FinTalk?")
        self.assertIn("FinTalk.AI", out)


class TestExtractFunctionCallNoneInput(unittest.TestCase):
    def setUp(self):
        self._orig = enhanced_fintalk.llm_caller

    def tearDown(self):
        enhanced_fintalk.llm_caller = self._orig

    def test_none_query_returns_none_without_llm_call(self):
        rec = _Recorder()
        enhanced_fintalk.llm_caller = rec
        self.assertIsNone(_make()._extract_function_call(None))
        self.assertEqual(rec.calls, [])

    def test_empty_query_returns_none_without_llm_call(self):
        rec = _Recorder()
        enhanced_fintalk.llm_caller = rec
        self.assertIsNone(_make()._extract_function_call(""))
        self.assertEqual(rec.calls, [])


if __name__ == "__main__":
    unittest.main()
