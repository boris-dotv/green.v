#!/usr/bin/env python3
"""Tests for EnhancedFinTalkAI._handle_general_query routing.

Pins the current contract of the hardcoded company-matching branch without
needing OSWorld, pandas, or network access: the method is bound to a bare
object that only supplies function_registry and nlg.
"""

import sys
import types
import unittest

# Stub heavy modules imported at enhanced_fintalk import time so the module
# can be imported in the stdlib-only test environment.
for _name in ("pandas",):
    if _name not in sys.modules:
        sys.modules[_name] = types.ModuleType(_name)

_osworld = types.ModuleType("OSWorld")
_docker = types.ModuleType("OSWorld.docker_osworld_adapter")


class _FakeAdapter:
    def __init__(self, *args, **kwargs):
        pass

    def close(self):
        pass


_docker.DockerOSWorldAdapter = _FakeAdapter
sys.modules.setdefault("OSWorld", _osworld)
sys.modules.setdefault("OSWorld.docker_osworld_adapter", _docker)

from enhanced_fintalk import EnhancedFinTalkAI  # noqa: E402


class _FakeRegistry:
    def __init__(self, result):
        self.result = result
        self.calls = []

    def execute(self, name, params):
        self.calls.append((name, params))
        return self.result


class _FakeNLG:
    def __init__(self):
        self.calls = []

    def generate_answer(self, query, func_result):
        self.calls.append((query, func_result))
        return "NLG_ANSWER"


def _make_client(registry_result):
    client = object.__new__(EnhancedFinTalkAI)
    client.function_registry = _FakeRegistry(registry_result)
    client.nlg = _FakeNLG()
    return client


class TestGeneralQueryRouting(unittest.TestCase):
    def test_za_bank_routes_to_company_info(self):
        client = _make_client({"company_name": "ZA Bank"})
        answer = client._handle_general_query("Tell me about ZA Bank")
        self.assertEqual(answer, "NLG_ANSWER")
        self.assertEqual(
            client.function_registry.calls,
            [("get_company_info", {"company_name": "ZA Bank"})],
        )

    def test_welab_routes_to_company_info(self):
        client = _make_client({"company_name": "WeLab Bank"})
        answer = client._handle_general_query("what about welab?")
        self.assertEqual(answer, "NLG_ANSWER")
        self.assertEqual(
            client.function_registry.calls,
            [("get_company_info", {"company_name": "WeLab Bank"})],
        )

    def test_fintalk_returns_static_message(self):
        client = _make_client({})
        answer = client._handle_general_query("What is FinTalk?")
        self.assertIn("FinTalk.AI", answer)
        self.assertEqual(client.function_registry.calls, [])

    def test_unknown_company_returns_guidance(self):
        client = _make_client({})
        answer = client._handle_general_query("Tell me about Foo Corp")
        self.assertIn("请指定", answer)
        self.assertIn("Foo Corp", answer)
        self.assertEqual(client.function_registry.calls, [])

    def test_function_error_is_surfaced(self):
        client = _make_client({"error": "db unavailable"})
        answer = client._handle_general_query("ZA Bank info")
        self.assertIn("db unavailable", answer)
        self.assertEqual(client.nlg.calls, [])


if __name__ == "__main__":
    unittest.main()
