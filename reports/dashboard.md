# Dashboard status and publication steps

## Status

`dashboard.png` and `visual_report.pdf` are static exports generated from the
analysis notebook. There is no live Looker Studio URL yet; publishing requires
an authenticated Google account, connecting the cleaned summary data, and
setting the intended sharing permissions. Do not describe the static export as
an interactive dashboard.

## Suggested Looker Studio build

- Scorecards: H1 revenue, distinct orders, average order value.
- Trend: monthly revenue, January to June 2026.
- Breakdowns: revenue by branch and category.
- Controls: date range and branch selector.
- Compare revenue against gross margin and in-stock rate once the business
  supplies those fields.

Verify controls affect all charts and the totals match `03_analysis.ipynb`
before publishing. Share the verified public URL in the README and LMS.
