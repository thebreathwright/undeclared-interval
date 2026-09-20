"""Process an explicit document review manifest through the shared local LRD runner.

Usage: python -m tools.lrd_document_review --manifest FILE --output NEW_DIRECTORY
Use --prepare-only for a hash/coverage preflight with no GPU calls. A live run
requires a fresh output directory; failed and earlier attempts are never erased.
Use --accept-from RUN --meaning-reviews FILE for offline meaning acceptance,
then --read-current SELECTION for current use within a designated selection.
--read-accepted ACCEPTANCE_DIRECTORY replays historical supplied reviews only.
Use --propose-correction-from RUN --corrected-response FILE --author NAME
--reason TEXT --output NEW_FILE to preserve a separately attributed correction.
"""

from __future__ import annotations

import argparse
import copy
import json
import re
import unicodedata
from pathlib import Path
from typing import Any

from brudo.crystalize.question_targets import targeted_source_unit
from brudo.crystalize.research_assay import source_question_instruction
from brudo.domains.legal.lrd.acceptance import (
    ACCEPTED,
    assess_answer_correction,
    assess_review_run,
    checked_tree,
    contained,
    propose_answer_correction,
    read_accepted_answer,
    read_accepted_correction,
)
from brudo.domains.legal.lrd.review import (
    MAX_PROMPT_BYTES,
    REPO,
    encoded,
    review_document_unit,
    save_artifact,
    sha256,
    source_unit,
)
from brudo.evidence_identity import identified


def prepare(root: Path, manifest: dict[str, Any]) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    """Validate all jobs and their declared file coverage before starting any GPU work."""
    if manifest.get("schema") != "brudo-lrd-document-review-v1" or not manifest.get("jobs"):
        raise ValueError("a nonempty LRD document review manifest is required")
    inventory = manifest.get("documents", [])
    declared = {item["path"]: item for item in inventory}
    if not declared or len(declared) != len(inventory):
        raise ValueError("declare each source document exactly once")
    for path, item in declared.items():
        relative = Path(path)
        resolved = (root / relative).resolve()
        if relative.is_absolute() or not resolved.is_relative_to(root.resolve()):
            raise ValueError("declared source path leaves the repository")
        if sha256(resolved.read_bytes()) != item["sha256"]:
            raise ValueError(f"declared source hash mismatch: {path}")
    jobs, seen, spans = [], set(), {path: [] for path in declared}
    for job in manifest["jobs"]:
        identity = job["id"]
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,100}", identity) or identity in seen:
            raise ValueError("review job IDs must be unique safe names")
        seen.add(identity)
        for document in job["documents"]:
            item = declared.get(document["path"])
            if item is None or any(document.get(k) != item.get(k) for k in ("sha256", "role")):
                raise ValueError("job input differs from declared document identity or role")
        unit = source_unit(root, identity, job["documents"])
        # These optional declarations are part of the assigned source contract.
        # Preserve them for the shared validators, runner and assignment replay;
        # dropping them here silently changes what the model is asked to review.
        for field in ("question_targets", "dialogue", "answer_limits"):
            if field in job:
                unit[field] = copy.deepcopy(job[field])
        unit = targeted_source_unit(unit, job["question"])
        prompt = source_question_instruction(unit, job["question"]) + encoded(unit).decode()
        if len(prompt.encode()) > MAX_PROMPT_BYTES:
            raise ValueError(f"job {identity} exceeds input bound; split it explicitly")
        for binding in unit["source_bindings"]:
            spans[binding["path"]].append((binding["start"], binding["end"]))
        jobs.append((job, unit))
    for path, item in declared.items():
        # Required ranges support an explicitly scoped excerpt; the default is the whole file.
        text = (root / path).read_text(encoding="utf-8")
        start, end = item.get("start", 0), item.get("end", len(text))
        if type(start) is not int or type(end) is not int or not 0 <= start < end <= len(text):
            raise ValueError(f"invalid declared coverage: {path}")
        covered = start
        for a, b in sorted(spans[path]):
            if a > covered:
                break
            covered = max(covered, b)
        if covered < end:
            raise ValueError(f"uncovered declared source text: {path}, from character {covered}")
    return jobs


