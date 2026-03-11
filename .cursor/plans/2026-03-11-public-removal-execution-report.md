# Public Removal Execution Report

Date: 2026-03-11
Branch: `codex/validate-public-removal`
Mode: approved execution

## Result

Approved removal batch executed successfully.

- Files removed from public branch: 15
- Files intentionally retained: 1
- Retained file: `Soft_Drink_Sales_Sample.xlsx`
- Removal scope matched the approved manifest exactly.
- No directories were removed.
- No history rewrite or force-push was used.

## Removed Files

- `ANZ-TC2U-Marvel_Dashboard.html`
- `Banking_Sample_Data_Set_into_BQ.ipynb`
- `Latitude_Enterprise_Console.html`
- `Latitude_sample.html`
- `Momentum2.html`
- `Momentum_Embed.html`
- `Momentum_Embed_B2B.html`
- `Momentum_Embed_B2B_invoice.html`
- `Momentum_Embed_B2Ba.html`
- `Momentum_Embed_B2C.html`
- `Querying_Tableau's_Metadata_API.ipynb`
- `Test.html`
- `examples/Tab_Workbook_Samples.twb`
- `examples/home_loan_mock_data.py`
- `slack-agentic-enterprise-demo_v2 copy.html`

## Validation

Post-change checks passed:
- 15 approved files are absent from the branch.
- `Soft_Drink_Sales_Sample.xlsx` is still present.
- No remaining repo-internal references were found for:
  - `ANZ-TC2U-Marvel_Dashboard.html`
  - `Banking_Sample_Data_Set_into_BQ.ipynb`
  - `Querying_Tableau's_Metadata_API.ipynb`
  - `examples/Tab_Workbook_Samples.twb`
- `git diff --name-status` shows only the approved 15 deletions.

## Rollback

- Rollback tag: `backup/pre-public-removal-2026-03-11`
- Rollback can be performed by checking out the tag or recreating the branch from it.
