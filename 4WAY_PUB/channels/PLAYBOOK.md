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

1. Choose a name. Suggested: `undeclared-interval`. Not `maps`. Not `homebrew-crystals`.
2. Create the repository **public** only when the tree matches `STRIP.md`.
3. Copy this packet (minus `kit_r2_snapshot/` if you prefer one tree).
4. `.gitignore` must include `__pycache__/`, `*.pyc`, `.DS_Store`.
5. First commit message should identify the exact Archive item and package hash;
   tag only after the Zenodo DOI is recorded.

The public repository is `thebreathwright/undeclared-interval`. Its retrieved
v4 archive is recorded as closed in `RELEASE_CLOSURE_RECORD.v1.md`.

See `GITHUB.md`.

## Way 3 — Zenodo (DOI)

Purpose: a permanent identifier. Irreversible when you click Publish.

Use `ZENODO_DEPOSIT.md` (from r2). Title stays on the method.

After you *reserve* a DOI, paste it into `README.md` and commit, then publish the deposit that contains that commit.

## Optional — OSF mirror

Purpose: a second date-stamp. Not a clinical-trial preregistration. Not a claim of priority over the 14 Sep 2025 Message-ID.

See `OSF.md`.

## Way 4 — Supersession note (drafted, not sent)

Purpose: the 14 Sep 2025 object is the one 66 addresses already have. A new DOI does not retract it. Only a note that points at the correction log does.

See `../notices/SUPERSESSION_NOTE.md`. Fill the DOI. Send only if you choose to. This desk does not send mail.
