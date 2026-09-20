# Zenodo Deposit

**Prepared, not submitted. No DOI exists. Zenodo is independent of the other
three ways.**

## Object

Upload the final sealed package ZIP and its matching `.sha256` sidecar. The
package contains findings, correction records, code, models, the rewritten
autism-paper set, and separately marked training files. Do not describe the
deposit as a clinical finding, a product claim, or a legal conclusion.

## Metadata

| Field | Value |
|---|---|
| Title | *An Undeclared Measurement Interval: signal averaging time in oximetry-based screening, and the prevalence figures that depend on it* |
| Upload type | Dataset |
| Version | 1.0.0 |
| Language | English |
| Creator | Wright, Bruce |
| Keywords | pulse oximetry; signal averaging time; sleep-disordered breathing; pregnancy; screening; measurement standards; reproducibility |
| Access | Choose and record the access setting before publication |

## Description

This is a methods and correction package. Read `corrections/` before
`findings/`. It distinguishes source claims, model output, estimates, and open
questions. It does not establish that screening pregnant people for
sleep-disordered breathing improves outcomes, identify any person's intent, or
make a clinical, legal, or product conclusion.

The package also contains a rewritten autism paper that preserves research
questions about feeding mechanics and measurement without asserting a
feeding-device-to-ASD causal claim. Separate training files carry their own
rights notice and price terms; they are not evidence for the autism paper.

## Rights Boundary

Do not mark the complete deposit CC0 as a single undifferentiated license. The
root license applies to the original open-evidence material; the two training
files retain their own terms. Zenodo applies an open-access license selection to
all files in an open deposit. Choose an access/license setting that accurately
reflects that mixed package, and record the choice in release closure.

## Close This Way

1. Create the deposit and upload the sealed ZIP plus sidecar.
2. Set the metadata and access/license choice above.
3. Publish after the resulting DOI and record URL are available.
4. Retrieve the published ZIP, compare its SHA-256 to the sidecar, run
   `verify_public_package.py` against extracted bytes, and record the result in
   `RELEASE_CLOSURE_TEMPLATE.v1.md`.
5. Add the DOI to a later GitHub closure record and, if useful, the
   supersession note. It does not delay Archive, GitHub, or the notice.
