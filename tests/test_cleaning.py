import sys
import unittest
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.cleaning import clean_sales


class CleanSalesTests(unittest.TestCase):
    def test_removes_invalid_and_duplicate_rows_and_logs_changes(self) -> None:
        raw = pd.DataFrame(
            [
                {
                    "order_id": " A ",
                    "order_date": "2026-01-02",
                    "branch": "Nairobi",
                    "region": "",
                    "product": "Laptop",
                    "category": "Computing",
                    "channel": "Online",
                    "units_sold": 2,
                    "unit_price": 100.0,
                },
                {
                    "order_id": "A",
                    "order_date": "2026-01-02",
                    "branch": "Nairobi",
                    "region": "Capital",
                    "product": "Laptop",
                    "category": "Computing",
                    "channel": "Online",
                    "units_sold": 2,
                    "unit_price": 100.0,
                },
                {
                    "order_id": "B",
                    "order_date": "not-a-date",
                    "branch": "Nairobi",
                    "region": "Capital",
                    "product": "Laptop",
                    "category": "Computing",
                    "channel": "Online",
                    "units_sold": 1,
                    "unit_price": 100.0,
                },
            ]
        )

        clean, log = clean_sales(raw)

        self.assertEqual(len(clean), 1)
        self.assertEqual(clean.loc[0, "order_id"], "A")
        self.assertEqual(clean.loc[0, "region"], "Capital")
        self.assertEqual(clean.loc[0, "revenue"], 200.0)
        self.assertEqual(
            log.set_index("step").loc["deduplicate_order_id", "rows_affected"],
            1,
        )
        self.assertEqual(
            log.set_index("step").loc["parse_order_date", "rows_affected"],
            1,
        )

    def test_rejects_missing_required_columns(self) -> None:
        with self.assertRaisesRegex(ValueError, "Missing required columns"):
            clean_sales(pd.DataFrame({"order_id": ["A"]}))


if __name__ == "__main__":
    unittest.main()
