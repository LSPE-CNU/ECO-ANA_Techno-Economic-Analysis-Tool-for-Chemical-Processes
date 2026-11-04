# Changelog

## [1.0.0] – unreleased

### Packaging and installation
- Repository restructured into a standard Python package layout: the package code is in the
  `ecoana/` folder (fixed name, independent of the version); `pyproject.toml`, `README.md`,
  `LICENSE.txt` and `examples/` are at the repository root.
- Added `pyproject.toml`, `requirements.txt` and `environment.yml`; the package can be installed
  with `pip install ecoana` (PyPI) or `pip install .` (source). Supported Python versions: 3.9–3.13.
- Imports between the internal modules changed to relative imports, so that `import ecoana`
  works after installation (in 0.0.x, importing the installed package failed with
  `ModuleNotFoundError: No module named 'unit_parameters'`).
- Removed the unused `pandas` import (the only runtime dependency is now `numpy >= 1.21`).
- Removed test code at the end of `eqpcomo.py` that was executed on every import.
- Added `ecoana.__version__`.
- `pyproject.toml`: the `classifiers` list was inside `[project.optional-dependencies]` and is now under
  `[project]`. Added `MANIFEST.in` so that the source distribution includes the tests, examples, the
  `docs/` tables used by the tests, and the changelog. Relative links in the README (supported-equipment table, license) were replaced with absolute
  GitHub links so that they work on the PyPI project page.

### eqpcomo() – common inputs
- Pressure convention: `P_bar` and `Pout_bar` are absolute pressures. The Turton and Seider models,
  whose pressure-dependent correlations use gauge pressure, now subtract 1.013 bar (Guthrie already
  converts to psig); Seider's exchanger and furnace pressure factors are set to 1 below the lower limit
  of their equations (100 and 500 psig). Documented in the README.
- Added `docs/ECO-ANA_supported_equipment.xlsx` / `.csv`: supported equipment, types, materials, size
  inputs and units, required inputs, and pressure/temperature dependence for every model.
- Vessels: `vol_cum` and `thickness_m` are optional, but the estimates were only made when they were
  `None` while their defaults are 0. When omitted, the shell mass was 0 (Seider: division by zero;
  Smith, Towler, Peters: cost at the minimum size) and Turton used the minimum volume. Both are now
  estimated when they are 0 or not given; a warning is issued if the estimated thickness is ~0
  (pressure 0 or not given).
- `vessel_thick()`: the allowable-stress selection was nested so that carbon steel used the stresses
  for other alloys and stainless steel returned `None`. Fixed.

### capconv()
- Accepted keywords and aliases for `cap_in` / `cap_out` defined in a module-level dictionary
  (`ecoana.capconv.CAP_KEYS`); added the aliases `IEC`, `PEC`, `Installed total equipment cost`
  (cost type returned by the Hill model), `Total purchased equipment cost` and
  `Total equipment purchased cost`.
- Aliases now also work with the Lang factor set (the conversion to standard keywords is done
  before the model-specific branches).
- Unknown cost-type labels now return `None` with an error message instead of raising `KeyError`.

### eqpcomo() – out-of-range sizes and error returns
- A `UserWarning` is now issued whenever a size is outside the range of a correlation, in all six models:
  - below the lower limit, when the cost is evaluated at the lower limit or extrapolated;
  - above the upper limit, when the equipment is split into identical parallel units (the number of units
    is reported) or the correlation is extrapolated.
  Previously, the warning was issued only for parallel units in the Peters model and for one Guthrie
  equipment class. All other range handling was silent.
- Seider centrifuges: a bowl diameter outside 20–70 in (auto batch, vertical) or 20–43 in (other types)
  no longer returns an error. Below the range the cost is evaluated at 20 in; above it the power law is
  extrapolated. A warning is issued in both cases.
- Seider trays: outside the 2–16 ft diameter range of Eq. (16.56), the cost is evaluated at 2 ft (below)
  or extrapolated with the log-log slope at 16 ft (above). Previously, very large diameters returned an
  infinite cost through the exponential form.
- Seider blowers: added the size ranges of Table 16.32 (centrifugal turbo 5–1,000 Hp, rotary straight-lobe
  1–1,000 Hp), with the same range handling as the other Seider correlations.