def process(
    root: Path, manifest_path: Path, output: Path, *, prepare_only: bool = False
) -> dict[str, Any]:
    manifest_bytes = manifest_path.read_bytes()
    manifest = json.loads(manifest_bytes)
    jobs = prepare(root, manifest)
    output.mkdir(parents=True, exist_ok=False)
    save_artifact(output / "INPUT_MANIFEST.json", manifest_bytes)
    save_artifact(output / "EXECUTOR.py", Path(__file__).read_bytes())
    receipts = []
    for job, unit in jobs:
        save_artifact(output / (job["id"] + ".source.json"), encoded(unit))
    for job, unit in jobs:
        if prepare_only:
            result = {"execution_status": "PREPARED_NOT_RUN", "semantic_review": "NOT_RUN"}
        else:
            # Detect source edits made since preflight, without using replacement bytes.
            try:
                for source in unit["source_bindings"]:
                    if sha256((root / source["path"]).read_bytes()) != source["sha256"]:
                        raise ValueError(f"source changed after preflight: {source['path']}")
                print(json.dumps({"job": job["id"], "event": "STARTING"}), flush=True)
                result = review_document_unit(unit, job["question"], output=output / job["id"])
            except Exception as error:
                result = {
                    "execution_status": "FAILED",
                    "error": str(error),
                    "semantic_review": "NOT_RUN",
                }
        receipt = {
            "job": job["id"],
            "paragraph_ids": [p["paragraph_id"] for p in unit["paragraphs"]],
            **result,
        }
        save_artifact(output / (job["id"] + ".receipt.json"), encoded(receipt))
        receipts.append(receipt)
        print(json.dumps({"job": job["id"], "event": result["execution_status"]}), flush=True)
    completed = sum(r["execution_status"] == "RESPONSE_VERIFIED" for r in receipts)
    result = {
        "input_manifest_sha256": sha256(manifest_bytes),
        "documents": len(manifest["documents"]),
        "jobs": len(jobs),
        "verified_responses": completed,
        "failed_jobs": [r["job"] for r in receipts if r["execution_status"] == "FAILED"],
        "status": "PREPARED_NOT_RUN"
        if prepare_only
        else ("RESPONSES_COMPLETE" if completed == len(jobs) else "PARTIAL"),
        "semantic_review": "REQUIRED",
        "accepted_answers": 0,
        "answer_acceptance": "NOT_ASSESSED",
        "legal_acceptance": "NOT_ASSERTED",
        "canon_effect": "NONE",
        "receipts": receipts,
    }
    save_artifact(output / "COVERAGE.json", encoded(result))
    files = [
        {"path": p.relative_to(output).as_posix(), "sha256": sha256(p.read_bytes())}
        for p in sorted(output.rglob("*"))
        if p.is_file()
    ]
    save_artifact(output / "MANIFEST.json", encoded({"files": files}))
    return result


def _original_jobs(root: Path, run: Path) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    checked_tree(run)
    manifest = json.loads((run / "INPUT_MANIFEST.json").read_bytes())
    jobs = prepare(root, manifest)
    for job, unit in jobs:
        if json.loads((run / (job["id"] + ".source.json")).read_bytes()) != unit:
            raise ValueError("original job projection differs from its requested source coverage")
    return jobs


def _job_contract(run: Path, job: dict[str, Any], unit: dict[str, Any]) -> None:
    if json.loads((run / "SOURCE.json").read_bytes()) != unit:
        raise ValueError("executed source unit differs from the original assigned job")
    if (run / "QUESTION.txt").read_bytes().decode("utf-8") != unicodedata.normalize(
        "NFC", job["question"]
    ):
        raise ValueError("executed question differs from the original assigned job")


