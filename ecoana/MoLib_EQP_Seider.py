# *******Seider model, (Warren D. Seider, 2016, “Product and Process Design Principles: Synthesis, Analysis and Evaluation”, 4th ed.)***************************
import numpy as np
from math import pi
import math
from unit_parameters import *
from numpy import log as ln

# Material density (density unit=kg/m3) ==========================================================
dictMatDensity={
     "Carbon steel":7810,
     "Stainless steel":7930,
     "Titanium(alloy)": 4507,
     "Monel":8800,
     "Inconel":8442.4,
     "Nickel(alloy)":8900,
     #"Ni alloy clad":8900,
     #"Ti clad":4507,
     #"SS clad":7930
     }  
# Base cost for packing (Cpk) [eqptype:[Material:[packing size:Cpk]]]=============================
dictCpkPacking={
    "Berl saddles":{
          "Ceramic":{1: 38, 1.5:29, 2:22} 
          },
     "Raschig rings":{
         "Carbon steel":{1:43, 1.5:32, 2:27, 3:21},
          "Stainless steel":{1:142, 1.5:110, 2:87,3:50},
          "Ceramic":{1:21, 1.5:17, 2:15, 3:12}
          },
     "Intalox saddles":{
          "Ceramic":{1:27, 1.5:22, 2:19, 3: 15 },
          "Polyethylene(plastic)":{1:29, 2:18, 3:9 }
          },
     "Pall rings":{
          "Carbon steel":{1:39, 1.5:29, 2:25},
          "Stainless steel":{1:133, 1.5:102, 2:87},
          "Polyethylene(plastic)":{1:29, 1.5:21, 2:17, 3:13 }
          },
     "Cascade mini-rings":{
         "Stainless steel":{1:106, 1.5:75, 2:55, 3:41 },
          "Ceramic":{1:71, 2:55, 3: 44},
          "Polyethylene(plastic)":{1:71, 2:55, 3: 44}
          },
     "Tellerettes":{"Polyethylene(plastic)":{1:60}}
     }

# Material factor (fm)==============================================================================
dictBaseFMaterial = {
     "Carbon steel": 1,
     "Aluminum(alloy)": 1.5,
     "Stainless steel": 2,
     "Copper(alloy)": 1.2,
     "Nickel(alloy)": 2.5,
     "Monel": 2.7,
     "Titanium(alloy)": 6
     #"Titanium(alloy)-clad": 3
     }
dictPumpFMaterial = {
     "Cast iron": 1,
     "Carbon steel": 1.35,
     "Stainless steel": 2,
     "Copper(alloy)": 1.9,
     "Nickel(alloy)": 3.5,
     "Monel": 3.3,
     "Titanium(alloy)": 9.7
     }
dict_HeaterBoxMaterial={
     "Carbon steel":1,
     "Stainless steel":1.7,
     "Hastelloy C":1.4,
     "Monel":1.4,
     "Inconel":1.4
     }
dictFmBlower={
    "Carbon steel":1, 
    "Stainless steel":2.5, 
    "Nickel(alloy)":5, 
    "Monel":5,
    "Inconel":5,
    "Hastelloy C":5,
    "Fiberglass":1.8
    }
dictFmComp={
    "Carbon steel":1, 
    "Stainless steel":2.5, 
    "Nickel(alloy)":5,
    "Monel":5,
    "Inconel":5,
    "Hastelloy C":5
    }
dictFmFan={
    "Carbon steel":1,
    "Stainless steel":2.5,
    "Nickel(alloy)":5,
    "Monel":5,
    "Inconel":5,
    "Hastelloy C":5,
    "Fiberglass":1.8
    }
dictFmaHEX={
     "CS shell/CS tube":0,
     "CS shell/SS tube":1.75,
     "CS shell/Mo(alloy) tube":2.1, 
     "CS shell/Ti(alloy) tube":5.2,
     "SS shell/SS tube":2.7, 
     "Ti(alloy) shell/Ti(alloy) tube":9.6
     }
dictFmbHEX={
     "CS shell/CS tube":0, 
     "CS shell/SS tube":0.13,
     "CS shell/Mo(alloy) tube":0.13, 
     "CS shell/Ti(alloy) tube":0.16,
     "SS shell/SS tube":0.07, 
     "Ti(alloy) shell/Ti(alloy) tube":0.06
     }
dictFmVessel={
    "Carbon steel":1, 
    "Stainless steel":1.7 ,
    "Titanium(alloy)":7.7
    }

# Driver factor for compressor(fd)==============================================================================
dictFdComp={
    "Gas turbine":1.25,
    "Steam turbine":1.15, 
    "Electric-explosion proof":1, 
    "Electric-totally enclosed":1, 
    "Electric-open/drip proof":1
    }
# Motor factor for pump (f_motor))==============================================================================
dictPumpMotorType={
     "Electric-open/drip proof":1, 
     "Electric-explosion proof":1.8, 
     "Electric-totally enclosed":1.4 
     }

# Equipment list that base material is carbon steel
lstCarbon = [
     "Agitator",
     "Crystallizer-continuous evaporative",
     "Dust collector",
     "Evaporator",
     "Furnace",
     "Liquid-liquid extractor",
     "Mixer",
     "Storage tank",
     "Turbines",
     "Size enlargement equipment"]

