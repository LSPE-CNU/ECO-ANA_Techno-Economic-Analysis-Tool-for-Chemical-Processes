# ECO-ANA (Process ECOnomic ANAlyzer)

<img width="4816" height="1256" alt="ECO-ANA" src="https://github.com/user-attachments/assets/49512815-1450-48d7-b29f-f2950aa8fdea" />

ECO-ANA is an open-source Python package for early-stage techno-economic analysis (TEA) of chemical processes. 
It estimates capital costs using several published cost estimation models through a unified interface, enabling users to evaluate and account for uncertainty associated with model selection in TEA results by reporting the variation in estimates across different models.

This was developed by **LSPE**, the *Laboratory for Sustainable Process Engineering* from Chungnam National University.  
LSPE@CNU: https://sites.google.com/view/rohgroup

- `eqpcomo` – equipment purchase cost (Turton, Seider, Smith, Towler, Peters, Guthrie)
- `capcomo` – conceptual (top-down) capital cost (Hill, Guthrie, Timms, Garrett, Petley, Lange 1, Lange 2)
- `capconv` – conversion between capital cost levels (TPEC → IEC → ISBL → FCI → TCI)

Current version: **1.0.0** · Install with `pip install ecoana`

## Repository structure

```
├── ecoana/            # the Python package (import ecoana)
├── examples/          # example scripts
├── docs/              # supported-equipment and capcomo model tables (XLSX, CSV)
├── tests/             # unit tests (pytest)
├── pyproject.toml     # package metadata and build configuration
├── requirements.txt   # runtime dependencies
├── environment.yml    # conda environment
├── MANIFEST.in      # extra files for the source distribution
├── README.md
├── CHANGELOG.md
└── LICENSE.txt
```

## Installation

### Requirements

| Item | Supported |
|---|---|
| Python | 3.9, 3.10, 3.11, 3.12, 3.13 |
| Operating system | Windows, macOS, Linux (pure Python, no compilation needed) |
| Dependencies | `numpy >= 1.21` (installed automatically) |

### Option A — install from PyPI (recommended)

```bash
# Create and activate a virtual environment (optional but recommended)
python -m venv .venv
# Windows:      .venv\Scripts\activate
# macOS/Linux:  source .venv/bin/activate

pip install ecoana
```

This installs ECO-ANA and its dependency (numpy). To upgrade an existing installation, use
`pip install --upgrade ecoana`.

### Option B — install from source

```bash
git clone https://github.com/LSPE-CNU/ECO-ANA_Techno-Economic-Analysis-Tool-for-Chemical-Processes.git
cd ECO-ANA_Techno-Economic-Analysis-Tool-for-Chemical-Processes
pip install .
```

or, without cloning:

```bash
pip install git+https://github.com/LSPE-CNU/ECO-ANA_Techno-Economic-Analysis-Tool-for-Chemical-Processes.git
```

The package can also be used without installation: after installing the dependency with
`pip install -r requirements.txt`, `from ecoana import ...` works when Python is started from the
repository root.

### Option C — conda

```bash
git clone https://github.com/LSPE-CNU/ECO-ANA_Techno-Economic-Analysis-Tool-for-Chemical-Processes.git
cd ECO-ANA_Techno-Economic-Analysis-Tool-for-Chemical-Processes
conda env create -f environment.yml
conda activate ecoana
```

### Check the installation

```bash
python examples/quickstart.py
```

or, after installing from PyPI, check the installed version with
`python -c "import ecoana; print(ecoana.__version__)"`.

The script estimates the cost of one pump with all six equipment cost models, runs one conceptual
capital cost model and one cost-level conversion, and ends with `ECO-ANA is installed and working.`

### Run the unit tests

From the repository root (source installation):

```bash
pip install pytest
python -m pytest tests
```

The tests do the following:
- Run every model/equipment/type combination of `eqpcomo()` (426 combinations).
- Check the process libraries of the Guthrie and Garrett models.
- Check range handling, input validation and error handling of `capcomo()`.
- Check the factor sets and keyword aliases of `capconv()`.
- Reproduce the calls reported during review and the worked examples of the source publications.

## Basic usage

```python
from ecoana import eqpcomo, capcomo, capconv

# Equipment purchase cost (returns cost in USD and the cost-index basis year of the model)
cost, basis = eqpcomo(model="Turton", equipment="Pumps", eqptype="Centrifugal",
                      material="Carbon steel", power_kW=50, P_bar=10)

# Conceptual capital cost
cost, basis, cost_type = capcomo(model="Hill", unit_num=10, scale_tpy=100_000)

# Total equipment purchase cost -> total capital investment
tci = capconv(model="Peters and Timmerhaus", phase_processing="Fluid",
              cap_in="TPEC", cap_out="TCI", base_cost=1_000_000)
```

## Examples

The `examples/` folder contains three scripts. Run them from the repository folder, or from anywhere
after installation:

| Script | What it shows |
|---|---|
| `examples/quickstart.py` | Installation check. Estimates the cost of one pump with the six equipment cost models, runs one plant-level model and one cost-level conversion. |
| `examples/methanol_plant_level.py` | Plant-level TCI of the 1,000 kt/y natural gas-to-methanol case study with the seven `capcomo()` models. |
| `examples/equipment_level_estimation.py` | Equipment purchase costs and TCI of a hypothetical process with the six `eqpcomo()` models. |

```bash
python examples/methanol_plant_level.py
python examples/equipment_level_estimation.py
```

### Plant-level TCI: `methanol_plant_level.py`

1. The plant-level inputs of the methanol case study (manuscript Table 4) are passed to `capcomo()` for
   each model. The inputs are the production scale, number of process units, energy loss, energy
   transfer duty, and maximum design temperature and pressure.
2. Each estimate is escalated from the basis year of its model to 2025 with the CEPCI (787.8).
3. The models return different cost levels (IEC, ISBL or FCI). `capconv()` converts each of them to TCI
   with the Peters and Timmerhaus factors for fluid-processing plants.
4. The script prints, for each model, the cost level returned by `capcomo()`, the basis year, the estimate,
   the 2025 value, the TCI and its deviation from the mean.
5. Warnings for inputs outside the range of a correlation are listed at the end (e.g., a plant split into
   parallel trains).

### Equipment-level TCI: `equipment_level_estimation.py`

1. The equipment list of a hypothetical gas compression and absorption unit is passed to `eqpcomo()` with
   each of the six models. The list has a compressor, a pump, two shell-and-tube exchangers and three
   vessels. The process is illustrative; the sizes are not taken from a real plant.
2. Each purchase cost is escalated from the basis year of its model to 2025 with the CEPCI (787.8).
3. The items are summed to the total purchased equipment cost (TPEC).
4. `capconv()` converts the TPEC to TCI with the Peters and Timmerhaus factors for fluid-processing plants.
5. The script prints the purchase cost of each item by model, the TPEC and TCI of each model, and the range
   of TCI across the models. `eqpcomo()` warnings, e.g. sizes below the lower limit of a correlation, are
   listed at the end.

The target cost year, the factor set and the inputs are defined at the top of each script and can be
changed for other cases.

## Inputs of `eqpcomo()` and conventions

| Input | Unit | Meaning |
|---|---|---|
| `model` | – | `"Turton"`, `"Seider"`, `"Smith"`, `"Towler"`, `"Peters"`, `"Guthrie"` |
| `equipment`, `eqptype` | – | Equipment class and sub-type (see the supported-equipment table) |
| `material` | – | Material of construction; aliases such as `"CS"`, `"SS"`, `"SS316"`, `"Cr-Mo"` are accepted |
| `P_bar`, `Pout_bar` | bar, **absolute** | Operating (inlet) and outlet/discharge pressure |
| `T_K` | K | Operating temperature |
| `vol_cum` | m³ | Volume |
| `area_sqm` | m² | Area (heat-transfer, filter, drying, screen area …) |
| `height_m`, `diameter_m`, `thickness_m` | m | Height/length, diameter (belt/pan width for conveyors), wall thickness |
| `length_m` | m | Conveying length (conveyors) |
| `volflow_cumph` | m³/h | Volumetric flow rate |
| `massflow_kgph` | kg/h | Mass flow rate (feed, solids, steam, evaporation or air load, depending on the equipment) |
| `power_kW` | kW | Power or heat duty, depending on the equipment |
| `pumphead_m` | m | Pump head |
| `num` | – | Number of trays |
| `packsize_in` | in | Packing size |
| `driver` | – | Driver type (compressors, pumps) |

- **Pressure is absolute.** `P_bar` and `Pout_bar` are absolute pressures. Correlations defined in gauge
  pressure (Turton, Seider and Guthrie pressure factors) convert internally with P(gauge) = P − 1.013 bar.
  For example, an operating pressure of 10 barg is entered as `P_bar=11.013`.
- Inputs left at their default (0 or `None`) are treated as not given. For vessels, `vol_cum` and
  `thickness_m` are optional and are estimated from the diameter, height, pressure and temperature
  (simplified ASME shell formula).
- **Sizes outside the range of a correlation** are handled as follows, and **a `UserWarning` is issued in
  every case**. The warning names the model, equipment, type, input size and limit, and the action taken.
  - **Below the lower limit:** the cost is evaluated at the lower limit. For tray, column and vessel
    diameters (Smith and Towler trays, Guthrie vessels), the correlation is extrapolated instead.
  - **Above the upper limit:** the equipment is represented as *k* = ceil(size / upper limit) identical
    parallel units, and the cost is *k* times the cost of one unit. Where a larger size cannot be represented
    by parallel units, the correlation is extrapolated. This applies to diameters of trays, centrifuge bowls
    and motionless mixers, and to vessel diameters.
  - Correlations with no size range in the source (cost proportional to the volume of packing or adsorbent,
    or to the membrane area) are applied without a limit.
- On an input error, `eqpcomo()` prints an error message and returns `None` as the cost. It always returns a
  2-tuple (`cost, basis`), so unpacking the result does not fail; the tuple is `(None, None)` when the model
  is missing or unknown.
- Costs are purchase costs in USD at the cost-index basis returned with the result (e.g.
  `"2001 year basis"`); escalate them to the target year with the CEPCI.

### Supported equipment

