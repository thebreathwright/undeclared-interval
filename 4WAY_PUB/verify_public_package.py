#!/usr/bin/env python3
"""Verify package boundaries and recorded bytes without network access."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
TRAINING = ROOT / "TRAINING"
AUTISM = ROOT / "AUTISM"
EXPECTED = {
    TRAINING / "iPAP Beginner Program SUMMARY.pdf": (
        "beda69ac4ad8ede03424237e0cdec69d68e374bd152a5e46c3932dc67c467ff1"
    ),
    TRAINING / "iPAP Beginner Program SUMMARY.pdf.txt": (
        "36a43690b42b97b3e162785be81ab906b453ede764117de3b0b45e9b51115796"
    ),
    AUTISM / "AUTISM_PAPER_REWRITE.v1.md": (
        "abcf7dee071d00aec059d26f1190d600eac625f1f96e5158c619c6e74fefbd29"
    ),
}
REQUIRED_AUTISM = {"AUTISM_PAPER_REWRITE.v1.md", "README.md"}
REQUIRED_TRAINING = {
    "iPAP Beginner Program SUMMARY.pdf",
    "iPAP Beginner Program SUMMARY.pdf.txt",
    "README.md",
    "LICENSE_AND_ACCESS.md",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def check(condition: bool, message: str) -> bool:
    print(f"{'PASS' if condition else 'FAIL'} {message}")
    return condition


def verify_ledger(ledger: Path, base: Path, label: str) -> bool:
    passed = True
    for line in ledger.read_text(encoding="utf-8").splitlines():
        expected, relative = line.split(maxsplit=1)
        path = base / relative.removeprefix("./")
        passed &= check(path.is_file() and sha256(path) == expected, f"{label} {relative}")
    return passed


def verify_json_manifest(manifest_path: Path, base: Path, label: str) -> bool:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    passed = True
    for entry in manifest["files"]:
        path = base / entry["path"]
        passed &= check(
            path.is_file() and sha256(path) == entry["sha256"],
            f"{label} {entry['path']}",
        )
    return passed


def main() -> int:
    passed = True
    passed &= check(AUTISM.is_dir(), "autism directory exists")
    passed &= check(TRAINING.is_dir(), "training directory exists")
    passed &= check(
        (ROOT / "RELEASE_CLOSURE_TEMPLATE.v1.md").is_file(),
        "four-way release-closure record exists",
    )
    passed &= check(
        (ROOT / "channels" / "INTERNET_ARCHIVE.md").is_file(),
        "Internet Archive complete-document channel exists",
    )
    passed &= check(
        {path.name for path in AUTISM.iterdir() if path.is_file()} >= REQUIRED_AUTISM,
        "autism set has its rewrite and scope file",
    )
    passed &= check(
        {path.name for path in TRAINING.iterdir() if path.is_file()} >= REQUIRED_TRAINING,
        "training set has source, reading copy, scope, and terms",
    )
    passed &= check(
        not any("ipap" in path.name.lower() for path in AUTISM.rglob("*")),
        "no training source is in the autism set",
    )
    for path, expected in EXPECTED.items():
        passed &= check(path.is_file() and sha256(path) == expected, f"sha256 {path.relative_to(ROOT)}")

    terms = (TRAINING / "LICENSE_AND_ACCESS.md").read_text(encoding="utf-8")
    passed &= check("$299 USD" in terms, "company price is $299")
    passed &= check("$599 USD" in terms, "military and military-support price is $599")
    audit_root = ROOT / "GRAx_AUDIT_RUN.v1"
    coverage = json.loads((audit_root / "COVERAGE.json").read_text(encoding="utf-8"))
    passed &= check(coverage["verified_responses"] == 2, "two routed Grax responses verified")
    passed &= check(not coverage["failed_jobs"], "Grax audit has no failed jobs")
    passed &= verify_json_manifest(audit_root / "MANIFEST.json", audit_root, "Grax")
    passed &= verify_ledger(ROOT / "SHA256SUMS.v1", ROOT, "v1")
    legacy_passed = verify_ledger(
        ROOT / "kit_r2_snapshot" / "SHA256SUMS.txt",
        ROOT / "kit_r2_snapshot",
        "r2",
    )
    if not legacy_passed:
        print("KNOWN LEGACY FAILURE see PACKAGE_INTEGRITY_FINDING.v1.md")

    print("UNRUN clinical validity, legal enforceability, payment collection, and publication acceptance")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
