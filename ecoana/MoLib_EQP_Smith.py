#*******Smith model, (Robin Smith ,2016, “Chemical Process Design and Integration”, 2nd ed.)***************************
import numpy as np
from math import pi
from numpy import log as ln
import math
from .WarningMessage import warn_below, warn_above

# Material density (density unit=kg/m3) =======================================================================================================
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
# Material factor(fm): "Vessel/Tower"  ==========================================================================================================
dictFMaterial_Vessel={"Carbon steel":1,
                        "Stainless steel":2.1,
                        "Monel":3.6,
                        "Inconel":3.9,
                        "Nickel(alloy)":5.4,
                        "Hastelloy C":5.4,   #allowed
                        "Titanium(alloy)":7.7
                        }
# Material factor(fm): "Reactor","Trays","Packing (Structured)","Heat exchanger (others)","Pumps","Compressor","Fans","Dryer"  =================
dictFMaterial_Others={"Carbon steel":1,
                        "Aluminum(alloy)":1.3,
                        "Stainless steel":2.4,
                        "Monel":4.1,
                        "Nickel(alloy)":4.4,
                        "Hastelloy C":3.6,   # Smith Table 2.2
                        "Inconel":4.4,
                        "Titanium(alloy)":5.8
                        }
# Material factor(fm): "Heat exchanger (Shell and tube)" =======================================================================================
dictFMaterial_HEX={"CS shell/CS tube":1,
                    "CS shell/Al(alloy) tube":1.3,
                    "CS shell/Monel tube":2.1,
                    "CS shell/SS tube":1.7,
                    "SS shell/SS tube":2.9
                    }
# Available equipment & type list for this model================================================================================================
lst_AllEqpType={
     "Vessel/Tower":["Vertical vessel", "Horizontal vessel","Pressured vessel"],
     "Filters":["Vacuum filter"],
     "Storage tank":["Open", "Cone roof", "Floating roof", "Spherical", "Gas holder"],
     "Heater":["Steam boiler"],
     "Reactor":["Jacketed agitated"],
     "Trays":["Sieve","Valve"],
     "Packing (Structured)":["Structured"],
     "Heat exchanger (others)":["Air cooler"],
     "Pumps":["Centrifugal"],
     "Compressor":["Centrifugal","Reciprocating"],
     "Fans":["Centrifugal straight-radial","Centrifugal backward-curved","Axial vane","Axial tube"],
     "Dryer":["Drum"],
     "Heat exchanger (shell and tube)":["Bayonet","Double Pipe","Fixed tube","Floating head","Kettle reboiler","Multiple Pipe","Scraped Wall","Spiral tube (shell and tube)","U-tube (shell and tube)"]
            }

