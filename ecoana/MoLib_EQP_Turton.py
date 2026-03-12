# *******Turton model, (Richard A. Turton, 2018, “Analysis, Synthesis, and Design of Chemical processes”, 5th ed.)***************************
import numpy as np
from math import pi
import math


#============================Equipment cost estimation model parameters============================

# Base cost (Cp0) factors; k1, k2, k3 
# Cp0 is the purchased equipment cost at ambient operating pressure & temperature and using carbon steel construction
lst_Cp0_k={"Blender":{"Kneader":[5.0141 , 0.5867, 0.3224], 
                    "Ribbon":[ 4.1366, 0.5072, 0.0070],
                    "Rotary":[4.1366, 0.5072, 0.0070]},
        "Centrifuge":{"Auto batch separator (vertical)":[ 4.7681, 0.9740, 0.0240], 
                        "Auto batch separator (horizontal)":[4.7681, 0.9740, 0.0240], 
                        "Centrifugal separator":[4.3612 , 0.8764, -0.0049], 
                        "Oscillating screen":[ 4.8600 , 0.3340, 0.1063], 
                        "Solid bowl w/o motor":[ 4.9697, 1.1689, 0.0038]},
        "Compressor":{ "Centrifugal":[2.2897, 1.3604,-0.1027 ], 
                        "Axial":[2.2897, 1.3604,-0.1027], 
                        "Reciprocating":[2.2897, 1.3604,-0.1027], 
                        "Rotary":[5.0355, -1.8002, 0.8253]},
        "Conveyor":{"Apron":[3.9255, 0.5039, 0.1506], 
                    "Belt":[4.0637 , 0.2584, 0.1550], 
                    "Pneumatic":[ 4.6616, 0.3205, 0.0638], 
                    "Screw":[ 3.6062, 0.2659,0.1982]},
        "Crystallizer-batch evaporative":{"Batch":[ 4.5097, 0.1731, 0.1344]},
        "Dryer":{"Drum":[ 4.5472,0.2731 , 0.1340], 
                "Rotary(gas fired)":[ 3.5645, 1.1118, -0.0777 ], 
                "Tray":[3.6951, 0.5442, -0.1248]},
        "Dust collector":{"Baghouse":[4.5007 , 0.4182,0.0813 ], 
                        "Cyclone scrubbers":[3.6298 ,0.5009 , 0.0411], 
                        "Electrostatic precipitator":[3.6298 ,0.5009 , 0.0411],
                        "Venturi scrubber":[3.6298 ,0.5009 , 0.0411]},
        "Evaporator":{"Forced circulation(pumped)":[5.0238,0.3475 ,0.0703 ], 
                        "Short tube":[5.2366 ,-0.6572 , 0.35], 
                        "Long tube":[ 4.6420,0.3698 , 0.0025], 
                        "Falling film":[ 3.9119, 0.8627, -0.0088], 
                        "Agitated film(scraped wall)":[ 5,0.1490 ,-0.0134 ]},
        "Fans":{"Centrifugal straight-radial":[3.5391 ,-0.3533 , 0.4477] , 
                "Centrifugal backward-curved":[3.3471, -0.0734, 0.3090 ], 
                "Axial vane":[3.1761 , -0.1373, 0.3414], 
                "Axial tube":[3.0414 , -0.3375,0.4722]},
        "Furnace":{"Reformer furnace":[ 3.0680, 0.6597,0.0194 ] , 
                    "Pyrolysis furnace":[ 2.3859,0.9721 ,-0.0206 ], 
                    "Nonreactive furnace":[7.3488 , -1.1666, 0.2028]},
        "Filters":{ "Bent":[5.1055 ,0.4999 ,0.0001 ], 
                    "Cartridge":[3.2107 , 0.7597, 0.0027], 
                    "Disc and drum":[4.8123 , 0.2858,0.0420 ], 
                    "Gravity":[ 4.2756, 0.3520, 0.0714], 
                    "Leaf":[3.8187 , 0.6235, 0.0176], 
                    "Pan":[4.8123 ,0.2858 , 0.0420], 
                    "Plate and frame":[4.2756 ,0.3520 , 0.0714], 
                    "Table":[5.1055 ,0.4999 , 0.0001], 
                    "Tube":[5.1055 ,0.4999 , 0.0001]},
        "Mixer":{"Impeller":[ 3.8511, 0.7009, -0.0003] , 
                "Propeller":[ 4.3207,0.0359 , 0.1346], 
                "Turbine": [3.4092 , 0.4896, 0.0030]},
        "Heater":{"Diphenyl heater":[ 2.2628, 0.8581, 0.0003] , 
                "Molten salt heater":[ 1.1979, 1.4782, -0.0958], 
                "Hot water heater":[ 2.0829, 0.9074, -0.0243], 
                "Steam boiler": [ 6.9617, -1.4800,0.3161 ]},
        "Packing":{ "Berl saddles":[ 2.4493, 0.9744, 0.0055], 
                    "Raschig rings":[2.4493, 0.9744, 0.0055 ], 
                    "Intalox saddles":[2.4493, 0.9744, 0.0055 ], 
                    "Pall rings":[2.4493, 0.9744, 0.0055 ],
                    "Cascade mini-rings":[2.4493, 0.9744, 0.0055 ], 
                    "Tellerettes":[2.4493, 0.9744, 0.0055 ]},
        "Vessel/Tower":{"Horizontal vessel":[3.5565 ,0.3776 ,0.0905 ] , 
                        "Vertical vessel": [ 3.4974,0.4485 , 0.1074]},
        "Pumps":{"Reciprocating":[3.8696 ,0.3161 ,0.1220 ] , 
                "Positive displacement":[ 3.4771, 0.1350,0.1438 ], 
                "Centrifugal": [ 3.3892, 0.0536, 0.1538]},
        "Reactor":{ "Autoclave":[ 4.5587,0.2986 ,0.0020 ],
                    "Fermenter": [4.1052 ,0.5320 ,-0.0005 ] , 
                    "Inoculum tank":[ 3.7957, 0.4593, 0.0160],
                    "Jacketed agitated" :[ 4.1052, 0.5320, -0.0005],
                    "Jacked nonagitated":[ 3.3496, 0.7235, 0.0025] , 
                    "Mixer/settler": [ 4.7116,0.4479 ,0.0004 ]},
        "Storage tank":{ "Fixed roof":[ 4.8509, -0.3973, 0.1445],
                        "Floating roof":[ 5.9567, -0.7585, 0.1749] },
        "Screens":{"DSM":[3.8050 , 0.5856, 0.2120] , 
                    "Rotary":[ 4.0485,0.1118 ,0.3260 ],
                    "Stationary":[ 3.8219,1.0368 ,-0.6050 ],
                    "Vibrating":[ 4.0485, 0.1118, 0.3260] },
        "Trays":{ "Sieve":[2.9949 ,0.4465 ,0.3961 ], 
                "Valve":[ 3.3322,0.4838 , 0.3434 ], 
                "Demisters":[ 3.2353,0.4838 , 0.3434 ]},
        "Turbines":{ "Axial gas turbines":[ 2.7051, 1.4398, -0.1776], 
                    "Liquid expanders":[2.2476 , 1.4965, -0.1618 ]},
        "Vaporizer":{ "Internal coils/jackets":[4 ,0.4321 ,0.17 ],
                        "Jacketed vessels":[3.8751 , 0.3328, 0.1901] },
        
        "Heat exchanger (shell and tube)":
                {"Bayonet":[4.2768 ,-0.0495 ,0.1431  ], 
                "Double pipe":[3.3444 , 0.2745, -0.0472  ], 
                "Fixed tube":[4.3247 , -0.3030,0.1634  ], 
                "Floating head":[ 4.8306, -0.8509,0.3187   ], 
                "Kettle reboiler":[4.4646 ,-0.5277 , 0.3955 ], 
                "Multiple pipe":[2.7652 ,0.7282 , 0.0783], 
                "Scraped wall":[3.7803 , 0.8569,0.0349  ], 
                "Spiral tube (shell and tube)":[ 3.9912, 0.0668, 0.2430], 
                "Spiral tube (tube only)":[3.9912, 0.0668, 0.2430], 
                "U-tube (shell and tube)":[4.1884 ,-0.2503 , 0.1974], 
                "U-tube (tube only)":[4.1884 ,-0.2503 , 0.1974], 
                "Teflon tube":[3.8062 , 0.8924, -0.1671]},
        "Heat exchanger (others)":
                {"Flat plate":[ 4.6656,-0.1557 , 0.1547], 
                "Spiral plate":[4.6561 , -0.2947, 0.2207], 
                "Air cooler":[ 4.0336,0.2341 , 0.0497]},

        "Driver":{"Gas turbine":[-21.7702, 13.2175, -1.5279 ],
                "Intern comb.engine":[2.7635, 0.8574, -0.0098],
                "Steam turbine" :[2.6259, 1.4398, -0.1776],
                "Electric-explosion proof":[2.4604, 1.4191, -0.1798],
                "Electric-totally enclosed":[1.9560, 1.7142, -0.2282],
                "Electric-open/drip proof":[2.9508,1.0688, -0.1315]}
                                    }

