"""Plant-level TCI estimates for the natural gas-to-methanol case study (1,000 kt/y).

The plant-level inputs of the case study (manuscript Table 4) are passed to capcomo() for each of the
seven plant-level models. Each model returns a different cost level (IEC, ISBL or FCI) in the dollars of
its own basis year. The script then
  1) escalates every estimate to 2025 with the CEPCI (787.8), and
  2) converts it to total capital investment (TCI) with capconv(), using the Peters and Timmerhaus
     factors for fluid-processing plants,
so that all models are compared on the same cost level and the same cost year.

Run from the repository folder (or anywhere after installation):
    python examples/methanol_plant_level.py
"""
import importlib
import warnings

try:
    from ecoana import capcomo, capconv
except ModuleNotFoundError:          # not installed: run from the repository folder
    import os, sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from ecoana import capcomo, capconv

# CE index of the basis year of each model (the function capcomo shadows the module name, so the
# module is fetched with importlib)
CE_BASIS = importlib.import_module("ecoana.capcomo").CE_basis_dict

# ---- Inputs ------------------------------------------------------------------------------------------------
CEPCI_TARGET = 787.8                 # CEPCI 2025 (target cost year)
FACTOR_SET = "Peters and Timmerhaus" # plant cost factors used to convert to TCI
PHASE = "Fluid"                      # fluid-processing plant

# Plant-level data of the methanol plant (manuscript Table 4)
plant = dict(
    scale_tpy=1_000_000,             # production scale, t/y (1,000 kt/y)
    unit_num=7,                      # number of process units: 2 reforming + 2 reaction + 3 separation steps
    energyloss_MW=232.36,            # energy loss = LHV(feed + fuel) - LHV(product), MW
    energytransfer_MW=787.95,        # energy transfer duty, MW
    Tmax_K=960.0 + 273.15,           # maximum design temperature, K
    Pmax_bar=93.0,                   # maximum design pressure, bar
)

# Inputs required by each plant-level model
cases = {
    "Hill":    dict(unit_num=plant["unit_num"], scale_tpy=plant["scale_tpy"]),
    "Guthrie": dict(process="Methanol", scale_tpy=plant["scale_tpy"]),
    "Timms":   dict(unit_num=plant["unit_num"], scale_tpy=plant["scale_tpy"],
                    Tmax_K=plant["Tmax_K"], Pmax_bar=plant["Pmax_bar"]),
    "Garrett": dict(process="Methanol (steam reforming & synthesis)", scale_tpy=plant["scale_tpy"]),
    "Petley":  dict(unit_num=plant["unit_num"], scale_tpy=plant["scale_tpy"],
                    Tmax_K=plant["Tmax_K"], Pmax_bar=plant["Pmax_bar"]),
    "Lange 1": dict(energyloss_MW=plant["energyloss_MW"]),
    "Lange 2": dict(energytransfer_MW=plant["energytransfer_MW"]),
}

# ---- 1) capcomo(): estimate of each model, 2) CEPCI escalation, 3) capconv(): conversion to TCI -------
rows, notes = [], []
for model, inputs in cases.items():
    with warnings.catch_warnings(record=True) as caught:          # collect range warnings as notes
        warnings.simplefilter("always")
        cost, basis, cost_type = capcomo(model=model, **inputs)
    notes += [f"{model}: {w.message}" for w in caught]
    if cost is None:
        continue

    ce_basis = CE_BASIS[model][0]
    cost_2025 = cost * CEPCI_TARGET / ce_basis                    # escalate to 2025
    tci_2025 = capconv(model=FACTOR_SET, phase_processing=PHASE,  # convert to TCI
                       cap_in=cost_type, cap_out="Total capital investment", base_cost=cost_2025)
    rows.append((model, cost_type, basis.split()[0], ce_basis, cost / 1e6, cost_2025 / 1e6, tci_2025 / 1e6))

# ---- Results ------------------------------------------------------------------------------------------------
mean_tci = sum(r[6] for r in rows) / len(rows)
print(f"Plant-level TCI of the 1,000 kt/y methanol plant (MMUSD, CEPCI 2025 = {CEPCI_TARGET}; "
      f"{FACTOR_SET} factors, {PHASE})\n")
print(f"{'Model':<8} {'Cost type returned by capcomo':<31} {'Basis':>5} {'CE':>6} "
      f"{'Estimate':>10} {'Est. 2025':>10} {'TCI 2025':>10} {'vs mean':>8}")
for model, ctype, year, ce, est, est25, tci in rows:
    print(f"{model:<8} {ctype:<31} {year:>5} {ce:>6.1f} {est:>10.1f} {est25:>10.1f} {tci:>10.1f} "
          f"{(tci - mean_tci) / mean_tci:>+8.1%}")
print(f"\nMean TCI: {mean_tci:,.1f} MMUSD; range {min(r[6] for r in rows):,.1f} to {max(r[6] for r in rows):,.1f} MMUSD")

if notes:
    print("\nNotes (inputs outside the range of a correlation):")
    for n in notes:
        print(" -", n)
