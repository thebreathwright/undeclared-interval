#!/usr/bin/env python3
"""
Apnea event burden, from sourced inputs, with every estimate flagged.

Run:  python3 apnea_burden.py
No dependencies. Python 3.8+.

Every constant below carries SOURCED or ESTIMATE. Change any of them and rerun;
the point of this file is that you do not have to accept our inputs.
"""

# ---------------------------------------------------------------- inputs ----
# SOURCED  Benjafield AV et al., Lancet Respir Med 2019;7(9):687-698.
#          Ages 30-69 ONLY. Both figures are from that paper.
OSA_AHI5   = 936e6
OSA_AHI15  = 425e6

# SOURCED  UN World Population Prospects 2024; Our World in Data 2025.
WORLD_POP  = 8.2e9
BIRTHS_YR  = 132e6

# SOURCED  WHO hypertension fact sheet, 25 September 2025, for comparison.
HYPERTENSION = 1.4e9

# ESTIMATE  mean hours of sleep, adult, global.
SLEEP_H    = 7.25
# SOURCED-DERIVED  gestation as a fraction of a year (39 weeks carried to term).
GESTATION  = 0.75

# ESTIMATE  pregnancy SDB prevalence. Anchors: nuMoM2b 8.2% mid-pregnancy
#           (nulliparous, home testing - a floor); Liu 2019 pooled 15%;
#           Benjafield adult baseline 25%.
PREG_PREV  = 0.20

# SOURCED-DERIVED  mean AHI across the AHI>=5 population.
#   mild band 5-15 at midpoint 10; the >=15 band is UNBOUNDED above, so
#   treating it at 22.5 understates. This is the conservative sourced value.
MILD = OSA_AHI5 - OSA_AHI15
MEAN_AHI_SOURCED = (MILD*10 + OSA_AHI15*22.5) / OSA_AHI5     # 15.7
# ESTIMATE  with a 60/40 moderate/severe split and severe mean 45.
MEAN_AHI_SPLIT   = (MILD*10 + OSA_AHI15*.6*22.5 + OSA_AHI15*.4*45) / OSA_AHI5

# SOURCED (at one remove - see corrections/LOG.md C9)
#   Won et al. via Singh A, Chou CA, Khan A. Sleep Sci Pract 2025;9(1):29.
#   Relative AHI increase under 3% vs 4% hypopnea scoring: 83% women, 64% men.
#   Benjafield's underlying studies are largely 4%. Sex mix roughly 2:1 male.
SCORING_3PCT = (2*1.64 + 1*1.83) / 3                          # 1.70

# ESTIMATE  adjustments, all ours, none sourced.
EST_AGE_BANDS  = 1.50   # under 30 and over 69, whom Benjafield excludes
EST_SUBTHRESH  = 1.25   # AHI 3-5: real events, not "cases"
EST_SEVERE_TAIL= 1.15   # the >=15 band is unbounded; 22.5 understates it

DAY = 86400

# ------------------------------------------------------------- functions ----
def events_per_sec(people, ahi, sleep_h=SLEEP_H, mult=1.0):
    """AHI is events per hour OF SLEEP. Sleep hours are not optional."""
    return people * ahi * sleep_h * mult / DAY

def per_pregnancy(ahi=None, prev=PREG_PREV, nights=270):
    """Intensive figure. Denominator-free: survives UN revisions."""
    ahi = MEAN_AHI_SOURCED if ahi is None else ahi
    return ahi * SLEEP_H * nights * prev

# ------------------------------------------------------------------ main ----
if __name__ == "__main__":
    W = 58
    print("=" * W); print("GLOBAL, ALL ADULTS"); print("=" * W)
    base = events_per_sec(OSA_AHI5, MEAN_AHI_SOURCED)
    print(f"  mean AHI, sourced ............... {MEAN_AHI_SOURCED:>14.1f}")
    print(f"  mean AHI, with 60/40 split ...... {MEAN_AHI_SPLIT:>14.1f}  ESTIMATE")
    print()
    print(f"  SOURCED  936M x {MEAN_AHI_SOURCED:.1f} x {SLEEP_H}h")
    print(f"           per second ............. {base:>14,.0f}")
    print(f"           per 24h ............... {base*DAY/1e9:>13,.0f} B")
    s = base * SCORING_3PCT
    print(f"  + 3% hypopnea scoring (x{SCORING_3PCT:.2f})")
    print(f"           per second ............. {s:>14,.0f}")
    print(f"           per 24h ............... {s*DAY/1e9:>13,.0f} B")
    print()
    print("  ESTIMATES, stated not baked in:")
    v = s
    for name, f in [("ages <30 and >69", EST_AGE_BANDS),
                    ("sub-threshold AHI 3-5", EST_SUBTHRESH),
                    ("severe tail", EST_SEVERE_TAIL)]:
        v *= f
        print(f"    x{f:<5} {name:<26} {v:>12,.0f} /s  {v*DAY/1e9:>6,.0f} B/day")
    print()
    print(f"  UNSIZED: signal averaging time.")
    print(f"           Farre 1998 - up to 60% underestimation at 12-21s vs 3s.")
    print()

    print("=" * W); print("PREGNANT WOMEN"); print("=" * W)
    pregnant = BIRTHS_YR * GESTATION
    pr = events_per_sec(pregnant * PREG_PREV, MEAN_AHI_SOURCED)
    print(f"  pregnant at any instant ......... {pregnant:>14,.0f}")
    print(f"  with SDB at {PREG_PREV:.0%} ................. {pregnant*PREG_PREV:>14,.0f}")
    print(f"  events per second ............... {pr:>14,.0f}")
    print(f"  share of the adult total ........ {pr/base:>13.1%}")
    print()
    print(f"  INTENSIVE (no population figure inside it):")
    print(f"    per woman-night, if she has it  {MEAN_AHI_SOURCED*SLEEP_H:>14,.0f}")
    print(f"    per pregnancy, if she has it .. {per_pregnancy(prev=1.0):>14,.0f}")
    print(f"    per pregnancy, averaged ....... {per_pregnancy():>14,.0f}")
    print()

    print("=" * W); print("WHAT IS COUNTED, AND WHAT IS NOT"); print("=" * W)
    print(f"  hypertension, adults 30-79 ...... {HYPERTENSION/1e9:>13.1f} B   WHO 2025")
    print(f"  sleep apnea, adults 30-69 ....... {OSA_AHI5/1e9:>13.1f} B   Benjafield 2019")
    print(f"  mouth breathing, any age ........ {'NO FIGURE EXISTS':>16}")
    print()
    print("  Mouth breathing is measured at 26-56% in Brazilian schoolchildren")
    print("  (Martins 2014, n=419, ages 6-11: 56.8%). There is no adult")
    print("  prevalence figure, in any country. A condition running at that rate")
    print("  in children cannot plausibly be rarer in adults than a condition")
    print("  affecting 1.4 billion people. The question has not been asked.")