# Baremodule factor: compressor - Centrifugal
Fbm_comp1={"Carbon steel":2.8,
           "Stainless steel":5.8,
           "Nickel(alloy)":11.45,
           "Monel":11.45,
           "Inconel":11.45,
           "Hastelloy C":11.45}
# Baremodule factor: compressor - Axial
Fbm_comp2={"Carbon steel":3.8,
           "Stainless steel":8,
           "Nickel(alloy)":15.9,
           "Monel":15.9,
           "Inconel":15.9,
           "Hastelloy C":15.9}
# Baremodule factor: compressor - Reciprocating
Fbm_comp3={"Carbon steel":3.4,
           "Stainless steel":7,
           "Nickel(alloy)":13.9,
           "Monel":13.9,
           "Inconel":13.9,
           "Hastelloy C":13.9}
# Baremodule factor: compressor - Rotary
Fbm_comp4={"Carbon steel":2.4,
           "Stainless steel":5,
           "Nickel(alloy)":9.9,
           "Monel":9.9,
           "Inconel":9.9,
           "Hastelloy C":9.9}
# Baremodule factor: Dryer - Drum
Fbm_dryer1={"Carbon steel":1.6}
# Baremodule factor: Dryer - Rotary(gas fired), Tray
Fbm_dryer2={"Carbon steel":1.25}
#Baremodule factor: Evaporator - ["Forced circulation(pumped)","Short tube","Long tube"]:
Fbm_eva1={"Carbon steel":2.9,
          "Copper(alloy)":3.6,
          "Stainless steel":5.1,
          "Nickel(alloy)":9.7,
          "Monel":9.7,
          "Inconel":9.7,
          "Hastelloy C":9.7,
          "Titanium(alloy)":14.5}
