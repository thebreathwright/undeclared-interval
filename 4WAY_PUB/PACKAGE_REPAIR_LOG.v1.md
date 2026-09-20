# Package Repair Log v1

## Closed Defects

| ID | Defect | Repair | Verification |
|---|---|---|---|
| P01 | Active r2 checksum ledger named an absent `.pyc` file | Removed the absent entry from the active ledger; preserved the supplied ledger as `SHA256SUMS.source-delivered.txt` | Active r2 ledger passes |
| P02 | Current package pages said no GitHub repository existed | Updated the current status, README, channel page, and source-kit wrappers to distinguish r2 history from current GitHub publication | Package verifier rejects the old current-README claim |
| P03 | A failed direct Grax request left an empty response file | Removed the empty file; retained the failure record with prompt hash and daemon error | Package verifier requires the empty artifact to remain absent |
| P04 | The front page made an absolute screening-recommendation statement | Narrowed it to the evidence claim this package can support | Current README checked in package review |
| P05 | Code verification was outside the package verifier | Added execution checks for both reproducible code outputs and all five models | `verify_public_package.py` executes them |
| P06 | Verifier execution created a compiled-cache directory under `code/` | Removed the cache and run all package Python with `-B` | Package verifier rejects any `code/__pycache__` directory |
| P07 | Release instructions treated Archive and Zenodo as dependencies for GitHub and the correction notice | Made all four ways independent; the notice now identifies the verified GitHub archive and a DOI is optional | Package verifier checks the current status and notice wording |

## Historical Records

The source-delivered r2 ledger and the frozen Grax audit remain as historical
records. They are not active package claims or active verification inputs.
