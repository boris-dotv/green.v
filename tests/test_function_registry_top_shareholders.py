#!/usr/bin/env python3
"""Unit tests for FinancialFunctionRegistry._get_top_shareholders SQL construction.

These tests lock in the observable behaviour of the top-shareholder query:
rows are ordered by share_percentage descending, the top_n argument is
interpolated into the LIMIT clause, and an unknown company yields an error
dict rather than an exception. An in-memory sqlite3 database is used so the
tests need no network or heavy dependencies.
"""

import sqlite3
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from enhanced_core.function_registry import FinancialFunctionRegistry  # noqa: E402


class TestGetTopShareholders(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(":memory:")
        self.db.execute(
            "CREATE TABLE companies (company_sort_id INTEGER, name TEXT)"
        )
        self.db.execute(
            "CREATE TABLE shareholders ("
            "company_sort_id INTEGER, shareholder_name TEXT, share_percentage TEXT)"
        )
        self.db.execute(
            "INSERT INTO companies (company_sort_id, name) VALUES (1, 'ZA Bank')"
        )
        self.db.executemany(
            "INSERT INTO shareholders "
            "(company_sort_id, shareholder_name, share_percentage) VALUES (?, ?, ?)",
            [
                (1, "Alpha Holdings", "10%"),
                (1, "Beta Capital", "50%"),
                (1, "Gamma Trust", "30%"),
            ],
        )
        self.db.commit()
        self.registry = FinancialFunctionRegistry(db_connection=self.db)

    def tearDown(self):
        self.db.close()

    def test_rows_ordered_by_share_percentage_descending(self):
        result = self.registry._get_top_shareholders("ZA Bank", 3)
        self.assertEqual(result["status"], "success")
        names = [r["shareholder_name"] for r in result["top_n_shareholders"]]
        self.assertEqual(names, ["Beta Capital", "Gamma Trust", "Alpha Holdings"])

    def test_top_n_limits_returned_rows(self):
        result = self.registry._get_top_shareholders("ZA Bank", 2)
        self.assertEqual(result["count"], 2)
        self.assertEqual(len(result["top_n_shareholders"]), 2)
        self.assertEqual(
            [r["shareholder_name"] for r in result["top_n_shareholders"]],
            ["Beta Capital", "Gamma Trust"],
        )

    def test_company_field_echoes_requested_name(self):
        result = self.registry._get_top_shareholders("ZA Bank", 1)
        self.assertEqual(result["company"], "ZA Bank")

    def test_unknown_company_returns_error_dict(self):
        result = self.registry._get_top_shareholders("Nonexistent Bank", 3)
        self.assertIsInstance(result, dict)
        self.assertIn("error", result)


if __name__ == "__main__":
    unittest.main()