#Baremodule factor: Evaporator - ["Falling film","Agitated film(scraped wall)"]:
Fbm_eva2={"Carbon steel":2.3,
          "Copper(alloy)":2.8,
          "Stainless steel":3.9,
          "Nickel(alloy)":7.5,
          "Monel":7.5,
           "Inconel":7.5,
           "Hastelloy C":7.5,
          "Titanium(alloy)":11.3}
#Baremodule factor: fan
Fbm_fan={"Carbon steel":2.8,
         "Fiberglass":5,
         "Stainless steel":5.8,
         "Nickel(alloy)":11.5, 
         "Monel":11.5,
         "Inconel":11.5,
        "Hastelloy C":11.5}
#Baremodule factor: furnace
Fbm_furnace={"Carbon steel":2.1,"Stainless steel":2.8}
#Baremodule factor: heater
Fbm_heater={"Carbon steel":2.1,
            "Nickel(alloy)":2.5, 
            "Monel":2.5,
            "Inconel":2.5,
            "Hastelloy C":2.5,
            "Stainless steel":2.8}
#Baremodule factor: mixer
Fbm_mixer={"Carbon steel":1.38}
#Baremodule factor: packing
Fbm_packing={"Carbon steel":7.1,"Polyethylene":1,"Ceramic":4.1}
#Baremodule factor: (batch)reactor
Fbm_reactor={"Carbon steel":4}

#Baremodule factor: Trays-["Sieve", "Valve"]
Fbm_tray1={"Carbon steel":1,
          "Stainless steel":1.8,
          "Nickel(alloy)":5.6}
#Baremodule factor: Trays-Demisters
Fbm_tray2={"Stainless steel":1,
           "Fluorocarbon":1.8,
           "Nickel(alloy)":5.6}

#Baremodule factor: Vaporizer - Internal coils/jackets
Fbm_vap1={"Carbon steel":3,
          "Copper(alloy)":3.8,
          #"Glass lined/SS coils":5.1,
          #"Glass lined/Ni coils":5.5,
          "Stainless steel":5.1,
          #"SS clad":4.1,
          "Nickel(alloy)":10.1,
          "Monel":10.1,
          "Inconel":10.1,
          "Hastelloy C":10.1,
          #"Ni alloy clad":6.6,
          "Titanium(alloy)":15.2
          #"Ti clad":10.6
          }
#Baremodule factor: Vaporizer - Jacketed vessels
Fbm_vap2={"Carbon steel":2.7,
          "Copper(alloy)":3.4,
          #"Glass lined/SS coils":4.7,
          #"Glass lined/Ni coils":4.9,
          "Stainless steel":4.8,
          #"SS clad":3.8,
          "Nickel(alloy)":9.1,
          "Monel":9.1,
          "Inconel":9.1,
          "Hastelloy C":9.1,
          #"Ni alloy clad":5.9,
          "Titanium(alloy)":13.7
          #"Ti clad":9.6
          }
