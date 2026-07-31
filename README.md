**[ECO-ANA: Techno-Economic Analysis Tool for Chemical Processes]**
---
**SUMMARY**
---
<img width="4816" height="1256" alt="Frame 21 (1)" src="https://github.com/user-attachments/assets/49512815-1450-48d7-b29f-f2950aa8fdea" />

**ECO-ANA**(Process **Eco**nomic-**Ana**lyzer) is designed to support early-stage techno-economic analysis (TEA) of chemical processes accounting for cost estimation model uncertainty.  
This was developed by **LSPE**, the *Laboratory for Sustainable Process Engineering* from Chungnam national university.  
LSPE@CNU: https://sites.google.com/view/rohgroup

**INSTALLATION**
---
Install the package from PyPI:
```
pip install ecoana
```

**MODULES**
---
1. `ecoana.eqpcomo()`  
     `eqpcomo()` is a Python module for chemical process equipment cost estimation.
     This module provides a unified interface to estimate equipment purchase costs using several well-known correlations from chemical engineering literature.
     Each model contains equipment-specific correlations, capacity ranges, and material factors based on the original literature sources.  
       
     The library currently implements equipment cost estimation models from:  
     > *Turton model*: Richard A. Turton (2018), “Analysis, Synthesis, and Design of Chemical processes” (5th ed.)  
     > *Seider model*: Warren D. Seider (2016), “Product and Process Design Principles: Synthesis, Analysis and Evaluation” (4th ed.)  
     > *Smith model*: Robin Smith (2016), “Chemical Process Design and Integration” (2nd ed.)  
     > *Peters model*: Max. S. Peters (2003), “Plant Design and Economics for Chemical Engineers” (5th ed.)  
     > *Towler model*: Gavin Towler (2007), “Chemical Engineering Design –Principles, Practice and Economics of plant” (1st ed.)  
     > *Guthrie model*: L. T. Biegler (1997) "Systematic Methods of Chemical Process Design" (1st ed.)
 <br />
 
   - Function Interface    <br />
     Main features:
     ```
     eqpcomo(model="model name", equipment="equipment name", eqptype="equipment type name", par_1=par_1_value, par_2=par_2_value,...)
     ```
     <br />
     Table of parameters to `eqpcomo()` function:
     
     | Parameter     | Description                                                                        |
     | ------------- | ---------------------------------------------------------------------------------- |
     | model         | Cost estimation model (`Turton`, `Seider`, `Smith`, `Towler`, `Peters`, `Guthrie`) |
     | equipment     | Equipment name                                                                     |
     | eqptype       | Equipment type                                                                     |
     | material      | Construction material                                                              |
     | T_K           | Design temperature (K)                                                             |
     | P_bar         | Design pressure (bar)                                                              |
     | vol_cum       | Volume (m³)                                                                        |
     | area_sqm      | Heat transfer area (m²)                                                            |
     | power_kW      | Equipment power (kW)                                                               |
     | massflow_kgph | Mass flow rate (kg/h)                                                              |
     | volflow_cumph | Volumetric flow rate (m³/h)                                                        |
     | diameter_m    | Diameter (m)                                                                       |
     | height_m      | Height (m)                                                                         |
     | thickness_m   | Wall thickness (m)                                                                 |
        <br />
        
 - Basic Usage <br />
     Example: Estimating the cost of a centrifugal compressor using the Smith model.
     ```
     from ecoana import eqpcomo
     
     cost = eqpcomo(
          model="Smith",
          equipment="Compressor",
          eqptype="Centrifugal",
          T_K=400,
          P_bar=10,
          material='Carbon steel',
          power_kW=1000
     )
     print(cost)
     ```
     Output: The `eqpcomo()` returns a tuple containing two values.
     ```
     (212390.5, '2000 year basis')
     ```
     Each equipment cost estimation models are based on correlations derived from price data for different years.  <br />
   Therefore, the function returns the basis year together with the cost estimate so that users can adjust the cost using an appropriate **Capital Cost Index (e.g., CEPCI)** if needed.  <br />
   <br />
   
 - Error Messages   <br />
     The required parameters for function can be differ depending on selected cost estimation model or equipment type.   <br />    
     Therefore, the `eqpcomo()` includes built-in input validation and guidance through error messages.  <br />
       <br /> 
     If required parameters are missing or invalid, the function returns a error message indicating:  <br />
     - which input parameter is missing  
     - whether the selected model or equipment type is unsupported  
     - the list of available options for the given model
      <br />
     Example 1: <br />
     If the essential parameters required for cost estimation is not input into the function,
     
     ```
     eqpcomo(model="Turton", equipment="Vaporizer")
     ```  
     ```
     Error: Missing required input variables for the selected model and equipment. Missing variables: ['eqptype', 'vol_cum', 'P_bar', 'material']
     ```
     
     <br />
     Example 2:   <br />
     If the model does not support the equipment cost estimation formula for the equipment specifiaction (e.g., material, equipment, eqptype) input by the user.
   
     ```
     eqpcomo(model="Turton", equipment="Membrane")
     ```  
     ```
     Error: The selected equipment 'Membrane' is not available in the equipment cost estimation model. Available equipment options: ['Blender', 'Centrifuge', 'Compressor', 'Conveyor', 'Crystallizer-batch evaporative', 'Dryer', 'Dust collector', 'Evaporator', 'Fans', 'Furnace', 'Filters', 'Mixer', 'Heater', 'Packing', 'Vessel/Tower', 'Pumps', 'Reactor', 'Storage tank', 'Screens', 'Trays', 'Turbines', 'Vaporizer', 'Heat exchanger (shell and tube)', 'Heat exchanger (others)']
     ```
     <br />
