"""Shared, local Grax execution for LRD document and infrastructure reviews.

The executor preserves exact requests, responses, source identities and failed
attempts. A valid response remains a proposed reading requiring semantic review;
it cannot accept an LRD assignment, authenticate an exhibit, or promote Canon.
Existing queue/custody/legal/red-team/integration stages remain independent.
"""

from __future__ import annotations

import hashlib
import io
import json
import subprocess
import threading
import unicodedata
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any
from uuid import uuid4

from brudo.brullama_grax_lookup import (
    build_predeclared_crystal_assay_bundle_from_text,
    is_prompt_bound_predeclared_crystal_assay,
    resolve_exact_grax_routing_bundle_for_model_input,
)
from brudo.brullama_jobs import (
    freeze_successful_job,
    invoke_brullama_budgeted,
    model_facing_route_source,
    verify_frozen_job,
)
from brudo.crystalize.packages import build_admitted_crystal_set
from brudo.crystalize.question_targets import targeted_source_unit
from brudo.crystalize.research_assay import (
    SOURCE_READING_CRYSTALS,
    SOURCE_READING_THINK,
    source_question_instruction,
    source_question_schema,
    validate_source_answer,
)

MODEL = "brullama-grax:8b"
ENDPOINT = "http://127.0.0.1:11435"
DECLARED_TRANSPORT = "CLI_LEAPTOIT_LOOPBACK_127_0_0_1_11435"
REPO = Path(__file__).resolve().parents[5]
MAX_PROMPT_BYTES = 100_000
_GPU_LOCK = threading.Lock()


def sha256(body: bytes) -> str:
    return hashlib.sha256(body).hexdigest()


def encoded(value: object) -> bytes:
    text = json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    return unicodedata.normalize("NFC", text).encode("utf-8")


def save_artifact(path: Path, body: bytes) -> str:
    """Create bytes and their digest exclusively; never replace an earlier run."""
    if path.exists() or path.with_name(path.name + ".sha256").exists():
        raise FileExistsError(path)
    with path.open("xb") as handle:
        handle.write(body)
    digest = sha256(body)
    with path.with_name(path.name + ".sha256").open("x") as handle:
        handle.write(f"{digest}  {path.name}\n")
    return digest


def source_unit(root: Path, unit_id: str, documents: list[dict[str, Any]]) -> dict[str, Any]:
    """Read declared UTF-8 documents/spans and verify hashes before inference.

    Optional start/end bounds are Unicode character offsets into the original
    decoded file. Full file hashes always bind those spans. Normalized semantic
    text has its own hash; it never replaces the original byte identity.
    """
    root = root.resolve()
    if not unit_id.strip() or not documents:
        raise ValueError("a unit identity and source documents are required")
    paragraphs, bindings = [], []
    for index, document in enumerate(documents, 1):
        relative = Path(document["path"])
        path = (root / relative).resolve()
        if relative.is_absolute() or not path.is_relative_to(root):
            raise ValueError("source path must remain relative to the repository")
        body = path.read_bytes()
        digest = sha256(body)
        if digest != document["sha256"]:
            raise ValueError(f"source hash mismatch: {relative}")
        role = document.get("role", "")
        if not isinstance(role, str) or not role.strip():
            raise ValueError("each document requires its representation role")
        text = body.decode("utf-8")
        start, end = document.get("start", 0), document.get("end", len(text))
        if type(start) is not int or type(end) is not int or not 0 <= start < end <= len(text):
            raise ValueError(f"invalid or empty source span: {relative}")
        selected = unicodedata.normalize("NFC", text[start:end])
        # Preserve every character, including whitespace. Do not truncate long paragraphs.
        pieces = selected.splitlines(keepends=True)
        current, chunks = "", []
        for piece in pieces:
            if current and len(current) + len(piece) > 3500:
                chunks.append(current)
                current = ""
            current += piece
        if current:
            chunks.append(current)
        if "".join(chunks) != selected:
            raise ValueError("source projection lost text")
        for number, chunk in enumerate(chunks, 1):
            paragraphs.append(
                {
                    "paragraph_id": f"D{index:02}_P{number:03}",
                    "text": chunk,
                    "source_path": relative.as_posix(),
                    "source_sha256": digest,
                    "source_role": role,
                }
            )
        bindings.append(
            {
                "path": relative.as_posix(),
                "sha256": digest,
                "bytes": len(body),
                "role": role,
                "start": start,
                "end": end,
                "whole_file": start == 0 and end == len(text),
                "selected_nfc_sha256": sha256(selected.encode()),
            }
        )
    return {
        "unit_id": unit_id,
        "whole_document": all(item["whole_file"] for item in bindings),
        "scope": "Only the named files or explicit spans; linked sources are not fetched.",
        "source_bindings": bindings,
        "paragraphs": paragraphs,
    }


