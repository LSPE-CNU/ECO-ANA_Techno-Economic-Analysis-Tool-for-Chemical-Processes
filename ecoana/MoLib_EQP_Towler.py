# *******Towler model, (Gavin Towler, 2007, “Chemical Engineering Design –Principles, Practice and Economics of plant”, 1st ed.)***************************
import numpy as np
from math import pi
from numpy import log as ln
import math

# Material density (density unit=kg/m3) ==========================================================================================================================================================
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
# Material factor(fm): "Mixer","Agitator","Compressor","Crystallizer-cooling","Dryer","Evaporator","Pumps","Reactor","Storage tank","Trays", "Heater","Furnace"
lst_Group1=["Mixer","Agitator","Compressor","Crystallizer-cooling","Dryer","Evaporator","Pumps","Reactor","Storage tank","Trays", "Heater","Furnace"]
dictFMaterial_Group1={"Carbon steel":1,
                        "Stainless steel":1.3,
                        "Aluminum(alloy)":1.07,
                        "Monel":1.65,
                        "Inconel":1.7,
                        "Nickel(alloy)":1.7,
                        "Hastelloy C":1.7         #allowed
                        }
# Material factor(fm): "Heat exchanger (others)" ====================================================================================================================================
dictFMaterial_HEXOthers={"Carbon steel":1/1.3,
                   "Stainless steel":1.3/1.3,
                   "Aluminum(alloy)":1.07/1.3,
                   "Monel":1.65/1.3,
                   "Inconel":1.7/1.3,
                   "Nickel(alloy)":1.7/1.3,
                   "Hastelloy C":1.7/1.3       #allowed
                   }
# Material factor(fm): "Heat exchanger (shell and tube)" ====================================================================================================================================
dictFMaterial_HEX={"CS shell/CS tube":1,
                   "CS shell/SS tube":1.15,
                   "CS shell/Al(alloy) tube":1.07,
                   "CS shell/Mo(alloy) tube":1.65,
                   "CS shell/Ni(alloy) tube":1.7,
                   "SS shell/SS tube":1.3}

# Available equipment & type list for this model================================================================================================
lst_alltype={"Trays":["Sieve","Valve","Bubble cap"],
                "Mixer":["Ribbon"],
                "Agitator":["Propeller, open tank","Propeller, closed vessel"],
                "Heater":["Steam boiler"],
                "Furnace":["Reformer furnace","Pyrolysis furnace", "Nonreactive furnace"],
                "Compressor":["Centrifugal","Reciprocating"],
                "Conveyor":["Belt"],
                "Size reduction equipment":["Hammer mill", "Ball mill" ],
                "Crystallizer-cooling":["Jacketed scraped wall"],
                "Vessel/Tower":["Vertical vessel","Horizontal vessel"],
                "Dryer":["Rotary(gas fired)","Pan","Spray" ],
                "Evaporator":["Long tube","Falling film" ],
                "Heat exchanger (shell and tube)":["U-tube (shell and tube)",
                                                "Floating head",
                                                "Double Pipe",
                                                "Kettle reboiler"],
                "Heat exchanger (others)":["Flat plate"],
                "Filters":["Vacuum filter", "Plate and frame"] , 
                "Packing":["Raschig rings","Pall rings","Intalox saddles"],
                "Packing (Structured)":["Structured"] ,
                "Pumps":["Centrifugal"], 
                "Reactor":["Jacketed agitated"], 
                "Storage tank":["Cone roof","Floating roof"],
                "Water ion exchanger":[]          # Equipment type variable is not required for cost estimation
                }



