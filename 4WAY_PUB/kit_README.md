# The Interval Nobody Declared — r2 Source-Kit Readme

**Historical r2 text, assembled 19 September 2026.** Its former statements
about no repository or public URL describe the r2 source state, not the current
successor package. Current GitHub release status is in
`RELEASE_CLOSURE_RECORD.v1.md`.

An instrument that measures blood oxygen continuously and non-invasively has
existed since 1940. Maternal nocturnal oxygen desaturation is associated with
impaired fetal growth. No body recommends screening pregnant women for it. No
global prevalence figure for mouth breathing exists anywhere.

Every source here was opened at the publisher or issuing body on the stated date.
Nothing is carried from memory or from summary. Where a figure is an estimate,
it is labelled as one, on the line where it appears.

## What is in here

    findings/      the claims, each with what it does and does not establish
    code/          every number in findings/ is reproducible from these scripts
    sources/       what was opened, what was blocked, and the access status of each
    corrections/   every number that was wrong, and what was wrong with it

## Read corrections/ first

That directory is not an appendix. During assembly the central estimate for
maternal apnea events moved 5,938 -> 36,300 -> 71,351 per second, and the global
figure moved 148B -> 272B -> 181B per day. Each move was a specific, named error.
They are logged because a number you cannot audit is not evidence.

## The three r2 claims

1. **The instrument existed.** Squire 1940 established the red/infrared principle.
   Millikan built the first practical portable oximeter in 1940 and presented it
   to the American Physiological Society in 1941. The American Society of
   Anesthesiologists made pulse oximetry mandatory for every administration of
   anesthesia in 1986.

2. **The harm is measured.** Fung 2013 (PLOS ONE, n=41 with sleep studies):
   impaired fetal growth in 43% of maternal OSA cases against 11% of controls,
   RR 2.67 (1.25-5.7), p=0.04. Liu 2019 (Sleep and Breathing, 33 studies): OSA
   in 15% of pregnancies, pre-eclampsia aOR 2.35, preterm birth aOR 1.62.

3. **Nobody is looking.** The USPSTF rates screening for obstructive sleep apnea
   in adults Grade I - insufficient evidence - and states: "This recommendation
   does not apply to children, adolescents, or pregnant persons." Pregnant women
   are not told the evidence is uncertain. They are outside the question. The
   questionnaires used in clinics run 37% specificity against a population in
   which 43.8% of third-trimester women have sleep-disordered breathing.

## The measurement hole

Medicare LCD L33797 requires an oximeter to "download data that allows
documentation of the duration of oxygen desaturation below a specified value."
It does not state the signal averaging time. Averaging time determines whether a
desaturation is registered at all: Farre 1998 found desaturation underestimated
by up to 60% at 12s and 21s against a 3s control. Vagedes 2024 found that 9 of
151 papers reporting SpO2 measures stated the averaging time.

So every prevalence figure and every AHI figure in this release - including the
ones used to compute its own numbers - was produced by instruments whose
averaging time was not declared.

## What this does not establish

- No trial shows that screening pregnant women improves outcomes. None exists.
- Fung is n=41; adjusted for BMI the association weakens to p=0.06.
- Most of this literature measures apnea-hypopnea indices, not desaturation.
  Arguing from it to "measure oxygen at night" is an inference, not a finding.
- Nothing here identifies any person's intent. The absence of a prevalence
  figure is documented; why it is absent is not.

## Licence

Findings, code and correction log: CC0 / public domain. Source documents remain
the property of their publishers and are cited, not reproduced.
