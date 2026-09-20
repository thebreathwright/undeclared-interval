#!/usr/bin/env python3
"""Maternal event -> fetal response. A MODEL. Parameters assumed."""
N = 2.7
P50_ADULT, P50_FETAL = 26.6, 19.5     # mmHg; HbF is left-shifted
def sat(p, p50):
    a,b = p**N, p50**N
    return a/(a+b)
def slope(p, p50, d=0.5):             # %sat per mmHg, local
    return (sat(p+d,p50)-sat(p-d,p50))/(2*d)*100

print("WHERE EACH ONE SITS ON ITS OWN CURVE\n")
print(f"{'':<28}{'PO2':>7}{'P50':>7}{'sat':>8}{'slope %/mmHg':>15}")
rows = [("mother, arterial",      100, P50_ADULT),
        ("mother, tissue end",     40, P50_ADULT),
        ("fetus, umbilical vein",  30, P50_FETAL),
        ("fetus, umbilical artery",18, P50_FETAL)]
for lab,po2,p50 in rows:
    print(f"{lab:<28}{po2:>7.0f}{p50:>7.1f}{sat(po2,p50):>8.1%}{slope(po2,p50):>15.2f}")

print("\nThe mother's finger sits at the flat top. The fetus sits on the knee.")
print(f"Slope ratio, fetal UV vs maternal arterial: "
      f"{slope(30,P50_FETAL)/slope(100,P50_ADULT):.0f}x\n")

# Almendros 2019, four ewes: maternal PO2 swing 21.0 mmHg -> fetal 3.1 mmHg
TRANSMIT = 3.1/21.0
print(f"--- transmit a maternal event at the ovine ratio {TRANSMIT:.2f} ---")
print("   (four ewes; the authors warn against exporting this ratio to humans)\n")
for drop in (10, 21, 30):
    fd = drop*TRANSMIT
    m0, m1 = sat(100,P50_ADULT), sat(100-drop,P50_ADULT)
    f0, f1 = sat(30,P50_FETAL),  sat(30-fd,P50_FETAL)
    print(f"  maternal PO2 -{drop:>2} mmHg -> fetal -{fd:4.1f} mmHg   "
          f"mother {m0:.1%}->{m1:.1%} ({(m1-m0)*100:+5.1f} pts)   "
          f"fetus {f0:.1%}->{f1:.1%} ({(f1-f0)*100:+5.1f} pts)")

print("\nWHAT IS NOT THE SAME")
print("  1. Different curve. P50 19.5 vs 26.6. HbF holds tighter by design.")
print("  2. Different operating point. Fetus is on the steep part, so a")
print("     SMALLER PO2 change makes a LARGER saturation change.")
print("  3. DOUBLE BOHR runs the other way. Maternal blood taking up CO2 at")
print("     the placenta acidifies and RELEASES O2; fetal blood losing CO2")
print("     alkalinizes and TAKES UP O2. A maternal acidosis briefly HELPS")
print("     transfer. That term is not 'the same, delayed'.")
print("  4. No ventilatory compensation. The fetus cannot breathe faster.")
print("     Its responses are flow redistribution and, late, bradycardia.")
print("\nASSUMED: Hill n, both P50s, all PO2 operating points, the transmit ratio.")