# Equipment list that base material is stainless steel
lstStain = [
     "Centrifuge",
     "Crystallizer-batch evaporative",
     "Crystallizer-cooling",
     "Dewatering press",
     "Dryer"
     ]

# Equipment list that using not common fm dictionary
lstSpecMaterial = [
     "Adsorbent",
     "Autoclave",
     "Blower",
     "Compressor",
     "Fans",
     "Filters",
     "Heat exchanger (others)",
     "Heat exchanger (shell and tube)",
     "Heater",
     "Membrane (for reverse osmosis)",
     "Membrane",
     "Packing",
     "Size reduction equipment",
     "Solid-liquid separator",
     "Trays",
     "Vacuum system",
     "Vessel/Tower",
     "Pumps"
]

# Equipment list that not requiring eqp type variable
lst_nontypeEq=["Liquid-liquid extractor",
               "Crystallizer-batch evaporative",
               "Autoclave"]

# Available equipment & type list for this model
dict_AllEqpType={"Pumps":["Centrifugal"],
               "Agitator":["Propeller, open tank","Propeller, closed vessel","Turbine, open tank","Turbine, closed vessel"],
               "Crystallizer-continuous evaporative":["Forced circulation", "Draft-tube baffed"],
               "Dust collector":["Baghouse", "Cyclone scrubbers", "Electrostatic precipitator", "Venturi scrubber"],
               "Evaporator": ["Short tube", "Long tube","Forced circulation(pumped)", "Falling film"], 
               "Furnace":["Reformer furnace", "Pyrolysis furnace", "Nonreactive furnace"],
               "Mixer": ["Kneader (tilting double arm)", "Kneader(sigma double arm)", "Muller", "Ribbon", "Tumblers, double cone", "Tumblers, twin shell"],
               "Storage tank":["Open", "Cone roof","Floating roof", "Spherical", "Gas holder"],
               "Turbines":["Axial gas turbines", "Liquid expanders"],
               "Centrifuge":["Auto batch separator (vertical)","Auto batch separator (horizontal)","Batch top-drive basket","Batch bottom-drive basket"],
               "Crystallizer-cooling":["Jacketed scraped wall"],
               "Dewatering press":["Screw press","Roll press"],
               "Dryer":["Drum", "Rotary(gas fired)", "Rotary(steam tube)", "Tray", "Spray"],
               "Adsorbent":["Activated alumina", "Activated carbon","Silica gel", "Molecular sieves"],
               "Blower":["Centrifugal(turbo)", "Rotary straight-lobo"],
               "Compressor":["Centrifugal","Reciprocating","Screw"],
               "Fans":["Centrifugal straight-radial","Centrelifugal backward-curved","Axial vane","Axial tube" ],
               "Filters":["Plate and frame","Leaf","Disc and drum","Pan"],
               "Heat exchanger (others)":["Flat plate","Spiral plate","Air cooler"],
               "Heat exchanger (shell and tube)":["Floating head","Fixed tube","U-tube (shell and tube)","Kettle reboiler"],
               "Heater":["Hot water heater","Molten salt heater","Diphenyl heater","Steam boiler"],
               "Membrane (for reverse osmosis)":["For seawater", "For brackish water"],
               "Membrane":["Gas permeation", "Pervaporation", "Ultrafiltration"],
               "Packing": ["Berl saddles", "Raschig rings", "Intalox saddles", "Pall rings", "Cascade mini-rings", "Tellerettes"],
               "Size enlargement equipment":["Disk agglomerator","Drum agglomerator","Pellet mill","Pug mill extruder","Screw extruder", "Roll-type presses", "Tableting presses"],
               "Size reduction equipment":["Gyratory crusher","Jaw crusher","Cone crusher","Hammer mill","Ball mill","Jet mill" ],
               "Solid-liquid separator":["Thickener, steel","Thickener, concrete","Clarilelifier, steel","Clarifier, concrete"],
               "Trays":["Sieve", "Valve", "Bubble cap"],
               "Vacuum system":["Liquid-ring pumps", "Three-stage lobe","Three-stage claw","Screw compressor" ],
               "Vessel/Tower":["Horizontal vessel", "Vertical vessel"]
               }

