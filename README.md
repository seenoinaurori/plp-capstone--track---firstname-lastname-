# Duka Electronics Sales Performance Analysis (H1 2026)

## Business Problem

Duka Electronics' commercial lead must decide where to focus H2 2026 inventory
and marketing. This analysis uses a synthetic H1 order dataset to compare
branch, product, category, channel, and monthly performance. Re-running the
seeded source, notebooks and SQL must reproduce order counts, H1 revenue, charts
and test results. For a proposed H2 pilot, a provisional business target is at
least 10% higher gross margin per pilot branch than a matched baseline, with
in-stock rate no worse than 5% below baseline. The dataset has no margin or
inventory fields, so the stakeholder must validate those targets before launch.

Questions: (1) How much revenue and how many orders did H1 produce? (2) Which
branches and categories contribute most? (3) How does revenue change month to
month? (4) How do online and in-store baskets compare? (5) Is the weekday vs
weekend average order revenue difference distinguishable statistically?

## Key Findings

- The 1,000 synthetic orders generated **KES 52.46 million** in H1 revenue,
  averaging **KES 52,464 per order**.
- **Mombasa** led branch revenue at **KES 8.18 million**; **Computing** led
  category revenue at **KES 25.51 million (48.6%)**.
- **June** was the highest-revenue month (**KES 11.00 million**) and February
  the lowest (**KES 6.70 million**).
- The weekday/weekend comparison and Welch test are reported with a 95%
  confidence interval in `notebooks/03_analysis.ipynb`; statistical
  significance is not a causal explanation.

All findings describe deterministic synthetic course data, not actual Duka
business records. See `reports/executive_summary.pdf` for recommendations and
limitations.

## Tools

Python (pandas, NumPy, Matplotlib, SciPy, openpyxl) | SQLite | Jupyter

## Repository Structure

```text
data/         synthetic source CSV, generator, provenance and privacy note
src/          reusable cleaning function
notebooks/    01_cleaning.ipynb, 02_eda.ipynb, 03_analysis.ipynb
sql/          commented SQLite analysis queries
reports/      executive summary, visual report, slides and Excel summary
```

## How to Run

From the repository root:

```bash
python -m pip install -r requirements.txt
python data/generate_data.py
```

Run `notebooks/01_cleaning.ipynb`, `notebooks/02_eda.ipynb`, and then
`notebooks/03_analysis.ipynb` from top to bottom in Jupyter or VS Code. For
headless reproducibility, run each in order from the repository root:

```bash
jupyter nbconvert --to notebook --execute --inplace notebooks/01_cleaning.ipynb
jupyter nbconvert --to notebook --execute --inplace notebooks/02_eda.ipynb
jupyter nbconvert --to notebook --execute --inplace notebooks/03_analysis.ipynb
```

Run the cleaning checks from the repository root with
`python -m unittest discover -s tests`.

The first notebook creates
`data/duka_sales.db`; later notebooks write figures, a PDF report, an
eight-slide PDF, and `reports/stakeholder_summary.xlsx`. The dataset is
synthetic and the generator is seeded for reproducibility.

## Dashboard

`reports/dashboard.png` is a static, stakeholder-friendly visual report.
There is no live Looker Studio link yet; publishing requires an authenticated
Google account and public sharing configuration. Do not treat the PNG as an
interactive dashboard. See [`reports/dashboard.md`](reports/dashboard.md) for
the dashboard specification and publication steps.

## Author

Seenoinaurori | GitHub: [@seenoinaurori](https://github.com/seenoinaurori)

## Data Source

Original synthetic educational data generated locally with seed 2026 on
7 November 2026. Data provenance, grain, licence, and privacy statement:
[`data/README.md`](data/README.md).
