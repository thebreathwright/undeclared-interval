# An Undeclared Measurement Interval

Signal averaging time in oximetry-based screening, and the prevalence figures that depend on it.

**GitHub Way 2 is public and retrieval-verified.** Read
`00_NOT_PUBLISHED.md` and `corrections/` before `findings/`.

## What this does not establish

- No trial shows that screening pregnant women for sleep-disordered breathing improves outcomes. None exists. That absence is the USPSTF's stated reason for Grade I.
- Fung 2013: n = 41 completers, 14 OSA cases. Impaired fetal growth 43% vs 11%, RR 2.67 (1.25–5.7), p = 0.04. **BMI-adjusted OR 5.3, p = 0.06.**
- Most of the cited literature measures apnea–hypopnea indices, not oxygen desaturation. Arguing from those papers to “measure oxygen at night” is an inference and is labelled as one.
- Nothing here identifies any person's intent.
- The 1-in-12-million figure is \(e^{-np}\) under an independence assumption that is false. It is not a posterior on steering. Do not put it in a title or abstract.
- 71,351 events/s and 2.7 billion deaths are **retired captions**, not findings of this packet.
- Physiology scripts in `models/` are models. Change a parameter and the printout changes.

## What it contains

1. A portable non-invasive blood-oxygen instrument has existed since 1940 (availability, not obstetric readiness).
2. Maternal nocturnal desaturation is *associated* with impaired fetal growth in small observational work. Limits above.
3. This package does not establish a consensus recommendation to screen
   pregnant persons for OSA. USPSTF Grade I does not apply that adult-screening
   question to them.
4. CMS Transmittal 166 (22 July 2005) and LCD L33797 specify custody of overnight oximetry and do not specify signal averaging time. Farré 1998: desaturation depth underestimated by up to 60% at 12 s and 21 s averaging versus 3 s.
5. Reconstruction rule: **the printed rule can be constant while the gas is not.** A 4-point saturation drop is ~39 mmHg from 98% and ~8 mmHg from 90% (Hill \(n=2.7\), \(P_{50}=26.6\)). Do not invert Hill near 98% ± 2 points and call the span a PaO₂.

## Four ways to publish

See `channels/PLAYBOOK.md`.

| Way | Object | Who clicks |
|---|---|---|
| 1 | Internet Archive complete-document item | authorized Archive account |
| 2 | GitHub public repository (history) | authorized GitHub account |
| 3 | Zenodo dataset/software (DOI) | authorized Zenodo account |
| 4 | One-page supersession note to the 14 Sep 2025 Message-ID list | authorized sender, after DOI |

OSF remains an optional mirror; it is not one of the four required surfaces.

## Layout

```
00_NOT_PUBLISHED.md
README.md                          this file
LICENSE
STRIP.md                           do not ship
channels/PLAYBOOK.md
channels/INTERNET_ARCHIVE.md
channels/ZENODO_DEPOSIT.md
channels/GITHUB.md
channels/OSF.md                     optional mirror only
notices/SUPERSESSION_NOTE.md       drafted, not sent
corrections/                       read first
findings/
sources/
code/                              apnea_burden + estimated_series
models/                            five Hill/HME scripts; all ASSUMED
kit_r2_snapshot/                   bytes this desk actually hashed
AUTISM/                            evidence-bound autism paper set; no training material
TRAINING/                          separate commercial material; not autism evidence
CONTENT_MANIFEST.v1.md             provenance and scope of post-r2 additions
verify_public_package.py           executable boundary and hash checks
RELEASE_CLOSURE_TEMPLATE.v1.md     per-channel shipment and retrieval evidence
```