def _assess_job(
    root: Path,
    run: Path,
    job: dict[str, Any],
    unit: dict[str, Any],
    meaning: dict[str, Any] | None,
    correction: dict[str, Any] | None,
) -> dict[str, Any]:
    """Bind either answer route to the same complete original assigned job."""
    kind = "lrd-source-answer-admission"
    if correction is None:
        decision = assess_review_run(root, run, meaning)
    else:
        kind = "lrd-source-answer-correction-admission"
        decision = assess_answer_correction(root, correction, meaning)
    try:
        _job_contract(run, job, unit)
        if correction is not None and decision["content"]["run"] not in {
            None,
            run.relative_to(root).as_posix(),
        }:
            raise ValueError("correction predecessor differs from the original assigned job")
    except Exception as error:
        decision = identified(
            kind,
            {
                **decision["content"],
                "status": "BLOCKED",
                "review_state": "INVALID_OR_FAILED_RUN",
                "reason": str(error),
            },
        )
    return decision


def _bound_inputs(root: Path, inputs: dict[str, Any], label: str) -> dict[str, bytes]:
    supplied = {}
    for identity, binding in inputs.items():
        relative = Path(binding["path"])
        if relative.is_absolute():
            raise ValueError(f"{label} path must be relative")
        body = contained(root, root / relative).read_bytes()
        if sha256(body) != binding["sha256"]:
            raise ValueError(f"{label} bytes differ: {identity}")
        supplied[identity] = body
    return supplied


def _captured_input(body: bytes, label: str) -> Any:
    """Keep invalid input identifiable; it must not choose the original-answer route."""
    try:
        value = json.loads(body)
        if label == "review" or isinstance(value, dict):
            return value
    except (ValueError, UnicodeDecodeError):
        pass
    return {f"invalid_{label}_artifact_sha256": sha256(body)}


def _output_enters_preserved_tree(root: Path, source: Path, output: Path) -> bool:
    """Protect this run and its nearest enclosing sealed assignment tree."""
    protected = source
    for parent in source.parents:
        if not parent.is_relative_to(root.resolve()):
            break
        if (parent / "INPUT_MANIFEST.json").is_file() and (parent / "MANIFEST.json").is_file():
            protected = parent
            break
    return output == protected or output.is_relative_to(protected)


def accept(root: Path, run: Path, meaning_manifest: Path, output: Path) -> dict[str, Any]:
    """Review all original jobs offline; omission never creates a passing subset."""
    root, run = root.resolve(), contained(root, run)
    jobs = _original_jobs(root, run)
    raw = meaning_manifest.read_bytes()
    request = json.loads(raw)
    if request.get("schema") != "brudo-lrd-meaning-reviews-v1":
        raise ValueError("an explicit LRD meaning-review manifest is required")
    original = request.get("input_run")
    if original != {
        "path": run.relative_to(root).as_posix(),
        "manifest_sha256": sha256((run / "MANIFEST.json").read_bytes()),
    }:
        raise ValueError("meaning reviews are not bound to the exact original run")
    reviews = request.get("reviews")
    identities = {job["id"] for job, _ in jobs}
    if not isinstance(reviews, dict) or set(reviews) - identities:
        raise ValueError("meaning review identities differ from the requested job set")
    corrections = request.get("corrections", {})
    if not isinstance(corrections, dict) or set(corrections) - identities:
        raise ValueError("correction identities differ from the requested job set")
    # Validate supplied custody before writing. Missing entries are preserved below.
    supplied = _bound_inputs(root, reviews, "meaning review")
    supplied_corrections = _bound_inputs(root, corrections, "correction")
    output = contained(root, output)
    if output == run or output.is_relative_to(run):
        raise ValueError("acceptance must be outside the immutable original run")
    output.mkdir(parents=True, exist_ok=False)
    save_artifact(output / "MEANING_MANIFEST.json", raw)
    save_artifact(output / "INPUT_MANIFEST.json", (run / "INPUT_MANIFEST.json").read_bytes())
    dispositions = []
    for job, unit in jobs:
        identity = job["id"]
        body = supplied.get(identity)
        meaning = None
        if body is not None:
            save_artifact(output / f"{identity}.meaning.json", body)
            meaning = _captured_input(body, "review")
        correction = None
        if identity in supplied_corrections:
            body = supplied_corrections[identity]
            save_artifact(output / f"{identity}.correction.json", body)
            correction = _captured_input(body, "correction")
        decision = _assess_job(root, run / identity, job, unit, meaning, correction)
        save_artifact(output / f"{identity}.admission.json", encoded(decision))
        dispositions.append(
            {
                "job": identity,
                "question_sha256": sha256(job["question"].encode()),
                "target_ids": [row["id"] for row in unit["question_targets"]],
                "source_unit_sha256": sha256(encoded(unit)),
                "admission_id": decision["id"],
                "status": decision["content"]["status"],
                "review_state": decision["content"]["review_state"],
            }
        )
    result = {
        "schema": "brudo-lrd-document-answer-acceptance-v1",
        "input_run": original,
        "meaning_manifest_sha256": sha256(raw),
        "jobs": dispositions,
        "accepted_jobs": [row["job"] for row in dispositions if row["status"] == ACCEPTED],
        "unresolved_jobs": [row["job"] for row in dispositions if row["status"] != ACCEPTED],
        "legal_acceptance": "NOT_ASSERTED",
        "canon_effect": "NONE",
    }
    result["status"] = (
        "ANSWERS_ACCEPTED_WITHIN_REVIEW" if not result["unresolved_jobs"] else "PARTIAL"
    )
    save_artifact(output / "ACCEPTANCE.json", encoded(result))
    files = [
        {"path": p.relative_to(output).as_posix(), "sha256": sha256(p.read_bytes())}
        for p in sorted(output.rglob("*"))
        if p.is_file()
    ]
    save_artifact(output / "MANIFEST.json", encoded({"files": files}))
    return result


