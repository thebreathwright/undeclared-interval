#!/usr/bin/env python3
"""
ESTIMATED SERIES — the 71,351/sec and 391B/day chains, shipped so they can be
audited rather than quoted.

NOTHING IN THIS FILE IS SOURCED. Every multiplier below is an estimate made by
the assembler. They are here because a number cited without its code is not
evidence, and because the defect logged in corrections/LOG.md C4 was precisely
that these factors were conceded in prose and left out of the arithmetic.

Sourced figures live in apnea_burden.py. Do not mix the two.

Run: python3 estimated_series.py
"""

from apnea_burden import (OSA_AHI5, MEAN_AHI_SOURCED, SLEEP_H, SCORING_3PCT,
                          BIRTHS_YR, GESTATION, PREG_PREV, DAY, events_per_sec)

# ---- ESTIMATE: global, all ages -------------------------------------------
GLOBAL_EST = [
    ("ages <30 and >69 Benjafield excludes", 1.50,
     "Benjafield covers 30-69 only. Prevalence RISES above 69. Children excluded."),
    ("sub-threshold AHI 3-5",                1.25,
     "AHI>=5 is a diagnostic threshold, not a physiological floor."),
    ("severe tail above midpoint 22.5",      1.15,
     "The >=15 band is unbounded; AHI reaches 100+."),
]

# ---- ESTIMATE: pregnant women ---------------------------------------------
PREG_EST = [
    ("pregnancy-time, not live births", 1.12,
     "~25% of pregnancies end early, mostly T1; adds woman-time."),
    ("trimester weighting",             1.30,
     "nuMoM2b 3.5% T1 -> 8.2% T2; T3 higher again. A flat annual figure understates."),
    ("sub-threshold AHI 3-5",           1.25, "as above"),
    ("severe tail",                     1.08, "as above"),
]

def chain(base, steps, label, unit="/sec"):
    print(f"\n{label}")
    print(f"  {'SOURCED START':<40} {base:>12,.0f} {unit}")
    v = base
    for name, f, why in steps:
        v *= f
        print(f"  x{f:<5} {name:<34} {v:>12,.0f} {unit}   ESTIMATE")
        print(f"         {why}")
    return v

if __name__ == "__main__":
    print("=" * 72)
    print("ESTIMATED SERIES - NOT SOURCED - see corrections/LOG.md C4 and C7")
    print("=" * 72)

    g0 = events_per_sec(OSA_AHI5, MEAN_AHI_SOURCED) * SCORING_3PCT
    g = chain(g0, GLOBAL_EST, "GLOBAL, ALL AGES  (sourced start = 936M x 15.7 x 7.25h x 1.70)")
    print(f"\n  -> {g:,.0f}/sec = {g*DAY/1e9:,.0f} B per 24h     ESTIMATED")
    print(f"     sourced figure for comparison: {g0*DAY/1e9:,.0f} B per 24h")

    p0 = events_per_sec(BIRTHS_YR*GESTATION*PREG_PREV, MEAN_AHI_SOURCED)
    p = chain(p0, PREG_EST, "PREGNANT WOMEN  (sourced start = 99M x 20% x 15.7 x 7.25h)")
    print(f"\n  -> {p:,.0f}/sec     ESTIMATED")
    print(f"     sourced figure for comparison: {p0:,.0f}/sec")

    print("\n" + "=" * 72)
    print("NOT IN EITHER NUMBER, direction known, magnitude not:")
    print("  signal averaging time. Farre 1998: desaturation underestimated by")
    print("  up to 60% at 12s and 21s against a 3s control. Averaging at 21s")
    print("  does not recover the nadir - the event is gone from the record,")
    print("  not attenuated in it.")
    print("=" * 72)
