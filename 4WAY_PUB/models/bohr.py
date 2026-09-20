#!/usr/bin/env python3
"""Hypocapnic alkalosis -> Bohr shift -> extraction. A MODEL."""
import math
N_HILL, BOHR_COEF, P50_0, PH_0 = 2.7, -0.48, 26.6, 7.40
PAO2, PVO2 = 100.0, 40.0      # mmHg, arterial / tissue-end capillary
HB, CO_0 = 15.0, 5.0          # g/dL, L/min
RMR, HEART_SHARE = 1586.0, 0.08

def p50(ph):  return P50_0 * 10**(BOHR_COEF*(ph-PH_0))
def sat(p, ph):
    a, b = p**N_HILL, p50(ph)**N_HILL
    return a/(a+b)

print(f"{'pH':>6}{'P50':>8}{'SaO2':>8}{'SvO2':>8}{'extract':>9}"
      f"{'CO needed':>11}{'cardiac':>10}{'Δ kcal/d':>10}")
print("-"*70)
base_ext = sat(PAO2,PH_0) - sat(PVO2,PH_0)
base_heart = RMR*HEART_SHARE
for ph in (7.40, 7.45, 7.50, 7.55, 7.60):
    sa, sv = sat(PAO2,ph), sat(PVO2,ph)
    ext = sa - sv
    co  = CO_0 * base_ext/ext              # CO to hold delivery constant
    heart = base_heart * co/CO_0
    print(f"{ph:>6.2f}{p50(ph):>8.1f}{sa:>8.1%}{sv:>8.1%}{ext:>9.1%}"
          f"{co:>11.2f}{heart:>10.1f}{heart-base_heart:>10.1f}")

print("\nSaO2 barely moves. That is the whole problem: the finger still prints 97-98%.")
ph = 7.50
sa, sv = sat(PAO2,ph), sat(PVO2,ph)
ext = sa - sv
print(f"\nAt pH {ph}:  extraction falls {1-ext/base_ext:.1%} per pass,")
print(f"  SaO2 moves {sat(PAO2,PH_0):.1%} -> {sa:.1%}  ({(sa-sat(PAO2,PH_0))*100:+.2f} points)")
print(f"  SvO2 moves {sat(PVO2,PH_0):.1%} -> {sv:.1%}  ({(sv-sat(PVO2,PH_0))*100:+.2f} points)")

print("\n--- and the ventilation that caused it is not free ---")
J_KCAL, MIN_DAY = 4184, 1440
COND_J_L, EFF, WOB_J_L = 105.9, 0.08, 0.5
for ve in (6.0, 7.5, 9.0):
    cond = COND_J_L*(1-0.05)*ve*MIN_DAY/J_KCAL      # oral route, 5% recovery
    wob  = (ve*WOB_J_L/EFF)*MIN_DAY/J_KCAL
    print(f"  VE {ve:4.1f} L/min   conditioning {cond:6.1f}   WOB {wob:5.1f}   "
          f"sum {cond+wob:6.1f} kcal/day")
print("\nBohr is textbook. That mouth breathing produces chronic hypocapnia")
print("is the causal step and it is NOT modelled here - it is assumed.")
