#!/usr/bin/env python3
"""Per-event pH swing across an obstructive apnea. A MODEL."""
import math
N, BOHR, P50_0, PH0 = 2.7, -0.48, 26.6, 7.40
DPH_PER_MMHG = -0.008          # acute, assumed
PACO2_RISE   = 5.0             # mmHg over a ~20 s event, assumed
PACO2_UNDER  = -3.0            # post-arousal overshoot, assumed
def p50(ph): return P50_0*10**(BOHR*(ph-PH0))
def sat(p,ph):
    a,b = p**N, p50(ph)**N
    return a/(a+b)

ph_lo = PH0 + PACO2_RISE*DPH_PER_MMHG        # during event: CO2 up, pH DOWN
ph_hi = PH0 + PACO2_UNDER*DPH_PER_MMHG       # after arousal: blown off, pH UP
print("ONE EVENT, both directions\n")
print(f"{'phase':<26}{'PaCO2':>8}{'pH':>8}{'P50':>8}{'SvO2 @40':>10}")
for lab,dco2,ph in (("baseline",0,PH0),
                    ("during apnea (CO2 up)",PACO2_RISE,ph_lo),
                    ("post-arousal overshoot",PACO2_UNDER,ph_hi)):
    print(f"{lab:<26}{40+dco2:>8.1f}{ph:>8.3f}{p50(ph):>8.1f}{sat(40,ph):>10.1%}")
print(f"\npH excursion per event: {ph_hi-ph_lo:.3f}   "
      f"P50 swing {p50(ph_lo):.1f} -> {p50(ph_hi):.1f} = {(p50(ph_lo)-p50(ph_hi))/p50(PH0):.1%}")
print("Acidosis UNLOADS (right shift). Alkalosis HOLDS. Both, every event.\n")

print("--- how many swings ---")
AHI, SLEEP_H = 20, 7.25
PEOPLE = 936e6            # Benjafield AHI>=5, ages 30-69, SOURCED
n_night = AHI*SLEEP_H
print(f"  per person-night at AHI {AHI}: {n_night:.0f}")
print(f"  {PEOPLE/1e6:.0f}M people, one night : {PEOPLE*n_night/1e9:,.0f} billion")
print(f"  one year                  : {PEOPLE*n_night*365.25/1e12:,.1f} trillion")
print()
print("--- and the instrument ---")
for avg in (3,4,12,21):
    print(f"  {avg:>2} s averaging vs a 20 s event: window is "
          f"{avg/20:.0%} of the event")
print("\n  Farre: desaturation underestimated up to 60% at 12 s and 21 s.")
print("  Those windows are 60% and 105% of the event they are meant to resolve.")
print("\nASSUMED: PaCO2 rise, overshoot, dpH/dmmHg, event length, AHI.")
print("SOURCED: 936e6 (Benjafield 2019).")
