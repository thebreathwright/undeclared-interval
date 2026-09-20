# Four-Way Release Closure

This record is blank because no remote publication has been verified. A local
archive, a correction-log entry, and a successful build are not closure.

## Bound Local Object

| Field | Value |
|---|---|
| Package archive | Fill from the final sealed archive |
| Package SHA-256 | Fill from the final sealed archive |
| Internal successor ledger | `SHA256SUMS.v1` |
| Local verifier | `verify_public_package.py` |
| Local status | Verified; inherited r2 cache-entry mismatch remains recorded in `PACKAGE_INTEGRITY_FINDING.v1.md` |

## Closure Rule

For each way, record all of the following before calling it closed:

1. The uploaded archive SHA-256 and internal ledger SHA-256.
2. The immutable remote identifier or URL.
3. A fresh retrieval of the remote object, its SHA-256, and retrieval time.
4. The verifier command and its exit status against the retrieved bytes.
5. The actor who performed the remote action.

`CLOSED` means all five fields are present and agree. `DRAFTED`, `UPLOADED`,
and `CHECKED_LOCALLY` are not synonyms for `CLOSED`.

## Way Records

| Way | Required remote object | Current state | Closure evidence |
|---|---|---|---|
| 1 Internet Archive | Complete ZIP item and retrieved bytes | DRAFTED | Not yet recorded |
| 2 GitHub | Public repository, commit, and tag | DRAFTED | Not yet recorded |
| 3 Zenodo | Published deposit and DOI | DRAFTED | Not yet recorded |
| 4 Notice | Sent supersession notice with DOI | DRAFTED | Not yet recorded |

## Correction-Shipment Rule

A correction that changes generated content is open until this record identifies
the generator hash, generated-data hash, rendered-object hash, and the remote
object that was retrieved and checked. A correction log may describe a defect;
it does not prove that the public object changed.
