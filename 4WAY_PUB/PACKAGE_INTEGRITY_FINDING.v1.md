# Package Integrity Finding v1

## Finding

The source archive `4WAY_PUB_20260920.zip`, SHA-256
`d466646964ad06fc51d57608f75cd4e907fa03df006ed477f61beb4c1c898de6`,
contains `kit_r2_snapshot/SHA256SUMS.txt`. That ledger lists:

```text
44f8b9a9a236676bd952c23a8036338909cdb01ee75de69c1df418b1fda603c6  ./code/__pycache__/apnea_burden.cpython-310.pyc
```

The corresponding file is absent from both the extracted source archive and
this working package. The same package's `STRIP.md` says compiled Python cache
files must not ship in an integrity manifest.

## Repair

The defective delivered ledger is retained verbatim as
`kit_r2_snapshot/SHA256SUMS.source-delivered.txt`. The active
`kit_r2_snapshot/SHA256SUMS.txt` removes only the absent compiled-cache entry.
It now verifies the 17 delivered files it names.

The source-ledger copy is historical evidence, not the active package verifier.
The successor package uses `SHA256SUMS.v1` for the complete tree.