def _healthcheck(directory: Path) -> None:
    commands = (
        ("make", ["make", "brullama-healthcheck"]),
        ("version", ["curl", "-fsS", ENDPOINT + "/api/version"]),
    )
    for label, command in commands:
        result = subprocess.run(command, cwd=REPO, capture_output=True, timeout=45)
        save_artifact(directory / f"HEALTH.{label}.stdout", result.stdout)
        save_artifact(directory / f"HEALTH.{label}.stderr", result.stderr)
        if result.returncode:
            raise RuntimeError(f"local Grax healthcheck failed: {label}")
        if label == "version" and not json.loads(result.stdout).get("version"):
            raise RuntimeError("local Grax version receipt is empty")


def _packages_delivered(response: dict[str, Any]) -> bool:
    runtime = response.get("crystal_runtime", {})
    composition = runtime.get("crystal_composition", {})
    attachment = runtime.get("crystal_context_attachment", {})
    consumed = sorted(item["crystal_id"] for item in runtime.get("consumed_crystal_packages", []))
    return (
        consumed == sorted(SOURCE_READING_CRYSTALS)
        and composition.get("status") == "CONSUMED"
        and not composition.get("conflicts")
        and runtime.get("crystal_context_bytes", 0) > 0
        and attachment.get("crystal_context_bytes", 0) > 0
        and attachment.get("delivery_status") == "BOUND_TO_LOCAL_COMPLETION_BOUNDARY"
        and bool(attachment.get("pre_attachment_input_sha256"))
        and bool(attachment.get("post_attachment_input_sha256"))
        and attachment["pre_attachment_input_sha256"] != attachment["post_attachment_input_sha256"]
    )


def _seal(directory: Path) -> None:
    files = [
        {"path": p.relative_to(directory).as_posix(), "sha256": sha256(p.read_bytes())}
        for p in sorted(directory.rglob("*"))
        if p.is_file()
    ]
    save_artifact(directory / "MANIFEST.json", encoded({"files": files}))


