# Addendum — C18–C34 reported

Dated 20 September 2026 on this desk.

These entries reconstruct from physics or from code on **this** disk (r2 kit + five models). They are **reported** here. They are not certified as the text of an r3 zip or of commits `547232a` / `360eba8`, which this desk has not hashed.

## Pattern

The printed rule can be constant. The gas, the minutes, and the smear are not.

## C18 — near-fit treated as range

`chain.py` totals: nasal 293, oral 348 kcal/day. 426 is **above both**. A dead branch would have printed “sits between them” if parameters ever put it there. They did not. Prose that says 426 is in range for the whole chain is a caption the script declined.

## C20 — 426 is three objects

Claimed whole-body RMR vs mechanical work of breathing (~12.9 kcal/day in `budget.py`) vs conditioning+WOB+heart (293–348). Do not ship 426 as any one of those without naming which.

## C21 — expired air is not 37 °C / 100% RH

`chain.py` recoveries 30% nasal vs 5% oral produce a 54.7 kcal/day “open mouth” line. Varène 1986 (PMID 3780165, n=4, abstract): expired gas not water-saturated; total respiratory heat-loss difference mouth vs nose **<10%**. Rebuild from expired water masses and the humidification gap is ~6 kcal/day, not 54.7. Abstract only on this desk.

## C22 — heart inside TOTAL

126.9 kcal (8% of RMR 1586) does not change with route. It is inside `chain.py` “TOTAL, nasal/oral.” The route delta 54.7 correctly excludes it.

## C23 — swing.py holds PO2 = 40

Bohr-only Sv change ~2.3 points. A real event also drops PO2. Do not caption “the event” as the 2.3 points.

## C24 — scoring ×1.70 is not gas exchange

3% vs 4% multiplies **counted** events. Do not fold it into a sourced physical rate.

## C25 — Almendros drop applied at PaO2 = 100

Anesthetized ewe carotid is not stated as 100. The same 21 mmHg drop from 80 is a larger maternal sat swing. Ovine 15% is not a human constant.

## C26 — +5 mmHg PaCO2 in ~20 s is assumed

Acute ΔpH ≈ −0.008 / mmHg is the bedside shortcut (keep). Event length ~20 s is near published mean event duration (keep). The **+5 mmHg amplitude** is a store-size claim, not a measurement in these scripts.

## C30 — 4-point rule is not one tension

Hill n=2.7, P50=26.6:

| sat drop | PO2 | Δ tension |
|---|---|---|
| 98 → 94% | 112 → 74 | −39 mmHg |
| 95 → 91% | 79 → 63 | −16 mmHg |
| 90 → 86% | 60 → 52 | −8 mmHg |

## C31 — Arms is not the scoring rule; 98% span is not gas

FDA/ISO Arms for transmittance pulse ox is typically ≤2–3% vs co-oximeter SaO2. The 3%/4% fight is event-to-event change on one device. Adjacent sizes, different comparisons.

**Do not ship** “±2 points at 98% = 103 mmHg of PaO2.” Inverse Hill diverges as sat → 1. Keep C30’s 95→91 table.

## C33 — pregnancy store is a sketch

Isolated-store empty time ~84 s uses non-pregnant FRC 2.5 L and VO2 250 mL/min. Term + supine: FRC down, VO2 up. Direction holds. **56 s / 1.78 mmHg/s** used FRC 2.0 L and VO2 300 mL/min as assumed. Source those two numbers before Finding 2 runs on them.

## C34 — 3.2 kcal is a third object

Sleep fraction of the *model* premium: 54.7 × 7.25/24 = **16.5** kcal.  
Varène-scale 24 h gap ~6; sleep-only ~2.  
**3.2** is not 16.5 and not 2. Do not print seventeenfold from 54.7 to 3.2 without the two cuts written on the same line.

## Two 60s (already split)

Farré depth underestimation “up to 60%” ≠ 12 s / 20 s event = 60% of event length.

## AHI 20 vs 15.7 (already split)

`swing.py` assumed AHI 20. Kit sourced mean 15.7. Do not add 49.6 trillion to 181 B/day.
