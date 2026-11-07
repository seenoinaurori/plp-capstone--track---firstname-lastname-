"""Copy the deterministic course synthetic dataset into the capstone data folder."""

from __future__ import annotations

import csv
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 2026
ORDER_COUNT = 1_000
BRANCHES = {
    "Nairobi": "Capital",
    "Westlands": "Capital",
    "Mombasa": "Coast",
    "Kisumu": "Western",
    "Nakuru": "Rift Valley",
    "Eldoret": "Rift Valley",
    "Thika": "Central",
    "Nyeri": "Central",
}
PRODUCTS = {
    "Smartphone X": ("Mobile", 42_000),
    "Budget Smartphone": ("Mobile", 18_500),
    "Laptop Pro 14": ("Computing", 115_000),
    "Chromebook Air": ("Computing", 32_000),
    "Wireless Headphones": ("Audio", 8_500),
    "Bluetooth Speaker": ("Audio", 6_800),
    "4K Television 43in": ("Television", 54_000),
    "HD Television 32in": ("Television", 27_500),
    "Wi-Fi Router AX": ("Networking", 12_000),
    "Power Bank 20K": ("Accessories", 4_500),
    "Smart Watch": ("Wearables", 22_000),
    "Tablet 10in": ("Computing", 29_500),
}


def generate_sales(seed: int = SEED, order_count: int = ORDER_COUNT) -> pd.DataFrame:
    """Generate deterministic order-level synthetic sales."""
    rng = np.random.default_rng(seed)
    names = np.array(list(PRODUCTS))
    selected = rng.choice(names, size=order_count)
    dates = pd.Timestamp("2026-01-01") + pd.to_timedelta(
        rng.integers(0, 181, size=order_count), unit="D"
    )
    rows = []
    for index, name in enumerate(selected):
        category, base_price = PRODUCTS[str(name)]
        price = int(round(base_price * rng.uniform(0.92, 1.08) / 100) * 100)
        branch = str(rng.choice(list(BRANCHES)))
        rows.append(
            {
                "order_id": f"DUKA-{index + 1:04d}",
                "order_date": dates[index].strftime("%Y-%m-%d"),
                "branch": branch,
                "region": BRANCHES[branch],
                "product": str(name),
                "category": category,
                "channel": str(rng.choice(["In-store", "Online"], p=[0.64, 0.36])),
                "units_sold": int(rng.choice([1, 2, 3, 4, 5], p=[0.58, 0.24, 0.11, 0.05, 0.02])),
                "unit_price": price,
            }
        )
    return pd.DataFrame(rows)


if __name__ == "__main__":
    output = Path(__file__).with_name("duka_sales.csv")
    generate_sales().to_csv(output, index=False, quoting=csv.QUOTE_MINIMAL)
    print(f"Generated {ORDER_COUNT:,} synthetic orders: {output}")