def eqpcomo_Smith(equipment,material,eqptype,pressure,Pout,volume,power,volflow,massflow,area,packsize,height,diameter,thick,temperature,num,drive):
     Cb=0
     f_scale=0
     m=0
     fm=0
     fp=0
     ft=0
     num_f=0
     temperature=temperature-273.15  #temperature unit = degC

     # Temperature factor (ft)================================================================================================================
     if temperature<=100:
          ft=1
     elif 100<temperature<=500:
          ft=0.0028*temperature+0.7417
     elif 500<temperature: #<=500:
          ft=2.1
     #elif 500<temperature:
          #return("Out of range - temperature")

     # Pressure factor (fp)================================================================================================================
     if pressure is None or pressure<=0:
          fp=1          # pressure not given (default 0): no pressure correction
     elif pressure<=0.01:
          fp=2          # Table 2.5 is in bar absolute: 0.01 bar = vacuum
     elif 0.01< pressure<=0.5:
          fp=-0.259*math.log(pressure)+0.7772
     elif 0.5<pressure<=7:
          fp=1
     elif 7<pressure<=100:
          fp=-4e-5*pressure**2 + 0.0139*pressure + 0.905
     elif 100<pressure:
          fp=1.9
     #elif 100<pressure:
          #return("Out of range - pressure")

     # Error message: Not available equipment spec. for model supporting list         
     eqp_type_list=lst_AllEqpType[equipment]
     if eqptype not in eqp_type_list:
          return(print(f"Error: The selected equipment type '{eqptype}' is not available for '{equipment}' in the cost estimation model. Available types for '{equipment}': {eqp_type_list}"))   

     if equipment=="Vessel/Tower":
          if material not in dictFMaterial_Vessel:
               return(print(f"Error: The selected equipment material '{material}' is not available for '{equipment}, {eqptype}' in the cost estimation model. Available materials: {list(dictFMaterial_Vessel.keys())}"))
          fm=dictFMaterial_Vessel[material]
     elif equipment in["Reactor","Trays","Packing (Structured)","Heat exchanger (others)","Pumps","Compressor","Fans","Dryer"]:
          if material not in dictFMaterial_Others:
               return(print(f"Error: The selected equipment material '{material}' is not available for '{equipment}, {eqptype}' in the cost estimation model. Available materials: {list(dictFMaterial_Others.keys())}"))
          fm=dictFMaterial_Others[material]
     elif equipment =="Heat exchanger (shell and tube)":
          if material not in dictFMaterial_HEX:
               return(print(f"Error: The selected equipment material '{material}' is not available for '{equipment}, {eqptype}' in the cost estimation model. Available materials: {list(dictFMaterial_HEX.keys())}"))
          fm=dictFMaterial_HEX[material]
     elif equipment=="Storage tank":                 # material optional; carbon steel if not given (Table 2.2 factors)
          if material is None:
               fm=1
          elif material not in dictFMaterial_Others:
               return(print(f"Error: The selected equipment material '{material}' is not available for '{equipment}, {eqptype}' in the cost estimation model. Available materials: {list(dictFMaterial_Others.keys())}"))
          else:
               fm=dictFMaterial_Others[material]
     elif equipment in["Filters","Heater"]:                 # Equipment material variable is not required for cost estimation
          fm=1  

     if equipment=="Reactor":
          if eqptype=="Jacketed agitated":
               capacity=volume
               r_max=50
               r_min=1
               Cb=1.15*10**4
               bsize=1
               m=0.45

     elif equipment=="Vessel/Tower" :
          # density unit = kg/m3
          den=dictMatDensity[material]
          # weight unit = t
          weight=(pi*diameter*thick*height*den)/1000
          if eqptype=="Pressured vessel" :
               fm=fm/dictFMaterial_Vessel["Stainless steel"]   # base cost is for SS (low grade), Table 2.1; fM = 2.1 (Table 2.3)
               capacity=weight
               r_max=100
               r_min=6
               Cb=9.84*10**4
               bsize=6
               m=0.82       
          elif eqptype in["Vertical vessel", "Horizontal vessel"]:
               capacity=weight
               r_max=300
               r_min=8
               Cb=6.56*10**4
               bsize=8
               m=0.89         
          
     elif equipment=="Trays":
          if eqptype=="Sieve": #and 0.5<=diameter<=4:
               capacity=diameter
               r_max=4
               r_min=0.5
               Cb=6.56*10**3
               bsize=0.5
               m=0.91              
          elif eqptype=="Valve": #and 0.5<=diameter<=4:
               capacity=diameter
               r_max=4
               r_min=0.5
               Cb=1.8*10**4
               bsize=0.5
               m=0.97        
          #else:
               #return("Out of range - capacity")
               
     elif equipment=="Packing (Structured)":
          if eqptype=="Structured": #and 0.5<=diameter<=40:
               fm=fm/dictFMaterial_Others["Stainless steel"]   # base cost is for SS (low grade), Table 2.1; fM = 2.4 (Table 2.2)
               capacity=diameter
               r_max=4
               r_min=0.5
               Cb=1.8*10**4
               bsize=0.5
               m=1.7
               
     elif equipment=="Filters" :
          if eqptype=="Vacuum filter":
               capacity=area
               r_max=25
               r_min=10
               Cb=8.36*10**4
               bsize=10
               m=0.49        

     elif equipment=="Heat exchanger (shell and tube)":
          capacity=area
          r_max=4000
          r_min=80
          Cb=3.28*10**4
          bsize=80
          m=0.68

     elif equipment=="Heat exchanger (others)":
          if eqptype=="Air cooler":
               capacity=area
               r_max=2000
               r_min=200
               Cb=1.56*10**5
               bsize=200
               m=0.89
     
     elif equipment=="Pumps":
          capacity=power
          if eqptype=="Centrifugal" and capacity<=10 :  
               fm=fm/3.4   # small-pump base cost is for high-grade SS (fM = 3.4, Smith Table 2.2)
               r_max=10
               r_min=1
               Cb=1.97*10**3
               bsize=1
               m=0.35
          if eqptype=="Centrifugal" and 10<capacity:
               r_max=700
               r_min=10
               Cb=9.84*10**3
               bsize=4
               m=0.55

     elif equipment=="Compressor":
          if eqptype in ["Reciprocating", "Centrifugal"]:
               capacity=power
               r_max=10000
               r_min=250
               bsize=250
               Cb=9.84*10**4
               m=0.46

     elif equipment=="Fans":
          capacity=power
          r_max=200
          r_min=50
          bsize=50
          Cb=1.23*10**4
          m=0.76

     elif equipment=="Storage tank":
          capacity=volume
          if volume<=20:                     # small atmospheric tank (0.1-20 m3); below 0.1 m3 evaluated at 0.1 m3
               fm=fm/dictFMaterial_Others["Stainless steel"]   # base cost is for SS (low grade), Table 2.1; fM = 2.4 (Table 2.2)
               r_max=20
               r_min=0.1
               bsize=0.1
               Cb=3.28*10**3
               m=0.57
          elif 20<volume:
               r_max=200
               r_min=20
               bsize=5
               Cb=1.15*10**4
               m=0.53
          
     elif equipment=="Heater": 
          capacity=massflow
          if eqptype=="Steam boiler" and 50000<=massflow<=350000:    # package (fire-tube) boiler
               r_max=350000
               r_min=50000
               bsize=50000
               Cb=4.64*10**5
               m=0.96
          elif eqptype=="Steam boiler":                              # field-erected (water-tube) boiler, 10,000-800,000 kg/h
               r_max=800000
               r_min=10000
               bsize=20000
               Cb=3.28*10**5
               m=0.81

     elif equipment=="Dryer":
          if eqptype=="Drum":
               fm=fm/dictFMaterial_Others["Stainless steel"]   # base cost is for SS (low grade), Table 2.1; fM = 2.4 (Table 2.2)
               capacity=massflow
               r_max=3000
               r_min=700
               bsize=700
               Cb=2.3*10**5
               m=0.65

     if equipment in ["Packing (Structured)","Trays"]:
          # diameter-based correlations (per tray / per 5 m of packing): extrapolated outside 0.5-4 m
          num_f=1
          if capacity<r_min:
               warn_below(capacity, r_min, equipment, eqptype, "Smith", unit="m (diameter)", extrapolated=True)
          elif capacity>r_max:
               warn_above(capacity, r_max, equipment, eqptype, "Smith", unit="m (diameter)")
     else:
          if capacity<r_min:
               warn_below(capacity, r_min, equipment, eqptype, "Smith")
               capacity=r_min
               num_f=1
          elif r_min<=capacity<=r_max:
                    num_f=1
          elif r_max<capacity:
                    num_f=math.ceil(capacity/r_max)
                    warn_above(capacity, r_max, equipment, eqptype, "Smith", eqnum=num_f)
                    capacity=capacity/num_f
     
     f_scale=capacity/bsize   

     if equipment=="Packing (Structured)":
          Cp=Cb*(f_scale**m)*fm*fp*ft*height/5
     elif equipment=="Trays":
          Cp=Cb*(f_scale**m)*fm*fp*ft*num/10
     else: 
          Cp=Cb*(f_scale**m)*fm*fp*ft*num_f

     return round(Cp,1) if Cp > 0 else "Error: No data"

          
     



