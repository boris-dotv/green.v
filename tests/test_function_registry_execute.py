#!/usr/bin/env python3
"""Unit tests for FinancialFunctionRegistry.execute dispatch and error contract.

These tests lock in the observable behaviour of execute() when the function
name is unknown, when a required parameter is missing, and when the underlying
handler raises: in every case the registry must return a dict with an 'error'
key rather than propagating the exception to the caller.
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from enhanced_core.function_registry import FinancialFunctionRegistry  # noqa: E402


class TestExecuteUnknownFunction(unittest.TestCase):
    def setUp(self):
        self.registry = FinancialFunctionRegistry()

    def test_unknown_function_returns_error_dict(self):
        result = self.registry.execute("no_such_function", {})
        self.assertIsInstance(result, dict)
        self.assertIn("error", result)
        self.assertIn("no_such_function", result["error"])

    def test_unknown_function_does_not_raise(self):
        # Must not propagate even with a completely empty parameter dict.
        self.registry.execute("", {})


class TestExecuteMissingParameter(unittest.TestCase):
    def setUp(self):
        self.registry = FinancialFunctionRegistry()

    def test_missing_company_name_returns_error_dict(self):
        result = self.registry.execute("get_company_info", {})
        self.assertIsInstance(result, dict)
        self.assertIn("error", result)

    def test_missing_compare_metric_returns_error_dict(self):
        result = self.registry.execute(
            "compare_companies", {"company1": "A", "company2": "B"}
        )
        self.assertIsInstance(result, dict)
        self.assertIn("error", result)


class TestExecuteHandlerException(unittest.TestCase):
    def setUp(self):
        self.registry = FinancialFunctionRegistry()

    def test_handler_exception_is_captured_as_error(self):
        def boom(company_name):
            raise RuntimeError("backend exploded")

        self.registry._get_company_info = boom
        result = self.registry.execute("get_company_info", {"company_name": "ZA Bank"})
        self.assertIsInstance(result, dict)
        self.assertIn("error", result)
        self.assertIn("backend exploded", result["error"])


class TestGetFunctions(unittest.TestCase):
    def test_get_functions_returns_declared_list(self):
        registry = FinancialFunctionRegistry()
        functions = registry.get_functions()
        self.assertIsInstance(functions, list)
        names = [f["function"]["name"] for f in functions]
        self.assertIn("get_company_info", names)
        self.assertIn("compare_companies", names)


if __name__ == "__main__":
    unittest.main()
