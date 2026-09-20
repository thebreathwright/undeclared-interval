#!/usr/bin/env python3
"""Nostril to cell and back. A MODEL. Every constant is assumed, none sourced."""
J_KCAL, MIN_DAY = 4184, 1440

# --- fixed starting point (pick one, state it) ---
T_AMB, RH_AMB = 20.0, 0.50      # degC, fraction
T_ALV, RH_ALV = 37.0, 1.00
VE     = 6.0                    # L/min
L_DAY  = VE * MIN_DAY           # 8640 L/day

# --- air properties (assumed) ---
RHO_AIR = 1.204                 # g/L at 20C
CP_AIR  = 1.005                 # J/g/K
SVD     = {20: 17.3, 37: 44.0}  # g/m3 saturation vapour density
LATENT  = 2414.0                # J/g at 37C

# --- efficiencies / recoveries (assumed) ---
EFF_RESP = 0.08                 # respiratory muscle efficiency
WOB_J_L  = 0.5                  # J/L mechanical work of breathing
REC_NASAL, REC_ORAL = 0.30, 0.05   # HME recovery on expiration
HEART_SHARE = 0.08              # heart's share of RMR at rest
RMR = 1586.0

def per_day(j_per_L): return j_per_L * L_DAY / J_KCAL

# 1 HEAT the air
heat_J_L = RHO_AIR * CP_AIR * (T_ALV - T_AMB)
# 2 HUMIDIFY the air
g_in  = SVD[20]/1000 * RH_AMB
g_out = SVD[37]/1000 * RH_ALV
hum_J_L = (g_out - g_in) * LATENT
cond_J_L = heat_J_L + hum_J_L

# 3 MECHANICAL
mech_kcal = (VE*WOB_J_L/EFF_RESP) * MIN_DAY / J_KCAL
# 4 CIRCULATION
heart_kcal = RMR * HEART_SHARE

print(f"START: {T_AMB:.0f}C / {RH_AMB:.0%} RH -> {T_ALV:.0f}C / {RH_ALV:.0%}, "
      f"VE {VE} L/min = {L_DAY:,.0f} L/day\n")
print(f"{'component':<34}{'J/L':>8}{'kcal/day':>11}")
print("-"*53)
print(f"{'heat air to 37C':<34}{heat_J_L:8.1f}{per_day(heat_J_L):11.1f}")
print(f"{'humidify to saturation':<34}{hum_J_L:8.1f}{per_day(hum_J_L):11.1f}")
print(f"{'  CONDITIONING, gross':<34}{cond_J_L:8.1f}{per_day(cond_J_L):11.1f}")
print()
for lab, rec in (("nasal route, %d%% recovered"%(REC_NASAL*100), REC_NASAL),
                 ("oral route,  %d%% recovered"%(REC_ORAL*100),  REC_ORAL)):
    print(f"{'  '+lab:<34}{cond_J_L*(1-rec):8.1f}{per_day(cond_J_L*(1-rec)):11.1f}")
route_cost = per_day(cond_J_L*(1-REC_ORAL)) - per_day(cond_J_L*(1-REC_NASAL))
print(f"\n{'  COST OF THE OPEN MOUTH':<34}{'':>8}{route_cost:11.1f}  kcal/day\n")
print(f"{'mechanical work of breathing':<34}{'':>8}{mech_kcal:11.1f}")
print(f"{'cardiac work (%d%% of RMR)'%(HEART_SHARE*100):<34}{'':>8}{heart_kcal:11.1f}")
print("-"*53)
for lab, rec in (("TOTAL, nasal", REC_NASAL), ("TOTAL, oral", REC_ORAL)):
    t = per_day(cond_J_L*(1-rec)) + mech_kcal + heart_kcal
    print(f"{lab:<34}{'':>8}{t:11.1f}   {t/RMR:6.1%} of RMR")
print()
t_n = per_day(cond_J_L*(1-REC_NASAL)) + mech_kcal + heart_kcal
t_o = per_day(cond_J_L*(1-REC_ORAL))  + mech_kcal + heart_kcal
print(f"426 sits between them: nasal {t_n:.0f} < 426 < oral {t_o:.0f}" if t_n<426<t_o
      else f"426 vs nasal {t_n:.0f} / oral {t_o:.0f}")
print(f"\nNOT sourced. Humidification is {hum_J_L/cond_J_L:.0%} of conditioning;")
print("it dominates, and it is the term the nose recovers.")
