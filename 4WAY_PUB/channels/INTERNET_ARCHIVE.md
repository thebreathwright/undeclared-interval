# Internet Archive Item

## Upload Object

Upload the final sealed `4WAY_PUB_COMPLETE_v*.zip` and its matching
`.zip.sha256` sidecar together. Do not upload a working directory, an earlier
archive, or a chart/generated file without its generator and a verified hash.

## Required Item Metadata

| Field | Value |
|---|---|
| Identifier | Choose an unused stable identifier; record it in release closure |
| Title | *An Undeclared Measurement Interval* |
| Creator | Bruce Wright |
| Date | Date of the final sealed archive |
| Collection | Chosen by the authorized account |
| Description | Methods package. Read corrections before findings. No clinical or legal conclusion. |
| License | CC0 only for files covered by the root license; training files retain their own terms. |

## Verification

After upload, retrieve the ZIP from the item URL, compute SHA-256, compare it
to the uploaded sidecar, run `verify_public_package.py` against extracted
bytes, and record all results in `RELEASE_CLOSURE_TEMPLATE.v1.md`.
