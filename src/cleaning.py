"""Reusable cleaning helpers for Duka Electronics order-level data."""

from __future__ import annotations

from collections.abc import Mapping

import pandas as pd


BRANCH_REGIONS = {
    "Nairobi": "Capital",
    "Westlands": "Capital",
    "Mombasa": "Coast",
    "Kisumu": "Western",
    "Nakuru": "Rift Valley",
    "Eldoret": "Rift Valley",
    "Thika": "Central",
    "Nyeri": "Central",
}

REQUIRED_COLUMNS = {
    "order_id",
    "order_date",
    "branch",
    "product",
    "category",
    "channel",
    "units_sold",
    "unit_price",
}


def clean_sales(
    data: pd.DataFrame,
    branch_regions: Mapping[str, str] = BRANCH_REGIONS,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return cleaned order rows and an auditable before/after cleaning log.

    Invalid dates, missing identifiers/dimensions, non-positive quantities,
    and negative prices are excluded. Duplicate order IDs keep their first row.
    Missing regions are inferred from the branch mapping when possible.
    """
    missing_columns = REQUIRED_COLUMNS.difference(data.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")

    clean = data.copy()
    initial_count = len(clean)
    log: list[dict[str, int | str]] = []

    def record(step: str, before: int, after: int, note: str) -> None:
        log.append(
            {
                "step": step,
                "rows_before": before,
                "rows_after": after,
                "rows_affected": before - after,
                "note": note,
            }
        )

    clean["order_id"] = clean["order_id"].astype("string").str.strip()
    clean = clean.drop_duplicates(subset="order_id", keep="first").copy()
    record("deduplicate_order_id", initial_count, len(clean), "Kept first occurrence of each order ID.")

    before = len(clean)
    clean["order_date"] = pd.to_datetime(clean["order_date"], errors="coerce")
    clean = clean.dropna(subset=["order_date"]).copy()
    record("parse_order_date", before, len(clean), "Removed rows with unparseable order dates.")

    for column in ("branch", "product", "category", "channel"):
        clean[column] = clean[column].astype("string").str.strip()
        clean.loc[clean[column].eq(""), column] = pd.NA

    if "region" not in clean:
        clean["region"] = pd.NA
    clean["region"] = clean["region"].astype("string").str.strip()
    clean.loc[clean["region"].eq(""), "region"] = pd.NA
    missing_regions = clean["region"].isna()
    clean.loc[missing_regions, "region"] = clean.loc[missing_regions, "branch"].map(branch_regions)
    record(
        "derive_missing_region",
        len(clean),
        len(clean),
        f"Derived {int(missing_regions.sum())} region value(s) from the branch lookup.",
    )

    before = len(clean)
    clean["units_sold"] = pd.to_numeric(clean["units_sold"], errors="coerce")
    clean["unit_price"] = pd.to_numeric(clean["unit_price"], errors="coerce")
    valid_amounts = (
        clean["units_sold"].gt(0)
        & clean["unit_price"].ge(0)
        & clean["units_sold"].notna()
        & clean["unit_price"].notna()
    )
    clean = clean.loc[valid_amounts].copy()
    record("validate_amounts", before, len(clean), "Removed missing/non-positive quantities and missing/negative prices.")

    before = len(clean)
    clean = clean.dropna(
        subset=["order_id", "branch", "product", "category", "channel", "region"]
    ).copy()
    record("remove_missing_dimensions", before, len(clean), "Removed rows missing required descriptive fields.")

    clean["units_sold"] = clean["units_sold"].astype("int64")
    clean["unit_price"] = clean["unit_price"].astype("float64")
    clean["revenue"] = clean["units_sold"] * clean["unit_price"]
    record("derive_revenue", len(clean), len(clean), "Calculated revenue as units_sold x unit_price.")

    return clean.reset_index(drop=True), pd.DataFrame(log)
