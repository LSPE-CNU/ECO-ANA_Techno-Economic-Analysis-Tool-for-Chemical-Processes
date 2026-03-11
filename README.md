**[ECO-ANA: Techno-Economic Analysis Tool for Chemical Processes]**
---
**SUMMARY**
---
<img width="4816" height="1256" alt="Frame 21 (1)" src="https://github.com/user-attachments/assets/49512815-1450-48d7-b29f-f2950aa8fdea" />

**ECO-ANA**(Process **Eco**nomic-**Ana**lyzer) is designed to support early-stage techno-economic analysis (TEA) of chemical processes accounting for cost estimation model uncertainty.  
This was developed by **LSPE**, the *Laboratory for Sustainable Process Engineering* from Chungnam national university.  
LSPE@CNU: https://sites.google.com/view/rohgroup

**MODULES**
---
1. `ecoana.eqpcomo`  
     `eqpcomo` is a Python module for chemical process equipment cost estimation.
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
  <br />
  
   - Function Interface  
     Main features:
     ```
     eqpcomo(model="model name", equipment="equipment name", eqptype="equipment type name", par_1=par_1_value, par_2=par_2_value,...)
     ```
     <br />
     Table of parameters to `eqpcomo` function:  
       
     | Parameter     | Description                                                                        |
     | ------------- | ---------------------------------------------------------------------------------- |
     | model         | Cost estimation model (`Turton`, `Seider`, `Smith`, `Towler`, `Peters`, `Guthrie`) |
     | equipment     | Equipment category                                                                 |
     | eqptype       | Equipment subtype                                                                  |
     | material      | Construction material                                                              |
     | T_K           | Operating temperature (K)                                                          |
     | P_bar         | Operating pressure (bar)                                                           |
     | vol_cum       | Volume (m³)                                                                        |
     | area_sqm      | Heat transfer area (m²)                                                            |
     | power_kW      | Equipment power (kW)                                                               |
     | massflow_kgph | Mass flow rate (kg/h)                                                              |
     | volflow_cumph | Volumetric flow rate (m³/h)                                                        |
     | diameter_m    | Diameter (m)                                                                       |
     | height_m      | Height (m)                                                                         |
     | thickness_m   | Wall thickness (m)                                                                 |
       
     
   - Input Validation and Error Messages  
     The required parameters for function can be differ depending on selected cost estimation model or equipment type.     
     Therefore, the `eqpcomo` includes built-in input validation and guidance through error messages.
       
     If required parameters are missing or invalid, the function returns a error message indicating:
     - which input parameter is missing  
     - whether the selected model or equipment type is unsupported  
     - the list of available options for the given model
     
     Example 1:
     If the essential parameters required for cost estimation is not input into the function,  
     ```
     eqpcomo(model="Turton", equipment="Vaporizer")
     ```  
     ```
     Error: Missing required input variables for the selected model and equipment. Missing variables: ['eqptype', 'vol_cum', 'P_bar', 'material']
     ```  
    
     Example 2:  
     If the model does not support the equipment cost estimation formula for the equipment specifiaction (e.g., material, equipment, eqptype) input by the user.
     ```
     eqpcomo(model="Turton", equipment="Membrane")
     ```  
     ```
     Error: The selected equipment 'Membrane' is not available in the equipment cost estimation model. Available equipment options: ['Blender', 'Centrifuge', 'Compressor', 'Conveyor', 'Crystallizer-batch evaporative', 'Dryer', 'Dust collector', 'Evaporator', 'Fans', 'Furnace', 'Filters', 'Mixer', 'Heater', 'Packing', 'Vessel/Tower', 'Pumps', 'Reactor', 'Storage tank', 'Screens', 'Trays', 'Turbines', 'Vaporizer', 'Heat exchanger (shell and tube)', 'Heat exchanger (others)']
     ```  
     
  
     

     
     Main function:
     The required parameters depend on the selected model and equipment type.
     
     
   - Basic Usage  
     Example: estimating the cost of a centrifugal compressor using the Smith model
     ```
     from eqpcomo import eqpcomo
     
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
     - Automatic Parameter Estimation
       Some parameters can be automatically estimated if not provided. These helper functions are implemented in the internal utility modules.

         - Vessel volume estimation from diameter and height
         - Vessel wall thickness estimation from pressure and temperature
         - Pump head estimation
       

**AUTHOR**
---
Haeun Choi  
E-mail: nolaaa@o.cnu.ac.kr

**ACKNOWLEDGEMENT**
---
This work is supported by the Development of next-generation biorefinery platform technologies for leading bio-based chemicals industry project (2022M3J5A1056072), by Development of platform technologies of microbial cell factories for the next-generation biorefineries project (2022M3J5A1056117), and by the Education and Research Center for Eco-Friendly Next-Generation Batteries (RS-2024-00447869) from National Research Foundation supported by the Korean Ministry of Science and ICT.

