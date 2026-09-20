# Content Manifest v1

## Scope

This manifest records additions made after the preserved r2 release snapshot.
It does not amend or recertify `kit_r2_snapshot/`, whose own manifest and hash
ledger remain its record.

| Path | Purpose | SHA-256 |
|---|---|---|
| `AUTISM/AUTISM_PAPER_REWRITE.v1.md` | Evidence-bound rewrite of the supplied autism paper | `abcf7dee071d00aec059d26f1190d600eac625f1f96e5158c619c6e74fefbd29` |
| `AUTISM/README.md` | Autism-set scope and source provenance | Recorded in `SHA256SUMS.v1` |
| `TRAINING/iPAP Beginner Program SUMMARY.pdf` | Separate source training material | `beda69ac4ad8ede03424237e0cdec69d68e374bd152a5e46c3932dc67c467ff1` |
| `TRAINING/iPAP Beginner Program SUMMARY.pdf.txt` | Reading copy of the training PDF | `36a43690b42b97b3e162785be81ab906b453ede764117de3b0b45e9b51115796` |
| `TRAINING/README.md` | Separation statement | Recorded in `SHA256SUMS.v1` |
| `TRAINING/LICENSE_AND_ACCESS.md` | $299 company and $599 military/military-support terms | Recorded in `SHA256SUMS.v1` |
| `PACKAGE_INTEGRITY_FINDING.v1.md` | Delivered-r2 ledger mismatch and disposition | Recorded in `SHA256SUMS.v1` |
| `verify_public_package.py` | Offline package verifier with an explicit `UNRUN` list | Recorded in `SHA256SUMS.v1` |
| `GRAx_AUDIT_MANIFEST.v1.json` | Five-file source contract for the local audit | Recorded in `SHA256SUMS.v1` |
| `GRAx_AUDIT_RUN.v1/` | Two routed Grax responses, frozen receipts, and SHA-256 sidecars | Internal run manifest and `SHA256SUMS.v1` |
| `GRAx_AUDIT_READBACK.v1.md` | Human readback of what the model result does and does not establish | Recorded in `SHA256SUMS.v1` |
| `GRAx_DIRECT_BATCH_FAILURE.v1.md` | Preserved failed preflight before route-custody repair | Recorded in `SHA256SUMS.v1` |
| `RELEASE_CLOSURE_TEMPLATE.v1.md` | Required shipment and remote-retrieval evidence for all four ways | Recorded in `SHA256SUMS.v1` |
| `RELEASE_CLOSURE_RECORD.v1.md` | Verified GitHub v4, v8, and v9 release records and outstanding channels | Recorded in `SHA256SUMS.v1` |
| `PACKAGE_REPAIR_LOG.v1.md` | Closed package defects and their verification predicates | Recorded in `SHA256SUMS.v1` |
| `channels/INTERNET_ARCHIVE.md` | Complete-document Archive.org upload and retrieval contract | Recorded in `SHA256SUMS.v1` |
| `notices/SUPERSESSION_NOTE.md` | Send-ready correction note with a verified GitHub archive, independent of Zenodo DOI status | Recorded in `SHA256SUMS.v1` |

## Boundaries Checked By Code

`verify_public_package.py` checks that the autism set contains no source
training file, that the training material is present only in `TRAINING/`, that
the stated prices are present, and that the listed source hashes match. It also
checks every available r2 snapshot hash. Its `UNRUN` output records what those
checks do not assess.

The source-delivered r2 ledger listed a compiled Python cache file that the
supplied archive did not contain. It is preserved as
`kit_r2_snapshot/SHA256SUMS.source-delivered.txt`; the active r2 ledger removes
that entry and passes. See `PACKAGE_INTEGRITY_FINDING.v1.md`.

## License Boundary

The root `LICENSE` applies to the original open-evidence release material. It
does not apply to the two files under `TRAINING/`; their source rights notice
and `TRAINING/LICENSE_AND_ACCESS.md` govern them.
