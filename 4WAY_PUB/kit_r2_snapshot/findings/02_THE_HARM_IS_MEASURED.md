# Finding 2 — the harm is measured

## Fung 2013 — prospective, fetal growth

Fung AM, Wilson DL, Lappas M, Howard M, Barnes M, O'Donoghue F, Tong S, Esdale H,
Fleming G, Walker SP. Effects of maternal obstructive sleep apnoea on fetal
growth: a prospective cohort study. *PLOS ONE* 2013;8(7):e68057.
DOI 10.1371/journal.pone.0068057.

371 women screened in the second trimester; 41 completed overnight sleep studies
and longitudinal assessment; 14 confirmed OSA cases, 27 controls.

> Impaired fetal growth was observed in 43% (6/14) of cases, vs 11% (3/27) of
> controls (RR 2.67; 1.25–5.7; p = 0.04).

Cases showed more desaturations at ≥3% and ≥4%, larger drops in saturation, lower
minimum saturation, and a greater proportion of total sleep time below 90%.
Univariate: OSA alone predicted impaired growth (OR 6; 1.2–29.7; p = 0.03).

**Adjusted for BMI the association weakens to OR 5.3 (0.93–30.34; p = 0.06).**
Stated here rather than left for a critic to find.

## Liu 2019 — pooled, perinatal outcomes

Liu L, Su G, Wang S, Zhu B. *Sleep and Breathing* 2019;23(2):399–412.
DOI 10.1007/s11325-018-1714-7. Thirty-three studies.

Pooled prevalence of objectively assessed OSA in pregnancy: **15% (95% CI 12–18%)**.

| Outcome | Adjusted OR |
|---|---|
| Pre-eclampsia | 2.35 |
| Gestational hypertension | 1.97 |
| Pulmonary edema | 6.35 |
| Preterm birth | 1.62 |
| Gestational diabetes | 1.55 |
| NICU admission | 1.28 |

**Open item: the confidence intervals for these adjusted odds ratios have not
been transcribed from the paper.** Point estimates without intervals are not a
finding. They must be read before this table is relied upon.

## The scale

Reproducible from `code/apnea_burden.py`.

| Quantity | Value | Status |
|---|---|---|
| Women pregnant at any instant | 99,000,000 | sourced |
| With SDB at 20% prevalence | 19,800,000 | prevalence is an estimate |
| Apnea events per second, pregnant women | 26,045 | sourced AHI |
| Share of the adult total | 2.1% | — |
| Events per pregnancy, population-averaged | 6,137 | intensive; no population figure inside it |

The intensive figure is the durable one. It does not move when the UN revises
fertility, because no population count is in it. Multiply by whatever denominator
you trust.

## The physiology, and its limit

Maternal apnea can lower fetal oxygenation. Almendros 2019 measured maternal and
fetal PO₂ swings of 21.0 against 3.1 mmHg in four ewes
(DOI 10.1152/japplphysiol.00303.2019). The placental mixing model in that paper
omits fetal oxygen withdrawal, and the authors acknowledge anatomical differences
between ovine and human placentas. **The four-ewe amplitude ratio must not become
a universal human attenuation factor.**

Reduced transfer is not zero transfer. A delay does not cancel exposure; it also
does not establish its severity.

## What this does not establish

- **No trial shows that screening helps.** Every source here is observational or
  diagnostic. Nobody has randomised pregnant women to screening versus none and
  measured outcomes. That absence is the USPSTF's own stated reason for Grade I.
- **Classifying every maternal respiratory event as a fetal asphyxiation event**
  additionally requires the resulting fetal gas-exchange deficit, and lasting
  injury requires an outcome connection. Neither is established here. *Asphyxia*
  is a threshold clinical entity with defined criteria — cord pH, Apgar,
  encephalopathy. What this literature describes is chronic intermittent
  hypoxemia. Different object; using the wrong word loses the reader who matters.
- **OSA is not nocturnal desaturation.** Most of this work measures
  apnea-hypopnea or respiratory disturbance indices. Desaturation is an
  associated finding, not the exposure variable. Arguing from here to "measure
  oxygen at night" is an inference and should be labelled one.

## Sources

S2, S3, S5 (see `sources/INDEX.md`). HypnoLaus — the best available independent
cross-check on prevalence — could not be reached; see the blocked table.
