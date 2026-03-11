# Public Removal Validation Report

Date: 2026-03-11
Mode: validation-only
Branch: `codex/validate-public-removal`
Source branch reviewed: `codex/validate-content-move`
Private branch verified: `codex/import-sensitive-content`

## Decision

Current decision: `NO-GO for deletion execution`

Reason:
- This branch is prepared for review only.
- The candidate set has been copied to the approved private destination and parity-checked.
- No public-repo deletions are approved or executed in this branch.

## Candidate Summary

- Candidates reviewed: 16
- Present in source repo: 16/16
- Present in private repo: 16/16
- Hash parity with private copy: 16/16 matched
- Candidates blocked from immediate deletion: 16/16

## Reference Impact

Repo-internal references found:
- `Banking_Sample_Data_Set_into_BQ.ipynb` contains a self-referential Colab badge URL.
- `Querying_Tableau's_Metadata_API.ipynb` contains a self-referential Colab badge URL.
- `AGENTS.md` explicitly names `examples/Tab_Workbook_Samples.twb` in the `Do Not Touch` section.

Assessment:
- The two notebook references are self-contained and disappear with file removal.
- `AGENTS.md` should be updated in the same branch as any future deletion of `examples/Tab_Workbook_Samples.twb` so the policy text remains accurate.

## Candidate States

- `eligible_after_explicit_approval`: 15 files
- `blocked_pending_binary_review`: 1 file

Blocked pending binary review:
- `Soft_Drink_Sales_Sample.xlsx`

## Future Removal Preconditions

All of the following must be true before any deletion run:
- User explicitly approves source-repo removals.
- Removal list matches the approved manifest exactly.
- `Soft_Drink_Sales_Sample.xlsx` receives an explicit keep/remove decision after binary review.
- `AGENTS.md` is updated if `examples/Tab_Workbook_Samples.twb` is removed.
- Deletion run occurs on a separate branch from `codex/validate-content-move`.
- No history rewrite, force-push, or directory-level removal is used.

## Abort Conditions

Stop immediately if any of the following occur:
- A file in the deletion set is missing from the private repo.
- Any hash mismatch appears between source and private copies.
- Any extra file enters the deletion set outside the approved manifest.
- Any new customer-identifiable or ambiguous content is discovered in files not yet reviewed.
- A command proposes directory removal instead of file-exact removal.

## Recommended Next Action

Prepare a separate removal-execution plan that:
- excludes `Soft_Drink_Sales_Sample.xlsx` by default,
- updates `AGENTS.md` in the same branch if `examples/Tab_Workbook_Samples.twb` is removed,
- uses file-exact deletion only,
- and re-runs validation before any push.