- Automatic Parameter Estimation  <br />
The `eqpcomo()` can automatically estimate some parameters when they are not explicitly provided, as long as enough related equipment data is available.<br />

| Estimated parameter | Description           | Required input parameters for estimation     | Applied condition                                                  |
| ------------------- | --------------------- | -------------------------------------------- | ------------------------------------------------------------------ |
| `vol_cum`           | Vessel volume         | `diameter_m`, `height_m`                     | When `equipment="Vessel/Tower"` and `vol_cum` is not provided      |
| `thickness_m`       | Vessel wall thickness | `diameter_m`, `P_bar`, `T_K`, `material`     | When `equipment="Vessel/Tower"` and `thickness_m` is not provided  |
| `pumphead_m`        | Pump head             | `power_kW`, `volflow_cumph`, `massflow_kgph` | Available through helper logic when pump head needs to be inferred |

<br />

2. `ecoana.capcomo()`  
     `capcomo()` is a Python module for project-level (plant-wide) capital cost estimation.
     Rather than summing up individual equipment costs, it provides capacity-based ("economy-of-scale") correlations that estimate an overall capital cost figure directly from the plant/process production capacity, so it is useful for very early (order-of-magnitude) cost screening before a full equipment list is available.
     Each model returns a capital cost defined at a specific project stage (e.g., installed equipment cost, inside battery limits, fixed capital investment, or total capital investment) — see the table below for the cost type and basis year returned by each model.  
       
     The library currently implements the following capacity-based capital cost estimation models:  
     > *Hill* (1956) — Installed total equipment cost, from number of processing units and plant capacity.  
     > *Guthrie* (conceptual estimate, 1970) — Fixed capital investment, from process-specific cost/capacity/scaling data for 18 predefined bulk chemical processes.  
     > *Timms* (1980) — Total capital investment, from number of units, capacity, and design temperature/pressure.  
     > *Garrett* (1989) — Inside battery limits, from process-specific correlations for a large set of predefined petrochemical processes.  
     > *Petley* (1997) — Inside battery limits, from number of units, capacity, and design temperature/pressure.  
     > *Lange 1 / Lange 2* (2001) — Total capital investment, from process energy-loss / energy-transfer duty (for utility-type processes such as refrigeration or heat recovery).  
     >
     > *Please add the full literature reference for each of the above models here, in the same citation style as the `eqpcomo()` models above.*
 <br />

   - Function Interface    <br />
     Main features:
     ```
     capcomo(model="model name", process="process name", scale_tpy=scale_tpy_value, unit_num=unit_num_value, Tmax_K=Tmax_K_value, Pmax_bar=Pmax_bar_value, energytransfer_MW=energytransfer_MW_value, energyloss_MW=energyloss_MW_value)
     ```
     <br />
     Table of parameters to `capcomo()` function:

     | Parameter          | Description                                       | Required by                                   |
     | ------------------ | -------------------------------------------------- | ---------------------------------------------- |
     | model               | Capital cost estimation model (`Hill`, `Guthrie`, `Timms`, `Garrett`, `Petley`, `Lange 1`, `Lange 2`) | all |
     | process             | Predefined process/product name (see source code for the full list) | `Guthrie`, `Garrett` |
     | scale_tpy           | Plant/production capacity (ton/year)               | `Hill`, `Guthrie`, `Timms`, `Garrett`, `Petley` |
     | unit_num            | Number of parallel processing units/trains         | `Hill`, `Timms`, `Petley`                      |
     | Tmax_K              | Maximum design temperature (K)                     | `Timms`, `Petley`                              |
     | Pmax_bar            | Maximum design pressure (bar)                      | `Timms`, `Petley`                              |
     | energyloss_MW       | Energy loss duty (MW)                              | `Lange 1`                                      |
     | energytransfer_MW   | Energy transfer duty (MW)                          | `Lange 2`                                      |
        <br />
     For the `Guthrie` model, `process` must be one of the following 18 predefined bulk chemicals: `Acetic acid`, `Acetone`, `Ammonia`, `Ammonium nitrate`, `Butanol`, `Chlorine`, `Ethylene`, `Ethylene oxide`, `Formaldehyde`, `Glycol`, `Hydrofluoric acid`, `Methanol`, `Nitric acid`, `Phosphoric acid`, `Polyethylene`, `Propylene`, `Sulfuric acid`, `Urea`.
        <br />

 - Basic Usage <br />
     Example: Estimating the fixed capital investment of a methanol plant using the Guthrie model.
     ```
     from ecoana import capcomo
     
     cost = capcomo(
          model="Guthrie",
          process="Methanol",
          scale_tpy=500000
     )
     print(cost)
     ```
     Output: The `capcomo()` returns a tuple containing three values — the estimated cost, the cost basis year, and the capital cost type that the selected model estimates.
     ```
     (56396953.9, '2000 year basis', 'Fixed capital investment')
     ```
     As with `eqpcomo()`, users should adjust the returned cost to the desired basis year using an appropriate **Capital Cost Index (e.g., CEPCI)** if needed.  <br />
   <br />
   
 - Error Messages   <br />
     Like `eqpcomo()`, `capcomo()` validates the required inputs for the selected model and returns a descriptive error message when required parameters are missing or an unsupported model/process is selected.  <br />
       <br /> 
     Example: <br />
     If the essential parameters required for cost estimation are not passed to the function,
     
     ```
     capcomo(model="Guthrie", process="Methanol")
     ```  
     ```
     Error: The 'scale_tpy' must be defined for capital cost estimation (Guthrie model).
     ```
     <br />

