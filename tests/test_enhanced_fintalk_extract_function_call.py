"""Tests for EnhancedFinTalkAI._extract_function_call parsing branches.

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


class _FakeRegistry:
    def get_functions(self):
        return [{"name": "get_company_info"}]


def _make(llm_reply):
    obj = EnhancedFinTalkAI.__new__(EnhancedFinTalkAI)
    obj.function_registry = _FakeRegistry()
    enhanced_fintalk.llm_caller = lambda prompt, temperature=0.3: llm_reply
    return obj


class TestExtractFunctionCall(unittest.TestCase):
    def setUp(self):
        self._orig = enhanced_fintalk.llm_caller

    def tearDown(self):
        enhanced_fintalk.llm_caller = self._orig

    def test_plain_json_returns_dict(self):
        obj = _make('{"function_name": "get_company_info", "parameters": {"company_name": "ZA Bank"}}')
        out = obj._extract_function_call("ZA Bank info")
        self.assertEqual(out["function_name"], "get_company_info")
        self.assertEqual(out["parameters"], {"company_name": "ZA Bank"})

    def test_code_fence_is_stripped(self):
        obj = _make('```json\n{"function_name": "list_companies"}\n```')
        out = obj._extract_function_call("list companies")
        self.assertEqual(out, {"function_name": "list_companies"})

    def test_surrounding_prose_is_ignored(self):
        obj = _make('Sure: {"function_name": "list_companies"} done')
        out = obj._extract_function_call("list companies")
        self.assertEqual(out, {"function_name": "list_companies"})

    def test_none_sentinel_returns_none(self):
        obj = _make('{"function_name": "none"}')
        self.assertIsNone(obj._extract_function_call("hello"))

    def test_malformed_json_returns_none(self):
        obj = _make('{"function_name": "get_company_info", }')
        self.assertIsNone(obj._extract_function_call("ZA Bank info"))

    def test_no_braces_returns_none(self):
        obj = _make("no json here")
        self.assertIsNone(obj._extract_function_call("hello"))

    def test_empty_reply_returns_none(self):
        obj = _make("")
        self.assertIsNone(obj._extract_function_call("hello"))


if __name__ == "__main__":
    unittest.main()