The full list of supported equipment is provided in
[`docs/ECO-ANA_supported_equipment.xlsx`](https://github.com/LSPE-CNU/ECO-ANA_Techno-Economic-Analysis-Tool-for-Chemical-Processes/blob/main/docs/ECO-ANA_supported_equipment.xlsx) (also as CSV). For every
model, equipment and type, it gives the accepted materials, the size (capacity) inputs and their units,
all required inputs, whether pressure, pressure rise or temperature affect the cost, the driver options
and notes.

The table below summarizes it. "Cost basis" is the cost-index basis year of each model; "Size / capacity
input(s)" are the inputs that change the cost; units of all inputs are given in the table above.

<details>
<summary>Supported equipment (426 model / equipment / type combinations)</summary>

| Model | Cost basis | Equipment | Type (eqptype) | Accepted materials | Size / capacity input(s) | Required inputs | Driver options | Notes |
|---|---|---|---|---|---|---|---|---|
| Turton | 2001 | Blender | Kneader | — (material does not affect the cost) | vol_cum | eqptype, material, vol_cum |  |  |
| Turton | 2001 | Blender | Ribbon | — (material does not affect the cost) | vol_cum | eqptype, material, vol_cum |  |  |
| Turton | 2001 | Blender | Rotary | — (material does not affect the cost) | vol_cum | eqptype, material, vol_cum |  |  |
| Turton | 2001 | Centrifuge | Auto batch separator (horizontal) | — (material does not affect the cost) | diameter_m | eqptype, material, diameter_m |  |  |
| Turton | 2001 | Centrifuge | Auto batch separator (vertical) | — (material does not affect the cost) | diameter_m | eqptype, material, diameter_m |  |  |
| Turton | 2001 | Centrifuge | Centrifugal separator | — (material does not affect the cost) | diameter_m | eqptype, material, diameter_m |  |  |
| Turton | 2001 | Centrifuge | Oscillating screen | — (material does not affect the cost) | diameter_m | eqptype, material, diameter_m |  |  |
| Turton | 2001 | Centrifuge | Solid bowl w/o motor | — (material does not affect the cost) | diameter_m | eqptype, material, diameter_m |  |  |
| Turton | 2001 | Compressor | Axial | Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | power_kW | eqptype, power_kW, P_bar, material, driver | Electric-open/drip proof, Electric-explosion proof, Electric-totally enclosed, Steam turbine, Gas turbine, Intern comb.engine | power_kW = compressor (shaft/fluid) power. |
| Turton | 2001 | Compressor | Centrifugal | Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | power_kW | eqptype, power_kW, P_bar, material, driver | Electric-open/drip proof, Electric-explosion proof, Electric-totally enclosed, Steam turbine, Gas turbine, Intern comb.engine | power_kW = compressor (shaft/fluid) power. |
| Turton | 2001 | Compressor | Reciprocating | Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | power_kW | eqptype, power_kW, P_bar, material, driver | Electric-open/drip proof, Electric-explosion proof, Electric-totally enclosed, Steam turbine, Gas turbine, Intern comb.engine | power_kW = compressor (shaft/fluid) power. |
| Turton | 2001 | Compressor | Rotary | Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | power_kW | eqptype, power_kW, P_bar, material, driver | Electric-open/drip proof, Electric-explosion proof, Electric-totally enclosed, Steam turbine, Gas turbine, Intern comb.engine | power_kW = compressor (shaft/fluid) power. |
| Turton | 2001 | Conveyor | Apron | — (material does not affect the cost) | area_sqm | eqptype, material, area_sqm |  |  |
| Turton | 2001 | Conveyor | Belt | — (material does not affect the cost) | area_sqm | eqptype, material, area_sqm |  |  |
| Turton | 2001 | Conveyor | Pneumatic | — (material does not affect the cost) | area_sqm | eqptype, material, area_sqm |  |  |
| Turton | 2001 | Conveyor | Screw | — (material does not affect the cost) | area_sqm | eqptype, material, area_sqm |  |  |
| Turton | 2001 | Crystallizer-batch evaporative | Batch | — (material does not affect the cost) | vol_cum | eqptype, material, vol_cum |  |  |
| Turton | 2001 | Dryer | Drum | Carbon steel | area_sqm | eqptype, material, area_sqm |  |  |
| Turton | 2001 | Dryer | Rotary(gas fired) | Carbon steel | area_sqm | eqptype, material, area_sqm |  |  |
| Turton | 2001 | Dryer | Tray | Carbon steel | area_sqm | eqptype, material, area_sqm |  |  |
| Turton | 2001 | Dust collector | Baghouse | — (material does not affect the cost) | vol_cum | eqptype, material, vol_cum |  | vol_cum = unit volume (Turton Table A.1). |
| Turton | 2001 | Dust collector | Cyclone scrubbers | — (material does not affect the cost) | vol_cum | eqptype, material, vol_cum |  | vol_cum = unit volume (Turton Table A.1). |
| Turton | 2001 | Dust collector | Electrostatic precipitator | — (material does not affect the cost) | vol_cum | eqptype, material, vol_cum |  | vol_cum = unit volume (Turton Table A.1). |
| Turton | 2001 | Dust collector | Venturi scrubber | — (material does not affect the cost) | vol_cum | eqptype, material, vol_cum |  | vol_cum = unit volume (Turton Table A.1). |
| Turton | 2001 | Evaporator | Agitated film(scraped wall) | Carbon steel, Copper(alloy), Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | area_sqm | eqptype, area_sqm, P_bar, material |  |  |
| Turton | 2001 | Evaporator | Falling film | Carbon steel, Copper(alloy), Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | area_sqm | eqptype, area_sqm, P_bar, material |  |  |
| Turton | 2001 | Evaporator | Forced circulation(pumped) | Carbon steel, Copper(alloy), Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | area_sqm | eqptype, area_sqm, P_bar, material |  |  |
| Turton | 2001 | Evaporator | Long tube | Carbon steel, Copper(alloy), Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | area_sqm | eqptype, area_sqm, P_bar, material |  |  |
| Turton | 2001 | Evaporator | Short tube | Carbon steel, Copper(alloy), Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | area_sqm | eqptype, area_sqm, P_bar, material |  |  |
| Turton | 2001 | Fans | Axial tube | Carbon steel, Fiberglass, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | volflow_cumph | eqptype, volflow_cumph, P_bar, material, Pout_bar |  | Pressure factor from the pressure rise Pout_bar − P_bar. |
| Turton | 2001 | Fans | Axial vane | Carbon steel, Fiberglass, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | volflow_cumph | eqptype, volflow_cumph, P_bar, material, Pout_bar |  | Pressure factor from the pressure rise Pout_bar − P_bar. |
| Turton | 2001 | Fans | Centrifugal backward-curved | Carbon steel, Fiberglass, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | volflow_cumph | eqptype, volflow_cumph, P_bar, material, Pout_bar |  | Pressure factor from the pressure rise Pout_bar − P_bar. |
| Turton | 2001 | Fans | Centrifugal straight-radial | Carbon steel, Fiberglass, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | volflow_cumph | eqptype, volflow_cumph, P_bar, material, Pout_bar |  | Pressure factor from the pressure rise Pout_bar − P_bar. |
| Turton | 2001 | Filters | Bent | — (material does not affect the cost) | area_sqm | eqptype, material, area_sqm |  |  |
| Turton | 2001 | Filters | Cartridge | — (material does not affect the cost) | area_sqm | eqptype, material, area_sqm |  |  |
| Turton | 2001 | Filters | Disc and drum | — (material does not affect the cost) | area_sqm | eqptype, material, area_sqm |  |  |
| Turton | 2001 | Filters | Gravity | — (material does not affect the cost) | area_sqm | eqptype, material, area_sqm |  |  |
| Turton | 2001 | Filters | Leaf | — (material does not affect the cost) | area_sqm | eqptype, material, area_sqm |  |  |
| Turton | 2001 | Filters | Pan | — (material does not affect the cost) | area_sqm | eqptype, material, area_sqm |  |  |
| Turton | 2001 | Filters | Plate and frame | — (material does not affect the cost) | area_sqm | eqptype, material, area_sqm |  |  |
| Turton | 2001 | Filters | Table | — (material does not affect the cost) | area_sqm | eqptype, material, area_sqm |  |  |
| Turton | 2001 | Filters | Tube | — (material does not affect the cost) | area_sqm | eqptype, material, area_sqm |  |  |
| Turton | 2001 | Furnace | Nonreactive furnace | Carbon steel, Stainless steel | power_kW | eqptype, power_kW, P_bar, material |  |  |
| Turton | 2001 | Furnace | Pyrolysis furnace | Carbon steel, Stainless steel | power_kW | eqptype, power_kW, P_bar, material |  |  |
| Turton | 2001 | Furnace | Reformer furnace | Carbon steel, Stainless steel | power_kW | eqptype, power_kW, P_bar, material |  |  |
| Turton | 2001 | Heat exchanger (others) | Air cooler | Aluminum(alloy), Carbon steel, Stainless steel | area_sqm | eqptype, area_sqm, P_bar, material |  |  |
| Turton | 2001 | Heat exchanger (others) | Flat plate | Aluminum(alloy), Carbon steel, Copper(alloy), Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | area_sqm | eqptype, area_sqm, P_bar, material |  |  |
| Turton | 2001 | Heat exchanger (others) | Spiral plate | Aluminum(alloy), Carbon steel, Copper(alloy), Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | area_sqm | eqptype, area_sqm, P_bar, material |  |  |
| Turton | 2001 | Heat exchanger (shell and tube) | Bayonet | CS shell/CS tube, CS shell/Cu tube, CS shell/Ni(alloy) tube, CS shell/SS tube, CS shell/Ti(alloy) tube, Cu shell/Cu tube, Ni(alloy) shell/Ni(alloy) tube, SS shell/SS tube, Ti(alloy) shell/Ti(alloy) tube | area_sqm | eqptype, area_sqm, P_bar, material |  |  |
| Turton | 2001 | Heat exchanger (shell and tube) | Double pipe | CS shell/CS tube, CS shell/Cu tube, CS shell/Ni(alloy) tube, CS shell/SS tube, CS shell/Ti(alloy) tube, Cu shell/Cu tube, Ni(alloy) shell/Ni(alloy) tube, SS shell/SS tube, Ti(alloy) shell/Ti(alloy) tube | area_sqm | eqptype, area_sqm, P_bar, material |  |  |
| Turton | 2001 | Heat exchanger (shell and tube) | Fixed tube | CS shell/CS tube, CS shell/Cu tube, CS shell/Ni(alloy) tube, CS shell/SS tube, CS shell/Ti(alloy) tube, Cu shell/Cu tube, Ni(alloy) shell/Ni(alloy) tube, SS shell/SS tube, Ti(alloy) shell/Ti(alloy) tube | area_sqm | eqptype, area_sqm, P_bar, material |  |  |
| Turton | 2001 | Heat exchanger (shell and tube) | Floating head | CS shell/CS tube, CS shell/Cu tube, CS shell/Ni(alloy) tube, CS shell/SS tube, CS shell/Ti(alloy) tube, Cu shell/Cu tube, Ni(alloy) shell/Ni(alloy) tube, SS shell/SS tube, Ti(alloy) shell/Ti(alloy) tube | area_sqm | eqptype, area_sqm, P_bar, material |  |  |
| Turton | 2001 | Heat exchanger (shell and tube) | Kettle reboiler | CS shell/CS tube, CS shell/Cu tube, CS shell/Ni(alloy) tube, CS shell/SS tube, CS shell/Ti(alloy) tube, Cu shell/Cu tube, Ni(alloy) shell/Ni(alloy) tube, SS shell/SS tube, Ti(alloy) shell/Ti(alloy) tube | area_sqm | eqptype, area_sqm, P_bar, material |  |  |
| Turton | 2001 | Heat exchanger (shell and tube) | Multiple pipe | CS shell/CS tube, CS shell/Cu tube, CS shell/Ni(alloy) tube, CS shell/SS tube, CS shell/Ti(alloy) tube, Cu shell/Cu tube, Ni(alloy) shell/Ni(alloy) tube, SS shell/SS tube, Ti(alloy) shell/Ti(alloy) tube | area_sqm | eqptype, area_sqm, P_bar, material |  |  |
| Turton | 2001 | Heat exchanger (shell and tube) | Scraped wall | CS shell/CS tube, CS shell/Cu tube, CS shell/Ni(alloy) tube, CS shell/SS tube, CS shell/Ti(alloy) tube, Cu shell/Cu tube, Ni(alloy) shell/Ni(alloy) tube, SS shell/SS tube, Ti(alloy) shell/Ti(alloy) tube | area_sqm | eqptype, area_sqm, P_bar, material |  |  |
| Turton | 2001 | Heat exchanger (shell and tube) | Spiral tube (shell and tube) | CS shell/CS tube, CS shell/Cu tube, CS shell/Ni(alloy) tube, CS shell/SS tube, CS shell/Ti(alloy) tube, Cu shell/Cu tube, Ni(alloy) shell/Ni(alloy) tube, SS shell/SS tube, Ti(alloy) shell/Ti(alloy) tube | area_sqm | eqptype, area_sqm, P_bar, material |  |  |
| Turton | 2001 | Heat exchanger (shell and tube) | Spiral tube (tube only) | CS shell/CS tube, CS shell/Cu tube, CS shell/Ni(alloy) tube, CS shell/SS tube, CS shell/Ti(alloy) tube, Cu shell/Cu tube, Ni(alloy) shell/Ni(alloy) tube, SS shell/SS tube, Ti(alloy) shell/Ti(alloy) tube | area_sqm | eqptype, area_sqm, P_bar, material |  |  |
| Turton | 2001 | Heat exchanger (shell and tube) | Teflon tube | Teflon tube | area_sqm | eqptype, area_sqm, P_bar, material |  |  |
| Turton | 2001 | Heat exchanger (shell and tube) | U-tube (shell and tube) | CS shell/CS tube, CS shell/Cu tube, CS shell/Ni(alloy) tube, CS shell/SS tube, CS shell/Ti(alloy) tube, Cu shell/Cu tube, Ni(alloy) shell/Ni(alloy) tube, SS shell/SS tube, Ti(alloy) shell/Ti(alloy) tube | area_sqm | eqptype, area_sqm, P_bar, material |  |  |
| Turton | 2001 | Heat exchanger (shell and tube) | U-tube (tube only) | CS shell/CS tube, CS shell/Cu tube, CS shell/Ni(alloy) tube, CS shell/SS tube, CS shell/Ti(alloy) tube, Cu shell/Cu tube, Ni(alloy) shell/Ni(alloy) tube, SS shell/SS tube, Ti(alloy) shell/Ti(alloy) tube | area_sqm | eqptype, area_sqm, P_bar, material |  |  |
| Turton | 2001 | Heater | Diphenyl heater | Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | power_kW | eqptype, power_kW, P_bar, material |  |  |
| Turton | 2001 | Heater | Hot water heater | Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | power_kW | eqptype, power_kW, P_bar, material |  |  |
| Turton | 2001 | Heater | Molten salt heater | Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | power_kW | eqptype, power_kW, P_bar, material |  |  |
| Turton | 2001 | Heater | Steam boiler | Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | power_kW | eqptype, power_kW, P_bar, material |  |  |
| Turton | 2001 | Mixer | Impeller | Carbon steel | power_kW | eqptype, material, power_kW |  |  |
| Turton | 2001 | Mixer | Propeller | Carbon steel | power_kW | eqptype, material, power_kW |  |  |
| Turton | 2001 | Mixer | Turbine | Carbon steel | power_kW | eqptype, material, power_kW |  |  |
| Turton | 2001 | Packing | Berl saddles | Carbon steel, Ceramic | vol_cum | eqptype, vol_cum, P_bar, material |  |  |
| Turton | 2001 | Packing | Cascade mini-rings | Carbon steel, Ceramic | vol_cum | eqptype, vol_cum, P_bar, material |  |  |
| Turton | 2001 | Packing | Intalox saddles | Carbon steel, Ceramic | vol_cum | eqptype, vol_cum, P_bar, material |  |  |
| Turton | 2001 | Packing | Pall rings | Carbon steel, Ceramic | vol_cum | eqptype, vol_cum, P_bar, material |  |  |
| Turton | 2001 | Packing | Raschig rings | Carbon steel, Ceramic | vol_cum | eqptype, vol_cum, P_bar, material |  |  |
| Turton | 2001 | Packing | Tellerettes | Carbon steel, Ceramic | vol_cum | eqptype, vol_cum, P_bar, material |  |  |
| Turton | 2001 | Pumps | Centrifugal | Carbon steel, Cast iron, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | power_kW | eqptype, power_kW, P_bar, material |  |  |
| Turton | 2001 | Pumps | Positive displacement | Carbon steel, Cast iron, Copper(alloy), Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | power_kW | eqptype, power_kW, P_bar, material |  |  |
| Turton | 2001 | Pumps | Reciprocating | Carbon steel, Cast iron, Copper(alloy), Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | power_kW | eqptype, power_kW, P_bar, material |  |  |
| Turton | 2001 | Reactor | Autoclave | Carbon steel | vol_cum | eqptype, material, vol_cum |  |  |
| Turton | 2001 | Reactor | Fermenter | Carbon steel | vol_cum | eqptype, material, vol_cum |  |  |
| Turton | 2001 | Reactor | Inoculum tank | Carbon steel | vol_cum | eqptype, material, vol_cum |  |  |
| Turton | 2001 | Reactor | Jacked nonagitated | Carbon steel | vol_cum | eqptype, material, vol_cum |  |  |
| Turton | 2001 | Reactor | Jacketed agitated | Carbon steel | vol_cum | eqptype, material, vol_cum |  |  |
| Turton | 2001 | Reactor | Mixer/settler | Carbon steel | vol_cum | eqptype, material, vol_cum |  |  |
| Turton | 2001 | Screens | DSM | — (material does not affect the cost) | area_sqm | eqptype, material, area_sqm |  |  |
| Turton | 2001 | Screens | Rotary | — (material does not affect the cost) | area_sqm | eqptype, material, area_sqm |  |  |
| Turton | 2001 | Screens | Stationary | — (material does not affect the cost) | area_sqm | eqptype, material, area_sqm |  |  |
| Turton | 2001 | Screens | Vibrating | — (material does not affect the cost) | area_sqm | eqptype, material, area_sqm |  |  |
| Turton | 2001 | Storage tank | Fixed roof | — (material does not affect the cost) | vol_cum | eqptype, vol_cum, P_bar, material |  |  |
| Turton | 2001 | Storage tank | Floating roof | — (material does not affect the cost) | vol_cum | eqptype, vol_cum, P_bar, material |  |  |
| Turton | 2001 | Trays | Demisters | Fluorocarbon, Nickel(alloy), Stainless steel | area_sqm, num | eqptype, area_sqm, P_bar, material, diameter_m, num |  | num = number of trays. |
| Turton | 2001 | Trays | Sieve | Carbon steel, Nickel(alloy), Stainless steel | area_sqm, num | eqptype, area_sqm, P_bar, material, diameter_m, num |  | num = number of trays. |
| Turton | 2001 | Trays | Valve | Carbon steel, Nickel(alloy), Stainless steel | area_sqm, num | eqptype, area_sqm, P_bar, material, diameter_m, num |  | num = number of trays. |
| Turton | 2001 | Turbines | Axial gas turbines | Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | power_kW | eqptype, material, power_kW |  |  |
| Turton | 2001 | Turbines | Liquid expanders | Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | power_kW | eqptype, material, power_kW |  |  |
| Turton | 2001 | Vaporizer | Internal coils/jackets | Carbon steel, Copper(alloy), Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | vol_cum | eqptype, vol_cum, P_bar, material |  |  |
| Turton | 2001 | Vaporizer | Jacketed vessels | Carbon steel, Copper(alloy), Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | vol_cum | eqptype, vol_cum, P_bar, material |  |  |
| Turton | 2001 | Vessel/Tower | Horizontal vessel | Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | vol_cum, diameter_m | eqptype, vol_cum, P_bar, material, diameter_m, height_m |  | vol_cum and thickness_m are optional; if not given they are estimated from D, H, P and T. |
| Turton | 2001 | Vessel/Tower | Vertical vessel | Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | vol_cum, diameter_m | eqptype, vol_cum, P_bar, material, diameter_m, height_m |  | vol_cum and thickness_m are optional; if not given they are estimated from D, H, P and T. |
| Seider | 2000 | Adsorbent | Activated alumina | — (material does not affect the cost) | vol_cum | eqptype, vol_cum |  |  |
| Seider | 2000 | Adsorbent | Activated carbon | — (material does not affect the cost) | vol_cum | eqptype, vol_cum |  |  |
| Seider | 2000 | Adsorbent | Molecular sieves | — (material does not affect the cost) | vol_cum | eqptype, vol_cum |  |  |
| Seider | 2000 | Adsorbent | Silica gel | — (material does not affect the cost) | vol_cum | eqptype, vol_cum |  |  |
| Seider | 2000 | Agitator | Propeller, closed vessel | Aluminum(alloy), Carbon steel, Copper(alloy), Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | power_kW | eqptype, material, power_kW |  |  |
| Seider | 2000 | Agitator | Propeller, open tank | Aluminum(alloy), Carbon steel, Copper(alloy), Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | power_kW | eqptype, material, power_kW |  |  |
| Seider | 2000 | Agitator | Turbine, closed vessel | Aluminum(alloy), Carbon steel, Copper(alloy), Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | power_kW | eqptype, material, power_kW |  |  |
| Seider | 2000 | Agitator | Turbine, open tank | Aluminum(alloy), Carbon steel, Copper(alloy), Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | power_kW | eqptype, material, power_kW |  |  |
| Seider | 2000 | Autoclave | — | Carbon steel, Stainless steel | vol_cum | material, vol_cum |  |  |
| Seider | 2000 | Blower | Centrifugal(turbo) | Carbon steel, Fiberglass, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | power_kW | eqptype, material, power_kW |  |  |
| Seider | 2000 | Blower | Rotary straight-lobo | Carbon steel, Fiberglass, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | power_kW | eqptype, material, power_kW |  |  |
| Seider | 2000 | Centrifuge | Auto batch separator (horizontal) | Aluminum(alloy), Carbon steel, Copper(alloy), Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | diameter_m | eqptype, material, diameter_m |  | diameter must be within the correlation range (20–70 in vertical; 20–43 in others), otherwise an error is returned. |
| Seider | 2000 | Centrifuge | Auto batch separator (vertical) | Aluminum(alloy), Carbon steel, Copper(alloy), Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | diameter_m | eqptype, material, diameter_m |  | diameter must be within the correlation range (20–70 in vertical; 20–43 in others), otherwise an error is returned. |
| Seider | 2000 | Centrifuge | Batch bottom-drive basket | Aluminum(alloy), Carbon steel, Copper(alloy), Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | diameter_m | eqptype, material, diameter_m |  | diameter must be within the correlation range (20–70 in vertical; 20–43 in others), otherwise an error is returned. |
| Seider | 2000 | Centrifuge | Batch top-drive basket | Aluminum(alloy), Carbon steel, Copper(alloy), Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | diameter_m | eqptype, material, diameter_m |  | diameter must be within the correlation range (20–70 in vertical; 20–43 in others), otherwise an error is returned. |
| Seider | 2000 | Compressor | Centrifugal | Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | power_kW | eqptype, material, power_kW, driver | Electric-open/drip proof, Electric-explosion proof, Electric-totally enclosed, Steam turbine, Gas turbine | power_kW = compressor (shaft/fluid) power. |
| Seider | 2000 | Compressor | Reciprocating | Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | power_kW | eqptype, material, power_kW, driver | Electric-open/drip proof, Electric-explosion proof, Electric-totally enclosed, Steam turbine, Gas turbine | power_kW = compressor (shaft/fluid) power. |
| Seider | 2000 | Compressor | Screw | Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | power_kW | eqptype, material, power_kW, driver | Electric-open/drip proof, Electric-explosion proof, Electric-totally enclosed, Steam turbine, Gas turbine | power_kW = compressor (shaft/fluid) power. |
| Seider | 2000 | Crystallizer-batch evaporative | — | Aluminum(alloy), Carbon steel, Copper(alloy), Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | vol_cum | material, vol_cum |  |  |
| Seider | 2000 | Crystallizer-continuous evaporative | Draft-tube baffed | Aluminum(alloy), Carbon steel, Copper(alloy), Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | massflow_kgph | eqptype, material, massflow_kgph |  |  |
| Seider | 2000 | Crystallizer-continuous evaporative | Forced circulation | Aluminum(alloy), Carbon steel, Copper(alloy), Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | massflow_kgph | eqptype, material, massflow_kgph |  |  |
| Seider | 2000 | Crystallizer-cooling | Jacketed scraped wall | Aluminum(alloy), Carbon steel, Copper(alloy), Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | height_m | eqptype, material, height_m |  |  |
| Seider | 2000 | Dewatering press | Roll press | Aluminum(alloy), Carbon steel, Copper(alloy), Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | massflow_kgph | eqptype, material, massflow_kgph |  |  |
| Seider | 2000 | Dewatering press | Screw press | Aluminum(alloy), Carbon steel, Copper(alloy), Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | massflow_kgph | eqptype, material, massflow_kgph |  |  |
| Seider | 2000 | Dryer | Drum | Aluminum(alloy), Carbon steel, Copper(alloy), Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | area_sqm | eqptype, material, area_sqm, massflow_kgph |  |  |
| Seider | 2000 | Dryer | Rotary(gas fired) | Aluminum(alloy), Carbon steel, Copper(alloy), Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | area_sqm | eqptype, material, area_sqm, massflow_kgph |  |  |
| Seider | 2000 | Dryer | Rotary(steam tube) | Aluminum(alloy), Carbon steel, Copper(alloy), Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | area_sqm | eqptype, material, area_sqm, massflow_kgph |  |  |
| Seider | 2000 | Dryer | Spray | Aluminum(alloy), Carbon steel, Copper(alloy), Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | massflow_kgph | eqptype, material, area_sqm, massflow_kgph |  |  |
| Seider | 2000 | Dryer | Tray | Aluminum(alloy), Carbon steel, Copper(alloy), Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | area_sqm | eqptype, material, area_sqm, massflow_kgph |  |  |
| Seider | 2000 | Dust collector | Baghouse | Aluminum(alloy), Carbon steel, Copper(alloy), Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | volflow_cumph | eqptype, material, volflow_cumph |  |  |
| Seider | 2000 | Dust collector | Cyclone scrubbers | Aluminum(alloy), Carbon steel, Copper(alloy), Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | volflow_cumph | eqptype, material, volflow_cumph |  |  |
| Seider | 2000 | Dust collector | Electrostatic precipitator | Aluminum(alloy), Carbon steel, Copper(alloy), Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | volflow_cumph | eqptype, material, volflow_cumph |  |  |
| Seider | 2000 | Dust collector | Venturi scrubber | Aluminum(alloy), Carbon steel, Copper(alloy), Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | volflow_cumph | eqptype, material, volflow_cumph |  |  |
| Seider | 2000 | Evaporator | Falling film | Aluminum(alloy), Carbon steel, Copper(alloy), Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | area_sqm | eqptype, material, area_sqm |  |  |
| Seider | 2000 | Evaporator | Forced circulation(pumped) | Aluminum(alloy), Carbon steel, Copper(alloy), Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | area_sqm | eqptype, material, area_sqm |  |  |
| Seider | 2000 | Evaporator | Long tube | Aluminum(alloy), Carbon steel, Copper(alloy), Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | area_sqm | eqptype, material, area_sqm |  |  |
| Seider | 2000 | Evaporator | Short tube | Aluminum(alloy), Carbon steel, Copper(alloy), Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | area_sqm | eqptype, material, area_sqm |  |  |
| Seider | 2000 | Fans | Axial tube | Carbon steel, Fiberglass, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | volflow_cumph | eqptype, material, Pout_bar, P_bar, volflow_cumph |  | Head factor from the pressure rise Pout_bar − P_bar. |
| Seider | 2000 | Fans | Axial vane | Carbon steel, Fiberglass, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | volflow_cumph | eqptype, material, Pout_bar, P_bar, volflow_cumph |  | Head factor from the pressure rise Pout_bar − P_bar. |
| Seider | 2000 | Fans | Centrifugal backward-curved | Carbon steel, Fiberglass, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | volflow_cumph | eqptype, material, Pout_bar, P_bar, volflow_cumph |  | Head factor from the pressure rise Pout_bar − P_bar. |
| Seider | 2000 | Fans | Centrifugal straight-radial | Carbon steel, Fiberglass, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | volflow_cumph | eqptype, material, Pout_bar, P_bar, volflow_cumph |  | Head factor from the pressure rise Pout_bar − P_bar. |
| Seider | 2000 | Filters | Disc and drum | — (material does not affect the cost) | area_sqm | eqptype, area_sqm |  |  |
| Seider | 2000 | Filters | Leaf | — (material does not affect the cost) | area_sqm | eqptype, area_sqm |  |  |
| Seider | 2000 | Filters | Pan | — (material does not affect the cost) | area_sqm | eqptype, area_sqm |  |  |
| Seider | 2000 | Filters | Plate and frame | — (material does not affect the cost) | area_sqm | eqptype, area_sqm |  |  |
| Seider | 2000 | Furnace | Nonreactive furnace | Carbon steel, Monel, Stainless steel | power_kW | eqptype, material, power_kW, P_bar |  |  |
| Seider | 2000 | Furnace | Pyrolysis furnace | Aluminum(alloy), Carbon steel, Copper(alloy), Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | power_kW | eqptype, material, power_kW, P_bar |  |  |
| Seider | 2000 | Furnace | Reformer furnace | Aluminum(alloy), Carbon steel, Copper(alloy), Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | power_kW | eqptype, material, power_kW, P_bar |  |  |
| Seider | 2000 | Heat exchanger (others) | Air cooler | Aluminum(alloy), Carbon steel, Copper(alloy), Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | area_sqm | eqptype, material, area_sqm |  |  |
| Seider | 2000 | Heat exchanger (others) | Flat plate | Aluminum(alloy), Carbon steel, Copper(alloy), Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | area_sqm | eqptype, material, area_sqm |  |  |
| Seider | 2000 | Heat exchanger (others) | Spiral plate | Aluminum(alloy), Carbon steel, Copper(alloy), Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | area_sqm | eqptype, material, area_sqm |  |  |
| Seider | 2000 | Heat exchanger (shell and tube) | Fixed tube | CS shell/CS tube, CS shell/Monel tube, CS shell/SS tube, CS shell/Ti(alloy) tube, SS shell/SS tube, Ti(alloy) shell/Ti(alloy) tube | area_sqm | eqptype, material, P_bar, area_sqm, height_m |  | height_m = tube length (tube-length factor). |
| Seider | 2000 | Heat exchanger (shell and tube) | Floating head | CS shell/CS tube, CS shell/Monel tube, CS shell/SS tube, CS shell/Ti(alloy) tube, SS shell/SS tube, Ti(alloy) shell/Ti(alloy) tube | area_sqm | eqptype, material, P_bar, area_sqm, height_m |  | height_m = tube length (tube-length factor). |
| Seider | 2000 | Heat exchanger (shell and tube) | Kettle reboiler | CS shell/CS tube, CS shell/Monel tube, CS shell/SS tube, CS shell/Ti(alloy) tube, SS shell/SS tube, Ti(alloy) shell/Ti(alloy) tube | area_sqm | eqptype, material, P_bar, area_sqm, height_m |  | height_m = tube length (tube-length factor). |
| Seider | 2000 | Heat exchanger (shell and tube) | U-tube (shell and tube) | CS shell/CS tube, CS shell/Monel tube, CS shell/SS tube, CS shell/Ti(alloy) tube, SS shell/SS tube, Ti(alloy) shell/Ti(alloy) tube | area_sqm | eqptype, material, P_bar, area_sqm, height_m |  | height_m = tube length (tube-length factor). |
| Seider | 2000 | Heater | Diphenyl heater | — (material does not affect the cost) | power_kW | eqptype, power_kW |  |  |
| Seider | 2000 | Heater | Hot water heater | — (material does not affect the cost) | power_kW | eqptype, power_kW |  |  |
| Seider | 2000 | Heater | Molten salt heater | — (material does not affect the cost) | power_kW | eqptype, power_kW |  |  |
| Seider | 2000 | Heater | Steam boiler | — (material does not affect the cost) | power_kW | eqptype, power_kW |  |  |
| Seider | 2000 | Liquid-liquid extractor | — | Aluminum(alloy), Carbon steel, Copper(alloy), Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | height_m, diameter_m | material, height_m, diameter_m |  |  |
| Seider | 2000 | Membrane | Gas permeation | — (material does not affect the cost) | area_sqm | eqptype, area_sqm |  |  |
| Seider | 2000 | Membrane | Pervaporation | — (material does not affect the cost) | area_sqm | eqptype, area_sqm |  |  |
| Seider | 2000 | Membrane | Ultrafiltration | — (material does not affect the cost) | area_sqm | eqptype, area_sqm |  |  |
| Seider | 2000 | Membrane (for reverse osmosis) | For brackish water | — (material does not affect the cost) | volflow_cumph | eqptype, volflow_cumph |  |  |
| Seider | 2000 | Membrane (for reverse osmosis) | For seawater | — (material does not affect the cost) | volflow_cumph | eqptype, volflow_cumph |  |  |
| Seider | 2000 | Mixer | Kneader (tilting double arm) | Aluminum(alloy), Carbon steel, Copper(alloy), Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | vol_cum | eqptype, material, vol_cum |  |  |
| Seider | 2000 | Mixer | Kneader(sigma double arm) | Aluminum(alloy), Carbon steel, Copper(alloy), Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | vol_cum | eqptype, material, vol_cum |  |  |
| Seider | 2000 | Mixer | Muller | Aluminum(alloy), Carbon steel, Copper(alloy), Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | vol_cum | eqptype, material, vol_cum |  |  |
| Seider | 2000 | Mixer | Ribbon | Aluminum(alloy), Carbon steel, Copper(alloy), Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | vol_cum | eqptype, material, vol_cum |  |  |
| Seider | 2000 | Mixer | Tumblers, double cone | Aluminum(alloy), Carbon steel, Copper(alloy), Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | vol_cum | eqptype, material, vol_cum |  |  |
| Seider | 2000 | Mixer | Tumblers, twin shell | Aluminum(alloy), Carbon steel, Copper(alloy), Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | vol_cum | eqptype, material, vol_cum |  |  |
| Seider | 2000 | Packing | Berl saddles | Ceramic | vol_cum, packsize_in | eqptype, material, vol_cum, packsize_in |  |  |
| Seider | 2000 | Packing | Cascade mini-rings | Ceramic, Polyethylene(plastic), Stainless steel | vol_cum, packsize_in | eqptype, material, vol_cum, packsize_in |  |  |
| Seider | 2000 | Packing | Intalox saddles | Ceramic, Polyethylene(plastic) | vol_cum, packsize_in | eqptype, material, vol_cum, packsize_in |  |  |
| Seider | 2000 | Packing | Pall rings | Carbon steel, Polyethylene(plastic), Stainless steel | vol_cum, packsize_in | eqptype, material, vol_cum, packsize_in |  |  |
| Seider | 2000 | Packing | Raschig rings | Carbon steel, Ceramic, Stainless steel | vol_cum, packsize_in | eqptype, material, vol_cum, packsize_in |  |  |
| Seider | 2000 | Packing | Tellerettes | Polyethylene(plastic) | vol_cum | eqptype, material, vol_cum, packsize_in |  |  |
| Seider | 2000 | Pumps | Centrifugal | Carbon steel, Cast iron, Copper(alloy), Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | volflow_cumph, power_kW, pumphead_m | eqptype, material, volflow_cumph, pumphead_m, power_kW, driver | Electric-open/drip proof, Electric-explosion proof, Electric-totally enclosed | pumphead_m = pump head; if omitted it is estimated from power_kW (brake power). |
| Seider | 2000 | Size enlargement equipment | Disk agglomerator | Aluminum(alloy), Carbon steel, Copper(alloy), Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | massflow_kgph | eqptype, material, massflow_kgph |  |  |
| Seider | 2000 | Size enlargement equipment | Drum agglomerator | Aluminum(alloy), Carbon steel, Copper(alloy), Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | massflow_kgph | eqptype, material, massflow_kgph |  |  |
| Seider | 2000 | Size enlargement equipment | Pellet mill | Aluminum(alloy), Carbon steel, Copper(alloy), Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | massflow_kgph | eqptype, material, massflow_kgph |  |  |
| Seider | 2000 | Size enlargement equipment | Pug mill extruder | Aluminum(alloy), Carbon steel, Copper(alloy), Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | massflow_kgph | eqptype, material, massflow_kgph |  |  |
| Seider | 2000 | Size enlargement equipment | Roll-type presses | Aluminum(alloy), Carbon steel, Copper(alloy), Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | massflow_kgph | eqptype, material, massflow_kgph |  |  |
| Seider | 2000 | Size enlargement equipment | Screw extruder | Aluminum(alloy), Carbon steel, Copper(alloy), Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | massflow_kgph | eqptype, material, massflow_kgph |  |  |
| Seider | 2000 | Size enlargement equipment | Tableting presses | Aluminum(alloy), Carbon steel, Copper(alloy), Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | massflow_kgph | eqptype, material, massflow_kgph |  |  |
| Seider | 2000 | Size reduction equipment | Ball mill | — (material does not affect the cost) | massflow_kgph | eqptype, massflow_kgph |  |  |
| Seider | 2000 | Size reduction equipment | Cone crusher | — (material does not affect the cost) | massflow_kgph | eqptype, massflow_kgph |  |  |
| Seider | 2000 | Size reduction equipment | Gyratory crusher | — (material does not affect the cost) | massflow_kgph | eqptype, massflow_kgph |  |  |
| Seider | 2000 | Size reduction equipment | Hammer mill | — (material does not affect the cost) | massflow_kgph | eqptype, massflow_kgph |  |  |
| Seider | 2000 | Size reduction equipment | Jaw crusher | — (material does not affect the cost) | massflow_kgph | eqptype, massflow_kgph |  |  |
| Seider | 2000 | Size reduction equipment | Jet mill | — (material does not affect the cost) | massflow_kgph | eqptype, massflow_kgph |  |  |
| Seider | 2000 | Solid-liquid separator | Clarifier, concrete | — (material does not affect the cost) | area_sqm | eqptype, area_sqm |  |  |
| Seider | 2000 | Solid-liquid separator | Clarifier, steel | — (material does not affect the cost) | area_sqm | eqptype, area_sqm |  |  |
| Seider | 2000 | Solid-liquid separator | Thickener, concrete | — (material does not affect the cost) | area_sqm | eqptype, area_sqm |  |  |
| Seider | 2000 | Solid-liquid separator | Thickener, steel | — (material does not affect the cost) | area_sqm | eqptype, area_sqm |  |  |
| Seider | 2000 | Storage tank | Cone roof | Aluminum(alloy), Carbon steel, Copper(alloy), Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | vol_cum | eqptype, material, vol_cum, P_bar |  |  |
| Seider | 2000 | Storage tank | Floating roof | Aluminum(alloy), Carbon steel, Copper(alloy), Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | vol_cum | eqptype, material, vol_cum, P_bar |  |  |
| Seider | 2000 | Storage tank | Gas holder | Aluminum(alloy), Carbon steel, Copper(alloy), Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | vol_cum | eqptype, material, vol_cum, P_bar |  |  |
| Seider | 2000 | Storage tank | Open | Aluminum(alloy), Carbon steel, Copper(alloy), Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | vol_cum | eqptype, material, vol_cum, P_bar |  |  |
| Seider | 2000 | Storage tank | Spherical | Aluminum(alloy), Carbon steel, Copper(alloy), Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | vol_cum | eqptype, material, vol_cum, P_bar |  |  |
| Seider | 2000 | Trays | Bubble cap | Carbon steel, Monel, Stainless steel | diameter_m, num | eqptype, material, diameter_m, num |  | num = number of trays. |
| Seider | 2000 | Trays | Sieve | Carbon steel, Monel, Stainless steel | diameter_m, num | eqptype, material, diameter_m, num |  | num = number of trays. |
| Seider | 2000 | Trays | Valve | Carbon steel, Monel, Stainless steel | diameter_m, num | eqptype, material, diameter_m, num |  | num = number of trays. |
| Seider | 2000 | Turbines | Axial gas turbines | Aluminum(alloy), Carbon steel, Copper(alloy), Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | power_kW | eqptype, material, power_kW |  |  |
| Seider | 2000 | Turbines | Liquid expanders | Aluminum(alloy), Carbon steel, Copper(alloy), Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | power_kW | eqptype, material, power_kW |  |  |
| Seider | 2000 | Vacuum system | Liquid-ring pumps | — (material does not affect the cost) | volflow_cumph | eqptype, volflow_cumph |  |  |
| Seider | 2000 | Vacuum system | Screw compressor | — (material does not affect the cost) | volflow_cumph | eqptype, volflow_cumph |  |  |
| Seider | 2000 | Vacuum system | Three-stage claw | — (material does not affect the cost) | volflow_cumph | eqptype, volflow_cumph |  |  |
| Seider | 2000 | Vacuum system | Three-stage lobe | — (material does not affect the cost) | volflow_cumph | eqptype, volflow_cumph |  |  |
| Seider | 2000 | Vessel/Tower | Horizontal vessel | Carbon steel, Stainless steel, Titanium(alloy) | height_m, diameter_m, thickness_m | eqptype, material, diameter_m, height_m, thickness_m |  | vol_cum and thickness_m are optional; if not given they are estimated from D, H, P and T. |
| Seider | 2000 | Vessel/Tower | Vertical vessel | Carbon steel, Stainless steel, Titanium(alloy) | height_m, diameter_m, thickness_m | eqptype, material, diameter_m, height_m, thickness_m |  | vol_cum and thickness_m are optional; if not given they are estimated from D, H, P and T. |
| Smith | 2000 | Compressor | Centrifugal | Aluminum(alloy), Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | power_kW | eqptype, T_K, P_bar, material, power_kW |  | power_kW = compressor (shaft/fluid) power. |
| Smith | 2000 | Compressor | Reciprocating | Aluminum(alloy), Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | power_kW | eqptype, T_K, P_bar, material, power_kW |  | power_kW = compressor (shaft/fluid) power. |
| Smith | 2000 | Dryer | Drum | Aluminum(alloy), Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | massflow_kgph | eqptype, T_K, P_bar, material, massflow_kgph |  |  |
| Smith | 2000 | Fans | Axial tube | Aluminum(alloy), Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | power_kW | eqptype, T_K, P_bar, material, power_kW |  |  |
| Smith | 2000 | Fans | Axial vane | Aluminum(alloy), Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | power_kW | eqptype, T_K, P_bar, material, power_kW |  |  |
| Smith | 2000 | Fans | Centrifugal backward-curved | Aluminum(alloy), Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | power_kW | eqptype, T_K, P_bar, material, power_kW |  |  |
| Smith | 2000 | Fans | Centrifugal straight-radial | Aluminum(alloy), Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | power_kW | eqptype, T_K, P_bar, material, power_kW |  |  |
| Smith | 2000 | Filters | Vacuum filter | — (material does not affect the cost) | area_sqm | eqptype, T_K, P_bar, area_sqm |  |  |
| Smith | 2000 | Heat exchanger (others) | Air cooler | Aluminum(alloy), Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | area_sqm | eqptype, T_K, P_bar, material, area_sqm |  |  |
| Smith | 2000 | Heat exchanger (shell and tube) | Bayonet | CS shell/Al(alloy) tube, CS shell/CS tube, CS shell/Monel tube, CS shell/SS tube, SS shell/SS tube | area_sqm | eqptype, T_K, P_bar, material, area_sqm |  |  |
| Smith | 2000 | Heat exchanger (shell and tube) | Double Pipe | CS shell/Al(alloy) tube, CS shell/CS tube, CS shell/Monel tube, CS shell/SS tube, SS shell/SS tube | area_sqm | eqptype, T_K, P_bar, material, area_sqm |  |  |
| Smith | 2000 | Heat exchanger (shell and tube) | Fixed tube | CS shell/Al(alloy) tube, CS shell/CS tube, CS shell/Monel tube, CS shell/SS tube, SS shell/SS tube | area_sqm | eqptype, T_K, P_bar, material, area_sqm |  |  |
| Smith | 2000 | Heat exchanger (shell and tube) | Floating head | CS shell/Al(alloy) tube, CS shell/CS tube, CS shell/Monel tube, CS shell/SS tube, SS shell/SS tube | area_sqm | eqptype, T_K, P_bar, material, area_sqm |  |  |
| Smith | 2000 | Heat exchanger (shell and tube) | Kettle reboiler | CS shell/Al(alloy) tube, CS shell/CS tube, CS shell/Monel tube, CS shell/SS tube, SS shell/SS tube | area_sqm | eqptype, T_K, P_bar, material, area_sqm |  |  |
| Smith | 2000 | Heat exchanger (shell and tube) | Multiple Pipe | CS shell/Al(alloy) tube, CS shell/CS tube, CS shell/Monel tube, CS shell/SS tube, SS shell/SS tube | area_sqm | eqptype, T_K, P_bar, material, area_sqm |  |  |
| Smith | 2000 | Heat exchanger (shell and tube) | Scraped Wall | CS shell/Al(alloy) tube, CS shell/CS tube, CS shell/Monel tube, CS shell/SS tube, SS shell/SS tube | area_sqm | eqptype, T_K, P_bar, material, area_sqm |  |  |
| Smith | 2000 | Heat exchanger (shell and tube) | Spiral tube (shell and tube) | CS shell/Al(alloy) tube, CS shell/CS tube, CS shell/Monel tube, CS shell/SS tube, SS shell/SS tube | area_sqm | eqptype, T_K, P_bar, material, area_sqm |  |  |
| Smith | 2000 | Heat exchanger (shell and tube) | U-tube (shell and tube) | CS shell/Al(alloy) tube, CS shell/CS tube, CS shell/Monel tube, CS shell/SS tube, SS shell/SS tube | area_sqm | eqptype, T_K, P_bar, material, area_sqm |  |  |
| Smith | 2000 | Heater | Steam boiler | — (material does not affect the cost) | massflow_kgph | eqptype, T_K, P_bar, massflow_kgph |  |  |
| Smith | 2000 | Packing (Structured) | Structured | Aluminum(alloy), Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | height_m, diameter_m | eqptype, T_K, P_bar, material, diameter_m, height_m |  |  |
| Smith | 2000 | Pumps | Centrifugal | Aluminum(alloy), Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | power_kW | eqptype, T_K, P_bar, material, power_kW |  |  |
| Smith | 2000 | Reactor | Jacketed agitated | Aluminum(alloy), Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | vol_cum | eqptype, T_K, P_bar, material, vol_cum |  |  |
| Smith | 2000 | Storage tank | Cone roof | Aluminum(alloy), Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | vol_cum | eqptype, T_K, P_bar, vol_cum |  |  |
| Smith | 2000 | Storage tank | Floating roof | Aluminum(alloy), Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | vol_cum | eqptype, T_K, P_bar, vol_cum |  |  |
| Smith | 2000 | Storage tank | Gas holder | Aluminum(alloy), Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | vol_cum | eqptype, T_K, P_bar, vol_cum |  |  |
| Smith | 2000 | Storage tank | Open | Aluminum(alloy), Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | vol_cum | eqptype, T_K, P_bar, vol_cum |  |  |
| Smith | 2000 | Storage tank | Spherical | Aluminum(alloy), Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | vol_cum | eqptype, T_K, P_bar, vol_cum |  |  |
| Smith | 2000 | Trays | Sieve | Aluminum(alloy), Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | diameter_m, num | eqptype, T_K, P_bar, material, diameter_m, num |  | num = number of trays. |
| Smith | 2000 | Trays | Valve | Aluminum(alloy), Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | diameter_m, num | eqptype, T_K, P_bar, material, diameter_m, num |  | num = number of trays. |
| Smith | 2000 | Vessel/Tower | Horizontal vessel | Carbon steel, Inconel, Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | height_m, diameter_m, thickness_m | eqptype, T_K, P_bar, material, diameter_m, thickness_m, height_m |  | vol_cum and thickness_m are optional; if not given they are estimated from D, H, P and T. |
| Smith | 2000 | Vessel/Tower | Pressured vessel | Carbon steel, Inconel, Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | height_m, diameter_m, thickness_m | eqptype, T_K, P_bar, material, diameter_m, thickness_m, height_m |  | vol_cum and thickness_m are optional; if not given they are estimated from D, H, P and T. |
| Smith | 2000 | Vessel/Tower | Vertical vessel | Carbon steel, Inconel, Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | height_m, diameter_m, thickness_m | eqptype, T_K, P_bar, material, diameter_m, thickness_m, height_m |  | vol_cum and thickness_m are optional; if not given they are estimated from D, H, P and T. |
| Towler | 2006 | Agitator | Propeller, closed vessel | Aluminum(alloy), Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | power_kW | eqptype, material, power_kW |  |  |
| Towler | 2006 | Agitator | Propeller, open tank | Aluminum(alloy), Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | power_kW | eqptype, material, power_kW |  |  |
| Towler | 2006 | Compressor | Centrifugal | Aluminum(alloy), Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | power_kW | eqptype, material, power_kW |  | power_kW = compressor (shaft/fluid) power. |
| Towler | 2006 | Compressor | Reciprocating | Aluminum(alloy), Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | power_kW | eqptype, material, power_kW |  | power_kW = compressor (shaft/fluid) power. |
| Towler | 2006 | Conveyor | Belt | — (material does not affect the cost) | length_m, diameter_m | eqptype, length_m |  | length_m = belt length; diameter_m = belt width 0.5–1.0 m (1.0 m if not given). |
| Towler | 2006 | Crystallizer-cooling | Jacketed scraped wall | Aluminum(alloy), Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | height_m | eqptype, material, height_m |  |  |
| Towler | 2006 | Dryer | Pan | Aluminum(alloy), Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | area_sqm | eqptype, material, area_sqm, massflow_kgph |  |  |
| Towler | 2006 | Dryer | Rotary(gas fired) | Aluminum(alloy), Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | area_sqm | eqptype, material, area_sqm, massflow_kgph |  |  |
| Towler | 2006 | Dryer | Spray | Aluminum(alloy), Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | massflow_kgph | eqptype, material, area_sqm, massflow_kgph |  |  |
| Towler | 2006 | Evaporator | Falling film | Aluminum(alloy), Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | area_sqm | eqptype, material, area_sqm |  |  |
| Towler | 2006 | Evaporator | Long tube | Aluminum(alloy), Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | area_sqm | eqptype, material, area_sqm |  |  |
| Towler | 2006 | Filters | Plate and frame | — (material does not affect the cost) | vol_cum | eqptype, vol_cum, area_sqm |  |  |
| Towler | 2006 | Filters | Vacuum filter | — (material does not affect the cost) | area_sqm | eqptype, vol_cum, area_sqm |  |  |
| Towler | 2006 | Furnace | Nonreactive furnace | Aluminum(alloy), Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | power_kW | eqptype, material, power_kW |  |  |
| Towler | 2006 | Furnace | Pyrolysis furnace | Aluminum(alloy), Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | power_kW | eqptype, material, power_kW |  |  |
| Towler | 2006 | Furnace | Reformer furnace | Aluminum(alloy), Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | power_kW | eqptype, material, power_kW |  |  |
| Towler | 2006 | Heat exchanger (others) | Flat plate | Aluminum(alloy), Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | area_sqm | eqptype, material, area_sqm |  |  |
| Towler | 2006 | Heat exchanger (shell and tube) | Double Pipe | CS shell/Al(alloy) tube, CS shell/CS tube, CS shell/Monel tube, CS shell/Ni(alloy) tube, CS shell/SS tube, SS shell/SS tube | area_sqm | eqptype, material, area_sqm |  |  |
| Towler | 2006 | Heat exchanger (shell and tube) | Floating head | CS shell/Al(alloy) tube, CS shell/CS tube, CS shell/Monel tube, CS shell/Ni(alloy) tube, CS shell/SS tube, SS shell/SS tube | area_sqm | eqptype, material, area_sqm |  |  |
| Towler | 2006 | Heat exchanger (shell and tube) | Kettle reboiler | CS shell/Al(alloy) tube, CS shell/CS tube, CS shell/Monel tube, CS shell/Ni(alloy) tube, CS shell/SS tube, SS shell/SS tube | area_sqm | eqptype, material, area_sqm |  |  |
| Towler | 2006 | Heat exchanger (shell and tube) | U-tube (shell and tube) | CS shell/Al(alloy) tube, CS shell/CS tube, CS shell/Monel tube, CS shell/Ni(alloy) tube, CS shell/SS tube, SS shell/SS tube | area_sqm | eqptype, material, area_sqm |  |  |
| Towler | 2006 | Heater | Steam boiler | Aluminum(alloy), Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | massflow_kgph | eqptype, material, massflow_kgph |  |  |
| Towler | 2006 | Mixer | Ribbon | Aluminum(alloy), Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | power_kW | eqptype, material, power_kW |  |  |
| Towler | 2006 | Packing | Intalox saddles | Ceramic | vol_cum | eqptype, material, vol_cum |  |  |
| Towler | 2006 | Packing | Pall rings | Stainless steel | vol_cum | eqptype, material, vol_cum |  |  |
| Towler | 2006 | Packing | Raschig rings | Stainless steel | vol_cum | eqptype, material, vol_cum |  |  |
| Towler | 2006 | Packing (Structured) | Structured | Stainless steel, PVC | height_m, diameter_m | eqptype, material, diameter_m, height_m |  | Packed volume computed from diameter_m and height_m. |
| Towler | 2006 | Pumps | Centrifugal | Aluminum(alloy), Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | volflow_cumph | eqptype, material, volflow_cumph |  |  |
| Towler | 2006 | Reactor | Jacketed agitated | Aluminum(alloy), Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | vol_cum | eqptype, material, vol_cum |  |  |
| Towler | 2006 | Size reduction equipment | Hammer mill | — (material does not affect the cost) | massflow_kgph | eqptype, massflow_kgph |  |  |
| Towler | 2006 | Size reduction equipment | Pulverizer | — (material does not affect the cost) | massflow_kgph | eqptype, massflow_kgph |  |  |
| Towler | 2006 | Storage tank | Cone roof | Aluminum(alloy), Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | vol_cum | eqptype, material, vol_cum |  |  |
| Towler | 2006 | Storage tank | Floating roof | Aluminum(alloy), Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | vol_cum | eqptype, material, vol_cum |  |  |
| Towler | 2006 | Trays | Bubble cap | Aluminum(alloy), Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | diameter_m, num | eqptype, material, diameter_m, num |  | num = number of trays. |
| Towler | 2006 | Trays | Sieve | Aluminum(alloy), Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | diameter_m, num | eqptype, material, diameter_m, num |  | num = number of trays. |
| Towler | 2006 | Trays | Valve | Aluminum(alloy), Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | diameter_m, num | eqptype, material, diameter_m, num |  | num = number of trays. |
| Towler | 2006 | Vessel/Tower | Horizontal vessel | Carbon steel, Stainless steel | height_m, diameter_m, thickness_m | eqptype, material, diameter_m, thickness_m, height_m |  | vol_cum and thickness_m are optional; if not given they are estimated from D, H, P and T. |
| Towler | 2006 | Vessel/Tower | Vertical vessel | Carbon steel, Stainless steel | height_m, diameter_m, thickness_m | eqptype, material, diameter_m, thickness_m, height_m |  | vol_cum and thickness_m are optional; if not given they are estimated from D, H, P and T. |
| Towler | 2006 | Water ion exchanger | — | — (material does not affect the cost) | volflow_cumph | volflow_cumph |  |  |
| Peters | 2002 | Agitator | Propeller, closed vessel | Carbon steel, Monel, Rubber-covered steel, Stainless steel, Stainless steel(316) | power_kW | eqptype, material, power_kW |  |  |
| Peters | 2002 | Agitator | Propeller, open tank | Carbon steel, Monel, Rubber-covered steel, Stainless steel, Stainless steel(316) | power_kW | eqptype, material, power_kW |  |  |
| Peters | 2002 | Agitator | Turbine, dual impeller | Carbon steel, Stainless steel(316) | power_kW | eqptype, material, power_kW |  |  |
| Peters | 2002 | Agitator | Turbine, single impeller | Carbon steel, Stainless steel(316) | power_kW | eqptype, material, power_kW |  |  |
| Peters | 2002 | Autoclave | — | Carbon steel, Glass-lined steel, Stainless steel | vol_cum | material, vol_cum |  |  |
| Peters | 2002 | Blender | Ribbon | Carbon steel, Stainless steel | vol_cum | eqptype, material, vol_cum |  |  |
| Peters | 2002 | Blender | Rotary | Carbon steel, Stainless steel | vol_cum | eqptype, material, vol_cum |  |  |
| Peters | 2002 | Blower | Centrifugal | — (material does not affect the cost) | volflow_cumph | eqptype, volflow_cumph, P_bar, Pout_bar |  | Turbo blower: the pressure rise Pout_bar − P_bar selects the curve. |
| Peters | 2002 | Blower | Centrifugal(turbo) | — (material does not affect the cost) | volflow_cumph | eqptype, volflow_cumph, P_bar, Pout_bar |  | Turbo blower: the pressure rise Pout_bar − P_bar selects the curve. |
| Peters | 2002 | Blower | Heavy-duty | — (material does not affect the cost) | volflow_cumph | eqptype, volflow_cumph, P_bar, Pout_bar |  | Turbo blower: the pressure rise Pout_bar − P_bar selects the curve. |
| Peters | 2002 | Blower | Rotary straight-lobo | — (material does not affect the cost) | volflow_cumph | eqptype, volflow_cumph, P_bar, Pout_bar |  | Turbo blower: the pressure rise Pout_bar − P_bar selects the curve. |
| Peters | 2002 | Centrifuge | Auto batch separator (horizontal) | Carbon steel, Stainless steel | diameter_m | eqptype, material, diameter_m |  |  |
| Peters | 2002 | Centrifuge | Auto batch separator (vertical) | Carbon steel | diameter_m | eqptype, material, diameter_m |  |  |
| Peters | 2002 | Centrifuge | Oscillating screen | Carbon steel, Stainless steel | diameter_m | eqptype, material, diameter_m |  |  |
| Peters | 2002 | Centrifuge | Pusher | Carbon steel, Stainless steel | diameter_m | eqptype, material, diameter_m |  |  |
| Peters | 2002 | Centrifuge | Scroll-conveyor | Carbon steel, Stainless steel | diameter_m | eqptype, material, diameter_m |  |  |
| Peters | 2002 | Centrifuge | Solid bowl w/o motor | Carbon steel, Stainless steel(316) | diameter_m | eqptype, material, diameter_m |  |  |
| Peters | 2002 | Compressor | Centrifugal | Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | power_kW | eqptype, material, power_kW, driver | Electric-open/drip proof, Electric-explosion proof, Electric-totally enclosed, Steam turbine, Gas turbine, Intern comb.engine | power_kW = compressor (shaft/fluid) power. |
| Peters | 2002 | Compressor | Reciprocating | Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | power_kW | eqptype, material, power_kW, driver | Electric-open/drip proof, Electric-explosion proof, Electric-totally enclosed, Steam turbine | power_kW = compressor (shaft/fluid) power. |
| Peters | 2002 | Conveyor | Apron | — (material does not affect the cost) | length_m, diameter_m | eqptype, length_m, diameter_m |  | length_m = conveying length; diameter_m = belt/apron/pan width or screw diameter; for Pneumatic, massflow_kgph = solids rate. |
| Peters | 2002 | Conveyor | Belt | — (material does not affect the cost) | length_m, diameter_m | eqptype, length_m, diameter_m |  | length_m = conveying length; diameter_m = belt/apron/pan width or screw diameter; for Pneumatic, massflow_kgph = solids rate. |
| Peters | 2002 | Conveyor | Bucket elevator | — (material does not affect the cost) | length_m, diameter_m | eqptype, length_m, diameter_m |  | length_m = conveying length; diameter_m = belt/apron/pan width or screw diameter; for Pneumatic, massflow_kgph = solids rate. |
| Peters | 2002 | Conveyor | Pneumatic | — (material does not affect the cost) | length_m, massflow_kgph | eqptype, length_m, massflow_kgph |  | length_m = conveying length; diameter_m = belt/apron/pan width or screw diameter; for Pneumatic, massflow_kgph = solids rate. |
| Peters | 2002 | Conveyor | Screw | — (material does not affect the cost) | length_m, diameter_m | eqptype, length_m, diameter_m |  | length_m = conveying length; diameter_m = belt/apron/pan width or screw diameter; for Pneumatic, massflow_kgph = solids rate. |
| Peters | 2002 | Conveyor | Vibrating | — (material does not affect the cost) | length_m, diameter_m | eqptype, length_m, diameter_m |  | length_m = conveying length; diameter_m = belt/apron/pan width or screw diameter; for Pneumatic, massflow_kgph = solids rate. |
| Peters | 2002 | Dewatering press | Screw press | — (material does not affect the cost) | massflow_kgph | eqptype, massflow_kgph |  |  |
| Peters | 2002 | Dryer | Pan | Carbon steel, Stainless steel, Stainless steel(316) | area_sqm | eqptype, material, area_sqm |  |  |
| Peters | 2002 | Dryer | Rotary vacuum | Carbon steel, Stainless steel, Stainless steel(316) | area_sqm | eqptype, material, area_sqm |  |  |
| Peters | 2002 | Dryer | Roto-Louvre | Carbon steel | area_sqm | eqptype, material, area_sqm |  |  |
| Peters | 2002 | Dryer | Vacuum shelf | Carbon steel | area_sqm | eqptype, material, area_sqm |  |  |
| Peters | 2002 | Dryer | Vibratory conveyor | Carbon steel, Stainless steel, Stainless steel(316) | area_sqm | eqptype, material, area_sqm |  |  |
| Peters | 2002 | Dust collector | Baghouse | Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | volflow_cumph | eqptype, volflow_cumph |  |  |
| Peters | 2002 | Dust collector | Baghouse (high temperature) | Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | volflow_cumph | eqptype, volflow_cumph |  |  |
| Peters | 2002 | Dust collector | Baghouse (intermittent cleaning) | Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | volflow_cumph | eqptype, volflow_cumph |  |  |
| Peters | 2002 | Dust collector | Cyclone | Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | volflow_cumph | eqptype, volflow_cumph |  |  |
| Peters | 2002 | Dust collector | Cyclone scrubbers | — (material does not affect the cost) | volflow_cumph | eqptype, volflow_cumph |  |  |
| Peters | 2002 | Dust collector | Electrostatic precipitator | Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | volflow_cumph | eqptype, volflow_cumph |  |  |
| Peters | 2002 | Dust collector | Gravity spray scrubber | — (material does not affect the cost) | volflow_cumph | eqptype, volflow_cumph |  |  |
| Peters | 2002 | Dust collector | Multiple cyclones | Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | volflow_cumph | eqptype, volflow_cumph |  |  |
| Peters | 2002 | Dust collector | Venturi scrubber | — (material does not affect the cost) | volflow_cumph | eqptype, volflow_cumph |  |  |
| Peters | 2002 | Dust collector | Venturi scrubber (low energy) | — (material does not affect the cost) | volflow_cumph | eqptype, volflow_cumph |  |  |
| Peters | 2002 | Evaporator | Agitated film(scraped wall) | Carbon steel, Copper(alloy), Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | area_sqm | eqptype, material, area_sqm, P_bar |  |  |
| Peters | 2002 | Evaporator | Falling film | Carbon steel, Copper(alloy), Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | area_sqm | eqptype, material, area_sqm, P_bar |  |  |
| Peters | 2002 | Evaporator | Forced circulation(pumped) | Carbon steel, Copper(alloy), Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | area_sqm | eqptype, material, area_sqm, P_bar |  |  |
| Peters | 2002 | Evaporator | Horizontal tube | Carbon steel, Copper(alloy), Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | area_sqm | eqptype, material, area_sqm, P_bar |  |  |
| Peters | 2002 | Evaporator | Vertical tube | Carbon steel, Copper(alloy), Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | area_sqm | eqptype, material, area_sqm, P_bar |  |  |
| Peters | 2002 | Fans | Axial tube | — (material does not affect the cost) | volflow_cumph | eqptype, volflow_cumph |  |  |
| Peters | 2002 | Fans | Axial vane | — (material does not affect the cost) | volflow_cumph | eqptype, volflow_cumph |  |  |
| Peters | 2002 | Fans | Centrifugal backward-curved | — (material does not affect the cost) | volflow_cumph | eqptype, volflow_cumph |  |  |
| Peters | 2002 | Fans | Centrifugal straight-radial | — (material does not affect the cost) | volflow_cumph | eqptype, volflow_cumph |  |  |
| Peters | 2002 | Filters | Cartridge | Carbon steel, Stainless steel, Stainless steel(316) | area_sqm | eqptype, material, area_sqm |  |  |
| Peters | 2002 | Filters | Disc and drum | Stainless steel, Stainless steel(316) | area_sqm | eqptype, material, area_sqm |  |  |
| Peters | 2002 | Filters | Leaf | Carbon steel, Stainless steel, Stainless steel(316) | area_sqm | eqptype, material, area_sqm |  |  |
| Peters | 2002 | Filters | Pan | Carbon steel, Stainless steel, Stainless steel(316) | area_sqm | eqptype, material, area_sqm |  |  |
| Peters | 2002 | Filters | Plate and frame | Aluminum(alloy), Carbon steel, Cast iron, PVC-coated steel, Rubber-covered steel, Stainless steel, Stainless steel(316), Wood | area_sqm | eqptype, material, area_sqm |  |  |
| Peters | 2002 | Filters | Table | Carbon steel, Stainless steel, Stainless steel(316) | area_sqm | eqptype, material, area_sqm |  |  |
| Peters | 2002 | Filters | Vacuum filter | Stainless steel, Stainless steel(316) | area_sqm | eqptype, material, area_sqm |  |  |
| Peters | 2002 | Furnace | Nonreactive furnace | — (material does not affect the cost) | power_kW | eqptype, power_kW |  |  |
| Peters | 2002 | Furnace | Pyrolysis furnace | — (material does not affect the cost) | power_kW | eqptype, power_kW |  |  |
| Peters | 2002 | Furnace | Reformer furnace | — (material does not affect the cost) | power_kW | eqptype, power_kW |  |  |
| Peters | 2002 | Heat exchanger (others) | Air cooler | Aluminum(alloy), Carbon steel, Stainless steel | area_sqm | eqptype, material, area_sqm |  |  |
| Peters | 2002 | Heat exchanger (others) | Flat plate | Aluminum(alloy), Carbon steel, Copper(alloy), Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | area_sqm | eqptype, material, area_sqm |  |  |
| Peters | 2002 | Heat exchanger (others) | Gasket plate | Aluminum(alloy), Carbon steel, Copper(alloy), Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | area_sqm | eqptype, material, area_sqm |  |  |
| Peters | 2002 | Heat exchanger (others) | Spiral plate | Aluminum(alloy), Carbon steel, Copper(alloy), Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | area_sqm | eqptype, material, area_sqm |  |  |
| Peters | 2002 | Heat exchanger (others) | Welded plate | — (material does not affect the cost) | area_sqm | eqptype, material, area_sqm |  |  |
| Peters | 2002 | Heat exchanger (shell and tube) | Double pipe | CS shell/CS tube, CS shell/Cu tube, CS shell/SS tube | area_sqm | eqptype, material, area_sqm |  |  |
| Peters | 2002 | Heat exchanger (shell and tube) | Fixed tube | CS shell/CS tube, CS shell/Cu tube, CS shell/Ni(alloy) tube, CS shell/SS tube, CS shell/Ti(alloy) tube, SS shell/SS tube | area_sqm | eqptype, material, area_sqm |  |  |
| Peters | 2002 | Heat exchanger (shell and tube) | Floating head | CS shell/CS tube, CS shell/Cu tube, CS shell/Ni(alloy) tube, CS shell/SS tube, CS shell/Ti(alloy) tube, SS shell/SS tube | area_sqm | eqptype, material, area_sqm |  |  |
| Peters | 2002 | Heat exchanger (shell and tube) | Multiple pipe | CS shell/CS tube, CS shell/Cu tube, CS shell/SS tube | area_sqm | eqptype, material, area_sqm |  |  |
| Peters | 2002 | Heat exchanger (shell and tube) | Scraped wall | CS shell/CS tube, CS shell/Cu tube, CS shell/Ni(alloy) tube, CS shell/SS tube, CS shell/Ti(alloy) tube, SS shell/SS tube | area_sqm | eqptype, material, area_sqm |  |  |
| Peters | 2002 | Heat exchanger (shell and tube) | Spiral tube (shell and tube) | CS shell/CS tube, CS shell/Cu tube, CS shell/Ni(alloy) tube, CS shell/SS tube, CS shell/Ti(alloy) tube, SS shell/SS tube | area_sqm | eqptype, material, area_sqm |  |  |
| Peters | 2002 | Heat exchanger (shell and tube) | U-tube (shell and tube) | CS shell/CS tube, CS shell/Cu tube, CS shell/Ni(alloy) tube, CS shell/SS tube, CS shell/Ti(alloy) tube, SS shell/SS tube | area_sqm | eqptype, material, area_sqm |  |  |
| Peters | 2002 | Heater | Cylindrical | Carbon steel, Cr-Mo steel, Stainless steel | power_kW | eqptype, material, power_kW, P_bar |  | Carbon steel: the 690 kPa curve is used up to 6.9 bar. |
| Peters | 2002 | Mixer | Kneader(sigma double arm) | Carbon steel | power_kW | eqptype, material |  | Size input depends on the type (volume, power or pipe diameter). |
| Peters | 2002 | Mixer | Motionless | Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | diameter_m | eqptype, material |  | Size input depends on the type (volume, power or pipe diameter). |
| Peters | 2002 | Mixer | Muller | Carbon steel | power_kW | eqptype, material |  | Size input depends on the type (volume, power or pipe diameter). |
| Peters | 2002 | Mixer | Propeller (fixed, direct drive) | Stainless steel | power_kW | eqptype, material |  | Size input depends on the type (volume, power or pipe diameter). |
| Peters | 2002 | Mixer | Propeller (fixed, gear drive) | Stainless steel | power_kW | eqptype, material |  | Size input depends on the type (volume, power or pipe diameter). |
| Peters | 2002 | Mixer | Propeller (portable, direct drive) | Stainless steel | power_kW | eqptype, material |  | Size input depends on the type (volume, power or pipe diameter). |
| Peters | 2002 | Mixer | Propeller (portable, gear drive) | Stainless steel | power_kW | eqptype, material |  | Size input depends on the type (volume, power or pipe diameter). |
| Peters | 2002 | Mixer | Ribbon | Carbon steel, Stainless steel | vol_cum | eqptype, material |  | Size input depends on the type (volume, power or pipe diameter). |
| Peters | 2002 | Mixer | Tumblers, double cone | Carbon steel, Stainless steel | vol_cum | eqptype, material |  | Size input depends on the type (volume, power or pipe diameter). |
| Peters | 2002 | Mixer | Tumblers, twin shell | Carbon steel, Stainless steel | vol_cum | eqptype, material |  | Size input depends on the type (volume, power or pipe diameter). |
| Peters | 2002 | Mixer | Two-roll | Carbon steel | power_kW | eqptype, material |  | Size input depends on the type (volume, power or pipe diameter). |
| Peters | 2002 | Packing | Berl saddles | Carbon steel, Ceramic, Polyethylene(plastic), Stainless steel, Stainless steel(316) | height_m, diameter_m | eqptype, material, diameter_m, height_m |  | height_m = packed height; diameter_m 0.3–4.0 m. |
| Peters | 2002 | Packing | Cascade mini-rings | Carbon steel, Ceramic, Polyethylene(plastic), Stainless steel, Stainless steel(316) | height_m, diameter_m | eqptype, material, diameter_m, height_m |  | height_m = packed height; diameter_m 0.3–4.0 m. |
| Peters | 2002 | Packing | Intalox saddles | Carbon steel, Ceramic, Polyethylene(plastic), Stainless steel, Stainless steel(316) | height_m, diameter_m | eqptype, material, diameter_m, height_m |  | height_m = packed height; diameter_m 0.3–4.0 m. |
| Peters | 2002 | Packing | Pall rings | Carbon steel, Ceramic, Polyethylene(plastic), Stainless steel, Stainless steel(316) | height_m, diameter_m | eqptype, material, diameter_m, height_m |  | height_m = packed height; diameter_m 0.3–4.0 m. |
| Peters | 2002 | Packing | Raschig rings | Carbon steel, Ceramic, Polyethylene(plastic), Stainless steel, Stainless steel(316) | height_m, diameter_m | eqptype, material, diameter_m, height_m |  | height_m = packed height; diameter_m 0.3–4.0 m. |
| Peters | 2002 | Pumps | Centrifugal | Carbon steel, Cast iron, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | volflow_cumph | eqptype, material, P_bar, volflow_cumph |  |  |
| Peters | 2002 | Pumps | Reciprocating | Carbon steel, Cast iron, Stainless steel, Stainless steel(316) | volflow_cumph | eqptype, material, P_bar, volflow_cumph |  |  |
| Peters | 2002 | Reactor | Jacketed agitated | Carbon steel, Glass-lined steel, Stainless steel | vol_cum | eqptype, material, vol_cum, P_bar |  | P_bar selects the design-pressure curve. |
| Peters | 2002 | Screens | Vibrating | Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | area_sqm | eqptype, material, area_sqm |  |  |
| Peters | 2002 | Screens | Vibrating (double deck) | Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | area_sqm | eqptype, material, area_sqm |  |  |
| Peters | 2002 | Size enlargement equipment | Pug mill extruder | — (material does not affect the cost) | massflow_kgph | eqptype, massflow_kgph |  |  |
| Peters | 2002 | Size enlargement equipment | Roll-type presses | — (material does not affect the cost) | massflow_kgph | eqptype, massflow_kgph |  |  |
| Peters | 2002 | Size enlargement equipment | Screw extruder | — (material does not affect the cost) | massflow_kgph | eqptype, massflow_kgph |  |  |
| Peters | 2002 | Size reduction equipment | Ball mill (dry, closed circuit, 13 mm to 100 mesh) | — (material does not affect the cost) | massflow_kgph | eqptype, massflow_kgph |  |  |
| Peters | 2002 | Size reduction equipment | Ball mill (dry, closed circuit, 19 mm to 48 mesh) | — (material does not affect the cost) | massflow_kgph | eqptype, massflow_kgph |  |  |
| Peters | 2002 | Size reduction equipment | Ball mill (dry, closed circuit, 6.4 mm to 325 mesh) | — (material does not affect the cost) | massflow_kgph | eqptype, massflow_kgph |  |  |
| Peters | 2002 | Size reduction equipment | Ball mill (dry, open circuit, 13 mm to 100 mesh) | — (material does not affect the cost) | massflow_kgph | eqptype, massflow_kgph |  |  |
| Peters | 2002 | Size reduction equipment | Ball mill (dry, open circuit, 19 mm to 48 mesh) | — (material does not affect the cost) | massflow_kgph | eqptype, massflow_kgph |  |  |
| Peters | 2002 | Size reduction equipment | Ball mill (dry, open circuit, 38 mm to 10 mesh) | — (material does not affect the cost) | massflow_kgph | eqptype, massflow_kgph |  |  |
| Peters | 2002 | Size reduction equipment | Ball mill (wet, closed circuit, 13 mm to 100 mesh) | — (material does not affect the cost) | massflow_kgph | eqptype, massflow_kgph |  |  |
| Peters | 2002 | Size reduction equipment | Ball mill (wet, closed circuit, 19 mm to 48 mesh) | — (material does not affect the cost) | massflow_kgph | eqptype, massflow_kgph |  |  |
| Peters | 2002 | Size reduction equipment | Ball mill (wet, closed circuit, 6.4 mm to 325 mesh) | — (material does not affect the cost) | massflow_kgph | eqptype, massflow_kgph |  |  |
| Peters | 2002 | Size reduction equipment | Ball mill (wet, open circuit, 13 mm to 100 mesh) | — (material does not affect the cost) | massflow_kgph | eqptype, massflow_kgph |  |  |
| Peters | 2002 | Size reduction equipment | Ball mill (wet, open circuit, 19 mm to 48 mesh) | — (material does not affect the cost) | massflow_kgph | eqptype, massflow_kgph |  |  |
| Peters | 2002 | Size reduction equipment | Ball mill (wet, open circuit, 38 mm to 10 mesh) | — (material does not affect the cost) | massflow_kgph | eqptype, massflow_kgph |  |  |
| Peters | 2002 | Size reduction equipment | Cage-type disintegrator | — (material does not affect the cost) | massflow_kgph | eqptype, massflow_kgph |  |  |
| Peters | 2002 | Size reduction equipment | Pulverizer | Carbon steel, Stainless steel(316) | massflow_kgph | eqptype, massflow_kgph |  |  |
| Peters | 2002 | Size reduction equipment | Rolling grinder | — (material does not affect the cost) | massflow_kgph | eqptype, massflow_kgph |  |  |
| Peters | 2002 | Size reduction equipment | Rotary cutter | — (material does not affect the cost) | massflow_kgph | eqptype, massflow_kgph |  |  |
| Peters | 2002 | Storage tank | Cone roof | Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel, Stainless steel(316), Titanium(alloy) | vol_cum | eqptype, material, vol_cum |  |  |
| Peters | 2002 | Storage tank | Floating roof | Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel, Stainless steel(316), Titanium(alloy) | vol_cum | eqptype, material, vol_cum |  |  |
| Peters | 2002 | Storage tank | Gas holder | Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel, Stainless steel(316), Titanium(alloy) | vol_cum | eqptype, material, vol_cum |  |  |
| Peters | 2002 | Storage tank | Open | Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel, Stainless steel(316), Titanium(alloy) | vol_cum | eqptype, material, vol_cum |  |  |
| Peters | 2002 | Storage tank | Spherical | Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel, Stainless steel(316), Titanium(alloy) | vol_cum | eqptype, material, vol_cum |  |  |
| Peters | 2002 | Trays | Bubble cap | Carbon steel, Stainless steel | diameter_m, num | eqptype, material, diameter_m, num |  | num = number of trays. |
| Peters | 2002 | Trays | Sieve | Carbon steel, Stainless steel | diameter_m, num | eqptype, material, diameter_m, num |  | num = number of trays. |
| Peters | 2002 | Trays | Turbogrid | Stainless steel | diameter_m, num | eqptype, material, diameter_m, num |  | num = number of trays. |
| Peters | 2002 | Trays | Valve | Carbon steel, Stainless steel | diameter_m, num | eqptype, material, diameter_m, num |  | num = number of trays. |
| Peters | 2002 | Turbines | Axial gas turbines | Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | power_kW | eqptype, material, power_kW |  |  |
| Peters | 2002 | Turbines | Liquid expanders | Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | power_kW | eqptype, material, power_kW |  |  |
| Peters | 2002 | Turbines | Radial expanders | Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | power_kW | eqptype, material, power_kW |  |  |
| Peters | 2002 | Vacuum system | Steam-jet ejector (1-stage) | Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | massflow_kgph | eqptype, material, massflow_kgph |  | massflow_kgph = air load to the ejector. |
| Peters | 2002 | Vacuum system | Steam-jet ejector (2-stage) | Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | massflow_kgph | eqptype, material, massflow_kgph |  | massflow_kgph = air load to the ejector. |
| Peters | 2002 | Vacuum system | Steam-jet ejector (4-stage) | Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel | massflow_kgph | eqptype, material, massflow_kgph |  | massflow_kgph = air load to the ejector. |
| Peters | 2002 | Vaporizer | Internal coils/jackets | Carbon steel, Glass-lined steel, Hastelloy C, Inconel, Monel, Nickel(alloy), SS clad, Stainless steel | vol_cum | eqptype, material, vol_cum, P_bar |  |  |
| Peters | 2002 | Vaporizer | Jacketed vessels | Carbon steel, Glass-lined steel, Hastelloy C, Inconel, Monel, Nickel(alloy), SS clad, Stainless steel | vol_cum | eqptype, material, vol_cum, P_bar |  |  |
| Peters | 2002 | Vessel/Tower | Horizontal vessel | Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel, Stainless steel(316) | height_m, diameter_m | eqptype, material, P_bar, diameter_m, height_m, thickness_m |  | vol_cum and thickness_m are optional; if not given they are estimated from D, H, P and T. |
| Peters | 2002 | Vessel/Tower | Vertical vessel | Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel, Stainless steel(316) | height_m, diameter_m, thickness_m | eqptype, material, P_bar, diameter_m, height_m, thickness_m |  | vol_cum and thickness_m are optional; if not given they are estimated from D, H, P and T. |
| Guthrie | 1968 | Compressor | Centrifugal | — (material does not affect the cost) | power_kW | eqptype, power_kW, driver | Electric-open/drip proof, Electric-explosion proof, Electric-totally enclosed, Steam turbine, Gas turbine | power_kW = compressor (shaft/fluid) power. |
| Guthrie | 1968 | Compressor | Reciprocating | — (material does not affect the cost) | power_kW | eqptype, power_kW, driver | Electric-open/drip proof, Electric-explosion proof, Electric-totally enclosed, Steam turbine, Intern comb.engine | power_kW = compressor (shaft/fluid) power. |
| Guthrie | 1968 | Furnace | Nonreactive furnace | Carbon steel, Cr-Mo steel, Stainless steel | power_kW | eqptype, material, P_bar, power_kW |  |  |
| Guthrie | 1968 | Furnace | Pyrolysis furnace | Carbon steel, Cr-Mo steel, Stainless steel | power_kW | eqptype, material, P_bar, power_kW |  |  |
| Guthrie | 1968 | Furnace | Reformer furnace | Carbon steel, Cr-Mo steel, Stainless steel | power_kW | eqptype, material, P_bar, power_kW |  |  |
| Guthrie | 1968 | Heat exchanger (others) | Air cooler | Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | area_sqm | eqptype, material, P_bar, area_sqm |  | area_sqm = calculated heat-transfer area; size S = area/15.5 (Biegler Table 4.12). |
| Guthrie | 1968 | Heat exchanger (shell and tube) | Fixed tube | CS shell/CS tube, CS shell/Cu tube, CS shell/Monel tube, CS shell/SS tube, CS shell/Ti(alloy) tube, Monel shell/Monel tube, SS shell/SS tube, Ti(alloy) shell/Ti(alloy) tube | area_sqm | eqptype, material, area_sqm, P_bar |  |  |
| Guthrie | 1968 | Heat exchanger (shell and tube) | Floating head | CS shell/CS tube, CS shell/Cu tube, CS shell/Monel tube, CS shell/SS tube, CS shell/Ti(alloy) tube, Monel shell/Monel tube, SS shell/SS tube, Ti(alloy) shell/Ti(alloy) tube | area_sqm | eqptype, material, area_sqm, P_bar |  |  |
| Guthrie | 1968 | Heat exchanger (shell and tube) | Kettle reboiler | CS shell/CS tube, CS shell/Cu tube, CS shell/Monel tube, CS shell/SS tube, CS shell/Ti(alloy) tube, Monel shell/Monel tube, SS shell/SS tube, Ti(alloy) shell/Ti(alloy) tube | area_sqm | eqptype, material, area_sqm, P_bar |  |  |
| Guthrie | 1968 | Heat exchanger (shell and tube) | U-tube (shell and tube) | CS shell/CS tube, CS shell/Cu tube, CS shell/Monel tube, CS shell/SS tube, CS shell/Ti(alloy) tube, Monel shell/Monel tube, SS shell/SS tube, Ti(alloy) shell/Ti(alloy) tube | area_sqm | eqptype, material, area_sqm, P_bar |  |  |
| Guthrie | 1968 | Heater | Cylindrical | Carbon steel, Cr-Mo steel, Stainless steel | power_kW | eqptype, material, P_bar, power_kW |  |  |
| Guthrie | 1968 | Heater | Diphenyl heater | Carbon steel, Cr-Mo steel, Stainless steel | power_kW | eqptype, material, P_bar, power_kW |  |  |
| Guthrie | 1968 | Pumps | Centrifugal | Carbon steel, Cast iron, Copper(alloy), Hastelloy C, Inconel, Monel, Nickel(alloy), Stainless steel, Titanium(alloy) | volflow_cumph | eqptype, material, volflow_cumph, P_bar, Pout_bar |  | Pout_bar required; T_K and P_bar set the operating-limit factor. |
| Guthrie | 1968 | Vessel/Tower | Horizontal vessel | Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), SS clad, Stainless steel, Titanium(alloy) | height_m, diameter_m | eqptype, material, P_bar, height_m, diameter_m |  | vol_cum and thickness_m are optional; if not given they are estimated from D, H, P and T. |
| Guthrie | 1968 | Vessel/Tower | Vertical vessel | Carbon steel, Hastelloy C, Inconel, Monel, Nickel(alloy), SS clad, Stainless steel, Titanium(alloy) | height_m, diameter_m | eqptype, material, P_bar, height_m, diameter_m |  | vol_cum and thickness_m are optional; if not given they are estimated from D, H, P and T. |