def eqpcomo_Towler(equipment,material,eqptype,pressure,Pout,volume,power,volflow,massflow,area,packsize,height,diameter,thick,temperature,num,drive):
     Ce=0
     a=0
     b=0
     n=0
     capacity=0
     fm=0
     # Error message: Not available equipment spec. for model supporting list & Material factor mapping
     eqp_type_list=lst_alltype[equipment]
     if equipment not in ["Water ion exchanger"] and eqptype not in eqp_type_list:
          return(print(f"Error: The selected equipment type '{eqptype}' is not available for '{equipment}' in the cost estimation model. Available types for '{equipment}': {eqp_type_list}"))  
     if equipment in lst_Group1:
          if material not in dictFMaterial_Group1:
               return(print(f"Error: The selected equipment material '{material}' is not available for '{equipment}, {eqptype}' in the cost estimation model. Available materials: {list(dictFMaterial_Group1.keys())}"))
          fm=dictFMaterial_Group1[material]
     elif equipment in ["Heat exchanger (shell and tube)"]:
               if material not in dictFMaterial_HEX:
                    return(print(f"Error: The selected equipment material '{material}' is not available for '{equipment}, {eqptype}' in the cost estimation model. Available materials: {list(dictFMaterial_HEX.keys())}"))
               fm=dictFMaterial_HEX[material]
     elif equipment in ["Heat exchanger (others)"]:
          if material not in dictFMaterial_HEXOthers:
               return(print(f"Error: The selected equipment material '{material}' is not available for '{equipment}, {eqptype}' in the cost estimation model. Available materials: {list(dictFMaterial_HEXOthers.keys())}"))
     else:
          fm=1
     
     if equipment in ["Mixer","Agitator"]:
          capacity=power
          if eqptype in["Propeller, open tank","Propeller, closed vessel"]:
               a=4300
               b=1920
               n=0.8
               r_max=75
               r_min=5
          elif eqptype=="Ribbon":
               a=11000
               b=420
               n=1.5
               r_max=5
               r_min=35          
     elif equipment=="Heater":
          capacity=massflow   # massflow unit = kg/h
          if eqptype=="Steam boiler" and capacity<=200000:           # Medium scale boiler
               a=4600
               b=62
               n=0.8
               r_max=200000
               r_min=5000
          elif eqptype=="Steam boiler" and 200000<capacity:          # Large scale boiler
               a=-90000
               b=93
               n=0.8
               r_max=800000
               r_min=200000
     elif equipment=="Furnace":         # Cylindrical furnace
          capacity=power/1000   # power unit = MW
          a=53000
          b=69000
          n=0.8
          r_max=60
          r_min=0.2
     elif equipment=="Compressor":
          capacity=power
          if eqptype=="Centrifugal":
               a=8400
               b=3100
               n=0.6
               r_max=29000
               r_min=132
          elif eqptype=="Reciprocating":
               a=240000
               b=1.33
               n=1.5
               r_max=16000
               r_min=100          
     elif equipment=="Conveyor":
          capacity=area
          if eqptype=="Belt":
               a=23000
               b=575
               n=1
               r_max=500
               r_min=10
     elif equipment=="Size reduction equipment":
          capacity=massflow
          if eqptype=="Hammer mill":
               a=400
               b=9900
               n=0.5
               r_max=400000
               r_min=20000
          elif eqptype=="Ball mill":
               a=3000
               b=390
               n=0.5
               r_max=4000
               r_min=200
     elif equipment=="Crystallizer-cooling":
          capacity=height
          if eqptype=="Jacketed scraped wall":
               a=41000
               b=40000
               n=0.7
               r_max=280
               r_min=7
     elif equipment=="Vessel/Tower":
          #weight unit=kg
          #density unit= kg/m3
          if material not in['Carbon steel','Stainless steel']:
               return(print(f"Error: The selected equipment material '{material}' is not available for '{equipment}, {eqptype}' in the cost estimation model. Available materials: ['Carbon steel','Stainless steel']"))
          den=dictMatDensity[material]
          weight=pi*diameter*thick*height*den
          capacity=weight    
          if eqptype=="Vertical vessel":
               if material=="Carbon steel":
                    a=-400
                    b=230
                    n=0.6
                    r_max=69200
                    r_min=150
               elif material=="Stainless steel":
                    a=-10000
                    b=600
                    n=0.6
                    r_max=124200
                    r_min=90               
          elif eqptype=="Horizontal vessel":
               if material=="Carbon steel" :
                    a=-2500
                    b=200
                    n=0.6
                    r_max=69200
                    r_min=250
               elif material=="Stainless steel" :
                    a=-15000
                    b=560
                    n=0.6       
                    r_max=114000
                    r_min=170          
     elif equipment=="Dryer":
          if eqptype=="Rotary(gas fired)" :
               capacity=area
               a=-7400
               b=4350
               n=0.9
               r_max=180
               r_min=11
          elif eqptype=="Pan":
               capacity=area
               a=-5300
               b=24000
               n=0.5
               r_max=15
               r_min=1.5
          elif eqptype=="Spray":
               capacity=massflow
               a=190000
               b=180
               n=0.9
               r_max=4000
               r_min=400
     elif equipment=="Evaporator":
          capacity=area
          if eqptype=="Long tube" :
               a=17000
               b=13500
               n=0.6
               r_max=640
               r_min=11
          elif eqptype=="Falling film":
               a=29000
               b=53500
               n=0.6
               r_max=12
               r_min=0.5

     elif equipment in ["Heat exchanger (shell and tube)","Heat exchanger (others)"]:
          capacity=area
          if eqptype=="U-tube (shell and tube)":
               a=10000
               b=88
               n=1
               r_max=1000
               r_min=10
          elif eqptype=="Floating head":
               a=11000
               b=115
               n=1
               r_max=1000
               r_min=10
          elif eqptype=="Double Pipe":
               a=500
               b=1100
               n=1
               r_max=80
               r_min=1
          elif eqptype=="Kettle reboiler":
               a=14000
               b=83
               n=1
               r_max=500
               r_min=10
          elif eqptype=="Flat plate":
               a=1100
               b=850
               n=0.4
               r_max=180
               r_min=1
          
     elif equipment=="Filters":
          if eqptype=="Plate and frame":
               capacity=volume
               a=76000
               b=54000
               n=0.5
               r_max=1.4
               r_min=0.4
          elif eqptype=="Vacuum filter":
               capacity=area
               a=-45000
               b=56000
               n=0.3
               r_max=180
               r_min=10

     elif equipment=="Packing":
          capacity=volume
          if eqptype=="Raschig rings":
               if material not in ['Stainless steel']:
                    return(print(f"Error: The selected equipment material '{material}' is not available for '{equipment}, {eqptype}' in the cost estimation model. Available materials: ['Stainless steel']"))
               else:
                    a=0
                    b=3700
                    n=1
          elif eqptype=="Pall rings":
               if material not in ['Stainless steel']:
                    return(print(f"Error: The selected equipment material '{material}' is not available for '{equipment}, {eqptype}' in the cost estimation model. Available materials: ['Stainless steel']"))
               else:
                    a=0
                    b=4000
                    n=1
          elif eqptype=="Intalox saddles":
               if material not in ['Ceramic']:
                    return(print(f"Error: The selected equipment material '{material}' is not available for '{equipment}, {eqptype}' in the cost estimation model. Available materials: ['Ceramic']"))
               else:
                    a=0
                    b=930
                    n=1
          
     elif equipment=="Packing (Structured)":
          capacity=(diameter/2)**2*pi*height
          if material not in['PVC','Stainless steel']:
               return(print(f"Error: The selected equipment material '{material}' is not available for '{equipment}, {eqptype}' in the cost estimation model. Available materials: ['PVC','Stainless steel']"))
          elif material=="PVC":
               a=0
               b=250
               n=1
          elif material=="Stainless steel":
               a=0
               b=3200
               n=1  

     elif equipment=="Pumps":
          if eqptype=="Centrifugal":
               capacity=volflow*1000/60/60  #flow=L/s
               a=3300
               b=48
               n=1.2
               r_max=500
               r_min=0.2

     elif equipment=="Reactor":
          if eqptype=="Jacketed agitated":
               capacity=volume
               a=14000
               b=15400
               n=0.7
               r_max=100
               r_min=0.5

     elif equipment=="Storage tank":
          capacity=volume
          if eqptype=="Floating roof":
               a=53000
               b=2400
               n=0.6
               r_max=10000
               r_min=100
          if eqptype=="Cone roof":
               a=5700
               b=700
               n=0.7
               r_max=4000
               r_min=10

     elif equipment=="Trays":
          capacity=diameter
          if eqptype=="Sieve": #nd 0.5<=capacity<=5:
               a=100
               b=120
               n=2
          elif eqptype=="Valve": #and 0.5<=capacity<=5:
               a=130
               b=146
               n=2
          elif eqptype=="Bubble cap": #and 0.5<=capacity<=5:
               a=200
               b-240
               n=2
          #else:
               #return("Out of range - capacity")

     elif equipment=="Water ion exchanger":
          capacity=volflow
          a=6200
          b=4300
          n=0.7
          r_max=50
          r_min=1
     #지정된 capa range 벗어나는 것들은 num_f로 보정
     #num_f 보정 적용 불가한 장치들 구분
     if equipment in["Packing","Packing (Structured)","Trays"]:
          capacity=capacity
          num_f=1
     else:
          if capacity<r_min:
               capacity=r_min
               num_f=1
               #return("Out of range - capacity")
          elif r_min<=capacity<=r_max:
               num_f=1
          elif r_max<capacity:
               num_f=math.ceil(capacity/r_max)
               capacity=capacity/num_f

     if equipment in ["Trays"]:
          Cp=(a+b*capacity**n)*fm*num
     elif equipment in["Mixer","Agitator","Heater","Furnace","Compressor","Conveyor","Size reduction equipment","Crystallizer-cooling", "Vessel/Tower", "Dryer","Evaporator" ,"Heat exchanger (shell and tube)" ,"Heat exchanger (others)" ,"Filters" , "Packing","Packing (Structured)" , "Pumps", "Reactor", "Storage tank","Water ion exchanger"]:
          Cp=(a+b*capacity**n)*fm*num_f
     

     return round(Cp,1) if Cp > 0 else "Error: NO data"
     