#Baremodule factor: turbine
Fbm_turbine={"Carbon steel":3.5,
             "Stainless steel":6.1,
             "Nickel(alloy)":11.7,
             "Monel":11.7,
             "Inconel":11.7,
             "Hastelloy C":11.7
             }

#Material factor: vessel
fm_vessel={"Carbon steel":1,
           #"SS clad":1.75,
           "Stainless steel":3.1,
           #"Ni alloy clad":3.6,
           "Nickel(alloy)":7.1,
           "Monel":7.1,
           "Inconel":7.1,
           "Hastelloy C":7.1,
           #"Ti clad":4.65,
           "Titanium(alloy)":9.4}
#Material factor: Pumps - Reciprocating
fm_pump1={"Cast iron":1,
          "Carbon steel":1.45,
          "Copper(alloy)":1.3,
          "Stainless steel":2.35,
          "Nickel(alloy)":4,
          "Monel":4,
           "Inconel":4,
           "Hastelloy C":4,
          "Titanium(alloy)":6.45}
#Material factor: Pumps-Positive displacement
fm_pump2={"Cast iron":1,
          "Carbon steel":1.4,
          "Copper(alloy)":1.3,
          "Stainless steel":2.65,
          "Nickel(alloy)":4.75,
          "Monel":4.75,
           "Inconel":4.75,
           "Hastelloy C":4.75,
          "Titanium(alloy)":10.65}
#Material factor: Pumps-Centrifugal
fm_pump3={"Cast iron":1,
          "Carbon steel":1.55,
          "Stainless steel":2.25,
          "Nickel(alloy)":4.4,
          "Monel":4.4,
          "Inconel":4.4,
          "Hastelloy C":4.4
          }

#Material factor: HEX(shell&tube)
fm_HEX1={"CS shell/CS tube":1,
         "CS shell/Cu tube":1.4,
         "Cu shell/Cu tube":1.7,
         "CS shell/SS tube":1.8,
         "SS shell/SS tube":2.75,
         "CS shell/Ni(alloy) tube":2.65,
         "Ni(alloy) shell/Ni(alloy) tube":3.7,
         "CS shell/Ti(alloy) tube":4.6,
         "Ti(alloy) shell/Ti(alloy) tube":11.4}

#Material factor: HEX(tube only)
fm_HEX2={"Teflon tube":1}

#Material factor: HEX(others) - Air cooler
fm_HEX3={"Carbon steel":1,
         "Aluminum(alloy)":1.4,
         "Stainless steel":2.9}
#Material factor: HEX(others) - "Flat plate","Spiral plate"
fm_HEX4={"Carbon steel":1,
         "Aluminum(alloy)":1.4,
         "Copper(alloy)":1.35,
         "Stainless steel":2.45,
         "Nickel(alloy)":2.7,
         "Monel":2.7,
         "Inconel":2.7,
         "Hastelloy C":2.7,
         "Titanium(alloy)":4.6}


