# *******Towler model, (Gavin Towler, 2007, “Chemical Engineering Design –Principles, Practice and Economics of plant”, 1st ed.)***************************
import numpy as np
from math import pi
import math
from unit_parameters import *

# Material density (density unit=kg/m3) ===================================================================================================================
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

# Material factor(fm): "Turbines" =====================================================================================================================
dictMaterial_turbine = {
        "Carbon steel": 1,
        "Stainless steel": 2,
        "Nickel(alloy)": 3,
        "Monel":3,       #allowed
        "Inconel":3,     #allowed
        "Hastelloy C":3  #allowed
    }
# Material factor(fm): "Compressor" =====================================================================================================================
dictMaterial_comp = {
     "Carbon steel": 1,
     "Stainless steel": 2.5,
     "Nickel(alloy)": 5.1 ,
     "Monel":5.1,       #allowed
     "Inconel":5.1,     #allowed
     "Hastelloy C":5.1  #allowed
    }
# Material factor(fm): "Heat exchanger (shell and tube)" ===============================================================================================
dictMaterial_hex = {
        "CS shell/CS tube":1,
        "CS shell/Cu tube":1.25,
        "CS shell/SS tube":1.7,
        "CS shell/Ni(alloy) tube":2.8,
        "SS shell/SS tube":3,
        "CS shell/Ti(alloy) tube":7.2, 
    }
# Material factor(fm): "Heat exchanger (others)" ==========================================================================================================
dictmaterial_hexelse={
     "Gasket plate":{
          "Carbon steel":1,
          "Stainless steel":2.3,
          "Copper(alloy)":1.2,
          "Nickel(alloy)":2.8,
          "Monel":2.8,       #allowed
          "Inconel":2.8,     #allowed
          "Hastelloy C":2.8,  #allowed
          "Titanium(alloy)":7.2,
          "Aluminum(alloy)":1.5},
     
     "Flat plate":{
          "Carbon steel":1,
          "Stainless steel":2.3,
          "Copper(alloy)":1.2,
          "Nickel(alloy)":2.8,
          "Monel":2.8,       #allowed
          "Inconel":2.8,     #allowed
          "Hastelloy C":2.8,  #allowed
          "Titanium(alloy)":7.2,
          "Aluminum(alloy)":1.5},

     "Air cooler":{
          "Carbon steel":1,
          "Stainless steel":3.0,
          "Aluminum(alloy)":1.5}
     }
# Material factor(fm): "Pumps" =====================================================================================================================
dictMaterial_pump = {
    "Cast iron":1,
    "Copper(alloy)":1.26,
    "Carbon steel":1.5,
    "Stainless steel":1.8     
    }
# Material factor(fm): "Vessel/Tower" =====================================================================================================================
dictMaterial_vessel = {
     "Carbon steel":1,
     "Nickel(alloy)":7.4,
     "Monel":7.4,       #allowed
     "Inconel":7.4,     #allowed
     "Hastelloy C":7.4,  #allowed
     "Stainless steel":3
    #"SS clad":3,
    #"Ni alloy clad":7.4
    }
# Material factor(fm): "Storage tank" =====================================================================================================================
dictMaterial_tank = {
     "Carbon steel": 1,
     "Stainless steel": 2,
     "Monel": 6,
     "Nickel(alloy)":6,
     "Inconel":6,     #allowed
     "Hastelloy C":6,  #allowed
     "Titanium(alloy)":9.6
    }

#==================================Material parameters mapping=============================================================================================
lst_FMaterial={
     "Turbines":{"Axial gas turbines":dictMaterial_turbine},
     "Compressor":{"Centrifugal":dictMaterial_comp, "Reciprocating":dictMaterial_comp},
     "Heat exchanger (shell and tube)":{"Fixed tube":dictMaterial_hex, "U-tube (shell and tube)":dictMaterial_hex, "Floating head":dictMaterial_hex},
     "Heat exchanger (others)":{"Gasket plate":dictmaterial_hexelse, "Flat plate":dictmaterial_hexelse, "Air cooler":dictmaterial_hexelse},
     "Pumps":{"Centrifugal":dictMaterial_pump, "Reciprocating":dictMaterial_pump},
     "Vessel/Tower":{"Horizontal vessel":dictMaterial_vessel, "Vertical vessel":dictMaterial_vessel},
     "Storage tank":{"Open":dictMaterial_tank, "Cone roof":dictMaterial_tank, "Floating roof":dictMaterial_tank, "Spherical":dictMaterial_tank, "Gas holder":dictMaterial_tank}
}


