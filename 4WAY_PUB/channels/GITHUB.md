# Way 2 — GitHub

**Status:** public and byte-verified.

Repository: `https://github.com/thebreathwright/undeclared-interval`.
The closure record identifies the verified v4 archive object; later commits
carry its closure record and successor package files.

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
