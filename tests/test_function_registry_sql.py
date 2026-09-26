#!/usr/bin/env python3
"""Unit tests for FinancialFunctionRegistry SQL execution and parsing helpers.

These tests lock in the observable behaviour of _execute_sql against an
in-memory sqlite3 connection (column-keyed dict rows, empty list on SQL
error, empty list when no backend is configured) and the defensive
percentage parsing used by _calculate_concentration.
"""

import sqlite3
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from enhanced_core.function_registry import FinancialFunctionRegistry  # noqa: E402


class TestExecuteSqlWithSqlite(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(":memory:")
        self.db.execute(
            "CREATE TABLE companies (company_sort_id INTEGER, name TEXT)"
        )
        self.db.execute(
            "INSERT INTO companies (company_sort_id, name) VALUES (1, 'ZA Bank')"
        )
        self.db.commit()
        self.registry = FinancialFunctionRegistry(db_connection=self.db)

    def tearDown(self):
        self.db.close()

    def test_rows_are_dicts_keyed_by_column_name(self):
        rows = self.registry._execute_sql(
            "SELECT company_sort_id, name FROM companies"
        )
        self.assertEqual(rows, [{"company_sort_id": 1, "name": "ZA Bank"}])

    def test_empty_result_returns_empty_list(self):
        rows = self.registry._execute_sql(
            "SELECT company_sort_id, name FROM companies WHERE company_sort_id = 999"
        )
        self.assertEqual(rows, [])

    def test_sql_error_returns_empty_list_not_raise(self):
        rows = self.registry._execute_sql("SELECT * FROM does_not_exist")
        self.assertEqual(rows, [])

    def test_get_company_id_finds_row_via_like(self):
        self.assertEqual(self.registry._get_company_id("ZA Bank"), 1)

    def test_get_company_id_is_case_insensitive(self):
        self.assertEqual(self.registry._get_company_id("za bank"), 1)

    def test_get_company_id_unknown_name_returns_none(self):
        self.assertIsNone(self.registry._get_company_id("Nonexistent Bank"))


class TestExecuteSqlWithoutBackend(unittest.TestCase):
    def test_no_db_and_no_osworld_returns_empty_list(self):
        # With no backend configured, _execute_sql must degrade to an empty
        # result (same contract as a SQL error) instead of raising
        # AttributeError on self.db.cursor().
        registry = FinancialFunctionRegistry()
        self.assertEqual(registry._execute_sql("SELECT 1"), [])

    def test_no_backend_company_lookup_returns_none(self):
        registry = FinancialFunctionRegistry()
        self.assertIsNone(registry._get_company_id("ZA Bank"))


class TestCalculateConcentrationParsing(unittest.TestCase):
    def setUp(self):
        self.registry = FinancialFunctionRegistry()

    def _concentration_for(self, percentages):
        rows = [
            {"shareholder_name": f"S{i}", "share_percentage": p}
            for i, p in enumerate(percentages)
        ]
        self.registry._get_top_shareholders = lambda name, n: {
            "company": name,
            "top_n_shareholders": rows,
            "count": len(rows),
            "status": "success",
        }
        return self.registry._calculate_concentration("ZA Bank", len(rows))

    def test_percent_strings_are_summed(self):
        result = self._concentration_for(["30%", "20.5%", "10%"])
        self.assertAlmostEqual(result["concentration"], 60.5)
        self.assertEqual(result["concentration_percentage"], "60.50%")
        self.assertEqual(result["status"], "success")

    def test_slash_and_none_contribute_zero(self):
        result = self._concentration_for(["/", None, "25%"])
        self.assertAlmostEqual(result["concentration"], 25.0)

    def test_unparseable_value_contributes_zero(self):
        result = self._concentration_for(["N/A", "15%"])
        self.assertAlmostEqual(result["concentration"], 15.0)

    def test_error_from_top_shareholders_propagates(self):
        self.registry._get_top_shareholders = lambda name, n: {
            "error": "Company not found: ZA Bank"
        }
        result = self.registry._calculate_concentration("ZA Bank", 3)
        self.assertEqual(result, {"error": "Company not found: ZA Bank"})


if __name__ == "__main__":
    unittest.main()