def run_review(
    prompt: str,
    *,
    output: Path,
    schema: dict[str, Any] | None = None,
    unit: dict[str, Any] | None = None,
    question: str | None = None,
    num_predict: int = 5000,
    timeout: float = 900,
) -> dict[str, Any]:
    """Execute one frozen review; return failures with custody, never acceptance.

    Capacity, daemon identity, terminal status and native package checks reuse
    brullama_jobs. Serial transport prevents competing local review threads from
    changing the runner's capacity envelope during another review.
    """
    prompt = unicodedata.normalize("NFC", prompt)
    if not prompt.strip() or len(prompt.encode()) > MAX_PROMPT_BYTES:
        raise ValueError("empty or oversized prompt; split sources explicitly, never truncate")
    if type(num_predict) is not int or num_predict <= 0 or timeout <= 0:
        raise ValueError("positive decode and timeout budgets are required")
    if (unit is None) != (question is None):
        raise ValueError("source unit and question must be supplied together")
    if unit is not None:
        question = unicodedata.normalize("NFC", question)
        expected_schema = source_question_schema(unit, question)
        if schema != expected_schema or encoded(unit).decode() not in prompt:
            raise ValueError("source/question contract differs from the actual prompt")
        if unicodedata.normalize("NFC", question) not in prompt:
            raise ValueError("question is not represented in the prompt")
    output = output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    bindings = {
        "prompt": save_artifact(output / "PROMPT.txt", prompt.encode()),
        "runner": sha256(Path(__file__).read_bytes()),
    }
    save_artifact(output / "RUNNER.py", Path(__file__).read_bytes())
    if schema is not None:
        bindings["schema"] = save_artifact(output / "SCHEMA.json", encoded(schema))
    if unit is not None:
        bindings["source"] = save_artifact(output / "SOURCE.json", encoded(unit))
        bindings["question"] = save_artifact(output / "QUESTION.txt", question.encode())
    exchange, frozen, phase = None, None, "health"
    result: dict[str, Any]
    with _GPU_LOCK:
        try:
            _healthcheck(output)
            phase = "route"
            crystals = build_admitted_crystal_set(SOURCE_READING_CRYSTALS)
            save_artifact(output / "CRYSTAL_SET.json", encoded(crystals))
            route_source = model_facing_route_source(prompt=prompt, system=None)
            design = {
                "schema_version": "brudo-lrd-review-design-v1",
                "source_bindings": bindings,
                "model": MODEL,
                "endpoint": ENDPOINT,
                "declared_transport": DECLARED_TRANSPORT,
                "num_ctx": 32768,
                "num_predict": num_predict,
                "think": SOURCE_READING_THINK,
                "selected_crystals": list(SOURCE_READING_CRYSTALS),
                "comparison": "NONE; one proposed reading, not an effect estimate",
                "canon_effect": "NONE",
            }
            design_sha = save_artifact(output / "DESIGN.json", encoded(design))
            allocation = "lrd-review:" + bindings["prompt"]
            plan = {
                "schema_version": "brudo-lrd-review-assignment-plan-v1",
                "allocation_id": allocation,
                "execution_unit_id": allocation + ":01",
                "assigned_arm": "TREATMENT",
                "assigned_crystal_set_sha256": crystals["set_sha256"],
                "assay_design_sha256": design_sha,
                "comparison": "NONE; TREATMENT is only the native route's label",
            }
            plan_sha = save_artifact(output / "ASSIGNMENT_PLAN.json", encoded(plan))
            assignment = {
                **{
                    k: plan[k]
                    for k in (
                        "allocation_id",
                        "execution_unit_id",
                        "assigned_arm",
                        "assigned_crystal_set_sha256",
                    )
                },
                "schema_version": "brudo-crystal-assay-assignment-receipt-v1",
                "assignment_plan_sha256": plan_sha,
            }
            save_artifact(output / "ASSIGNMENT.json", encoded(assignment))
            bundle = build_predeclared_crystal_assay_bundle_from_text(
                allocation,
                route_source,
                projection_id=allocation,
                selected_crystals=SOURCE_READING_CRYSTALS,
                assay_design_sha256=design_sha,
                assay_assignment=assignment,
                routing_mode="semantic",
                crystal_set_override=crystals,
            )
            if not is_prompt_bound_predeclared_crystal_assay(bundle, text=route_source):
                raise ValueError("native route lost its full prompt binding")
            resolved, origin = resolve_exact_grax_routing_bundle_for_model_input(
                bundle, source_id=allocation, text=route_source, projection_id=allocation
            )
            if resolved != bundle or origin != "CALLER_SUPPLIED_FROZEN_ASSAY":
                raise ValueError("native resolver changed the declared route")
            save_artifact(output / "ROUTING_BUNDLE.json", encoded(bundle))
            sequence = 0

            def opener(request: Any, timeout: float) -> io.BytesIO:
                nonlocal sequence
                sequence += 1
                stem = f"HTTP.{sequence:02}"
                save_artifact(
                    output / f"{stem}.request.json",
                    encoded({"url": request.full_url, "method": request.method}),
                )
                if request.data is not None:
                    save_artifact(output / f"{stem}.request.body", request.data)
                try:
                    with urllib.request.urlopen(request, timeout=timeout) as response:
                        body = response.read()
                        status = response.status
                except urllib.error.HTTPError as error:
                    save_artifact(output / f"{stem}.response.body", error.read())
                    save_artifact(output / f"{stem}.status.json", encoded({"status": error.code}))
                    raise
                save_artifact(output / f"{stem}.response.body", body)
                save_artifact(output / f"{stem}.status.json", encoded({"status": status}))
                return io.BytesIO(body)

            phase = "invoke"
            exchange = invoke_brullama_budgeted(
                prompt,
                model=MODEL,
                format_schema=schema,
                format_json=schema is None,
                routing_bundle=bundle,
                num_ctx=32768,
                num_predict=num_predict,
                timeout_seconds=timeout,
                seed=141,
                temperature=0,
                think=SOURCE_READING_THINK,
                reset_prefix_cache=True,
                urlopen=opener,
            )
            phase = "terminal"
            if exchange.response_object.get("model") != MODEL:
                raise ValueError("returned model identity differs")
            if (
                exchange.response_object.get("done") is not True
                or exchange.response_object.get("done_reason") != "stop"
            ):
                raise ValueError("response did not terminate completely")
            phase = "freeze"
            frozen = freeze_successful_job(
                output / "frozen",
                job_id="review",
                external_id="lrd-document-review",
                prompt=prompt,
                source_bindings=bindings,
                exchange=exchange,
            )
            verification = verify_frozen_job(Path(str(frozen["artifact_path"])))
            phase = "native_packages"
            if not _packages_delivered(exchange.response_object):
                raise ValueError("required native package delivery was not observed")
            phase = "response_contract"
            parsed = json.loads(exchange.response_text)
            if not isinstance(parsed, dict):
                raise ValueError("review response must be a JSON object")
            contract = (
                validate_source_answer(unit, question, exchange.response_text)
                if unit is not None
                else {"status": "JSON_OBJECT_ONLY", "semantic_review": "REQUIRED"}
            )
            result = {
                "parse_status": "PASS",
                "execution_status": "RESPONSE_VERIFIED",
                "contract": {k: v for k, v in contract.items() if k != "parsed"},
                "review": parsed,
                "verification": verification,
                "packages_delivered": True,
            }
            if "rendered_answer" in contract:
                # Only acceptance.read_accepted_answer exposes an admitted answer.
                # Keep the model's complete proposal for review, including errors.
                result["proposed_answer"] = contract["rendered_answer"]
                result["answer_acceptance"] = "PENDING_TARGET_MEANING_REVIEW"
        except Exception as error:
            retained = exchange or getattr(error, "exchange", None)
            evidence = getattr(error, "retained_response_evidence", {})
            if retained is not None:
                evidence = {
                    "request_bytes": retained.request_bytes,
                    "response_bytes": retained.response_bytes,
                }
            for name in ("request_bytes", "response_bytes"):
                if name in evidence:
                    save_artifact(output / f"FAILED.{name}", evidence[name])
            result = {
                "parse_status": "FAIL_PRESERVED",
                "execution_status": "FAILED",
                "phase": phase,
                "review": {"error": str(error), "error_type": type(error).__name__},
            }
    result.update(
        {
            "model": MODEL,
            "endpoint": ENDPOINT,
            "artifact_path": str(output),
            "frozen": frozen,
            "source_bindings": bindings,
            "semantic_review": "REQUIRED",
            "answer_acceptance": result.get(
                "answer_acceptance", "UNAVAILABLE_NO_SOURCE_TARGET_REVIEW"
            ),
            "authority_status": "AI_PROPOSED_REVIEW",
            "canon_effect": "NONE",
        }
    )
    save_artifact(output / "RESULT.json", encoded(result))
    _seal(output)
    return result


def review_json(
    prompt: str, *, num_predict: int, timeout: float, output: Path | None = None
) -> dict[str, Any]:
    """Compatibility boundary for existing LRD route/queue/slice CLI consumers."""
    output = output or REPO / ".brudo/legal/review_runs" / uuid4().hex
    return run_review(prompt, output=output, num_predict=num_predict, timeout=timeout)


def review_document_unit(
    unit: dict[str, Any], question: str, *, output: Path, timeout: float = 900
) -> dict[str, Any]:
    unit = targeted_source_unit(unit, question)
    prompt = source_question_instruction(unit, question) + encoded(unit).decode()
    return run_review(
        prompt,
        output=output,
        schema=source_question_schema(unit, question),
        unit=unit,
        question=question,
        timeout=timeout,
    )
