# Way 1 — GitHub

**Status:** not created for this work.

Authenticated here as `thebreathwright` (https://github.com/thebreathwright).

Do not reuse `maps` (private, symbolic maps) or `homebrew-crystals` (public, unrelated tap).

## Suggested remote

    thebreathwright/undeclared-interval

README first paragraph = “What this does not establish.”

## Files that belong

- `README.md`, `LICENSE`, `corrections/`, `findings/`, `sources/`, `code/`, `models/`
- `.gitignore` with `__pycache__/` and `*.pyc`

## Files that do not belong

- J1/J3 letters, EOBs, attorney zips, astronomy PDFs
- `NOTIFICATION_MANIFEST` body that leads with 2.7 billion deaths
- Anything on `STRIP.md`

## After a DOI exists

    git tag -a v1.0.0 -m "Zenodo DOI: 10.5281/zenodo.XXXX"
    git push origin v1.0.0