- Guthrie vessels: a warning is issued for diameters outside 1–10 ft (Biegler Table 4.11); the correlation
  is extrapolated.
- An error message is no longer returned in place of the cost. Examples are an unsupported material, or
  "Error: No data" in Turton, Smith and Towler. `eqpcomo()` now prints the message and returns
  `(None, basis)`. A non-finite or negative cost is reported as an error.
- The artificial lower cost threshold of the Turton model (cost <= $10 returned "Error: No data") was
  removed; for example, very small packing volumes now return the cost at the lower limit.
- `eqpcomo()` always returns a 2-tuple, `(None, None)` when the model is missing or unknown.
- The remaining Korean code comments were translated into English.

### Examples
- Added `examples/methanol_plant_level.py`. It estimates the plant-level cost of the 1,000 kt/y
  methanol case study with the seven `capcomo()` models (inputs of manuscript Table 4), escalates the
  estimates to 2025 with the CEPCI (787.8), and converts them to TCI with `capconv()` (Peters and
  Timmerhaus factors, fluid processing). The number of process units is 7 (two reforming, two
  reaction and three separation steps), following the process-unit definition of the manuscript.
- Added `examples/equipment_level_estimation.py`. It calculates the purchase costs of the equipment list of a
  hypothetical gas compression and absorption unit with the six `eqpcomo()` models, escalates them to
  2025 (CEPCI 787.8), sums them to the TPEC, converts the TPEC to TCI with `capconv()`, and reports the
  range across the models.

### Tests
- Added a pytest suite (`tests/`, 830 tests), which covers the following:
  - every model/equipment/type combination of `eqpcomo()`;
  - the Guthrie and Garrett process libraries;
  - range handling and input validation of `capcomo()`;
  - the factor sets and keyword aliases of `capconv()`;
  - the calls reported during review and worked examples from the source publications.
- Run with `python -m pytest tests`; `pip install .[test]` installs pytest.

### eqpcomo() – invalid model name
- An invalid model name now prints the package error message and returns `None`. Previously it
  raised `KeyError`, because the basis year was looked up before the model name was checked.

### capcomo() – input handling
- Garrett model: zero or negative `scale_tpy` now returns an error message. Previously, zero
  returned a cost of 0 and a negative value raised `TypeError`.
- Numeric inputs of all models are checked. Non-numeric values (strings, lists, booleans), NaN and
  infinity now return an error message instead of raising `TypeError` / `OverflowError` or
  returning NaN. NumPy numbers are accepted.
- A missing or unknown model now returns `(None, None, None)` instead of `None`, so
  `cost, basis, cost_type = capcomo(...)` no longer raises `TypeError`.
- Model names are matched ignoring letter case, spaces, hyphens and underscores
  (e.g. `"lange1"` -> `"Lange 1"`).
- Removed the unused `numpy` import.

### capcomo() – Guthrie model
- Source reference corrected in the code: Peters, Timmerhaus & West (2003), Table 6-11 (2000 USD),
  adapted from Guthrie (1970). All 18 chemical-plant entries were checked against the table; they
  match.
- Added the 10 petroleum processing plants of Table 6-11 (alkylation, delayed and fluid coking,
  fluid and thermal cracking, atmospheric and vacuum distillation, hydrotreating, reforming and
  polymerization). Their capacity (m3/d) is converted from `scale_tpy` with documented liquid
  densities and 365 operating days per year.
- Added the range of the power factors (1/3 to 3 times the base plant size, Table 6-11 footnote).
  Below the range the correlation is extrapolated; above it the plant is estimated as identical
  parallel trains. A `UserWarning` is issued in both cases.
- Fixed the process description "Refinary gases" -> "Refinery gases"; the product conditions
  (formaldehyde 37%, high-strength nitric acid, high-density polyethylene) are now stated in the
  process descriptions and the README.
- Zero or negative `scale_tpy` now returns an error message.

### capcomo() – input validation (Hill, Timms, Petley)
- Zero or negative `unit_num`, `scale_tpy`, `Tmax_K` or `Pmax_bar` now returns an error message
  (cost `None`) instead of a meaningless result or a math error.

### capcomo() – Petley model
- Corrected the cost basis from 1987 (CE 323.7) to mid-1988 (CE 342.5): the correlation gives the
  cost in US dollars of a plant constructed in West Germany in 1988 (Petley 1997). The location
  basis is documented in the code and the README.