def eqpcomo_Peters(equipment,material,eqptype,pressure,Pout,volume,power,volflow,massflow,area,packsize,height,diameter,thick,temperature,num,drive):
     Cb=0    #2002 basis
     f_material=1
     f_pressure=1
     f_diameter=1
     # Error message: Not available equipment spec. for model supporting list & Material factor mapping
     eqp_type_list=lst_FMaterial[equipment].keys()
     eqp_mat_list=lst_FMaterial[equipment][eqptype].keys()

     if eqptype not in eqp_type_list:
          return(print(f"Error: The selected equipment type '{eqptype}' is not available for '{equipment}' in the cost estimation model. Available types for '{equipment}': {list(eqp_type_list)}"))  
     if material not in eqp_mat_list:
          return(f"Error: The selected equipment material '{material}' is not available for '{equipment}, {eqptype}' in the cost estimation model. Available materials: {list(eqp_mat_list)}")
     else:
          f_material=lst_FMaterial[equipment][eqptype][material]

     if equipment =="Storage tank":
          capacity=volume #unit=m3
          if capacity <=3000:   #small erected tank
               capa_min=80
               capa_max=3000
               if capacity<=capa_min:
                    capacity=capa_min
               eqnum=math.ceil(capacity/capa_max)
               capa_input=capacity/eqnum
               Cb=(-0.0097*capa_input**2 + 64.635*capa_input + 24892)*eqnum          # Cb is the base equipment cost at ambient operating pressure & temperature and using carbon steel construction
               Cp=Cb*f_material

          elif 3000<capacity:   #small erected tank
               capa_max=50000
               eqnum=math.ceil(capacity/capa_max)
               capa_input=capacity/eqnum
               Cb=(37.962*capa_input + 101644)*eqnum
               Cp=Cb*f_material

     elif equipment =="Turbines":
          capacity=abs(power) #unit=kW
          if eqptype=="Axial gas turbines":
               capa_min=100
               capa_max=4000
               if capacity<=capa_min:
                    capacity=capa_min
               eqnum=math.ceil(capacity/capa_max)
               capa_input=capacity/eqnum
               Cb=(3167.9*capa_input**0.5989)*eqnum
               Cp=Cb*f_material

     elif equipment=="Heat exchanger (others)":
          capacity=area #unit=m2
          if eqptype =="Gasket plate":
               capa_min=1
               capa_max=1500
               if capacity<=capa_min:
                    capacity=capa_min
                    eqnum=math.ceil(capacity/capa_max)
                    capa_input=capacity/eqnum
                    Cb=(12.228*capa_input+612.02)*eqnum
                    Cp=Cb*f_material
          elif eqptype=="Flat plate": 
               capa_min=10     
               capa_max=1500
               if capacity<=capa_min:
                    capacity=capa_min
                    eqnum=math.ceil(capacity/capa_max)
                    capa_input=capacity/eqnum
                    Cb=(-0.0784*capa_input**2 + 151.57*capa_input + 25299)*eqnum
                    Cp=Cb*f_material
          elif eqptype=="Air cooler": 
               capa_min=3.5
               capa_max=10000
               if capacity<=capa_min:
                    capacity=capa_min
                    eqnum=math.ceil(capacity/capa_max)
                    capa_input=capacity/eqnum
                    Cb=(3406*capa_input**0.4367)*eqnum
                    Cp=Cb*f_material

     elif equipment =="Compressor":
          capacity=power # power unit = m3/s*kPa = kW
          if eqptype=="Centrifugal":
               capa_min=75
               capa_max=6000
               if capacity<=capa_min:
                    capacity=capa_min
               eqnum=math.ceil(capacity/capa_max)
               capa_input=capacity/eqnum
               Cb=(-0.0185*capa_input**2 + 609.97*capa_input + 7616.3)*eqnum          
          elif eqptype=="Reciprocating" and drive not in ["Steam turbine","Electric-open/drip proof","Electric-explosion proof","Electric-totally enclosed"] :
               return(print(f"Error: The selected driver type '{drive}' is not available in this model. Available driver types: ['Steam turbine','Electric-open/drip proof','Electric-explosion proof','Electric-totally enclosed']"))
          elif eqptype=="Reciprocating" and drive=="Steam turbine":
               capa_min=75
               capa_max=6000
               if capacity<=capa_min:
                    capacity=capa_min
               eqnum=math.ceil(capacity/capa_max)
               capa_input=capacity/eqnum
               Cb=(-0.0146*capa_input**2 + 672.09*capa_input + 4112)*eqnum
          elif eqptype=="Reciprocating" and drive in ["Electric-open/drip proof","Electric-explosion proof","Electric-totally enclosed"]:
               capa_min=75
               capa_max=6000
               if capacity<=capa_min:
                    capacity=capa_min
               eqnum=math.ceil(capacity/capa_max)
               capa_input=capacity/eqnum
               Cb=(-0.0249*capa_input**2 + 813.46*capa_input + 15098)*eqnum
          
          Cp=Cb*f_material

     elif equipment =="Heat exchanger (shell and tube)":
          capacity=area #area unit=m2

          if pressure <10.35: # pressure unit=
               f_pressure=1
          elif 10.35<=pressure<=150:
               f_pressure= 0.7912*pressure**0.099
          elif 150<pressure:
               f_pressure=1.31

          if eqptype=="Fixed tube":
               capa_max=600
               capa_min=5
               if capacity<=capa_min:
                    capacity=capa_min
               eqnum=math.ceil(capacity/capa_max)
               capa_input=capacity/eqnum
               Cb=(-0.0358*capa_input**2 + 81.708*capa_input + 3615.8)*eqnum

          elif eqptype=="U-tube (shell and tube)":
               capa_max=400    
               capa_min=3
               if capacity<=capa_min:
                    capacity=capa_min      
               eqnum=math.ceil(capacity/capa_max)
               capa_input=capacity/eqnum
               Cb=(-0.0873*capa_input**2 + 104.2*capa_input + 2292.6)*eqnum

          elif eqptype=="Floating head":
               capa_max=1000  
               capa_min=10
               if capacity<=capa_min:
                    capacity=capa_min   
               eqnum=math.ceil(capacity/capa_max)
               capa_input=capacity/eqnum
               Cb=(0.0023*capa_input**2 + 138.33*capa_input + 7416.8)*eqnum
          Cp=Cb*f_material*f_pressure

     elif equipment =="Pumps":          
          if pressure<10.35:
               f_pressure=1
          elif 10.35<=pressure<=1000:
               f_pressure=0.3676*math.log(pressure) + 0.1398
          elif 1000<pressure:
               f_pressure=2.7
               
          if eqptype=="Centrifugal":
               capacity=volflow/unit_sec*pressure*unit_kPa         #unit=m3/s*kPa
               capa_max=200
               capa_min=6
               if capacity<=capa_min:
                    capacity=capa_min
               eqnum=math.ceil(capacity/capa_max)
               capa_input=capacity/eqnum
               Cb=(1.054*capa_input**2 + 117.48*capa_input + 8449) * eqnum

          if eqptype=="Reciprocating":
               capacity=volflow/unit_sec           #unit=m3/s
               capa_max=0.06
               capa_min=0.0001
               if capacity<=capa_min:
                    capacity=capa_min
               eqnum=math.ceil(capacity/capa_max)
               capa_input=capacity/eqnum
               Cb=(-280362*capa_input**2 + 170921*capa_input + 710.84) * eqnum
          Cp=Cb*f_material*f_pressure

     elif equipment =="Vessel/Tower":
          density=dictMatDensity[material]
          weight=pi*diameter*thick*height*density   #unit=kg
          
          if material not in dictMaterial_vessel:
               return(print(f"Error: The selected equipment material '{material}' is not available for '{equipment}, {eqptype}' in the cost estimation model. Available materials: {list(dictMaterial_vessel.keys())}"))
          else:
               f_material = dictMaterial_vessel[material]

          if pressure<=400:
               f_pressure= 0.0365*pressure + 1.2265
          elif 400<pressure:
               f_pressure=15.8

          if eqptype=="Vertical vessel":
               f_diameter=1
               capacity=weight
               capa_max=30000
               capa_min=400
               if capacity<=capa_min:
                    capacity=capa_min
               eqnum=math.ceil(capacity/capa_max)
               capa_input=capacity/eqnum
               Cb=(-0.0002*capa_input**2 + 7.9324*capa_input + 8291.4) * eqnum

          if eqptype== "Horizontal vessel":
               if diameter <0.44:
                    f_diameter=0.25
               elif 3.87<diameter:
                    f_diameter=2
               elif diameter==2:
                    f_diameter=1
               else:
                    f_diameter= 0.5093*diameter + 0.027    
               capacity=height  # height&diameter  unit=m
               capa_max=55
               capa_min=1.5
               if capacity<=capa_min:
                    capacity=capa_min
               eqnum=math.ceil(capacity/capa_max)
               capa_input=capacity/eqnum
               Cb=(2.954*capa_input**2 + 1150.3*capa_input + 4908.8)*eqnum
          
          Cp=Cb*f_material*f_pressure*f_diameter

     return round(Cp,0)