def read_accepted_batch(
    root: Path, directory: Path, *, require_complete: bool = True
) -> dict[str, Any]:
    """Consume accepted text after replay of the complete original assignment."""
    root, directory = root.resolve(), contained(root, directory)
    checked_tree(directory)
    result = json.loads((directory / "ACCEPTANCE.json").read_bytes())
    meaning_bytes = (directory / "MEANING_MANIFEST.json").read_bytes()
    meaning_manifest = json.loads(meaning_bytes)
    if (
        sha256(meaning_bytes) != result["meaning_manifest_sha256"]
        or meaning_manifest.get("input_run") != result["input_run"]
    ):
        raise ValueError("acceptance meaning manifest binding differs")
    run = contained(root, root / result["input_run"]["path"])
    jobs = _original_jobs(root, run)
    if checked_tree(run) != result["input_run"]["manifest_sha256"]:
        raise ValueError("original run changed after acceptance")
    if (run / "INPUT_MANIFEST.json").read_bytes() != (
        directory / "INPUT_MANIFEST.json"
    ).read_bytes():
        raise ValueError("acceptance changed original assignment coverage")
    if [row["job"] for row in result["jobs"]] != [job["id"] for job, _ in jobs]:
        raise ValueError("acceptance omits or reorders original jobs")
    corrections = meaning_manifest.get("corrections", {})
    identities = {job["id"] for job, _ in jobs}
    if not isinstance(corrections, dict) or set(corrections) - identities:
        raise ValueError("correction identities differ from the requested job set")
    answers, unresolved = {}, []
    for (job, unit), row in zip(jobs, result["jobs"], strict=True):
        if (
            row["target_ids"] != [target["id"] for target in unit["question_targets"]]
            or row["source_unit_sha256"] != sha256(encoded(unit))
            or row["question_sha256"] != sha256(job["question"].encode())
        ):
            raise ValueError("acceptance changed question targets or source coverage")
        receipt = json.loads((directory / f"{job['id']}.admission.json").read_bytes())
        meaning_binding = meaning_manifest["reviews"].get(job["id"])
        if meaning_binding is None:
            expected_meaning = None
        else:
            captured = (directory / f"{job['id']}.meaning.json").read_bytes()
            if sha256(captured) != meaning_binding["sha256"]:
                raise ValueError("captured meaning review differs from its declared source")
            expected_meaning = _captured_input(captured, "review")
        correction = None
        if job["id"] in corrections:
            captured = (directory / f"{job['id']}.correction.json").read_bytes()
            if sha256(captured) != corrections[job["id"]]["sha256"]:
                raise ValueError("captured correction differs from its declared source")
            correction = _captured_input(captured, "correction")
        if receipt["content"].get("meaning_review") != expected_meaning:
            raise ValueError("admission does not bind the supplied meaning review")
        if receipt["id"] != row["admission_id"]:
            raise ValueError("acceptance decision identity differs")
        if (
            receipt["content"]["status"] != row["status"]
            or receipt["content"]["review_state"] != row["review_state"]
            or _assess_job(root, run / job["id"], job, unit, expected_meaning, correction)
            != receipt
        ):
            raise ValueError("acceptance decision does not bind this job and disposition")
        if receipt["content"]["status"] == ACCEPTED:
            _job_contract(run / job["id"], job, unit)
            answers[job["id"]] = (
                read_accepted_answer(root, receipt)
                if correction is None
                else read_accepted_correction(root, receipt)
            )
        else:
            unresolved.append(
                {"job": job["id"], "review_state": receipt["content"]["review_state"]}
            )
    if require_complete and unresolved:
        raise ValueError("original assignment has unresolved answer reviews")
    if result["accepted_jobs"] != list(answers) or result["unresolved_jobs"] != [
        item["job"] for item in unresolved
    ]:
        raise ValueError("acceptance summary differs from replayed job coverage")
    return {
        "answers": answers,
        "unresolved": unresolved,
        "original_jobs": [job["id"] for job, _ in jobs],
        "complete_within_declared_reviews": not unresolved,
        "current_admission": False,
        "replay_scope": "HISTORICAL_BOUND_REVIEW",
        "legal_acceptance": "NOT_ASSERTED",
        "canon_effect": "NONE",
    }


