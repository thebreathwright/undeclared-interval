# 4WAY release playbook

Order matters. Corrections and strip list first. Then the machine. Then the identifier. Then the note.

## Way 1 — Internet Archive (complete document package)

Purpose: one public item containing the complete verified archive, rather than
a local directory or a partial web page.

Use `INTERNET_ARCHIVE.md`. Upload the final sealed ZIP and its `.sha256`
sidecar as one item. Record the item identifier, item URL, retrieved ZIP hash,
and retrieval time in `RELEASE_CLOSURE_TEMPLATE.v1.md`.

## Way 2 — GitHub (history)

Purpose: diffs, not another zip filename.

1. The public repository is `thebreathwright/undeclared-interval`.
2. Each commit must identify its exact archive hash in the closure record.
3. `.gitignore` must include `__pycache__/`, `*.pyc`, `.DS_Store`.
4. A GitHub release does not wait for an Archive item or Zenodo DOI. Tags are
   optional immutable labels and may be added before or after a DOI.

The public repository is `thebreathwright/undeclared-interval`. Its retrieved
v4 archive is recorded as closed in `RELEASE_CLOSURE_RECORD.v1.md`.

See `GITHUB.md`.

## Way 3 — Zenodo (DOI)

Purpose: an independent permanent identifier. Irreversible when you click
Publish, but not a prerequisite for the other ways.

Use `ZENODO_DEPOSIT.md` (from r2). Title stays on the method.

After you reserve or publish a DOI, record it in the closure record and a later
GitHub commit. Do not reseal an otherwise verified archive merely to insert a
DOI; that creates a circular release requirement.

## Optional — OSF mirror

Purpose: a second date-stamp. Not a clinical-trial preregistration. Not a claim of priority over the 14 Sep 2025 Message-ID.

See `OSF.md`.

## Way 4 — Supersession note (drafted, not sent)

Purpose: the 14 Sep 2025 object is the one 66 addresses already have. A new DOI does not retract it. Only a note that points at the correction log does.

See `../notices/SUPERSESSION_NOTE.md`. It already cites a verified GitHub
archive. Add a DOI when one exists; it is not a sending prerequisite.
