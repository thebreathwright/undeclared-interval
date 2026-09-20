# Correction log

Every number in this release that was wrong before it was right, with the defect
named. Dated 19 September 2026 unless stated.

Read this before findings/. A number whose error history is hidden cannot be
audited, and an unauditable number is not evidence.

---

## C1 — median used to compute a total

**Wrong:** maternal apnea events estimated at 5,938/sec using AHI 7.9.

**Defect:** 7.9 was the *median* RDI of Fung's cases. A total is N x mean. A
median is a position in a distribution and cannot be summed. AHI is right-skewed,
so the median sits below the mean and the error is always downward.

**Right:** severity-weighted mean across Benjafield's bands — mild 5-15 (54.6%
of cases), moderate 15-30 (27.2%), severe 30+ (18.2%). With the unbounded severe
band treated conservatively at 22.5, the sourced mean is **15.7**. With a 60/40
moderate/severe split and severe mean 45 it is 19.8; that split is an assumption
and is not used in the sourced figure.

---

## C2 — wrong subpopulation

**Wrong:** the same 7.9 applied to everyone, including severe cases.

**Defect:** 7.9 is a mild-band value. Applying it across all severities
understates by roughly half.

---

## C3 — a floor used as a central estimate

**Wrong:** pregnancy SDB prevalence taken as 8.2% (nuMoM2b).

**Defect:** nuMoM2b measured **nulliparous** women — first pregnancies, younger
and leaner — by home sleep apnea testing, which underdetects against in-lab PSG.
Both facts were known when the figure was used. 8.2% is a floor for a specific
subpopulation.

**Right:** Benjafield's global adult rate is 25% at AHI>=5 and 11.5% at AHI>=15.
A pregnancy figure below the general adult rate is not credible. The defensible
band is 15-25%.

---

## C4 — conservative factors conceded in prose, dropped from the arithmetic

**Wrong:** central estimate published at 36,300/sec after agreeing in the same
session that six factors all pushed the figure upward.

**Defect:** the concession was made in text and none of it entered the
calculation. The model still used live births, flat prevalence across trimesters,
AHI>=5 as a floor, and a midpoint for an unbounded band.

**Right, with the conceded factors actually propagated:**

    published central                                36,300 /sec
    x1.12  pregnancy-time, not live births           40,656
    x1.30  trimester weighting                       52,853
    x1.25  sub-threshold AHI 3-5                     66,066
    x1.08  severe tail above midpoint 45             71,351

The four multipliers are estimates and are labelled as such. The defect being
logged is not their size. It is that they were agreed to and then omitted.

---

## C5 — mismatched source revisions

**Wrong:** a births series built as UN population x crude birth rate, giving
141.2M for 2024.

**Defect:** the crude-birth-rate series predates the UN World Population
Prospects 2024 fertility revision. The sourced births figure is 132M. The series
ran ~7% high at the recent end, less so historically, which flattened the trend.

**Right:** corrected with a ramp anchored at 1.0 in 1950 (where the series
reconciles) to 132/141.2 at 2024. Stated rather than silently applied.

**Generalisation:** publish the **intensive** quantity and let the denominator be
a parameter. ~8,500 apnea events per pregnancy, population-averaged, does not
move when the UN revises fertility, because no population figure is inside it.

---

## C6 — an uncertainty band that vanished where the uncertainty was largest

**Wrong:** a chart whose three model lines converged to a single value at 2024.

**Defect:** only obesity-trend uncertainty was modelled. The largest uncertainty
— whether today's prevalence is 15%, 20% or 25% — was invisible at exactly the
year a reader would look.

---

## C7 — adjustments baked into a headline figure

**Wrong:** 272 billion events in 24 hours, presented as the number.

**Defect:** three unsourced multipliers were inside it. The sourced figure is
**107 billion**; with the one further *sourced* adjustment (3% hypopnea scoring,
Won et al. via Singh 2025) it is **181 billion**; the rest is estimate and is now
listed separately rather than folded in.

---

## C8 — a rhetorical line that reversed the arithmetic

**Wrong:** "It didn't reach 50,000. It grew into it." Written one turn after
computing 36,231 and 46,013 per second and agreeing 50,000 was defensible.

**Defect:** no basis. A stylistic flourish that took back a validated number.

---

## C9 — citations at one remove

**Standing risk, partially unresolved.** Won et al.'s figure (AHI rises 83% in
women under 3% scoring against 64% in men) reaches this release through Singh
2025's scoping review, not from Won directly. It is flagged wherever it appears
and must be read at source before it is relied upon.

Earlier instances in the wider work: a transmittal note read as the letter it
enclosed; an LCD provision cited from a paraphrase; a device's FDA status read
from a 510(k) summary checkbox rather than the GUDID record.

---

## C10 — shelf time presented as exposure

**Wrong:** treating a book's presence in a library as reader exposure.

**Defect:** most library books are never opened. Worse, six of the nine confirmed
holdings are in vaults, rare-book rooms, special collections or offsite storage —
request-only. You cannot walk past them; you must already know the title to ask.

**What survives:** not the book. The span, and the fact that the material was
also in school syllabuses (1904, 1909), in standard pediatric texts (Holt 1897),
and in clinical practice (Lermoyez 1904). Curriculum, textbook and clinic — not
one overlooked volume.

---

## C11 — a number that changed the moment its code shipped

**Reported earlier:** 71,351/sec for pregnant women, and 391B/day globally, as
the estimate-adjusted figures.

**Defect:** those chains were computed in an ad-hoc worksheet, not in the
released code. When the multipliers were moved into `code/estimated_series.py`
and forced to start from the *sourced* mean AHI (15.7) rather than the estimated
one (19.8), the pregnant chain came out at **51,193/sec**, not 71,351.

The difference is entirely the AHI: 19.8 carries a 60/40 moderate/severe split
that is an assumption. The earlier figure had an estimate hidden in its starting
point as well as in its multipliers.

**Right:** sourced start, estimated multipliers, both labelled, one file.

    pregnant women   sourced 26,045/sec   estimate-adjusted 51,193/sec
    global all ages  sourced    181 B/day estimate-adjusted    391 B/day

**The general rule this produced:** a number that has not been run from released
code is reported, not derived, and stays labelled estimated until the code ships
beside it. 71,351 and the 5,938 -> 36,300 -> 71,351 chain are logged above as
*reported*. They are not findings of this repository.