def eqpcomo_Seider(equipment,material,eqptype,pressure, Pout,volume,power,volflow,massflow,area,packsize,height,diameter,thick,temperature,num,drive, pumphead):
     capacity=1
     r_max=1
     r_min=1
     eqp_list=dict_AllEqpType.keys()
     eqp_type_list=dict_AllEqpType[equipment]

     # Error message: Not available equipment spec. for model supporting list    
     if eqptype not in eqp_type_list:
          return(print(f"Error: The selected equipment type '{eqptype}' is not available for '{equipment}' in the cost estimation model. Available types for '{equipment}': {eqp_type_list}"))
     if equipment in (lstCarbon+lstStain) and material not in dictBaseFMaterial:
          return(print(f"Error: The selected equipment material '{material}' is not available for '{equipment}, {eqptype}' in the cost estimation model. Available materials: {list(dictBaseFMaterial.keys())}"))
     if equipment in lstCarbon:
          f_material=dictBaseFMaterial[material]
     elif equipment in lstStain:
          f_material=dictBaseFMaterial[material]/2
     elif equipment in lstSpecMaterial:
          f_material=0
     
     if equipment =="Pumps" and eqptype=="Centrifugal":
          if material not in dictPumpFMaterial:
               return(print(f"Error: The selected equipment material '{material}' is not available for '{equipment}, {eqptype}' in the cost estimation model. Available materials: {list(dictPumpFMaterial.keys())}"))
          else:
               f_material = dictPumpFMaterial[material]
          if drive not in dictPumpMotorType:
               return(print(f"Error: The selected driver type '{drive}' is not available in this model. Available driver types: {list(dictPumpMotorType.keys())}"))
          else:
               f_motor=dictPumpMotorType[drive]
     
          # volflow default unit=m3/h
          volflow=volflow*unit_gal/60   #volflow unit= gal/min
          pumphead=height*unit_ft       #pumphead unit=ft
          capacity=volflow*(pumphead**0.5)
          capa_max=100000
          capa_min=400
          eqnum_pump=math.ceil(capacity/capa_max)
          
          # pump drive cost
          power=power*unit_hph
          motor_eff=0.8+0.0319*math.log(power)-0.00182*(math.log(power)**2)
          Pc=power/motor_eff
          Pc_min=1
          Pc_max=1500
          eqnum_motor=math.ceil(Pc/Pc_max)

          if eqnum_pump<eqnum_motor:
               eqnum=eqnum_motor
          else:
               eqnum=eqnum_pump

          if capacity<=capa_min:
               capacity=capa_min
          if Pc<=Pc_min:
               Pc=Pc_min
          capa_input=capacity/eqnum

          Pc_input=Pc/eqnum
          Cb_motor=np.exp(5.4866+0.13141*math.log(Pc_input) + 0.053255*(math.log(Pc_input)**2) + 0.028628*(math.log(Pc_input)**3) - 0.0035549* math.log(Pc_input)**4)*eqnum
          Cb_pump=np.exp(9.2951 - 0.6019*math.log(capa_input) + 0.0519* math.log(capa_input)**2)*eqnum
          Ft=-3e-6*Pc_input**2 + 0.0108*Pc_input + 0.1891
          Cp=(Cb_pump*f_material*Ft+Cb_motor*f_motor)       # Equipment purcahse cost

     elif equipment == "Agitator":
          power=power*unit_hph
          capacity=power 
          if eqptype=="Propeller, open tank":
               a=1810
               b=0.34
               r_max=8
               r_min=1
          elif eqptype=="Propeller, closed vessel":
               a=2600
               b=0.17
               r_max=8
               r_min=1                   
          elif eqptype=="Turbine, open tank":
               a=2590
               b=0.54
               r_max=60
               r_min=2
          elif eqptype=="Turbine, closed vessel":
               a=2850
               b=0.57
               r_max=60
               r_min=2
          num_f=math.ceil(capacity/r_max)
          if capacity<=r_min:
               capacity=r_min
          else:
               capacity=capacity/num_f
          Cb=(a*capacity**b)*num_f
          Cp=Cb*f_material

     elif equipment == "Crystallizer-continuous evaporative":
          flow=massflow*unit_ton  #unit: ton/h
          capacity=flow
          if eqptype=="Forced circulation":
               a=27500
               b=0.56
               r_max=1000
               r_min=10  
          elif eqptype=="Draft-tube baffed":
               a=22200
               b=0.63
               r_max=250
               r_min=10   
          num_f=math.ceil(capacity/r_max)
          if capacity<=r_min:
               capacity=r_min
          else:
               capacity=capacity/num_f
          Cb=(a*capacity**b)*num_f
          Cp=Cb*f_material
     elif equipment == "Dust collector":
          flow=volflow*unit_ft3/60        #unit: ft3/min
          capacity=flow
          if eqptype=="Baghouse":
               a=10.020
               b=- 0.4381
               c=0.05563
               r_max=2000000
               r_min=5000   
          elif eqptype=="Cyclone scrubbers":
               a=8.9845 
               b=- 0.7892
               c=0.08487
               r_max=100000
               r_min=200                    
          elif eqptype=="Electrostatic precipitator":
               a=11.442
               b=- 0.5300
               c=0.05454
               r_max=2000000
               r_min=10000                    
          elif eqptype=="Venturi scrubber":
               a=9.3773
               b=- 0.3281
               c=0.0500
               r_max=20000
               r_min=2000   

          num_f=math.ceil(capacity/r_max)
          if capacity<=r_min:
               capacity=r_min
          else:
               capacity=capacity/num_f
          Cb=np.exp(a+b*ln(capacity)+c*(ln(capacity))**2)*num_f
          Cp=Cb*f_material

     elif equipment == "Evaporator":
          area=area*unit_ft2
          capacity=area
          if eqptype=="Short tube":
               a=3200
               b=0.53
               r_max=8000
               r_min=100
          elif eqptype=="Long tube":
               a=4500
               b=0.55
               r_max=8000
               r_min=100
          elif eqptype=="Forced circulation(pumped)":
               a=8.0604
               b=0.5329
               c=- 0.000196
               r_max=8000
               r_min=150
          elif eqptype=="Falling film":
               a=10800
               b=0.55
               r_max=4000
               r_min=150
          num_f=math.ceil(capacity/r_max)
          if capacity<=r_min:
               capacity=r_min
          else:
               capacity=capacity/num_f
          if eqptype in ["Short tube","Long tube","Falling film"]:
               Cb=(a*capacity**b)*num_f
          elif eqptype in ["Forced circulation(pumped)"]:
               Cb=np.exp(a+b*ln(capacity)+c*(ln(capacity))**2)*num_f
          Cp=Cb*f_material

     elif equipment =="Furnace":
          power=power*unit_btu
          capacity=power
          if eqptype=="Reformer furnace":
               a=0.677
               b=0.81
               r_max=500*10**6
               r_min=10*10**6
          elif eqptype=="Pyrolysis furnace":
               a=0.512
               b=0.81
               r_max=500*10**6
               r_min=10*10**6
          elif eqptype=="Nonreactive furnace":
               pressure=pressure*unit_psi
               r_max=500000000
               r_min=10000000
               Fp=0.986- 0.0035*(pressure/500) + 0.0175*(pressure/500)**2
               fm=dict_HeaterBoxMaterial[material]
          num_f=math.ceil(capacity/r_max)
          if capacity<=r_min:
               capacity=r_min
          else:
               capacity=capacity/num_f
          if eqptype in ["Reformer furnace", "Pyrolysis furnace"]:
               Cb=(a*capacity**b)*num_f
               Cp=Cb*f_material
          elif eqptype in ["Nonreactive furnace"]:
               Cb=np.exp(0.08505 + 0.766*ln(capacity))*num_f
               Cp=Cp=Cb*Fp*fm

     elif equipment == "Liquid-liquid extractor":
          height=height*unit_ft
          diameter=diameter*unit_ft
          S=height*diameter**1.5
          capacity=S
          a=250
          b=0.84
          r_max=2000
          r_min=3
          num_f=math.ceil(capacity/r_max)
          if capacity<=r_min:
               capacity=r_min
          else:
               capacity=capacity/num_f
          Cb=(a*capacity**b)*num_f
          Cp=Cb*f_material

     elif equipment == "Mixer":
          volume=volume*unit_ft3
          capacity=volume
          if eqptype=="Kneader (tilting double arm)":
               a=1400
               b=0.58
               r_max=56
               r_min=10
          elif eqptype=="Kneader(sigma double arm)":
               a=1300
               b=0.60
               r_max=380
               r_min=20
          elif eqptype=="Muller":
               a=11000
               b=0.56
               r_max=380
               r_min=10
          elif eqptype=="Ribbon":
               a=1700
               b=0.60
               r_max=320
               r_min=25
          elif eqptype=="Tumblers, double cone":
               a=2700
               b=0.42
               r_max=270
               r_min=50
          elif eqptype=="Tumblers, twin shell":
               a=1200
               b=0.60
               r_max=330
               r_min=35
          num_f=math.ceil(capacity/r_max)
          if capacity<=r_min:
               capacity=r_min
          else:
               capacity=capacity/num_f
          Cb=(a*capacity**b)*num_f
          Cp=Cb*f_material
          
     elif equipment == "Storage tank":
          volume=volume*unit_ft3
          #1ft3=7.48 gal
          gal=7.480519*volume
          pressure=pressure*unit_psi
          capacity=gal
          if eqptype=="Open":
               a=14
               b=0.72
               r_max=30000
               r_min=1000
          elif eqptype=="Cone roof":
               a=210
               b=0.51
               r_max=1000000
               r_min=10000
          elif eqptype=="Floating roof":
               a=375
               b=0.51
               r_max=1000000
               r_min=30000
          elif eqptype=="Spherical"and pressure<=30:
               a=47
               b=0.72
               r_max=1000000
               r_min=10000
          elif eqptype=="Spherical"and 30<pressure: #<=200:
               a=37
               b=0.78
               r_max=750000
               r_min=10000
          #elif eqptype =="Spherical" and 200<pressure:
               #return("Out of range - pressure")
          elif eqptype=="Gas holder" :
               capacity=volume
               a=2500
               b=0.43
               r_max=400000
               r_min=4000
          num_f=math.ceil(capacity/r_max)
          if capacity<=r_min:
               capacity=r_min
          else:
               capacity=capacity/num_f
          Cb=(a*capacity**b)*num_f
          Cp=Cb*f_material       

     elif equipment == "Turbines":
          power=power*unit_hph
          capacity=abs(power)
          if eqptype=="Axial gas turbines":
               a=420
               b=0.81
               r_max=5000
               r_min=20
          elif eqptype=="Liquid expanders":
               a=1100
               b=0.70
               r_max=2000
               r_min=150
          num_f=math.ceil(capacity/r_max)
          if capacity<=r_min:
               capacity=r_min
          else:
               capacity=capacity/num_f
          Cb=(a*capacity**b)*num_f
          Cp=Cb*f_material

     elif equipment == "Centrifuge":
          diameter=diameter*unit_in
          if eqptype=="Auto batch separator (vertical)" and 20<=diameter<=70:
               Cb=4300*diameter**0.94
          elif eqptype=="Auto batch separator (horizontal)" and 20<=diameter<=43:
               Cb=1700*diameter**1.11
          elif eqptype=="Batch top-drive basket" and 20<=diameter<=43:
               Cb=1600*diameter**0.95
          elif eqptype=="Batch bottom-drive basket" and 20<=diameter<=43:
               Cb=680*diameter
          else:
               return(print("Error: Out of capacity range - diameter"))
          Cp=Cb*f_material

     elif equipment == "Crystallizer-batch evaporative":
          volume=volume*unit_ft3
          capacity=volume
          a=32200
          b=0.41
          r_max=1000
          r_min=50
          num_f=math.ceil(capacity/r_max)
          if capacity<=r_min:
               capacity=r_min
          else:
               capacity=capacity/num_f
          Cb=(a*capacity**b)*num_f
          Cp=Cb*f_material

     elif equipment == "Crystallizer-cooling":
          height=height*unit_ft
          capacity=height
          if eqptype=="Jacketed scraped wall":
               a=11400
               b=0.67
               r_max=200
               r_min=15
          num_f=math.ceil(capacity/r_max)
          if capacity<=r_min:
               capacity=r_min
          else:
               capacity=capacity/num_f
          Cb=(a*capacity**b)*num_f
          Cp=Cb*f_material

     elif equipment == "Dewatering press":
          flow=massflow*unit_lb
          capacity=flow
          if eqptype=="Screw press":
               a=10.7951
               b=- 0.3580
               c=0.05853
               r_max=12000
               r_min=150
          elif eqptype=="Roll press":
               a=10.6167
               b=- 0.4467
               c=0.06136
               r_max=12000
               r_min=150
          num_f=math.ceil(capacity/r_max)
          if capacity<=r_min:
               capacity=r_min
          else:
               capacity=capacity/num_f
          Cb=np.exp(a+b*ln(capacity)+c*(ln(capacity))**2)*num_f
          Cp=Cb*f_material

     elif equipment == "Dryer":
          area=area*unit_ft2
          flow=massflow*unit_lb
          if eqptype=="Drum":
               capacity=area
               a=25000
               b=0.38
               r_max=480
               r_min=60
          elif eqptype=="Rotary(gas fired)":
               capacity=area
               a= 10.158
               b= 0.1003
               c=0.04303
               r_max=2000
               r_min=200
          elif eqptype=="Rotary(steam tube)":
               capacity=area
               a=1200
               b=0.92
               r_max=1400
               r_min=100
          elif eqptype=="Tray":
               capacity=area
               a=3500
               b=0.38
               r_max=200
               r_min=20
          elif eqptype=="Spray":
               capacity=flow
               a=8.0556
               b=0.8526
               c=- 0.0229
               r_max=3000
               r_min=30
          num_f=math.ceil(capacity/r_max)
          if capacity<=r_min:
               capacity=r_min
          else:
               capacity=capacity/num_f
          if eqptype in ["Rotary(gas fired)","Spray"]:
               Cb=np.exp(a+b*ln(capacity)+c*(ln(capacity))**2)*num_f
          elif eqptype in ["Drum","Rotary(steam tube)","Tray"]:
               Cb=(a*capacity**b)*num_f
          Cp=Cb*f_material

     elif equipment == "Adsorbent":
          volume=volume*unit_ft3
          if eqptype=="Activated alumina":
               Cp=35*volume
          elif eqptype=="Activated carbon":
               Cp=25*volume
          elif eqptype=="Silica gel":
               Cp=90*volume
          elif eqptype=="Molecular sieves":
               Cp=60*volume

     elif equipment == "Autoclave":
          pressure=pressure*unit_psi
          volume=volume*unit_gal
          capacity=volume
          if material not in["Carbon steel","Stainless steel","Glass-lined"]:
               return(print(f"Error: The selected equipment material '{material}' is not available for '{equipment}, {eqptype}' in the cost estimation model. Available materials: ['Carbon steel','Stainless steel','Glass-lined']"))
          elif material=="Carbon steel":# and pressure<=300:
               a=825
               b=0.52
               r_max=8000
               r_min=30
          elif material=="Stainless steel":# and pressure<=300:
               a=1560
               b=0.58
               r_max=2000
               r_min=30
          elif material=="Glass-lined":#  and pressure<=100:   
               a=1450
               b=0.54
               r_max=4000
               r_min=30
          
          num_f=math.ceil(capacity/r_max)
          if capacity<=r_min:
               capacity=r_min
          else:
               capacity=capacity/num_f
          Cb=(a*capacity**b)*num_f
          Cp=Cb*f_material
          
     elif equipment == "Blower":
          power=power*unit_hph
          capacity=power
          if material not in dictFmBlower:
               return(print(f"Error: The selected equipment material '{material}' is not available for '{equipment}, {eqptype}' in the cost estimation model. Available materials: {dictFmBlower.keys()}"))
          f_material=dictFmBlower[material]
          
          if eqptype=="Centrifugal(turbo)":
               a=6.6547
               b=0.7900
               c=0
          elif eqptype=="Rotary straight-lobo":
               a=7.35356 
               b=0.79320
               c=-0.012900           
          Cp=np.exp(a+b*ln(capacity)+c*(ln(capacity))**2)
          Cp=Cb*f_material

     elif equipment == "Compressor":
          power=power*unit_hph
          capacity=power
          if drive not in dictFdComp:
               return(print(f"Error: The selected driver type '{drive}' is not available in this model. Available driver types: {dictFdComp.keys()}"))
          fd=dictFdComp[drive]
          
          if material not in dictFmComp:
               return(print(f"Error: The selected equipment material '{material}' is not available for '{equipment}, {eqptype}' in the cost estimation model. Available materials: {dictFmComp.keys()}"))
          f_material=dictFmComp[material]
          
          if eqptype=="Centrifugal":
               r_max=30000
               r_min=200
               a=7.2223
               b=0.8  
          elif eqptype=="Reciprocating":
               r_max=20000
               r_min=100
               a=7.6084
               b=0.8
          elif eqptype=="Screw":
               r_max=8000
               r_min=10
               a=7.7661
               b=0.7243
          num_f=math.ceil(capacity/r_max)
          if capacity<=r_min:
               capacity=r_min
          else:
               capacity=capacity/num_f
          Cb=np.exp(a+b*ln(capacity))*num_f
          Cp=fd*f_material*Cb

     elif equipment == "Fans":
          Pout=Pout*unit_inH2O
          pressure=pressure*unit_inH2O
          fanhead=abs(pressure-Pout)
          flow=volflow*unit_ft3*60
          capacity=flow
          """
          if Pout<5:
               return("Out of capacity - pressure")
          elif Pout>40:
               return("Out of capacity - pressure")
          """
          if fanhead<=8:
               fh=1.15
          elif 8<fanhead<=15:
               fh=1.3
          elif 15<fanhead<=30:
               fh=1.45
          elif 30<fanhead:
               fh=1.55
          if material not in dictFmFan:
               return(print(f"Error: The selected equipment material '{material}' is not available for '{equipment}, {eqptype}' in the cost estimation model. Available materials: {dictFmFan.keys()}"))
          f_material=dictFmFan[material]
          if eqptype=="Centrifugal straight-radial":
               a=11.9296
               b=- 1.31363
               c=0.09974
               r_max=20000
          elif eqptype=="Centrelifugal backward-curved":
               a=10.8375 
               b=- 1.12906
               c= 0.08860
               r_max=100000
          elif eqptype=="Axial vane":
               a=9.2847
               b=- 0.97566
               c=0.08532
               r_max=900000
          elif eqptype=="Axial tube":
               a=5.89085 
               b=- 0.40254
               c=0.05787
               r_max=900000
          num_f=math.ceil(capacity/r_max)
          capacity=capacity/num_f
          Cb=np.exp(a+b*ln(capacity)+c*(ln(capacity))**2)*num_f
          Cp=fh*f_material*Cb

     elif equipment == "Filters":
          area=area*unit_ft2
          capacity=area
          if eqptype=="Plate and frame":
               a=3800
               b=0.52
               r_max=800
               r_min=130
          elif eqptype=="Leaf":
               a=960
               b=0.71
               r_max=2500
               r_min=30
          elif eqptype=="Disc and drum":
               a=11.432
               b=- 0.1905
               c=0.0554
               r_max=800
               r_min=10
          elif eqptype=="Pan":
               a=19500
               b=0.48
               r_max=1100
               r_min=100       
          num_f=math.ceil(capacity/r_max)
          if capacity<=r_min:
               capacity=r_min
          else:
               capacity=capacity/num_f
          if eqptype in ["Molten salt heater", "Diphenyl heater", "Steam boiler"]:
               Cp=(a*capacity**b)*num_f
          else:
               Cp=np.exp(a+b*ln(capacity)+c*(ln(capacity))**2)*num_f

     elif equipment in ["Heat exchanger (others)"]:
          area=area*unit_ft2
          capacity=area
          if material not in dictBaseFMaterial:
               return(print(f"Error: The selected equipment material '{material}' is not available for '{equipment}, {eqptype}' in the cost estimation model. Available materials: {dictBaseFMaterial.keys()}"))
          if eqptype in ["Flat plate","Spiral plate"]:
               f_material=dictBaseFMaterial[material]/2
          elif eqptype in ["Air cooler"]:
               f_material=dictBaseFMaterial[material]  
               
          if eqptype=="Air cooler" :
               a=1970
               b=0.4
               r_max=150000
               r_min=40
          elif eqptype=="Flat plate" :
               a=7000
               b=0.42
               r_max=15000
               r_min=150
          elif eqptype=="Spiral plate":
               a=4900
               b=0.42
               r_max=2000
               r_min=20
          num_f=math.ceil(capacity/r_max)
          if capacity<=r_min:
               capacity=r_min
          else:
               capacity=capacity/num_f
          Cb=(a*capacity**b)*num_f
          Cp=Cb*f_material

     elif equipment == "Heat exchanger (shell and tube)":
          if material not in dictFmaHEX:
               return(print(f"Error: The selected equipment material '{material}' is not available for '{equipment}, {eqptype}' in the cost estimation model. Available materials: {dictFmaHEX.keys()}"))
          
          pressure=pressure*unit_psi
          fp=0.9803 + 0.018*(pressure/100) + 0.0017*(pressure/100)**2
          area=area*unit_ft2
          height=height*unit_ft
          capacity=area
          ma=dictFmaHEX[material]
          mb=dictFmbHEX[material]
          f_material=ma+(capacity/100)**mb

          if eqptype=="Floating head":
               a=11.667
               b=- 0.8709
               c=0.09005
               r_max=12000
               r_min=150
          elif eqptype=="Fixed tube" :
               a=11.0545
               b= - 0.9228
               c=0.09861
               r_max=12000
               r_min=150
          elif eqptype=="U-tube (shell and tube)" :
               a=11.147
               b=- 0.9186
               c=0.09790
               r_max=12000
               r_min=150                 
          elif eqptype=="Kettle reboiler" :
               a=11.967
               b=- 0.8709
               c=0.09005
               r_max=12000
               r_min=150    
          
          if height<=8:
               fl=1.25
          elif 8<height<=12:
               fl=1.12
          elif 12<height<=16:
               fl=1.05
          elif 16<height:
               fl=1
          num_f=math.ceil(capacity/r_max)
          if capacity<=r_min:
               capacity=r_min
          else:
               capacity=capacity/num_f
          Cb=np.exp(a+b*ln(capacity)+c*(ln(capacity))**2)*num_f
          Cp=fp*f_material*fl*Cb

     elif equipment == "Heater":
          power=power*unit_btu
          capacity=power
          if eqptype=="Hot water heater":
               a=9.3548
               b=- 0.3769
               c=0.03434
               r_max=70*10**6
               r_min=0.5*10**6
          elif eqptype=="Molten salt heater":
               a=9.71
               b=0.64
               r_max=70*10**6
               r_min=0.5*10**6
          elif eqptype=="Diphenyl heater":
               a=9.83
               b=0.65
               r_max=70*10**6
               r_min=0.5*10**6
          elif eqptype=="Steam boiler":
               a=0.289
               b=0.77
               r_max=70*10**6
               r_min=0.5*10**6
          num_f=math.ceil(capacity/r_max)
          if capacity<=r_min:
               capacity=r_min
          else:
               capacity=capacity/num_f
          if eqptype in ["Molten salt heater", "Diphenyl heater", "Steam boiler"]:
               Cp=(a*capacity**b)*num_f
          if eqptype in ["Hot water heater"]:
               Cp=np.exp(a+b*ln(capacity)+c*(ln(capacity))**2)*num_f

     elif equipment == "Membrane (for reverse osmosis)":
          #기본 flow = m3/h
          flow=volflow*unit_gal/unit_day
          capacity=flow
          if eqptype=="For seawater":
               a= 0
               b= 0.8020
               c= 0.01775
               r_max=50*10**6
               r_min=2*10**6
          elif eqptype=="For brackish water":
               a=2.1
               b=1
               r_max=14*10**6
               r_min=0.2*10**6
          num_f=math.ceil(capacity/r_max)
          if capacity<=r_min:
               capacity=r_min
          else:
               capacity=capacity/num_f
          if eqptype in ["For brackish water"]:
               Cp=(a*capacity**b)*num_f
          if eqptype in ["For seawater"]:
               Cp=np.exp(a+b*ln(capacity)+c*(ln(capacity))**2)*num_f

     elif equipment == "Membrane":
          area=area*unit_ft2
          if eqptype=="Gas permeation":
               Cp=35*area
          elif eqptype=="Pervaporation":
               Cp=30*area
          elif eqptype=="Ultrafiltration":
               Cp=16*area

     elif equipment == "Packing":
          volume=volume*unit_ft3
          if material not in dictCpkPacking[eqptype]:
               return(print(f"Error: The selected equipment material '{material}' is not available for '{equipment}, {eqptype}' in the cost estimation model. Available materials: {dictCpkPacking[eqptype].keys()}"))
          if packsize not in dictCpkPacking[eqptype][material]:
               return(print(f"Error: The selected packing size '{packsize} in' is not available for '{equipment}, {eqptype}' in the cost estimation model. Available packsize: {dictCpkPacking[eqptype][material].keys()}"))
          Cpk=dictCpkPacking[eqptype][material][packsize]
          Cp=volume*Cpk

     elif equipment == "Size enlargement equipment":
          flow=massflow*unit_lb
          capacity=flow
          if eqptype=="Disk agglomerator":
               a= 10.4947
               b=-0.4915
               c=0.03648
               r_max=80000
               r_min=800
          elif eqptype=="Drum agglomerator":
               a= 11.1885 
               b=- 0.5981
               c=0.04451
               r_max=240000
               r_min=800
          elif eqptype=="Pellet mill":
               a=5500
               b=0.11
               r_max=80000
               r_min=800
               Cp=5500*flow**0.11
          elif eqptype=="Pug mill extruder" :
               a=9.2486
               b=- 0.01453
               c=0.01019
               r_max=40000
               r_min=80
          elif eqptype=="Screw extruder":
               a=10.5546
               b=0
               c= 0.02099
               r_max=800
               r_min=8
          elif eqptype=="Roll-type presses":
               a=91
               b=0.59
               r_max=140000
               r_min=8000
          elif eqptype=="Tableting presses":
               a=8.9188
               b=0.1050
               c=0.01885
               r_max=8000
               r_min=800
          num_f=math.ceil(capacity/r_max)
          if capacity<=r_min:
               capacity=r_min
          else:
               capacity=capacity/num_f
          if eqptype in ["Pellet mill", "Roll-type presses"]:
               Cb=(a*capacity**b)*num_f
          if eqptype in ["Disk agglomerator","Drum agglomerator","Pug mill extruder", "Screw extruder", "Tableting presses"]:
               Cb=np.exp(a+b*ln(capacity)+c*(ln(capacity))**2)*num_f
          Cp=Cb*f_material

     elif equipment == "Size reduction equipment":
          flow=massflow*unit_ton
          capacity=flow
          if eqptype=="Gyratory crusher":
               a=8300
               b=0.6
               r_max=1200
               r_min=25
          elif eqptype=="Jaw crusher":
               a=1800
               b=0.89
               r_max=200
               r_min=10
          elif eqptype=="Cone crusher":
               a=1400
               b=1.05
               r_max=300
               r_min=20
          elif eqptype=="Hammer mill":
               a=3000
               b=0.78
               r_max=200
               r_min=2
          elif eqptype=="Ball mill":
               a=45000
               b=0.69
               r_max=30
               r_min=1
          elif eqptype=="Jet mill" :
               a=27000
               b=0.39
               r_max=5
               r_min=1
          num_f=math.ceil(capacity/r_max)
          if capacity<=r_min:
               capacity=r_min
          else:
               capacity=capacity/num_f
          Cp=(a*capacity**b)*num_f

     elif equipment == "Solid-liquid separator":
          area=area*unit_ft2
          capacity=area
          if eqptype=="Thickener, steel":
               a=2650
               b=0.58
               r_max=8000
               r_min=80
          elif eqptype=="Thickener, concrete":
               a=1900
               b=0.58
               r_max=125000
               r_min=8000
          elif eqptype=="Clarilelifier, steel":
               a=2400
               b=0.58
               r_max=8000
               r_min=80
          elif eqptype=="Clarifier, concrete":
               a=1700
               b=0.58
               r_max=125000
               r_min=8000
          num_f=math.ceil(capacity/r_max)
          if capacity<=r_min:
               capacity=r_min
          else:
               capacity=capacity/num_f
          Cp=(a*capacity**b)*num_f

     elif equipment == "Trays":
          diameter=diameter*unit_ft
          if eqptype=="Sieve":
               Ftt=1
          elif eqptype=="Valve":
               Ftt=1.18
          elif eqptype=="Bubble cap":
               Ftt=1.87
          if material not in ["Carbon steel","Stainless steel","Monel"]:
               return(print(f"Error: The selected equipment material '{material}' is not available for '{equipment}, {eqptype}' in the cost estimation model. Available materials: ['Carbon steel','Stainless steel','Monel']"))
          elif material=="Carbon steel":
               Ftm=1
          elif material=="Stainless steel":
               Ftm=1.189+0.0577*diameter
          elif material=="Monel":
               Ftm=2.306+0.1120*diameter
          if 20<=num:
               Fnt=1
          elif num<20:
               Fnt=2.25/(1.0414**num)
          Cbt=369*np.exp(0.1739*diameter)
          Cp=num*Fnt*Ftt*Ftm*Cbt

     elif equipment == "Vacuum system":
          flow=volflow*unit_ft3
          capacity=flow
          if eqptype=="Liquid-ring pumps" :
               a=6500
               b=0.35
               r_max=350
               r_min=50
          elif eqptype=="Three-stage lobe":
               a=5610
               b=0.41
               r_max=240
               r_min=60
          elif eqptype=="Three-stage claw":
               a=6800
               b=0.36
               r_max=270
               r_min=60
          elif eqptype=="Screw compressor":
               a=7560
               b=0.38
               r_max=350
               r_min=50
          num_f=math.ceil(capacity/r_max)
          if capacity<=r_min:
               capacity=r_min
          else:
               capacity=capacity/num_f
          Cp=(a*capacity**b)*num_f

     elif equipment == "Vessel/Tower":
          diameter=diameter*unit_ft
          height=height*unit_ft
          thick=thick*unit_ft
          if material not in dictFmVessel:
               return(print(f"Error: The selected equipment material '{material}' is not available for '{equipment}, {eqptype}' in the cost estimation model. Available materials: {dictFmVessel.keys()}"))
          den=dictMatDensity[material]*unit_lb/unit_ft3        #lb/ft3
          f_material=dictFmVessel[material]
          weight=pi*(diameter+thick)*(height+0.8*diameter)*thick*den
          capacity=weight
          #density 단위=lb/ft3, weight=lb
          #separation tower은 type에서 제외되었음.
          if eqptype=="Horizontal vessel":
               r_max=920000
               r_min=1000
               Cpl=1580*(diameter)**0.20294
               num_f=math.ceil(capacity/r_max)
               if capacity<=r_min:
                    capacity=r_min
               else:
                    capacity=capacity/num_f
               Cv=np.exp(8.717 - 0.2330*ln(capacity) + 0.04333*(ln(capacity))**2)
               
          # 입력된 weight의 구간에 따라 vertical vessel과 sepa tower을 구분하여 사용
          elif eqptype=="Vertical vessel" and weight<=500000:
               a=6.775
               b=0.18255
               c=0.02297
               r_max=500000
               r_min=4200
               num_f=math.ceil(capacity/r_max)
               if capacity<=r_min:
                    capacity=r_min
               else:
                    capacity=capacity/num_f
               height=height/num_f
               Cpl=285.1*(diameter**0.73960)*(height**0.70684)
               Cv=np.exp(6.775 + 0.18255*ln(capacity) + 0.02297*(ln(capacity))**2)

          elif eqptype=="Vertical vessel" and 500000<weight:
               r_max=2500000
               r_min=500000
               num_f=math.ceil(capacity/r_max)
               height=height/num_f
               capacity=capacity/num_f
               Cpl=237.1*(diameter**0.63316)*(height**0.80161)
               Cv=np.exp(7.0374 + 0.18255*ln(capacity) + 0.02297*(ln(capacity))**2)
          Cp=(f_material*Cv+Cpl)*num_f
          
     return(round(Cp,1))

     