def _selection_json(raw: bytes) -> dict[str, Any]:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError("duplicate selection JSON key")
            result[key] = value
        return result

    value = json.loads(raw, object_pairs_hook=pairs)
    if not isinstance(value, dict):
        raise ValueError("selection dependency must be an object")
    return value


def _selection_binding(root: Path, binding: dict[str, Any]) -> bytes:
    if not isinstance(binding, dict) or set(binding) != {"path", "sha256"}:
        raise ValueError("selection dependency requires exact path and SHA-256")
    relative = Path(binding["path"])
    if relative.is_absolute():
        raise ValueError("selection dependency path must be relative")
    body = contained(root, root / relative).read_bytes()
    if sha256(body) != binding["sha256"]:
        raise ValueError("selection dependency bytes changed")
    return body


def _replay_selection_admission(root: Path, receipt: dict[str, Any]) -> dict[str, Any]:
    body = receipt.get("content", {})
    if body.get("schema") == "brudo.lrd-source-answer-admission.v1":
        current = assess_review_run(root, root / body["run"], body.get("meaning_review"))
    elif body.get("schema") == "brudo.lrd-source-answer-correction-admission.v1":
        current = assess_answer_correction(root, body.get("proposal"), body.get("meaning_review"))
    else:
        raise ValueError("unknown selection admission kind")
    if current != receipt or body.get("review_state") not in {
        "ALL_DECLARED_CHECKS_PASSED",
        "ADVERSE",
        "UNKNOWN",
    }:
        raise ValueError("selection revision has no replayable meaning assessment")
    return body