#==================================Material parameters mapping==================================
lst_MaterialFm={"Compressor":{"Centrifugal":Fbm_comp1, 
                        "Axial":Fbm_comp2, 
                        "Reciprocating":Fbm_comp3, 
                        "Rotary":Fbm_comp4},

                "Dryer":{"Drum":Fbm_dryer1, 
                        "Rotary(gas fired)":Fbm_dryer2, 
                        "Tray":Fbm_dryer2},

                "Evaporator":{"Forced circulation(pumped)":Fbm_eva1, 
                                "Short tube":Fbm_eva1, 
                                "Long tube":Fbm_eva1, 
                                "Falling film":Fbm_eva2, 
                                "Agitated film(scraped wall)":Fbm_eva2},

                "Fans":{"Centrifugal straight-radial":Fbm_fan, 
                        "Centrifugal backward-curved":Fbm_fan, 
                        "Axial vane":Fbm_fan, 
                        "Axial tube":Fbm_fan},

                "Furnace":{"Reformer furnace":Fbm_furnace, 
                        "Pyrolysis furnace":Fbm_furnace, 
                        "Nonreactive furnace":Fbm_furnace},

                "Mixer":{"Impeller": Fbm_mixer, 
                        "Propeller":Fbm_mixer, 
                        "Turbine": Fbm_mixer},

                "Heater":{"Diphenyl heater": Fbm_heater, 
                        "Molten salt heater":Fbm_heater, 
                        "Hot water heater":Fbm_heater, 
                        "Steam boiler":Fbm_heater },

                "Packing":{ "Berl saddles":Fbm_packing, 
                        "Raschig rings":Fbm_packing, 
                        "Intalox saddles":Fbm_packing, 
                        "Pall rings":Fbm_packing,
                        "Cascade mini-rings":Fbm_packing, 
                        "Tellerettes":Fbm_packing},

                "Reactor":{ "Autoclave":Fbm_reactor,
                        "Fermenter":Fbm_reactor, 
                        "Inoculum tank":Fbm_reactor,
                        "Jacketed agitated" :Fbm_reactor,
                        "Jacked nonagitated":Fbm_reactor, 
                        "Mixer/settler":Fbm_reactor},

                "Trays":{"Sieve":Fbm_tray1, 
                        "Valve":Fbm_tray1, 
                        "Demisters":Fbm_tray2},

                "Turbines":{ "Axial gas turbines":Fbm_turbine, 
                        "Liquid expanders":Fbm_turbine},

                "Vaporizer":{ "Internal coils/jackets":Fbm_vap1,
                                "Jacketed vessels":Fbm_vap2 },

                "Vessel/Tower":{"Horizontal vessel":fm_vessel, 
                                "Vertical vessel":fm_vessel},

                "Pumps":{"Reciprocating": fm_pump1, 
                        "Positive displacement":fm_pump2, 
                        "Centrifugal":fm_pump3},
                
                "Heat exchanger (shell and tube)":{"Bayonet":fm_HEX1, 
                                                "Double pipe":fm_HEX1, 
                                                "Fixed tube":fm_HEX1, 
                                                "Floating head":fm_HEX1, 
                                                "Kettle reboiler":fm_HEX1, 
                                                "Multiple pipe":fm_HEX1, 
                                                "Scraped wall":fm_HEX1, 
                                                "Spiral tube (shell and tube)":fm_HEX1, 
                                                "Spiral tube (tube only)":fm_HEX1, 
                                                "U-tube (shell and tube)":fm_HEX1, 
                                                "U-tube (tube only)":fm_HEX1, 
                                                "Teflon tube":fm_HEX2},
                "Heat exchanger (others)":{"Flat plate":fm_HEX4, 
                                        "Spiral plate":fm_HEX4, 
                                        "Air cooler":fm_HEX3}
                                        }

