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

## Effect

The r2 snapshot's ledger does not fully verify as delivered: 17 listed files
verify and one listed compiled-cache file is absent. This finding does not
change the bytes or stated provenance of the 17 verified records.

## Disposition

`kit_r2_snapshot/` is retained unchanged as source evidence. The successor
package must use its own hash ledger and must not represent the r2 ledger as a
complete verification of the delivered snapshot.