</details>

## Inputs of `capcomo()` and conventions

### Supported models

| Model | Source | Estimated cost type | Basis year | Currency / location | Required inputs | Input units | Valid range and out-of-range handling |
|---|---|---|---|---|---|---|---|
| `"Hill"` | Hill (1956), as given in Petley (1997), eqs. 3.3–3.4 | Installed total equipment cost | 1954 | USD | `unit_num`, `scale_tpy` | unit_num: – (process units); scale_tpy: t/y | No range check. |
| `"Guthrie"` | Peters, Timmerhaus & West (2003), Table 6-11 (p. 255), adapted from Guthrie (1970, 1974) | Fixed capital investment | 2000 | USD | `process`, `scale_tpy` | process: name (see the Guthrie plant table below); scale_tpy: t/y (product, or feed for petroleum units) | 1/3–3 × base plant size (Table 6-11 footnote). Below: extrapolated + warning. Above: identical parallel trains + warning. |
| `"Timms"` | Timms (1980), Method 2, as given in Petley (1997), eq. 3.20 | Inside battery limits | 1992 | USD | `unit_num`, `scale_tpy`, `Tmax_K`, `Pmax_bar` | unit_num: – (process units); scale_tpy: t/y; Tmax_K: K; Pmax_bar: bar | No range check. |
| `"Garrett"` | Garrett (2012); Towler & Sinnott (2008), Table 6.2 (Hydrocarbon Processing, Nexant PERP data) | Inside battery limits | 2006 | USD, U.S. Gulf Coast (January 2006) | `process`, `scale_tpy` | process: name (see the Garrett plant table below); scale_tpy: t/y (product for chemicals, feed for fuels) | S_lower–S_upper of each process. Below: extrapolated + warning. Above: identical parallel trains + warning. |
| `"Petley"` | Petley (1997), eq. 5.6 | Inside battery limits | 1988 | USD, plant built in West Germany (mid-1988) | `unit_num`, `scale_tpy`, `Tmax_K`, `Pmax_bar` | unit_num: – (process units); scale_tpy: t/y; Tmax_K: K; Pmax_bar: bar | 2,250–990,000 t/y (79 plants). Below: lower bound used + warning. Above: identical parallel trains + warning. |
| `"Lange 1"` | Lange (2001), CATTECH 5(2), eq. 2 | Fixed capital investment | 1993 | USD | `energyloss_MW` | energyloss_MW: MW | 3–8,000 MW (Figure 4 data). Below: extrapolated + warning. Above: identical parallel units + warning. |
| `"Lange 2"` | Lange (2001), CATTECH 5(2), eq. 3 | Fixed capital investment | 1993 | USD | `energytransfer_MW` | energytransfer_MW: MW | 2–650 MW (Figure 6 data, per process segment). Below: extrapolated + warning. Above: identical parallel units + warning. |