- Known limitation  <br />
The `Garrett` model is included in the source code but is currently not functional (an internal issue in how the process lookup table is accessed causes it to fail); this is planned to be fixed in an upcoming release. All other models (`Hill`, `Guthrie`, `Timms`, `Petley`, `Lange 1`, `Lange 2`) have been verified to work as documented above.

<br />

3. `ecoana.capconv()`  
     `capconv()` is a Python module that converts a known capital cost from one capital-cost category to another (for example, from purchased equipment cost to total capital investment), using a factor-based (Lang-factor style) method.
     This is useful when a cost is known at one project stage but a different stage is needed for the techno-economic analysis.  
       
     The library currently implements the factor method of:  
     > *Peters and Timmerhaus* — capital cost factors classified by process type (`Fluid`, `Solids-fluid`, `Solid`).  
     >
     > *Please add the full literature reference for this model here, in the same citation style as the `eqpcomo()` models above.*
 <br />

   - Function Interface    <br />
     Main features:
     ```
     capconv(model="model name", phase_processing="process type", cap_in="known cost category", cap_out="target cost category", base_cost=base_cost_value, rate_WC=0.15)
     ```
     <br />
     Table of parameters to `capconv()` function:

     | Parameter          | Description                                                                                   |
     | ------------------ | ----------------------------------------------------------------------------------------------- |
     | model               | Capital cost conversion model (currently only `Peters and Timmerhaus`)                          |
     | phase_processing    | Process type used by the `Peters and Timmerhaus` model (`Fluid`, `Solids-fluid`, `Solid`)        |
     | cap_in              | Capital cost category of `base_cost` (see table below)                                          |
     | cap_out             | Capital cost category to convert to (see table below)                                           |
     | base_cost           | Known cost value, in the `cap_in` category                                                      |
     | rate_WC             | Working capital as a fraction of fixed capital investment, used when converting to/from total capital investment (default: `0.15`) |
        <br />
     `cap_in` / `cap_out` accept the following capital cost categories. Using the short code (e.g., `tci`) is recommended for reliable matching:

     | Capital cost category       | Short code | Also accepted                                                              |
     | ---------------------------- | ---------- | --------------------------------------------------------------------------- |
     | Equipment cost                | `tpec`     | `equipment cost`, `total equipment cost`, `total equipment purchase cost`, `equipment`, `total equipment` |
     | Installed equipment cost      | `tiec`     | `installed equipment cost`, `total installed equipment cost`, `total installed equipment`, `installed equipment` |
     | Inside battery limits          | `isbl`     | `inside battery limits`, `inside battery limits cost`                       |
     | Fixed capital investment       | `fci`      | `fixed capital`, `fixed capital investment`, `fixed capital cost`           |
     | Total capital investment       | `tci`      | `total capital`, `total capital cost`                                       |
        <br />

 - Basic Usage <br />
     Example: Converting an equipment cost of $1,000,000 to total capital investment for a fluid-processing plant.
     ```
     from ecoana import capconv
     
     cost = capconv(
          model="Peters and Timmerhaus",
          phase_processing="Fluid",
          cap_in="tpec",
          cap_out="tci",
          base_cost=1000000
     )
     print(cost)
     ```
     Output: The `capconv()` returns a single converted cost value (float), on the same basis/currency as `base_cost`.
     ```
     5554500.0
     ```
     <br />

 - Error Messages   <br />
     `capconv()` validates the required inputs and returns a descriptive error message when required parameters are missing or an unsupported model, phase, or cost category is selected.  <br />
       <br /> 
     Example: <br />
     If the process type is not passed to the function,
     
     ```
     capconv(model="Peters and Timmerhaus", cap_in="tpec", cap_out="tci", base_cost=1000000)
     ```  
     ```
     Error: The 'phase_processing' must be defined for plant capital estimation (Peters and Timmerhaus model).
     ```
     <br />



<br />

**AUTHOR**
---
Haeun Choi  
E-mail: nolaaa@o.cnu.ac.kr

**ACKNOWLEDGEMENT**
---
This work is supported by the Development of next-generation biorefinery platform technologies for leading bio-based chemicals industry project (2022M3J5A1056072), by Development of platform technologies of microbial cell factories for the next-generation biorefineries project (2022M3J5A1056117), and by the Education and Research Center for Eco-Friendly Next-Generation Batteries (RS-2024-00447869) from National Research Foundation supported by the Korean Ministry of Science and ICT.

