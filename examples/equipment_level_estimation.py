"""Equipment-level purchase costs and TCI of a hypothetical process with the six equipment cost models.

The equipment list of a small, hypothetical gas compression and absorption unit is passed to eqpcomo()
with each of the six equipment cost models (Turton, Seider, Smith, Towler, Peters, Guthrie). For each model
the script
  1) calculates the purchase cost of every item and escalates it to 2025 with the CEPCI (787.8),
  2) sums the items to the total purchased equipment cost (TPEC), and
  3) converts the TPEC to total capital investment (TCI) with capconv(), using the Peters and Timmerhaus
     factors for fluid-processing plants,
and finally reports the range of TCI across the six models.

The process is illustrative only; the equipment sizes are not taken from a real plant.

Run from the repository folder (or anywhere after installation):
    python examples/equipment_level_estimation.py
"""
import importlib
import warnings

try:
    from ecoana import eqpcomo, capconv
except ModuleNotFoundError:          # not installed: run from the repository folder
    import os, sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from ecoana import eqpcomo, capconv

# CE index of the basis year of each model (the function eqpcomo shadows the module name, so the module is
# fetched with importlib)
CE_BASIS = importlib.import_module("ecoana.eqpcomo").CE_basis_dict

# ---- Inputs ------------------------------------------------------------------------------------------------
CEPCI_TARGET = 787.8                 # CEPCI 2025 (target cost year)
FACTOR_SET = "Peters and Timmerhaus" # plant cost factors used to convert TPEC to TCI
PHASE = "Fluid"                      # fluid-processing plant
MODELS = ["Turton", "Seider", "Smith", "Towler", "Peters", "Guthrie"]

# Equipment list of the hypothetical process. Pressures are absolute (bar). Every item carries all inputs
# needed by any of the six models; each model uses only the inputs it requires.
equipment_list = [
    ("K-101 feed gas compressor", dict(equipment="Compressor", eqptype="Centrifugal", material="Carbon steel",
                                       power_kW=750, P_bar=5, Pout_bar=20, T_K=320,
                                       driver="Electric-explosion proof")),
    ("P-101 solvent pump",        dict(equipment="Pumps", eqptype="Centrifugal", material="Carbon steel",
                                       power_kW=15, volflow_cumph=40, pumphead_m=60, P_bar=3, Pout_bar=8,
                                       T_K=310, driver="Electric-explosion proof")),
    ("E-101 feed/effluent exchanger", dict(equipment="Heat exchanger (shell and tube)", eqptype="Floating head",
                                       material="CS shell/CS tube", area_sqm=150, P_bar=20, T_K=420, height_m=6)),
    ("E-102 gas cooler",          dict(equipment="Heat exchanger (shell and tube)", eqptype="U-tube (shell and tube)",
                                       material="CS shell/CS tube", area_sqm=80, P_bar=20, T_K=400, height_m=6)),
    ("V-101 flash drum",          dict(equipment="Vessel/Tower", eqptype="Vertical vessel", material="Carbon steel",
                                       diameter_m=1.5, height_m=4.5, P_bar=20, T_K=310)),
    ("T-101 absorber shell",      dict(equipment="Vessel/Tower", eqptype="Vertical vessel", material="Carbon steel",
                                       diameter_m=2.0, height_m=18, P_bar=20, T_K=310)),
    ("V-102 knock-out drum",      dict(equipment="Vessel/Tower", eqptype="Horizontal vessel", material="Carbon steel",
                                       diameter_m=1.2, height_m=3.6, P_bar=5, T_K=310)),
]

# ---- 1) eqpcomo(): purchase cost of each item, escalated to 2025 -------------------------------------------
costs = {m: {} for m in MODELS}      # costs[model][item] = purchase cost, USD 2025
notes = []
for model in MODELS:
    for tag, spec in equipment_list:
        with warnings.catch_warnings(record=True) as caught:      # collect range warnings as notes
            warnings.simplefilter("always")
            cost, basis = eqpcomo(model=model, **spec)
        notes += [f"{model}, {tag}: {w.message}" for w in caught]
        if cost is not None:
            costs[model][tag] = float(cost) * CEPCI_TARGET / CE_BASIS[model][0]

# ---- 2) TPEC and 3) capconv(): TPEC -> TCI ------------------------------------------------------------------
summary = []
for model in MODELS:
    tpec = sum(costs[model].values())
    tci = capconv(model=FACTOR_SET, phase_processing=PHASE, cap_in="Equipment cost",
                  cap_out="Total capital investment", base_cost=tpec)
    summary.append((model, tpec, tci))

# ---- Results ------------------------------------------------------------------------------------------------
print(f"Purchased equipment cost by item (thousand USD, CEPCI 2025 = {CEPCI_TARGET})\n")
print(f"{'Item':<31}" + "".join(f"{m:>10}" for m in MODELS))
for tag, _ in equipment_list:
    print(f"{tag:<31}" + "".join(f"{costs[m][tag]/1e3:>10,.0f}" if tag in costs[m] else f"{'n/a':>10}"
                                 for m in MODELS))
print(f"{'TPEC':<31}" + "".join(f"{tpec/1e3:>10,.0f}" for _, tpec, _ in summary))

mean_tci = sum(t for *_, t in summary) / len(summary)
print(f"\nTCI by model (million USD, 2025; {FACTOR_SET} factors, {PHASE})\n")
print(f"{'Model':<8}{'TPEC':>10}{'TCI':>10}{'vs mean':>10}")
for model, tpec, tci in summary:
    print(f"{model:<8}{tpec/1e6:>10.2f}{tci/1e6:>10.2f}{(tci - mean_tci)/mean_tci:>+10.1%}")
tcis = [t for *_, t in summary]
print(f"\nMean TCI: {mean_tci/1e6:,.2f} million USD; range {min(tcis)/1e6:,.2f} to {max(tcis)/1e6:,.2f} million USD "
      f"({(min(tcis)-mean_tci)/mean_tci:+.1%} to {(max(tcis)-mean_tci)/mean_tci:+.1%} of the mean)")

if notes:
    print("\nNotes (warnings from eqpcomo):")
    for n in notes:
        print(" -", n)