def _current_selection_context(
    root: Path, directory: Path, revisions: list[dict[str, Any]]
) -> tuple[dict[str, Any], dict[str, Any]]:
    root, directory = root.resolve(), contained(root, directory)
    if not isinstance(revisions, list):
        raise ValueError("review revisions must be an explicit list")
    manifest_sha = checked_tree(directory)
    batch = _selection_json((directory / "ACCEPTANCE.json").read_bytes())
    run = contained(root, root / batch["input_run"]["path"])
    allowed_runs = {str((run / row["job"]).relative_to(root)) for row in batch["jobs"]}
    retired_admissions, retired_reviews, edges = set(), set(), {}
    for revision in revisions:
        if not isinstance(revision, dict) or set(revision) != {
            "prior_admission",
            "revised_admission",
        }:
            raise ValueError("review revision requires prior and revised admissions")
        receipts = [
            _selection_json(_selection_binding(root, revision[key]))
            for key in ("prior_admission", "revised_admission")
        ]
        old, new = [_replay_selection_admission(root, receipt) for receipt in receipts]
        if old["bindings"] != new["bindings"] or old["run"] not in allowed_runs:
            raise ValueError("review revision changes the original assignment or predecessor")
        effective = [
            body.get("corrected_response_sha256", body["bindings"]["response_sha256"])
            for body in (old, new)
        ]
        if effective[0] != effective[1]:
            raise ValueError("review revision changes the effective reviewed response")
        before, after = (body["meaning_review"]["id"] for body in (old, new))
        if before == after or before in retired_reviews:
            raise ValueError("review revision is unchanged or has competing successors")
        retired_admissions.add(receipts[0]["id"])
        retired_reviews.add(before)
        edges[before] = after
    for start in edges:
        seen, node = set(), start
        while node in edges:
            if node in seen:
                raise ValueError("review revision cycle")
            seen.add(node)
            node = edges[node]
    answer = read_accepted_batch(root, directory)
    for value in answer["answers"].values():
        if (
            value["admission_id"] in retired_admissions
            or value["meaning_review_id"] in retired_reviews
        ):
            raise ValueError("selected answer uses a withdrawn admission or meaning review")
    record = identified(
        "lrd-current-answer-selection",
        {
            "schema": "brudo.lrd-current-answer-selection.v1",
            "input_run": batch["input_run"],
            "acceptance": {
                "path": directory.relative_to(root).as_posix(),
                "manifest_sha256": manifest_sha,
            },
            "review_revisions": revisions,
            "reader_sha256": sha256(Path(__file__).read_bytes()),
            "purpose": "local_research",
            "scope": "Current within this explicitly designated selection and review frontier; "
            "not a global latest-state discovery or release authority.",
        },
    )
    _recheck_selection_context(root, directory, record)
    return record, answer


def _recheck_selection_context(root: Path, directory: Path, record: dict[str, Any]) -> None:
    body = record["content"]
    if checked_tree(directory) != body["acceptance"]["manifest_sha256"]:
        raise ValueError("selected acceptance changed during read")
    run = contained(root, root / body["input_run"]["path"])
    if checked_tree(run) != body["input_run"]["manifest_sha256"]:
        raise ValueError("original assignment changed during read")
    _original_jobs(root, run)  # Recheck the actual outside source bytes as well.
    for revision in body["review_revisions"]:
        for binding in revision.values():
            _selection_binding(root, binding)
    if sha256(Path(__file__).read_bytes()) != body["reader_sha256"]:
        raise ValueError("selection reader changed during read")


def select_current_batch(
    root: Path, directory: Path, review_revisions: list[dict[str, Any]]
) -> dict[str, Any]:
    """Construct a checked research selection; caller designates its current use."""
    return _current_selection_context(root, directory, review_revisions)[0]


