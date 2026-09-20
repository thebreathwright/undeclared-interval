#!/usr/bin/env python3
"""
Work-of-breathing budget. THIS IS A MODEL, NOT A MEASUREMENT.

Every constant below is a parameter you can change. None was read from a
source document in this session. The component splits are textbook-typical
values, not measurements of any person. Change them and the answer changes.
"""
J_PER_KCAL = 4184
MIN_PER_DAY = 1440

# --- PARAMETERS (all assumed) ----------------------------------------------
VE_REST      = 6.0    # L/min  minute ventilation at rest
WOB_PER_L    = 0.5    # J/L    mechanical work of breathing, resting
EFFICIENCY   = 0.08   # respiratory muscle efficiency, 2-10% typical

# component splits of MECHANICAL work (assumed, textbook-typical)
SPLIT_WORK = [("elastic, lung",        0.35),
              ("elastic, chest wall",  0.30),
              ("resistive, airway",    0.28),
              ("resistive, tissue",    0.07)]
# which muscles do it (assumed; expiration is passive at rest)
SPLIT_MUSCLE = [("diaphragm",            0.70),
                ("external intercostals",0.22),
                ("accessory (scalene/SCM)",0.08),
                ("expiratory muscles",   0.00)]

TARGET = 426.0   # kcal/day, the figure under test
RMR    = 1586.0  # kcal/day, the measured group mean in the corpus

# --- FORWARD: what standard mechanics gives --------------------------------
mech_J_min = VE_REST * WOB_PER_L
met_J_min  = mech_J_min / EFFICIENCY
kcal_day   = met_J_min * MIN_PER_DAY / J_PER_KCAL

print("FORWARD MODEL  (resting, from mechanics)\n")
print(f"  ventilation            {VE_REST:6.2f} L/min")
print(f"  mechanical work        {mech_J_min:6.2f} J/min   ({WOB_PER_L} J/L)")
print(f"  at {EFFICIENCY:.0%} efficiency      {met_J_min:6.2f} J/min metabolic")
print(f"  COST OF BREATHING      {kcal_day:6.1f} kcal/day   = {kcal_day/RMR:.1%} of {RMR:.0f}\n")

print("  by mechanical component:")
for n,f in SPLIT_WORK:
    print(f"    {n:<24}{kcal_day*f:6.2f} kcal/day")
print("\n  by muscle:")
for n,f in SPLIT_MUSCLE:
    print(f"    {n:<24}{kcal_day*f:6.2f} kcal/day")

# --- REVERSE: what 426 would require ---------------------------------------
print("\n" + "="*64)
print(f"REVERSE  (what would make the cost of breathing {TARGET:.0f} kcal/day)\n")
need_J_min = TARGET * J_PER_KCAL / MIN_PER_DAY
print(f"  required metabolic power   {need_J_min:8.1f} J/min")
print(f"  ratio to the forward model {need_J_min/met_J_min:8.1f} x\n")
print("  holding mechanics fixed, efficiency would have to be:")
print(f"    {mech_J_min/need_J_min:.3%}   (measured range is 2-10%)\n")
print("  holding efficiency fixed, mechanical work would have to be:")
w = need_J_min*EFFICIENCY
print(f"    {w:.1f} J/min = {w/WOB_PER_L:.1f} L/min ventilation")
print(f"    that is {w/WOB_PER_L/VE_REST:.0f}x resting VE - heavy exercise, not rest\n")
print(f"  {TARGET:.0f}/{RMR:.0f} = {TARGET/RMR:.1%} of RMR. Cost of breathing at rest")
print("  is usually put at 1-3%. The gap is about one order of magnitude.")
print("\nNOTHING ABOVE IS SOURCED. It is arithmetic on assumed parameters.")