def eqpcomo_Turton(equipment,material,eqptype,pressure,Pout,volume,power,volflow,massflow,area,packsize,height,diameter,thick,temperature,num,drive):
        Cp_0=0
        fp=1
        fm=0
        fq=1
        c1=0
        c2=0
        c3=0
        # Model range; equipment capacity boundary definition [Equipment:[Eqp type:[capacity variable, min.value, max. value]]]
        lst_CapaBound={
                "Blender":{"Kneader":[volume, 0.14, 3], 
                        "Ribbon":[volume, 0.7, 11],
                        "Rotary":[volume, 0.7, 11]},

                "Centrifuge":{"Auto batch separator (vertical)":[diameter, 0.5, 1.7], 
                                "Auto batch separator (horizontal)":[diameter, 0.5, 1.7], 
                                "Centrifugal separator":[diameter, 0.5, 1.7], 
                                "Oscillating screen":[diameter, 0.5, 1.7], 
                                "Solid bowl w/o motor":[diameter, 0.3, 2]},

                "Compressor":{ "Centrifugal":[power, 450, 3000 ], 
                                "Axial":[power, 450, 3000], 
                                "Reciprocating":[power, 450, 3000], 
                                "Rotary":[power, 18, 950]},

                "Conveyor":{"Apron":[area, 1, 15], 
                        "Belt":[area, 0.5, 325], 
                        "Pneumatic":[area, 0.75, 65], 
                        "Screw":[area, 1.5, 30]},

                "Crystallizer-batch evaporative":{"Batch":[volume, 1.5, 30]},

                "Dryer":{"Drum":[area, 0.5, 50], 
                        "Rotary(gas fired)":[area, 5, 100], 
                        "Tray":[area, 1.8, 20]},

                "Dust collector":{"Baghouse":[volume, 0.08, 350], 
                                "Cyclone scrubbers":[volume, 0.06, 200], 
                                "Electrostatic precipitator":[volume, 0.06, 200],
                                "Venturi scrubber":[volume, 0.06, 200]},

                "Evaporator":{"Forced circulation(pumped)":[area, 5, 1000], 
                                "Short tube":[area, 10, 100], 
                                "Long tube":[area, 100, 10000], 
                                "Falling film":[area, 50, 500], 
                                "Agitated film(scraped wall)":[area, 0.5, 5]},

                "Fans":{"Centrifugal straight-radial":[volflow, 1, 100] , 
                        "Centrifugal backward-curved":[volflow, 1, 100], 
                        "Axial vane":[volflow, 1, 100], 
                        "Axial tube":[volflow, 1, 100]},

                "Furnace":{"Reformer furnace":[power, 3000, 100000] , 
                        "Pyrolysis furnace":[power, 3000, 100000 ], 
                        "Nonreactive furnace":[power, 1000, 100000]},

                "Filters":{ "Bent":[area,0.9,115 ], 
                        "Cartridge":[area, 15, 200], 
                        "Disc and drum":[ area, 0.9, 300], 
                        "Gravity":[area, 0.5, 80], 
                        "Leaf":[area, 0.6, 235], 
                        "Pan":[area, 0.9, 300], 
                        "Plate and frame":[area, 0.5, 80], 
                        "Table":[area, 0.9, 115], 
                        "Tube":[area, 0.9, 115]},

                "Mixer":{"Impeller":[volume,5,150 ] , 
                        "Propeller":[volume,5,500 ], 
                        "Turbine": [volume, 5, 150]},

                "Heater":{"Diphenyl heater":[power, 650, 10750] , 
                        "Molten salt heater":[power,650,10750 ], 
                        "Hot water heater":[power,650,10750], 
                        "Steam boiler": [power,1200,9400]},

                "Packing":{ "Berl saddles":[volume,0.03, 628], 
                        "Raschig rings":[volume,0.03, 628], 
                        "Intalox saddles":[ volume,0.03, 628], 
                        "Pall rings":[volume,0.03, 628 ],
                        "Cascade mini-rings":[volume,0.03, 628], 
                        "Tellerettes":[volume,0.03, 628]},

                "Vessel/Tower":{"Horizontal vessel":[volume,0.1,628] , 
                                "Vertical vessel": [volume,0.3,520 ]},

                "Pumps":{"Reciprocating":[power, 0.1, 200] , 
                        "Positive displacement":[power, 1, 100], 
                        "Centrifugal": [power,1, 300]},

                "Reactor":{ "Autoclave":[volume,1,15 ],
                        "Fermenter": [volume,0.1,35 ] , 
                        "Inoculum tank":[volume,0.07,1 ],
                        "Jacketed agitated" :[volume,0.1,35],
                        "Jacked nonagitated":[volume,5,45] , 
                        "Mixer/settler": [volume,0.04,60 ]},

                "Storage tank":{"Fixed roof":[volume, 90,30000 ],
                                "Floating roof":[volume, 1000, 40000 ] },

                "Screens":{"DSM":[area, 0.3, 6] , 
                        "Rotary":[area, 0.3, 15 ],
                        "Stationary":[area, 2, 11],
                        "Vibrating":[area, 0.3, 15 ] },

                "Trays":{"Sieve":[area, 0.07, 12.3], 
                        "Valve":[area, 0.7, 10.5], 
                        "Demisters":[area, 0.7, 10.5]},

                "Turbines":{ "Axial gas turbines":[abs(power),100, 4000], 
                        "Liquid expanders":[abs(power),100,1500 ]},

                "Vaporizer":{ "Internal coils/jackets":[volume, 1, 100],
                                "Jacketed vessels":[volume, 1, 100] },
                
                "Heat exchanger (shell and tube)":{"Bayonet":[area, 10, 1000], 
                                                "Double pipe":[area,1 , 10 ], 
                                                "Fixed tube":[area, 10,  1000], 
                                                "Floating head":[area, 10, 1000 ], 
                                                "Kettle reboiler":[area, 10, 100], 
                                                "Multiple pipe":[area, 10, 100], 
                                                "Scraped wall":[area, 2, 20], 
                                                "Spiral tube (shell and tube)":[area, 1, 100], 
                                                "Spiral tube (tube only)":[area, 1, 100], 
                                                "U-tube (shell and tube)":[area, 10, 1000], 
                                                "U-tube (tube only)":[area, 10, 1000], 
                                                "Teflon tube":[area, 1, 10]},

                "Heat exchanger (others)":{"Flat plate":[area,10,1000 ], 
                                        "Spiral plate":[area,1,100], 
                                        "Air cooler":[area,10,10000]},

                "Driver":{"Gas turbine":[power, 7500,23000],
                        "Intern comb.engine":[power, 10, 10000],
                        "Steam turbine" :[power, 70, 7500],
                        "Electric-explosion proof":[power, 75, 2600],
                        "Electric-totally enclosed":[power, 75, 2600],
                        "Electric-open/drip proof":[power, 75, 2600]}
                                        }
        
        capacity=lst_CapaBound[equipment][eqptype][0]
        r_min=lst_CapaBound[equipment][eqptype][1]
        r_max=lst_CapaBound[equipment][eqptype][2]
        eqp_list=lst_Cp0_k.keys()
        eqp_type_list=lst_Cp0_k[equipment].keys()
        mat_list=lst_MaterialFm[equipment][eqptype].keys()
        driver_list=lst_Cp0_k["Driver"].keys()
        
        # Error message: Not available equipment spec. for model supporting list
        if eqptype not in lst_Cp0_k[equipment]:
                return(f"Error: The selected equipment type '{eqptype}' is not available for '{equipment}' in the cost estimation model. Available types for {equipment}: {eqp_type_list}")
        if material not in lst_MaterialFm[equipment][eqptype]:
                return(f"Error: The selected equipment material '{material}' is not available for '{equipment}, {eqptype}' in the cost estimation model. Available materials: {mat_list}")
        
        k1=lst_Cp0_k[equipment][eqptype][0]
        k2=lst_Cp0_k[equipment][eqptype][1]
        k3=lst_Cp0_k[equipment][eqptype][2]

        if capacity<r_min:
                capacity=r_min
        eqnum=math.ceil(capacity/r_max)
        capa_input=capacity/eqnum
        
        # c1, c2, c3: Pressure factor model parameters
        if equipment=="Evaporator":
                if pressure<=10:
                        c1=0
                        c2=0
                        c3=0
                elif 10<pressure:
                        c1=0.1578
                        c2=-0.2292
                        c3=0.1413

        elif equipment=="Fans":
                if abs(pressure-Pout)<=0.01:
                        c1=0
                        c2=0
                        c3=0
                elif 0.01<abs(pressure-Pout) and eqptype in["Centrifugal straight-radial","Centrifugal backward-curved"] :
                        c1=0
                        c2=0.20899
                        c3=-0.0328
                elif 0.01 < abs(pressure-Pout) and eqptype in["Axial vane" ,"Axial tube"]:
                        c1=0
                        c2=0.20899
                        c3=-0.0328
      
        elif equipment=="Furnace":
                if eqptype=="Reformer furnace":
                        c1=0.1405
                        c2=-0.2698
                        c3=0.1293
                elif eqptype=="Pyrolysis furnace":
                        c1=0.1017
                        c2=-0.1957
                        c3=0.09403
                elif eqptype=="Nonreactive furnace":
                        c1=0.1347
                        c2=-0.2368
                        c3=0.1021
                if pressure<=10:
                        c1=0
                        c2=0
                        c3=0

        elif equipment=="Heater":
                if pressure<=2:
                        c1=0
                        c2=0
                        c3=0
                elif 2<=pressure:
                        c1=-0.01633
                        c2=0.056875
                        c3=-0.00876   
                #elif 200<pressure:
                #return("Out of range - pressure")
                #if 40<pressure:
                        #return("Out of range - pressure")
                if pressure<20:
                        c1=0
                        c2=0
                        c3=0
                elif 20<=pressure:
                        c1=2.594072
                        c2=-4.23476
                        c3=1.722404

        elif equipment=="Packing":
                c1=0
                c2=0
                c3=0

        elif equipment=="Pumps":
                if eqptype=="Reciprocating":
                        if pressure<10:
                                c1=0
                                c2=0
                                c3=0
                        elif 10<=pressure:
                                c1=-0.245382
                                c2=0.259016
                                c3=-0.01363        
                elif eqptype=="Positive displacement":
                        if pressure<10:
                                c1=0
                                c2=0
                                c3=0
                        elif 10<=pressure:
                                c1=-0.245382
                                c2=0.259016
                                c3=-0.01363      
                elif eqptype=="Centrifugal":
                        if pressure<10:
                                c1=0
                                c2=0
                                c3=0
                        elif 10<=pressure:
                                c1=-0.3935
                                c2=0.3957
                                c3=-0.00226

        elif equipment=="Storage tank":
                if eqptype=="Fixed roof":
                        c1=0
                        c2=0
                        c3=0

                elif eqptype=="Floating roof":
                        c1=0
                        c2=0
                        c3=0

        elif equipment=="Vaporizer":
                #if 320<pressure:
                        #return("Out of range - pressure")   
                if pressure<5:
                        c1=0
                        c2=0
                        c3=0
                elif 5<=pressure:
                        c1=-0.16742
                        c2=0.13428
                        c3=0.15058           

        elif equipment in["Heat exchanger (shell and tube)","Heat exchanger (others)"]:
                if eqptype=="Scraped wall":
                        if pressure<=40:
                                c1=0
                                c2=0
                                c3=0
                        elif 40<pressure<=100:
                                c1=0.6072
                                c2=-0.9120
                                c3=0.3327
                        elif 100<pressure: #<=300:
                                c1=13.1467
                                c2=-12.6574
                                c3=3.0705                
                elif eqptype=="Teflon tube":
                        #if pressure<=15:
                        c1=0
                        c2=0
                        c3=0
                if eqptype in["Floating head","Bayonet","Fixed tube","Kettle reboiler","U-tube (shell and tube)"]:
                        if 5<=pressure: #<=140:
                                c1=0.03881
                                c2=-0.11272
                                c3=0.08183
                        elif pressure<5:
                                c1=0
                                c2=0
                                c3=0
                
                if eqptype in["Double pipe","Multiple pipe"]:
                        if pressure<40:
                                c1=0
                                c2=0
                                c3=0
                        elif 40<=pressure<100:
                                c1=0.6072
                                c2=-0.9120
                                c3=0.3327    
                        elif 100<=pressure: #<=300:
                                c1=13.1467
                                c2=-12.6574
                                c3=3.0705
                
                if eqptype in["Flat plate","Spiral plate"]: #and pressure<=19:
                        c1=0
                        c2=0
                        c3=0    
                if eqptype=="Air cooler":
                        if pressure<10:
                                c1=0
                                c2=0
                                c3=0
                        elif 10<=pressure: #<=100:
                                c1=-0.1250
                                c2=0.15361
                                c3=-0.02861 
                        
                if eqptype=="Spiral tube (shell and tube)":
                        if pressure<150:
                                c1=0
                                c2=0
                                c3=0
                        elif 150<=pressure: #<=400: 
                                c1=-0.4045
                                c2=0.1859
                                c3=0
                
                if eqptype=="Spiral tube (tube only)":
                        if pressure<150:
                                c1=0
                                c2=0
                                c3=0
                        elif 150<=pressure: #<=400:
                                c1=-0.2115
                                c2=0.09717
                                c3=0      
                
        # 1. Calculate equipment base cost (Cp0)==============================================================
        if equipment =="Compressor":
                if drive not in lst_Cp0_k["Driver"]:
                        return(f"Error: The selected driver type '{drive}' is not available in this model. Available driver types: {driver_list}")
                else:
                        Cp0_comp=10**(k1+k2*np.log10(capa_input)+k3*((np.log10(capa_input))**2))*eqnum
                        k1_driver=lst_Cp0_k["Driver"][drive][0]
                        k2_driver=lst_Cp0_k["Driver"][drive][1]
                        k3_driver=lst_Cp0_k["Driver"][drive][2]
                        Cp0_driver=10**(k1_driver+k2_driver*np.log10(capa_input)+k3_driver*((np.log10(capa_input))**2))*eqnum
                        Cp_0=Cp0_comp+Cp0_driver
        else:
                Cp_0=10**(k1+k2*np.log10(capa_input)+k3*((np.log10(capa_input))**2))*eqnum

        # 2. Calculate pressure factor (fp)
        if equipment=="Vessel/Tower":
                fp=((pressure)*diameter /(2*(850-0.6*(pressure))) +0.00315)/0.0063
                if pressure<=0.5:
                        fp=1.25    
        else:
                fp=10**(c1+c2*np.log10(pressure)+c3*((np.log10(pressure))**2))    

        # 3. Mapping material factor (fm)
        if equipment =="Heat exchanger (shell and tube)":
                fm=lst_MaterialFm[equipment][eqptype][material]/lst_MaterialFm[equipment][eqptype]["CS shell/CS tube"]
        else:
                fm=lst_MaterialFm[equipment][eqptype][material]/lst_MaterialFm[equipment][eqptype]["Carbon steel"]

        # 4. Mapping quantity factor (fq) (only for trays)
        if equipment=="Trays":
                if num<20:
                        fq=10**(0.4771+0.08516*np.log10(num)-0.3473*((np.log10(num))**2))
                elif num>=20:
                        fq=1   
        if equipment not in ["Trays"]:
                num=1
                
        return round(Cp_0*fp*fm*fq*num,1) if Cp_0 > 10 else "Error: No data"