The full table, with the CE index of each basis year and notes, is in `docs/ECO-ANA_capcomo_models.xlsx` (sheet *Models*).

`scale_tpy` is the plant capacity in metric tons per year.

- Model names are matched ignoring letter case, spaces, hyphens and underscores. For example, `"lange1"`
  and `"LANGE 1"` both select `"Lange 1"`.
- All numeric inputs must be finite positive numbers. Python and NumPy numbers are accepted.
- On an input error, `capcomo()` prints an error message and returns `None` as the cost. It always returns
  a 3-tuple (`cost, basis, cost_type`), so unpacking the result does not fail. When the model itself is
  missing or unknown, the tuple is `(None, None, None)`.

### Guthrie model

Source: Peters, Timmerhaus and West (2003), *Plant Design and Economics for Chemical Engineers*, 5th ed.,
Table 6-11 (p. 255), adapted from Guthrie (1970, 1974):

FCI [million USD, 2000] = *C*<sub>base</sub> · (*Q*/*Q*<sub>base</sub>)<sup>*n*</sup>

- **Cost type:** Fixed capital investment (FCI), 2000 USD (CE = 394.1).
- **Units:** chemical plants use *Q*<sub>base</sub> in t/y. Petroleum processing plants use *Q*<sub>base</sub>
  in m³/d. For these, `scale_tpy` is converted with the liquid density listed below and 365 operating days
  per year. These conversion values are **ECO-ANA assumptions** (not given in the source). For feed-based
  units, pass the feed rate as `scale_tpy`.
- **Range:** the power factors apply within roughly a 3-fold ratio either way from *Q*<sub>base</sub>
  (Table 6-11, footnote).
  - Below *Q*<sub>base</sub>/3, the correlation is extrapolated, and a `UserWarning` is issued.
  - Above 3·*Q*<sub>base</sub>, the plant is split into *k* = ceil(*Q*/(3·*Q*<sub>base</sub>)) identical
    parallel trains. The cost is *k* · FCI(*Q*/*k*), and a `UserWarning` is issued.

<details>
<summary>Supported plants of the Guthrie model (28 processes)</summary>

| `process` (key) | Group | Process description | Capacity unit | Capacity range | Capacity basis | Conversion assumption (ECO-ANA) |
|---|---|---|---|---|---|---|
| Acetic acid | Chemical | CH3OH and CO - catalytic | t/y | 3,000–27,000 | Product | — |
| Acetone | Chemical | Propylene-copper chloride catalyst | t/y | 30,000–270,000 | Product | — |
| Ammonia | Chemical | Steam reforming | t/y | 30,000–270,000 | Product | — |
| Ammonium nitrate | Chemical | Ammonia and nitric acid | t/y | 30,000–270,000 | Product | — |
| Butanol | Chemical | Propylene, CO, and H2O - catalytic | t/y | 15,000–135,000 | Product | — |
| Chlorine | Chemical | Electrolysis of NaCl | t/y | 15,000–135,000 | Product | — |
| Ethylene | Chemical | Refinery gases | t/y | 15,000–135,000 | Product | — |
| Ethylene oxide | Chemical | Ethylene - catalytic | t/y | 15,000–135,000 | Product | — |
| Formaldehyde | Chemical | Methanol - catalytic; product: formaldehyde (37%) | t/y | 3,000–27,000 | Product | — |
| Glycol | Chemical | Ethylene and chlorine | t/y | 1,500–13,500 | Product | — |
| Hydrofluoric acid | Chemical | Hydrogen fluoride and H2O | t/y | 3,000–27,000 | Product | — |
| Methanol | Chemical | CO2, natural gas, and steam | t/y | 18,333.33–165,000 | Product | — |
| Nitric acid | Chemical | Ammonia - catalytic; product: high-strength nitric acid | t/y | 30,000–270,000 | Product | — |
| Phosphoric acid | Chemical | Calcium phosphate and H2SO4 | t/y | 1,500–13,500 | Product | — |
| Polyethylene | Chemical | Ethylene - catalytic; product: high-density polyethylene | t/y | 1,500–13,500 | Product | — |
| Propylene | Chemical | Refinery gases | t/y | 3,000–27,000 | Product | — |
| Sulfuric acid | Chemical | Sulfur - contact catalytic | t/y | 30,000–270,000 | Product | — |
| Urea | Chemical | Ammonia and CO2 | t/y | 18,333.33–165,000 | Product | — |
| Alkylation (H2SO4) | Petroleum processing | Catalytic | m³/d | 533.33–4,800 | Product | alkylate product; ρ = 0.70 t/m³; 365 d/y |
| Coking (delayed) | Petroleum processing | Thermal | m³/d | 533.33–4,800 | Feed | vacuum residue feed; ρ = 1.00 t/m³; 365 d/y |
| Coking (fluid) | Petroleum processing | Thermal | m³/d | 533.33–4,800 | Feed | vacuum residue feed; ρ = 1.00 t/m³; 365 d/y |
| Cracking (fluid) | Petroleum processing | Catalytic | m³/d | 533.33–4,800 | Feed | gas oil feed; ρ = 0.92 t/m³; 365 d/y |
| Cracking (thermal) | Petroleum processing | Thermal | m³/d | 533.33–4,800 | Feed | residue feed; ρ = 1.00 t/m³; 365 d/y |
| Distillation (atm.) | Petroleum processing | 65% vaporized | m³/d | 5,333.33–48,000 | Feed | crude oil feed; ρ = 0.87 t/m³; 365 d/y |
| Distillation (vac.) | Petroleum processing | 65% vaporized | m³/d | 5,333.33–48,000 | Feed | atmospheric residue feed; ρ = 0.95 t/m³; 365 d/y |
| Hydrotreating | Petroleum processing | Catalytic desulfurization | m³/d | 533.33–4,800 | Feed | distillate feed; ρ = 0.85 t/m³; 365 d/y |
| Reforming | Petroleum processing | Catalytic | m³/d | 533.33–4,800 | Feed | naphtha feed; ρ = 0.74 t/m³; 365 d/y |
| Polymerization | Petroleum processing | Catalytic | m³/d | 533.33–4,800 | Product | polymer gasoline product; ρ = 0.73 t/m³; 365 d/y |

Capacity range = 1/3 to 3 times the base plant size of Table 6-11, in the capacity unit. Base sizes, FCI values and power factors are in `docs/ECO-ANA_capcomo_models.xlsx` (sheet *Guthrie plants*).

</details>

### Timms model

Source: Timms (1980), as given in Petley (1997), eq. 3.20 (Method 2):

ISBL [GBP, 1992] = 3860 · *N* · *Q*<sup>0.639</sup> · *F*<sub>m</sub> · *T*<sub>max</sub><sup>0.066</sup> · *P*<sub>max</sub><sup>−0.016</sup>

- Inputs:
  - *N* = `unit_num`, the number of process units ("functional units" in the original source).
  - *Q* = `scale_tpy`, in t/y.
  - *T*<sub>max</sub> = `Tmax_K`, the maximum temperature in K.
  - *P*<sub>max</sub> = `Pmax_bar`, the maximum pressure in bar.
- *F*<sub>m</sub> is the materials-of-construction factor. The source gives Wilson factors from 1.0 (carbon
  steel) to 1.3 (high-grade stainless steel). ECO-ANA uses *F*<sub>m</sub> = 1.0 (carbon steel).
- **Cost type:** Inside battery limits (ISBL). Petley evaluated all existing methods on the battery-limits
  basis.
- **Currency:** the source cost is in 1992 GBP. It is converted to 1992 USD with
  `GBP_TO_USD_1992` = 1.7643 USD/GBP, a constant of the `ecoana.capcomo` module. You can change this value
  before calling `capcomo()`. Because `ecoana.capcomo` refers to the function, access the module with
  `importlib`:
  ```python
  import importlib
  importlib.import_module("ecoana.capcomo").GBP_TO_USD_1992 = 1.80
  ```

### Petley model

Source: Petley (1997), eq. 5.6:

ISBL [USD, mid-1988] = 55882 · *Q*<sup>0.44</sup> · *N*<sup>0.486</sup> · *T*<sub>max</sub><sup>0.038</sup> · *P*<sub>max</sub><sup>−0.02</sup> · *F*<sub>m</sub><sup>0.341</sup>

- Inputs:
  - *Q* = `scale_tpy`, in t/y.
  - *N* = `unit_num`, the number of process units ("functional units" in the original source).
  - *T*<sub>max</sub> = `Tmax_K`, in K.
  - *P*<sub>max</sub> = `Pmax_bar`, in bar.
- *F*<sub>m</sub> is the materials-of-construction (Wilson) factor. ECO-ANA uses *F*<sub>m</sub> = 1.0 (carbon
  steel).
- **Cost basis:** battery-limits capital cost (ISBL), in US dollars, for a plant **built in West Germany in
  mid-1988**. The CE index is 342.5 (1988). The cost is not corrected for location; apply a location
  factor if needed.
- **Capacity range** of the correlation data (79 plants): 2,250–990,000 t/y.
  - Below the range, the lower bound (2,250 t/y) is used, and a `UserWarning` is issued.
  - Above the range, the plant is split into *k* = ceil(*Q*/990,000) identical parallel trains, each with
    *N* process units. The cost is *k* · ISBL(*Q*/*k*), and a `UserWarning` is issued.

### Garrett model (process cost correlations)

Sources:
- Garrett, D.E. (2012), *Chemical Engineering Economics*, Springer Science & Business Media.
- Towler, G. and Sinnott, R. (2008), *Chemical Engineering Design*, Table 6.2. The process library of
  100 processes is taken from this table (data from Hydrocarbon Processing and Nexant PERP reports).

The correlation is:

ISBL [MM$, January 2006, U.S. Gulf Coast, CE = 478.6] = *a* · *S*<sup>*n*</sup>

- *S* is the **product rate for chemicals** and the **feed rate for fuels/refinery units** (Table 6.2,
  note 3). For the feed-based processes (marked *Feed* below), pass the feed rate as `scale_tpy`.
- **Below the range** (*S* < *S*<sub>lower</sub>): the correlation is extrapolated, and a `UserWarning`
  is issued. Correlations with *n* = 0.6 are already an extrapolation around a single cost point
  (note 4).
- **Above the range** (*S* > *S*<sub>upper</sub>): the plant is split into *k* = ceil(*S*/*S*<sub>upper</sub>)
  identical parallel trains. The cost is *k* · *a* · (*S*/*k*)<sup>*n*</sup>, and a `UserWarning` is
  issued. The split is an ECO-ANA assumption, not part of the source.
- Correlations defined in MMlb/y or t/y are converted from `scale_tpy` exactly (1 t = 0.002204623 MMlb).
  The other units need the density, molar mass and operating days listed below. These values are
  **ECO-ANA assumptions** (not given in the source):
  - t/d, bpd and MMscf/d use 365 operating days per year.
  - Gas volumes are ideal gas at 60 °F and 1 atm (379.49 scf/lbmol).
  - Liquid volumes are at about 15 °C.
- Table 6.2 gives the unit of "Ethanol by ethylene hydration" as "Mgal/y" (30–90). ECO-ANA reads this
  as MMgal/y, because 30–90 thousand gal/y is not a realistic plant size.

<details>
<summary>Supported plants of the Garrett model (100 processes)</summary>

| `process` (key) | Licensor | Capacity unit | Capacity range | Capacity basis | Conversion assumption (ECO-ANA) |
|---|---|---|---|---|---|
| ABSResin (15%Rubber) (emulsion polymerization) | Generic | MMlb/y | 50–300 | Product | exact (1 t = 0.002204623 MMlb) |
| Acetic Acid (Cativa) | BP | MMlb/y | 500–2,000 | Product | exact (1 t = 0.002204623 MMlb) |
| Acetic Acid (Low Water Methanol Carbonylation) | Celanese | MMlb/y | 500–2,000 | Product | exact (1 t = 0.002204623 MMlb) |
| Acrolein (propylene oxidation with Bi/Mo catalyst) | Generic | MMlb/y | 30–150 | Product | exact (1 t = 0.002204623 MMlb) |
| Adipic acid (phenol) | Generic | MMlb/y | 300–1,000 | Product | exact (1 t = 0.002204623 MMlb) |
| Alkylation (sulfuric acid effluent refrigeration) | Stratco/DuPont | bpd | 4,000–20,000 | Product | bpd of alkylate (rho 0.70); 365 d/y |
| Alkylation (HF) | UOP | bpd | 5,000–12,000 | Product | bpd of alkylate (rho 0.70); 365 d/y |
| Allyl chloride (propylene chlorination) | Generic | MMlb/y | 80–250 | Product | exact (1 t = 0.002204623 MMlb) |
| Alpha olefins (full-range, Chevron Phillips) | Chevron Phillips | MMlb/y | 400–1,200 | Product | exact (1 t = 0.002204623 MMlb) |
| Alpha olefins (full-range, Shell) | Shell | MMlb/y | 400–1,000 | Product | exact (1 t = 0.002204623 MMlb) |
| Benzene (Sulfolane extraction) | UOP/Shell | MMgal/y | 50–200 | Product | MMgal/y of benzene (rho 0.879) |
| Benzene (toluene hydrodealkylation) | Generic | MMgal/y | 50–200 | Product | MMgal/y of benzene (rho 0.879) |
| Benzene reduction (Bensat) | UOP | bpd | 8,000–15,000 | Feed | bpd of light reformate feed (rho 0.70); 365 d/y |
| Biodiesel(FAME) (vegetable oil) | Generic | MMlb/y | 100–500 | Product | exact (1 t = 0.002204623 MMlb) |
| bis-HET (Eastman Glycolysis) | Eastman | MMlb/y | 50–200 | Product | exact (1 t = 0.002204623 MMlb) |
| BTX Aromatics (Cyclar) | BP/UOP | t/y | 200,000–800,000 | Product | — |
| BTX Aromatics (CCR Platforming) | UOP | t/y | 200,000–800,000 | Product | — |
| Butadiene (extractive distillation) | UOP/BASF | MMlb/y | 100–500 | Product | exact (1 t = 0.002204623 MMlb) |
| Butadiene (Oxo-D plus extractive distillation) | Texas Petrochem. | MMlb/y | 100–500 | Product | exact (1 t = 0.002204623 MMlb) |
| Butene-1 (Alphabutol ethylene dimerization) | Axens | t/y | 5,000–30,000 | Product | — |
| Butene-1 (BP) | BP | t/y | 20,000–80,000 | Product | — |
| Caprolactam (nitration-grade toluene) | SNIA BPD S.p.A. | t/y | 40,000–120,000 | Product | — |
| Carbon monoxide (steam methane reforming) | Generic | MMscf/y | 2,000–6,000 | Product | MMscf/y of CO (M 28.01) |
| Catalytic Condensation (Gasoline Production) | UOP | bpd | 10,000–30,000 | Product | bpd of polymer gasoline (rho 0.73); 365 d/y |
| Catalytic reforming (CCR Platforming) | UOP | bpd | 15,000–60,000 | Feed | bpd of naphtha FEED (rho 0.74); 365 d/y |
| Coking (Flexicoking including Fluid Coking) | ExxonMobil | bpd | 15,000–40,000 | Feed | bpd of vacuum residue FEED (rho 1.00); 365 d/y |
| Coking (Selective Yield Delayed Coking) | Foster Wheeler/UOP | bpd | 15,000–60,000 | Feed | bpd of vacuum residue FEED (rho 1.00); 365 d/y |
| Copolymer polypropylene (INNOVENE) | BP | MMlb/y | 300–900 | Product | exact (1 t = 0.002204623 MMlb) |
| Copolymer polypropylene (Unipol) | Dow | MMlb/y | 300–900 | Product | exact (1 t = 0.002204623 MMlb) |
| Copolymer polypropylene (SPHERIPOL Bulk) | Basell | MMlb/y | 300–900 | Product | exact (1 t = 0.002204623 MMlb) |
| Copolymer polypropylene (BORSTAR) | Borealis | MMlb/y | 300–900 | Product | exact (1 t = 0.002204623 MMlb) |
| Crude distillation (D2000) | TOTAL/Technip | bpd | 150,000–300,000 | Feed | bpd of crude oil FEED (rho 0.87); 365 d/y |
| Cumene (Q-Max) | UOP | t/y | 150,000–450,000 | Product | — |
| Cyclic Olefin Copolymer (Mitsui) | Mitsui | MMlb/y | 60–120 | Product | exact (1 t = 0.002204623 MMlb) |
| Cyclohexane (liq-phase hydrogenation of benzene) | Axens | t/y | 100,000–300,000 | Product | — |
| Dewaxing (ISODEWAXING) | Chevron Lummus | bpd | 6,000–15,000 | Feed | bpd of waxy lube oil FEED (rho 0.87); 365 d/y |
| 2,6-Dimethylnaphthalene (Methanol alkylation) | Exxon Mobil/Kobe | MMlb/y | 50–100 | Product | exact (1 t = 0.002204623 MMlb) |
| Dimethyl terephthalate (methanolysis) | Generic | MMlb/y | 30–80 | Product | exact (1 t = 0.002204623 MMlb) |
| Dimethyl terephthalate (Huels Oxidation) | Huels | MMlb/y | 300–800 | Product | exact (1 t = 0.002204623 MMlb) |
| Ethanol (ethylene hydration) | Generic | MMgal/y (book: Mgal/y) | 30–90 | Product | million gal/y of ethanol (rho 0.789) |
| Ethanol (fuel-grade) (Corn Dry Milling) | Generic | t/y | 100,000–300,000 | Product | — |
| Ethylbenzene (EBOne) | ABB Lummus/UOP | t/y | 300,000–700,000 | Product | — |
| Ethylene (ethane cracking) | Generic | MMlb/y | 500–2,000 | Product | exact (1 t = 0.002204623 MMlb) |
| Ethylene (UOP Hydro MTO) | UOP/Norsk Hydro | MMlb/y | 500–2,000 | Product | exact (1 t = 0.002204623 MMlb) |
| Ethylene (light naphtha cracker) | Generic | MMlb/y | 1,000–2,000 | Product | exact (1 t = 0.002204623 MMlb) |
| Ethylene (ethane/propane cracker) | Generic | MMlb/y | 1,000–2,000 | Product | exact (1 t = 0.002204623 MMlb) |
| Ethylene (gas oil cracker) | Generic | MMlb/y | 1,000–2,000 | Product | exact (1 t = 0.002204623 MMlb) |
| Ethylene glycol (ethylene oxide hydrolysis) | Shell | MMlb/y | 500–1,000 | Product | exact (1 t = 0.002204623 MMlb) |
| Expandable poly-styrene (suspension) | Generic | MMlb/y | 50–100 | Product | exact (1 t = 0.002204623 MMlb) |
| Fischer Tropsch (ExxonMobil) | ExxonMobil | t/y | 200,000–700,000 | Product | — |
| Fluid catalytic cracking (KBR) | KBR | bpd | 20,000–60,000 | Feed | bpd of gas oil FEED (rho 0.92); 365 d/y |
| Fluid catalytic cracking (power recovery) | UOP | bpd | 20,000–60,000 | Feed | bpd of gas oil FEED (rho 0.92); 365 d/y |
| Gas to liquids (Syntroleum) | Syntroleum | bpd | 30,000–100,000 | Product | bpd of liquid product (rho 0.77); 365 d/y |
| Gas sweetening (Amine Guard FS to pipeline spec) | UOP | MMscf/d | 300–800 | Feed | MMscf/d of natural gas FEED (M 17.4); 365 d/y |
| Gasification (GE Gasification Process Mayacrude) | GE Energy | bpd | 7,000–15,000 | Feed | bpd of Maya crude FEED (rho 0.92); 365 d/y |
| Gasoline desulfurization (Prime-G+) | Axens | bpd | 7,000–15,000 | Feed | bpd of FCC gasoline FEED (rho 0.74); 365 d/y |
| Glucose(40%Solution) (basic wet cornmilling) | Generic | MMlb/y | 300–800 | Product | exact (1 t = 0.002204623 MMlb) |
| HDPE Pellets (BP Gas Phase) | BP Amoco | MMlb/y | 300–700 | Product | exact (1 t = 0.002204623 MMlb) |
| HDPE Pellets (Phillips Slurry) | Phillips | MMlb/y | 300–700 | Product | exact (1 t = 0.002204623 MMlb) |
| HDPE Pellets (Zeigler Slurry) | Zeigler | MMlb/y | 300–700 | Product | exact (1 t = 0.002204623 MMlb) |
| High impact polystyrene (bulk polymerization) | Dow | MMlb/y | 70–160 | Product | exact (1 t = 0.002204623 MMlb) |
| Hydrocracking (ISOCRACKING) | Chevron Lummus | bpd | 20,000–45,000 | Feed | bpd of vacuum gas oil FEED (rho 0.92); 365 d/y |
| Hydrocracking (Unicracking, distillate) | UOP | bpd | 20,000–45,000 | Feed | bpd of vacuum gas oil FEED (rho 0.92); 365 d/y |
| Hydrocracking (Axens) | Axens | bpd | 20,000–45,000 | Feed | bpd of vacuum gas oil FEED (rho 0.92); 365 d/y |
| Hydrogen (steam methane reforming) | Foster Wheeler | MMscf/d | 10–50 | Product | MMscf/d of H2 (M 2.016); 365 d/y |
| Hydrotreating (Unionfining) | UOP | bpd | 10,000–40,000 | Feed | bpd of distillate FEED (rho 0.85); 365 d/y |
| Isomerization (Once-through Penex) | UOP | bpd | 8,000–15,000 | Feed | bpd of light naphtha FEED (rho 0.65); 365 d/y |
| Isomerization (Penex-Molex) | UOP | bpd | 8,000–15,000 | Feed | bpd of light naphtha FEED (rho 0.65); 365 d/y |
| Isophthalic acid (m-Xylene oxidation) | Generic | MMlb/y | 160–300 | Product | exact (1 t = 0.002204623 MMlb) |
| Isoprene (isobutylene carbonylation) | IFP | MMlb/y | 60–200 | Product | exact (1 t = 0.002204623 MMlb) |
| Isoprene (propylene dimerization and pyrolysis) | Generic | MMlb/y | 60–200 | Product | exact (1 t = 0.002204623 MMlb) |
| Linear alkylbenzene (PACOL/DeFine/PEP/Detal) | UOP | MMlb/y | 100–250 | Product | exact (1 t = 0.002204623 MMlb) |
| Linear alpha olefins (Chevron) | Chevron | MMlb/y | 300–700 | Product | exact (1 t = 0.002204623 MMlb) |
| Linear alpha olefins (Linear-1) | UOP | t/y | 200,000–300,000 | Product | — |
| Maleic anhydride (fluid bed) | Generic | MMlb/y | 70–150 | Product | exact (1 t = 0.002204623 MMlb) |
| Methacrylic acid (isobutylene oxidation) | Generic | MMlb/y | 70–150 | Product | exact (1 t = 0.002204623 MMlb) |
| Methanol (steam reforming & synthesis) | Davy Process Tech. | t/d | 3,000–7,000 | Product | t/d of methanol; 365 d/y |
| m-Xylene (MX Sorbex) | UOP | MMlb/y | 150–300 | Product | exact (1 t = 0.002204623 MMlb) |
| Naphthalene (3-stage fractional crystallizer) | Generic | MMlb/y | 20–50 | Product | exact (1 t = 0.002204623 MMlb) |
| N-Butanol (crude C4s) | BASF | MMlb/y | 150–300 | Product | exact (1 t = 0.002204623 MMlb) |
| Norbornene (Diels-Alder reaction) | Generic | MMlb/y | 40–90 | Product | exact (1 t = 0.002204623 MMlb) |
| Pentaerythritol (condensation) | Generic | MMlb/y | 40–90 | Product | exact (1 t = 0.002204623 MMlb) |
| PET resin chip (comonomer by NG3) | DuPont | MMlb/y | 150–300 | Product | exact (1 t = 0.002204623 MMlb) |
| Phenol (cumene, zeolite catalyst basis) | UOP/ABB Lummus | MMlb/y | 200–600 | Product | exact (1 t = 0.002204623 MMlb) |
| Phthalic anhydride (catalytic oxidation) | Generic | MMlb/y | 100–200 | Product | exact (1 t = 0.002204623 MMlb) |
| Polycarbonate (interfacial polymerization) | Generic | MMlb/y | 70–150 | Product | exact (1 t = 0.002204623 MMlb) |
| Polyethylene terephthalate (meltphase) | Generic | MMlb/y | 70–200 | Product | exact (1 t = 0.002204623 MMlb) |
| Polystyrene (bulk polymerization, plugflow) | Generic | MMlb/y | 70–200 | Product | exact (1 t = 0.002204623 MMlb) |
| Propylene (Oleflex) | UOP | t/y | 150,000–350,000 | Product | — |
| Propylene (metathesis) | Generic | MMlb/y | 500–1,000 | Product | exact (1 t = 0.002204623 MMlb) |
| Purified terphthalic acid (EniChem/Technimont) | EniChem/Technimont | MMlb/y | 350–700 | Product | exact (1 t = 0.002204623 MMlb) |
| p-Xylene (Isomar and Parex) | UOP | t/y | 300,000–700,000 | Product | — |
| p-Xylene (Tatoray) | UOP | bpd | 12,000–20,000 | Feed | bpd of toluene/C9 aromatics FEED (rho 0.87); 365 d/y |
| Refined Glycerine (distillation/adsorption) | Generic | MMlb/y | 30–60 | Product | exact (1 t = 0.002204623 MMlb) |
| Sebaccic Acid (cyclododecanone route) | Sumitomo | MMlb/y | 8–16 | Product | exact (1 t = 0.002204623 MMlb) |
| Sorbitol(70%) (continuous hydrogenation) | Generic | MMlb/y | 50–120 | Product | exact (1 t = 0.002204623 MMlb) |
| Styrene (SMART) | ABB Lummus/UOP | t/y | 300,000–700,000 | Product | — |
| Vinyl acetate (Cativa Integrated) | BP | MMlb/y | 300–800 | Product | exact (1 t = 0.002204623 MMlb) |
| Vinyl acetate (Celanese VAntage) | Celanese | MMlb/y | 300–800 | Product | exact (1 t = 0.002204623 MMlb) |
| Visbreaking (coil-type visbreaker) | Foster Wheeler/UOP | bpd | 6,000–15,000 | Feed | bpd of vacuum residue FEED (rho 1.00); 365 d/y |

Capacity range = S<sub>lower</sub>–S<sub>upper</sub> of Table 6.2, in the capacity unit. The coefficients *a* and *n* are in `docs/ECO-ANA_capcomo_models.xlsx` (sheet *Garrett plants*).

</details>

### Lange 1 and Lange 2 models

Source: Lange (2001), *CATTECH* 5(2), 82–95.

| Model | Correlation (MMUSD, 1993) | Input | Range of the correlation data |
|---|---|---|---|
| `"Lange 1"` | FCI = 3.0 · *E*<sub>loss</sub><sup>0.84</sup> (eq. 2) | `energyloss_MW` | 3–8,000 MW (Figure 4) |
| `"Lange 2"` | FCI = 2.9 · *E*<sub>transfer</sub><sup>0.55</sup> (eq. 3) | `energytransfer_MW` | 2–650 MW (Figure 6) |

- **Cost type: Fixed capital investment (FCI).** The investment data of both correlations cover the plant
  and its off-sites. For Lange 1, the source converts ISBL costs to plant totals with a factor of 1.4
  (notes [iii] and [iv]). Working capital is not included.
- **`energyloss_MW`** is the energy loss of the whole plant: LHV(feed + fuel) − LHV(product), in MW. It
  covers the losses through the heat of reaction, fuel combustion and the heating value of purge streams.
- **`energytransfer_MW`** is the energy transfer duty, in MW: the sum of the duties of all heat- and
  impulse- (momentum-) transfer units in a process segment, taken from the process flowsheet.
  - It is mostly the heat-transfer duty for the heat of reaction and the feed–effluent heat exchange.
  - Gas compression duty matters for high-pressure gas-phase processes. Liquid pumping duty is negligible.
  - The energy loss is **not** added to this duty.
  - The process segments in the correlation data are:
    - Conversion segments: steam reforming, partial oxidation and combined reforming, methanol synthesis,
      Fischer–Tropsch synthesis, hydrocracking, paraffin alkylation, hydrodesulfurization, platforming,
      ethene oxide synthesis and hydration.
    - Auxiliary units: distillation trains, large multistep compressors, cryogenic air separation units,
      boilers and diesel engines.
- **Below the data range:** the correlation is extrapolated, and a `UserWarning` is issued.
- **Above the data range:** the estimate is split into *k* = ceil(*E*/*E*<sub>max</sub>) identical parallel
  units. The cost is *k* · *a* · (*E*/*k*)<sup>*n*</sup>, and a `UserWarning` is issued.
- The data ranges were read from the data points in Figures 4 and 6 of the source.

## Capital cost keywords for `capconv()`

`cap_in` and `cap_out` take one of five predefined keywords, which correspond to the capital cost
levels used by the plant cost factor sets (equipment cost → installed equipment cost → ISBL → FCI → TCI).

| Standard keyword | Also accepted (aliases) |
|---|---|
| `"Equipment cost"` | `TPEC`, `PEC`, `Total equipment cost`, `Total purchased equipment cost`, `Total equipment purchase(d) cost`, `Purchased equipment cost`, `Equipment`, `Total equipment` |
| `"Installed equipment cost"` | `IEC`, `TIEC`, `Total installed equipment cost`, `Installed total equipment cost`, `Total installed equipment`, `Installed equipment` |
| `"Inside battery limits"` | `ISBL`, `ISBL cost`, `Inside battery limits cost` |
| `"Fixed capital investment"` | `FCI`, `Fixed capital`, `Fixed capital cost` |
| `"Total capital investment"` | `TCI`, `Total capital`, `Total capital cost`, `Total capital investment cost` |

- The aliases are a fixed list (`ecoana.capconv.CAP_KEYS`). They cover the abbreviations used in the
  source publications and the cost type returned by `capcomo()`, so that its output can be passed to
  `capconv()` directly.
- Letter case, spaces and punctuation are ignored, so `"TCI"`, `"tci"` and `"T.C.I."` are equivalent.
- Any other label is rejected: `capconv()` prints an error message listing the standard keywords and
  returns `None`. Labels are never guessed.
- The Lang factor set only converts between `"Equipment cost"`, `"Fixed capital investment"` and
  `"Total capital investment"`.

```python
# Pass the capcomo() result straight to capconv()
cost, basis, cost_type = capcomo(model="Hill", unit_num=10, scale_tpy=100_000)
tci = capconv(model="Peters and Timmerhaus", phase_processing="Fluid",
              cap_in=cost_type, cap_out="Total capital investment", base_cost=cost)
```

## License

ECO-ANA is released under the MIT License. See [LICENSE.txt](https://github.com/LSPE-CNU/ECO-ANA_Techno-Economic-Analysis-Tool-for-Chemical-Processes/blob/main/LICENSE.txt) for details.

## Contact

For questions, bug reports, or suggestions, please open an issue on
[GitHub](https://github.com/LSPE-CNU/ECO-ANA_Techno-Economic-Analysis-Tool-for-Chemical-Processes/issues)
or contact the developers by e-mail.

- **Developer:** Haeun Choi — [nolaaa@o.cnu.ac.kr](mailto:nolaaa@o.cnu.ac.kr)
- **Corresponding:** Kosan Roh — [ksroh@cnu.ac.kr](mailto:ksroh@cnu.ac.kr)

Laboratory for Sustainable Process Engineering (LSPE), Chungnam National University