- Added the capacity range of the correlation data (2,250–990,000 t/y). Below the range the lower
  bound is used; above it the plant is estimated as identical parallel trains. A `UserWarning` is
  issued in both cases.
- The materials-of-construction factor of eq. 5.6 is set to Fm = 1.0 (carbon steel); this is
  documented in the code and the README.

### capcomo() – Timms model
- Corrected the coefficient from 2570 to 3860 (Timms Method 2, Petley 1997, eq. 3.20). The value
  2570 does not appear in the source.
- The source cost is in 1992 GBP; it is now converted to 1992 USD with `GBP_TO_USD_1992` = 1.7643.
- The returned cost type is now "Inside battery limits" (previously "Total capital investment"),
  in line with the battery-limits basis on which Petley (1997) evaluated the method.
- The materials-of-construction factor of the source is set to Fm = 1.0 (carbon steel); this is
  documented in the code and the README.

### capcomo() – Lange 1 and Lange 2 models
- Lange 2: corrected the coefficient from 12.9 to 2.9 (Lange 2001, eq. 3). The previous value
  overestimated the cost by a factor of 4.45.
- Lange 1 and Lange 2 now return the cost type "Fixed capital investment" (previously "Total
  capital investment"). The source investment data cover the plant and its off-sites (ISBL x 1.4)
  without working capital (Lange 2001, notes [iii] and [iv]).
- Added the applicable ranges read from the source data (Lange 1: 3–8,000 MW energy loss;
  Lange 2: 2–650 MW energy transfer duty). Below the range the correlation is extrapolated;
  above it the estimate is split into identical parallel units. A `UserWarning` is issued in both
  cases.
- Zero or negative `energyloss_MW` / `energytransfer_MW` now returns an error message.
- Documented the definitions of the energy loss and of the energy transfer duty, including the
  process segments covered by the Lange 2 correlation (code comments and README).

### capcomo() – Garrett model
- All 100 entries (a, n, lower and upper bounds) were checked against the source table
  (Towler and Sinnott, 2008, Table 6.2); they match.
- Below the lower bound of a correlation, the capacity is no longer clipped to the lower bound;
  the correlation is extrapolated and a `UserWarning` is issued. Example: a 1,000 kt/y methanol
  plant (2,740 t/d < 3,000 t/d) now gives 320.5 MM$ instead of 338.5 MM$.
- Above the upper bound, the plant is still estimated as identical parallel trains
  (ceil(S/S_upper)), and a `UserWarning` now reports the number of trains.
- The unit "Mgal/y" printed in Table 6.2 for ethanol by ethylene hydration is read as MMgal/y
  (documented in the code and the README).
- The README documents the densities, molar masses and operating days assumed for the unit
  conversions (they are not given in the source).
- All 100 processes of the library are now active. Capacities defined in t/d, bpd,
  MMgal/y and MMscf/y are converted from the production scale (t/y) with explicit unit-conversion
  functions and documented densities / molar masses. For refinery units whose capacity is defined
  on a feed basis, `scale_tpy` is interpreted as the feed rate.
- Fixed a corrupted character in the process name "Gasoline desulfurization (Prime-G+)".

### eqpcomo() – Turton model
- Blenders, centrifuges, conveyors, crystallizers, dust collectors, filters, screens and storage
  tanks have no material factors in Turton (Tables A.1 and A.7); the material now does not affect
  their cost (FM = 1). Previously all 32 sub-types of these equipment raised `KeyError`.
- Demister pads and Teflon-tube exchangers have no carbon-steel option; their material factors are
  now normalized by the reference material of the type (stainless steel for demister pads, Turton
  Table A.6; Teflon for Teflon-tube exchangers, Turton Table A.4). Previously they raised `KeyError`.
- An unknown equipment type now returns an error message instead of raising `KeyError`.
- Fans: the capacity is now converted from m3/h to m3/s (Table A.1; previously m3/h was used as
  m3/s), and the pressure factor uses the pressure rise across the fan in kPa (Table A.2 footnote;
  previously log10 of `P_bar`), limited to the correlation range (16 kPa centrifugal, 4 kPa axial).
- Mixers: sized by power (`power_kW`, Table A.1) instead of volume.
- Vessel pressure factor (Eq. A.2): FP is now at least 1, and 1.25 is used only below −0.5 barg
  (previously 1.25 for every P ≤ 0.5 and values below 1 at low pressure).
- Heaters: the steam-boiler pressure factor no longer overwrites the factor of diphenyl, molten-salt
  and hot-water heaters (Table A.2).
- Evaporator pressure factor: C2 corrected from −0.2292 to −0.2992 (Table A.2).
- Trays: `num` < 1 returns an error message instead of a cost of 0.
- Pressure factor: when `P_bar` was 0 or not given, every Turton equipment returned NaN because
  log10(0) was evaluated even where the pressure-factor coefficients are zero. FP is now 1 when all
  coefficients are zero or P ≤ 0; results for P > 0 are unchanged.

### eqpcomo() – Seider model
- Fans: the size factor is now ACFM = m3/h × 35.31 / 60 (previously × 60, 3,600 times too high);
  the head factor is 1.0 up to 4 in. H2O (Table 16.24; previously 1.15); the lower flow limits of
  Table 16.23 are applied.
- Centrifugal pumps: the size factor S = Q·H^0.5 now uses `pumphead_m` (previously `height_m`, so the
  head input had no effect); if `pumphead_m` is not given, the head is estimated from the brake power
  with Eqs. (16.16)–(16.17) and a warning is issued. The pump-type factor FT now takes the values of
  Table 16.20 (1.00–8.90), selecting the first pump type whose flow, head and motor-power limits
  cover the duty, instead of an unreferenced function of motor power (FT ≈ 0.2 at 1 hp, ≈ 6 at
  700 hp); duties beyond all pump types are split over identical pumps.
- Vacuum systems: size in ft3/min at suction (Table 16.32; previously ft3/h, about 60 times too high);
  the book example (272 ft3/min liquid-ring pump, about $47,000) is now reproduced.
- Continuous evaporative crystallizers: size in tons of crystals per day (Table 16.32; previously t/h).
- Corrected misspelled sub-type names "Centrelifugal backward-curved" (fans) and "Clarilelifier, steel"
  (solid–liquid separator) to "Centrifugal backward-curved" and "Clarifier, steel".
- Autoclave, liquid–liquid extractor (RDC) and batch evaporative crystallizer have no sub-types
  in Seider; `eqptype` is no longer required for them (previously they could not be calculated).
  The autoclave cost no longer multiplies a zero material factor, because the material is
  reflected in the material-specific correlations (Seider Table 16.32).
- Blower: the purchase cost was assigned to the wrong variable (`Cp` instead of `Cb`), which
  raised `UnboundLocalError`. Fixed; results agree with Seider Eqs. (16.32)–(16.33).
- Filters (plate-and-frame, pressure leaf, rotary pan): the power-law correlations were routed to
  the exponential form, which raised `UnboundLocalError`. Fixed; results agree with Seider
  Table 16.32.

### eqpcomo() – Peters model
- Heat exchanger (others): material factors are now looked up per equipment type (gasket plate,
  flat plate, air cooler), and the cost equations, which were only evaluated below the lower
  capacity limit because of an indentation error, are now evaluated for all capacities.
- An unknown equipment type now returns an error message instead of raising `KeyError`.
- Flat-plate heat exchanger: the quadratic correlation, which deviated from Peters Fig. 14-27 by
  −39% to +35% and decreased above about 1,000 m², replaced by the power-law fit
  Cp = 8,501 A^0.3605 (10–1,500 m², carbon steel; within 5% of the digitized figure).
- New equipment and sub-types digitized from Peters, Timmerhaus & West (5th ed., Jan. 2002 basis).
  Each curve was digitized at 300 dpi with axis calibration checked by overlay, and fitted as a
  power law or a log-polynomial (maximum deviation from the figure in brackets):
  - Heat exchanger (shell and tube): double pipe and multiple pipe (Figs. 14-15, 14-16; the tube
    material CS / Admiralty (Cu) / SS selects the curve; tabulated pressure factors; 3%),
    scraped wall and spiral tube (Fig. 14-26; tabulated material and pressure factors; 2–3.5%).
  - Heat exchanger (others): spiral plate (Fig. 14-27; 2%) and welded plate (Fig. 14-25; 2.5%).
  - Turbines: radial expander for gas and liquid service, available as "Radial expanders" or
    "Liquid expanders" (Fig. 12-34; 1%).
  - Evaporator: forced circulation, falling film, agitated film (scraped wall), horizontal tube and
    vertical tube, single effect (Fig. 14-33; material and pressure factors; 3.5%).
  - Vaporizer: jacketed vessel and jacketed vessel with internal coil (Fig. 14-32; material and
    pressure factors; 3%).
  - Furnace: reformer, pyrolysis and nonreactive (process-fired) box furnaces (Fig. 14-37; 2%).
  - Heater: cylindrical direct-fired heater; the tube material (CS / Cr-Mo / SS) selects the curve
    and carbon steel uses the 690 kPa curve up to 6.9 bar (Fig. 14-38; 2%).
  - Reactor: jacketed agitated; material and design pressure (345 / 2,070 / 10,350 kPa, glass-lined
    690 kPa) select the curve (Fig. 13-15; 1%). Autoclave: CS, SS and glass-lined (Fig. 13-16; 1%).
  - Fans: centrifugal radial, centrifugal backward-curved, vane-axial and tube-axial
    (Fig. 12-31; 4%). Blower: centrifugal, turbo (21 / 69 / 207 kPa maximum discharge, selected by
    the pressure rise), rotary and heavy-duty (Fig. 12-32; 3%, heavy-duty 5%).
  - Trays: sieve, valve, bubble cap (CS, SS) and stamped turbogrid (SS), cost per tray with the
    tabulated quantity factor (Fig. 15-13; 5%).
  - Packing: ring and saddle packings (Fig. 15-14 does not distinguish packing shapes); cost vs
    packed height for 0.3–4.0 m diameters, log-log interpolation between diameters; tabulated
    material factors (1.5%).
- New material names: "Cr-Mo steel", "Glass-lined steel", "SS clad", "Stainless steel(316)".
- Second digitization batch (data in `ecoana/peters_digitized.py`, Jan. 2002 basis, purchased cost;
  every curve checked by overlay; maximum deviation from the figure ≤ 4% unless noted):
  - Vacuum system: steam-jet ejectors, 1-, 2- and 4-stage (Fig. 12-33; air load in `massflow_kgph`;
    material factors). The axis of Fig. 12-33 reads "installed cost" while the caption reads
    "purchased cost"; the curves are for a steam use of 0.126 kg/s.
  - Agitator: propeller (open tank / closed vessel; material factors) and turbine, single and dual
    impeller (CS or 316 SS curves) (Fig. 12-42). Mixer: motionless (pipe diameter), propeller mixers
    (fixed/portable, gear/direct drive), double-cone and twin-shell tumblers, ribbon (working volume),
    sigma double-arm kneader, two-roll and muller (power) (Figs. 12-41, 12-43 to 12-47).
    Blender: ribbon and rotary (double cone) (Figs. 12-44, 12-45).
  - Size enlargement equipment: screw extruder, pug mill extruder, roll-type presses; Dewatering
    press: screw press (Fig. 12-49; solids rate in `massflow_kgph`).
  - Conveyor: belt, screw, apron, bucket elevator, pneumatic and vibrating (Figs. 12-60, 12-61,
    12-63, 12-64). The cost is given against conveying length (new argument `length_m`); the width
    or diameter (`diameter_m`) or, for pneumatic conveyors, the solids rate (`massflow_kgph`) is
    interpolated log-log between the plotted curves.
  - Size reduction equipment: ball mills, dry and wet, for six circuit/product-size combinations
    (Figs. 12-69, 12-70), pulverizer (CS / 316 SS), rolling grinder, rotary cutter and cage-type
    disintegrator (Figs. 12-73, 12-74).
  - Dryer: pan, rotary vacuum and vibratory-conveyor dryers (CS / 304 SS / 316 SS curves), Roto-Louvre
    and vacuum shelf dryers (Figs. 15-30, 15-32). Figures that give installed cost (tray dryers,
    drum and rotary dryers, spray dryers; Figs. 15-29, 15-33, 15-35) were not implemented.
  - Filters: tilting pan, table, continuous vacuum drum (stainless-steel base), vertical leaf, plate
    and frame and cartridge (Fig. 15-39, material factors); plate-and-frame filters of other materials
    from Fig. 15-40.
  - Screens: vibrating, single and double deck (Fig. 15-42; as printed, the single-deck label points
    to the more expensive curve).
  - Centrifuge: solid bowl, oscillating screen, pusher, scroll-conveyor and automatic batch
    (horizontal/vertical basket), sized by bowl or basket diameter (Figs. 15-43, 15-44, 15-46).
  - Dust collector: electrostatic precipitator, baghouse (continuous, intermittent cleaning, high
    temperature), cyclone, multiple cyclones (Fig. 15-48, material factors), venturi scrubber (high
    and low energy), centrifugal (cyclone) scrubber and gravity spray scrubber (Fig. 15-49).
- New material names: "Rubber-covered steel", "PVC-coated steel", "Wood".
- Remaining refits checked against the figures:
  - Floating-head exchangers: the quadratic correlation followed the highest-pressure curve and was then
    multiplied by a pressure factor (1.5–1.7 times the 1,035 kPa curve). Now the five design-pressure
    curves of Fig. 14-19 (690–6,895 kPa) are used directly, interpolated log-log in pressure.
  - Vertical vessels: Fig. 15-10 gives cost against shell weight with separate curves for carbon steel,
    304 SS and 316 SS; these curves are now used, and the pressure factor of Fig. 12-54 (which was
    applied on top, although the weight already reflects the pressure) was removed. Nickel alloys use the
    CS curve × 7.4 (Fig. 15-11).
  - Horizontal vessels: the pressure factor (Fig. 12-54) is 1.0 at atmospheric pressure and interpolated
    in the table (previously ≥ 1.23 even at 0 bar).
  - Centrifugal pumps: material factors (cast iron 1.0, cast steel 1.8, SS 2.4, Ni 5.0) and pressure
    factors from Fig. 12-23; previously unreferenced material factors and the reciprocating-pump pressure
    curve were used. Parallel units no longer make the cost drop at the capacity limit.
  - Reciprocating pumps: cast-iron, cast-steel and 316 SS curves and the pressure table of Fig. 12-21
    replace a single quadratic with material factors.
  - Field-erected tanks: the small-tank quadratic, 8–23% low at 2,000–3,000 m³, replaced by the CS,
    304 SS and 316 SS curves of Fig. 12-55; other alloys relative to 316 SS (Hastelloy 3.8 instead of an
    overall 6 relative to CS); large tanks use the Fig. 12-56 curve and factors (CS 1, 304 SS 2, 316 SS 3).
  - Heavy-duty blower: lower limit raised to 0.6 m³/s, where the fit has a shallow minimum.
  - Diameter-based curves (centrifuges, motionless mixers) are extrapolated beyond the curve instead of
    being split into parallel units of smaller diameter.
- Above the upper limit of a new curve, the equipment is represented as identical parallel units
  and a warning is issued; pressures above the highest tabulated pressure factor also issue a
  warning.

### eqpcomo() – Towler model
- Bubble-cap trays: `b-240` (no assignment) corrected to `b=240`; the cost was a constant 200 per tray.
- Ribbon mixer: the size limits were swapped (r_max = 5, r_min = 35 kW); corrected to 5–35 kW.
- Reversible hammer mill: the correlation is in t/h; the capacity is now converted from kg/h (previously
  kg/h was used directly, about 32 times too high).
- Trays: `num` is now a required input; `num` < 1 returns an error message.
- Checked against Towler & Sinnott (2008), Tables 6.5 and 6.6:
  - "Heat exchanger (others)" / flat plate is the plate-and-frame exchanger of Table 6.6 (type 304 SS,
    note 3). Its material factor was checked but never assigned (fm = 0), so the cost was 0; it is now
    applied (relative to 304 SS) and the type is available again.
  - Hastelloy C material factor corrected from 1.7 to 1.55 (Table 6.5).
  - Belt conveyor: sized by length (`length_m`, 10–500 m) instead of area; belt width via
    `diameter_m` (0.5–1.0 m, linear between the 0.5 m and 1.0 m correlations; 1.0 m if not given).
  - Furnaces: the box-furnace correlation (30–120 MW) is used above 60 MW, where it meets the
    cylindrical-furnace curve; previously large duties were split into 60 MW cylindrical units.
  - The size-reduction type "Ball mill" used the pulverizer correlation (kg/h, 200–4,000) and is
    renamed "Pulverizer".

### eqpcomo() – Smith model
- Pressure factor: with `P_bar` not given (default 0) the vacuum factor 2.0 was applied; Table 2.5 is
  in bar absolute, so P ≤ 0 is now treated as "not given" (fP = 1).
- Correlations whose base material is stainless steel (Table 2.1: pressure vessel, structured
  packing, dryer, small storage tank) are now normalized to carbon steel (÷2.1 for the pressure
  vessel, Table 2.3; ÷2.4 otherwise, Table 2.2). Storage tanks now apply the material factor
  (carbon steel if `material` is not given).
- Storage tanks below 0.1 m3 and steam boilers below 50,000 kg/h raised `UnboundLocalError`; they now
  use the small-tank correlation (evaluated at 0.1 m3) and the field-erected boiler correlation
  (10,000–800,000 kg/h, Table 2.1).
- Small centrifugal pumps (≤ 10 kW): the base cost refers to high-grade stainless steel; the
  material factor is now normalized by 3.4 (Smith Table 2.2) instead of 2.4.
- Material factor for Hastelloy C (equipment other than vessels and columns) corrected from 4.4
  to 3.6 (Smith Table 2.2).

### eqpcomo() – Guthrie model
Checked against Biegler, Grossmann & Westerberg (1997), Ch. 4 (Tables 4.2, 4.4–4.6, 4.8, 4.9, 4.11, 4.12):
- Pressure factors now use the "up to" step tables of the book instead of fitted curves (vessels
  Table 4.2, exchangers Table 4.4, furnaces Table 4.5, fired heaters Table 4.6). The exchanger fit was
  negative just above 150 psi (higher pressure gave a lower cost), and the vessel fit was up to 10% low.
- Pressures: the factor tables are in psig; `P_bar` (absolute) is converted to psig, and the design
  pressure P_rated = 1.5 P_actual (book p. 112–113) is used for vessels, exchangers, air coolers,
  furnaces and heaters (`DESIGN_PRESSURE_FACTOR` in the module).
- Pump operating factor Fo: steps 1.0/1.5/2.9 by maximum suction pressure (150/500/1000 psig) and
  temperature (250/550/850 °F), the more severe limit governing (Table 4.8); the fitted curve exceeded
  2.9 below 1000 psi and dropped back above it. Bronze added (`Copper(alloy)`, 1.28). `Pout_bar` is
  required.
- Exchanger materials: "CS shell/Mo(alloy) tube" was the book's CS/Monel column and is renamed
  "CS shell/Monel tube" (the old name is still accepted, also in the Seider, Smith and Towler models,
  where it had the same meaning); "Monel shell/Monel tube" added.
- Furnace and fired-heater materials: the 0.35/0.45 factors are for Cr-Mo tubes, not Monel/Ni/Inconel/
  Hastelloy; they are now listed as "Cr-Mo steel" only.
- Vessels: "SS clad" (2.25) added.
- Compressor drivers follow Table 4.9 (centrifugal: motor 1.00, turbine 1.15; reciprocating: steam
  turbine 1.07, motor 1.29, gas engine 1.82); combinations not in the table now return an error, and
  `material` is no longer required.
- Air coolers: S = calculated area/15.5 (Table 4.12) is restored (the divisor removed earlier in this
  release is the book's definition). The book gives no material or pressure factors for air coolers;
  Fm·(1 + Fp) with the exchanger pressure steps is kept as an assumption. The pressure adders are no
  longer multiplied with the base cost (previously about 10% of the base cost).
- Pumps: the duplicate "Hastelloy C" entry (2.89 overwritten by 3.48) was removed.
- Cost index basis changed from CE 113.7 to CE 115 (mid-1968, book p. 133).
- Output is the uninstalled cost BC × MPF (the book's bare-module factors are not applied).

### Documentation
- README: the `unit_num` input of the Hill, Timms and Petley models is described as the number of
  process units (called "functional units" in the original sources), consistent with the manuscript.
- README: corrected how to change `GBP_TO_USD_1992` (Timms model). `ecoana.capcomo` refers to the
  function, so the module is accessed with `importlib.import_module("ecoana.capcomo")`.

### Warnings
- Fixed `warn_LowPressure`, which referred to undefined variables.
