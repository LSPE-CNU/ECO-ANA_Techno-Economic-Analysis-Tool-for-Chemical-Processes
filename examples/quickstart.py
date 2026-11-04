"""Quick check that ECO-ANA is installed correctly.

Run from any folder after installation:
    python examples/quickstart.py
"""
try:
    from ecoana import eqpcomo, capcomo, capconv
except ModuleNotFoundError:          # not installed: run from the repository folder
    import os, sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from ecoana import eqpcomo, capcomo, capconv

# 1) Equipment cost of one centrifugal pump with the six equipment cost models
pump = dict(equipment="Pumps", eqptype="Centrifugal", material="Carbon steel",
            power_kW=50, P_bar=10, Pout_bar=15, volflow_cumph=50, pumphead_m=50,
            driver="Electric-open/drip proof")
print("Equipment cost of a centrifugal pump (USD, model basis year)")
for model in ["Turton", "Seider", "Smith", "Towler", "Peters", "Guthrie"]:
    cost, basis = eqpcomo(model=model, **pump)
    print(f"  {model:<8s}: {float(cost):>12,.0f}  ({basis})")

# 2) Conceptual (top-down) capital cost with the Hill model
cost, basis, cost_type = capcomo(model="Hill", unit_num=10, scale_tpy=100_000)
print(f"\nHill model: {cost:,.0f} USD ({cost_type}, {basis})")

# 3) Convert total equipment cost to total capital investment
tci = capconv(model="Peters and Timmerhaus", phase_processing="Fluid",
              cap_in="TPEC", cap_out="TCI", base_cost=1_000_000)
print(f"Peters and Timmerhaus factors: TPEC 1,000,000 USD -> TCI {tci:,.0f} USD")
print("\nECO-ANA is installed and working.")
