#!/usr/bin/env python3
"""Lazy-import contract tests for run.py handlers.

run_demo, run_test and run_main deliberately import their target module
inside the function body so that the interactive menu stays cheap and the
heavy demo dependencies are only loaded when actually selected. These tests
pin the exact module paths and entry-point names by installing stub modules
in sys.modules, so a rename or a move of a demo entry point is caught here
instead of at runtime.
"""

import sys
import types
import unittest
from unittest import mock

import run


class _StubModule(types.ModuleType):
    """Module stub that records calls to its attributes."""

    def __init__(self, name):
        super().__init__(name)
        self.calls = []

    def make_recorder(self, attr):
        def recorder(*args, **kwargs):
            self.calls.append((attr, args, kwargs))
            return None
        return recorder


def _install(name, attrs):
    module = _StubModule(name)
    for attr in attrs:
        setattr(module, attr, module.make_recorder(attr))
    sys.modules[name] = module
    return module


class TestRunDemo(unittest.TestCase):
    def test_imports_demo_with_mcp_and_calls_it(self):
        stub = _install("demos.demo_with_mcp", ["demo_with_mcp"])
        with mock.patch.object(run, "input", return_value=""):
            run.run_demo()
        self.assertEqual(stub.calls, [("demo_with_mcp", (), {})])

    def test_waits_for_enter_after_demo(self):
        _install("demos.demo_with_mcp", ["demo_with_mcp"])
        with mock.patch.object(run, "input", return_value="") as fake_input:
            run.run_demo()
        fake_input.assert_called_once()


class TestRunTest(unittest.TestCase):
    def test_imports_github_test_main_and_calls_it(self):
        stub = _install("tests.test_github_mcp", ["main"])
        run.run_test()
        self.assertEqual(stub.calls, [("main", (), {})])


class TestRunMain(unittest.TestCase):
    def test_imports_demo_enhanced_and_calls_it(self):
        stub = _install("enhanced_fintalk", ["demo_enhanced"])
        run.run_main()
        self.assertEqual(stub.calls, [("demo_enhanced", (), {})])


class TestLazyImportIsolation(unittest.TestCase):
    def test_handlers_do_not_import_each_others_modules(self):
        demo_stub = _install("demos.demo_with_mcp", ["demo_with_mcp"])
        test_stub = _install("tests.test_github_mcp", ["main"])
        main_stub = _install("enhanced_fintalk", ["demo_enhanced"])
        with mock.patch.object(run, "input", return_value=""):
            run.run_demo()
        self.assertEqual(test_stub.calls, [])
        self.assertEqual(main_stub.calls, [])
        self.assertEqual(len(demo_stub.calls), 1)


if __name__ == "__main__":
    unittest.main()