def read_current_batch(root: Path, directory: Path, selection_path: Path) -> dict[str, Any]:
    """Read within the exact designated frontier, never from a historical label alone."""
    root, directory = root.resolve(), contained(root, directory)
    selection_path = contained(root, selection_path)
    raw = selection_path.read_bytes()
    selected = _selection_json(raw)
    body = selected.get("content", {})
    if body.get("acceptance", {}).get("path") != directory.relative_to(root).as_posix():
        raise ValueError("requested acceptance differs from current selection")
    replay, answer = _current_selection_context(root, directory, body.get("review_revisions"))
    if replay != selected:
        raise ValueError("current selection no longer replays against its dependencies")
    if selection_path.read_bytes() != raw:
        raise ValueError("current selection changed during read")
    return {
        **answer,
        "current_admission": True,
        "replay_scope": "CURRENT_WITHIN_DESIGNATED_SELECTION",
        "current_selection": {
            "path": selection_path.relative_to(root).as_posix(),
            "sha256": sha256(raw),
            "id": selected["id"],
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--manifest", type=Path)
    mode.add_argument("--accept-from", type=Path)
    mode.add_argument("--read-accepted", type=Path)
    mode.add_argument("--read-current", type=Path)
    mode.add_argument("--propose-correction-from", type=Path)
    parser.add_argument("--meaning-reviews", type=Path)
    parser.add_argument("--corrected-response", type=Path)
    parser.add_argument("--author")
    parser.add_argument("--reason")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--prepare-only", action="store_true")
    args = parser.parse_args()
    if args.propose_correction_from:
        if (
            args.corrected_response is None
            or not args.author
            or not args.reason
            or args.meaning_reviews is not None
            or args.prepare_only
        ):
            parser.error(
                "--propose-correction-from requires --corrected-response, --author and "
                "--reason; it proposes an offline correction, not acceptance"
            )
        run = contained(REPO, args.propose_correction_from)
        output = contained(REPO, args.output)
        if _output_enters_preserved_tree(REPO, run, output):
            parser.error("a correction must be outside the immutable original run and batch")
        response = args.corrected_response.read_bytes().decode("utf-8")
        proposal = propose_answer_correction(REPO, run, response, args.author, args.reason)
        output.parent.mkdir(parents=True, exist_ok=True)
        save_artifact(output, encoded(proposal))
        print(json.dumps({"correction_id": proposal["id"], "status": "PROPOSED_NOT_ACCEPTED"}))
        return
    if args.corrected_response is not None or args.author is not None or args.reason is not None:
        parser.error("correction arguments require --propose-correction-from")
    if args.read_current:
        if args.meaning_reviews is not None or args.prepare_only:
            parser.error("--read-current replays its designated selection and review frontier")
        selected = _selection_json(args.read_current.read_bytes())
        directory = contained(REPO, REPO / selected["content"]["acceptance"]["path"])
        result = read_current_batch(REPO, directory, args.read_current)
        output = contained(REPO, args.output)
        original = contained(REPO, REPO / selected["content"]["input_run"]["path"])
        if any(
            _output_enters_preserved_tree(REPO, source, output) for source in (directory, original)
        ):
            parser.error("an answer export must be outside its preserved acceptance and run trees")
        save_artifact(output, encoded(result))
        print(
            json.dumps(
                {
                    "current_answers": len(result["answers"]),
                    "selection": result["current_selection"],
                }
            ),
            flush=True,
        )
        return
    if args.accept_from:
        if args.meaning_reviews is None or args.prepare_only:
            parser.error("--accept-from requires --meaning-reviews and is an offline operation")
        result = accept(REPO, args.accept_from, args.meaning_reviews, args.output)
        print(json.dumps(result), flush=True)
        if result["unresolved_jobs"]:
            raise SystemExit(1)
        return
    if args.read_accepted:
        if args.meaning_reviews is not None or args.prepare_only:
            parser.error("--read-accepted replays the already bound reviews")
        directory = contained(REPO, args.read_accepted)
        output = contained(REPO, args.output)
        result = read_accepted_batch(REPO, directory)
        assignment = json.loads((directory / "ACCEPTANCE.json").read_bytes())["input_run"]["path"]
        original = contained(REPO, REPO / assignment)
        if any(
            _output_enters_preserved_tree(REPO, source, output) for source in (directory, original)
        ):
            parser.error("an answer export must be outside its preserved acceptance and run trees")
        save_artifact(output, encoded(result))
        print(
            json.dumps(
                {
                    "accepted_answers": len(result["answers"]),
                    "current_admission": False,
                    "replay_scope": result["replay_scope"],
                }
            ),
            flush=True,
        )
        return
    if args.meaning_reviews is not None:
        parser.error("--meaning-reviews requires --accept-from")
    result = process(REPO, args.manifest, args.output, prepare_only=args.prepare_only)
    print(json.dumps({k: v for k, v in result.items() if k != "receipts"}), flush=True)
    if result["failed_jobs"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
