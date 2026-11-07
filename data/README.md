# Data provenance, grain and privacy

## Source and licence

`duka_sales.csv` is a synthetic, order-level teaching dataset generated with the
included `generate_data.py` script (NumPy seed 2026; 1,000 orders; 1 January-30
June 2026). It is not a real retailer's transaction data and has no external
source licence; it is original educational data distributed under this
repository's MIT licence. Generated locally on 7 November 2026. Re-run
`python data/generate_data.py` from the repository root to reproduce it.

## Grain and fields

The CSV grain is one order per row. `order_id` is the synthetic order key;
`order_date`, `branch`, `region`, `product`, `category`, `channel`,
`units_sold`, and `unit_price` describe an order. `revenue` is derived during
cleaning as quantity times unit price. Currency is Kenyan shillings (KES).
There are no person-level records or linked customer tables.

## Ethics and privacy statement

No direct identifiers, contact details, account identifiers, or sensitive
personal attributes are present. Order IDs are synthetic, not pseudonyms for
real people. No personal data were collected, removed, or pseudonymised. The
published summaries aggregate synthetic orders by month, branch, product,
category, and channel; they cannot identify a real individual. Findings are
illustrative and must not be presented as evidence about an actual business or
customer population.
