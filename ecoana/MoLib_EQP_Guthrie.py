# *******Guthrie model(L. T. Biegler, 1997, "Systematic Methods of Chemical Process Design", 1st ed.)

import numpy as np
from math import pi
from numpy import log as ln
import math
from unit_parameters import *



# Available equipment & eqptype list for this model==============================================================================
lst_alltype={"Vessel/Tower":["Vertical vessel","Horizontal vessel"], 
          "Furnace":["Reformer furnace", "Pyrolysis furnace", "Nonreactive furnace"], 
          "Heater":["Diphenyl heater", "Cylindrical"], 
          "Heat exchanger (others)":["Air cooler"],
          "Heat exchanger (shell and tube)":["Kettle reboiler","Floating head", "U-tube (shell and tube)", "Fixed tube"], 
          "Pumps":["Centrifugal"], 
          "Compressor":["Centrifugal", "Reciprocating"]
          }

# equipment eqptype factor (fd): Furnace==============================================================================
fd_furnace={
     "Reformer furnace":1.35,
     "Pyrolysis furnace":1.1, 
     "Nonreactive furnace":1 }
# equipment eqptype factor (fd): Heater==============================================================================
fd_heater={
     "Diphenyl heater":1.33,
     "Cylindrical":1}
# equipment eqptype factor (fd): Heat exchanger (shell and tube)======================================================
fd_heatexchanger={
     "Kettle reboiler":1.35,
     "Floating head":1,
     "U-tube (shell and tube)":0.85,
     "Fixed tube":0.8}

# equipment material factor (fm)=================================================================================
fm_vessel={
     "Carbon steel":1, 
     "Stainless steel":3.67,
     "Monel":6.34, 
     "Nickel(alloy)":6.34,              #allowed
     "Inconel":6.34,                    #allowed
     "Hastelloy C":6.34,                #allowed
     "Titanium(alloy)":7.89}

fm_furnace={
     "Carbon steel":0,
     "Stainless steel":0.75,
     "Monel":0.35,
     "Nickel(alloy)":0.35,              #allowed
     "Hastelloy C":0.35,                #allowed
     "Inconel":0.35}

fm_heater={
     "Carbon steel":0,
     "Stainless steel":0.5,
     "Hastelloy C":0.45                # allowed (Cr-Mo alloy)
     }                

# available material factor set for heat exchanger area <=100
fm_heatexchanger_100={
     "CS shell/CS tube":1,
     "CS shell/Cu tube":1.05,
     "CS shell/SS tube":1.54,
     "SS shell/SS tube":2.5,
     "CS shell/Mo(alloy) tube":2,
     "CS shell/Ti(alloy) tube":4.1,
     "Ti(alloy) shell/Ti(alloy) tube":10.28}
# available for area <=500
fm_heatexchanger_500={
     "CS shell/CS tube":1,
     "CS shell/Cu tube":1.1,
     "CS shell/SS tube":1.78,
     "SS shell/SS tube":3.1,
     "CS shell/Mo(alloy) tube":2.3,
     "CS shell/Ti(alloy) tube":5.2,
     "Ti(alloy) shell/Ti(alloy) tube":10.6}
# available for area <=1000
fm_heatexchanger_1000={
     "CS shell/CS tube":1,
     "CS shell/Cu tube":1.15,
     "CS shell/SS tube":2.25,
     "SS shell/SS tube":3.26,
     "CS shell/Mo(alloy) tube":2.5,
     "CS shell/Ti(alloy) tube":6.15,
     "Ti(alloy) shell/Ti(alloy) tube":10.75}
# available for area <=5000
fm_heatexchanger_5000={
     "CS shell/CS tube":1,
     "CS shell/Cu tube":1.3,
     "CS shell/SS tube":2.81,
     "SS shell/SS tube":3.75,
     "CS shell/Mo(alloy) tube":3.1,
     "CS shell/Ti(alloy) tube":8.95,
     "Ti(alloy) shell/Ti(alloy) tube":13.05}
fm_hexelse={
     "Carbon steel":1, 
     "Stainless steel":3.67, 
     "Monel":6.34, 
     "Nickel(alloy)":6.34,              #allowed
     "Inconel":6.34,                    #allowed
     "Hastelloy C":6.34,                #allowed
     "Titanium(alloy)":7.89
                }
fm_pump={
     "Cast iron":1,
     "Carbon steel":1,
     "Stainless steel":1.93,
     "Hastelloy C":2.89,
     "Monel":3.23,
     "Inconel":3.23,                    #allowed
     "Nickel(alloy)":3.48,
     "Hastelloy C":3.48,               #allowed
     "Titanium(alloy)":8.98
              }

#Material parameters(fm) mapping=============================================================================================
lst_FMaterial={
     "Vessel/Tower":fm_vessel, 
     "Furnace":fm_furnace, 
     "Heater":fm_heater, 
     "Heat exchanger (others)":fm_hexelse,
     "Heat exchanger (shell and tube)":fm_heatexchanger_100, 
     "Pumps":fm_pump, 
     "Compressor":{}    # No material variable requires for cost estimation

}

def eqpcomo_Guthrie(equipment,material,eqptype,pressure,Pout,volume,power,volflow,massflow,area,packsize,height,diameter,thick,temperature,num,drive):
     C0=0
     Cb=0   
     fm=1
     fp=1
     # Unit normalize
     pressure=pressure*unit_psi
     Pout=Pout*unit_psi
     height=height*unit_ft
     diameter=diameter*unit_ft
     area=area*unit_ft2
     # Error message: Not available equipment spec. for model supporting list & Material factor mapping
     eqp_type_list=lst_alltype[equipment]
     eqp_mat_list=lst_FMaterial[equipment].keys()
     if eqptype not in eqp_type_list:
          return(print(f"Error: The selected equipment type '{eqptype}' is not available for '{equipment}' in the cost estimation model. Available types for '{equipment}': {eqp_type_list}"))  
     if equipment== "Compressor":
          fm=1
     elif material not in eqp_mat_list:
          return(f"Error: The selected equipment material '{material}' is not available for '{equipment}, {eqptype}' in the cost estimation model. Available materials: {list(eqp_mat_list)}")
     else:
          fm=lst_FMaterial[equipment][eqptype][material]

     if equipment=="Vessel/Tower":  
     #elif pressure > 1000:
          #return("Out of capacity - Pressure too high")
          if pressure<=50:
               fp=1
          elif 50<pressure<1000:
               fp=0.000001*pressure**2+0.0003*pressure+1.0136
          elif 1000<=pressure: #<=1000:
               fp=2.5
          # Material and Pressure factor (MPF)
          mpf=fm*fp

          if eqptype=="Vertical vessel":
               C0=1000
               Lmax=100
               Lmin=4
               L0=4
               D0=3
               a=0.81
               b=1.05
               eqnum=math.ceil(height/Lmax)
               if height <=Lmin:
                    L_input=Lmin
               elif height>Lmin:
                    L_input=height/eqnum
               C=C0*((L_input/L0)**a)*((diameter/D0)**b)
               Cb=mpf*C*eqnum
               return round(Cb,0)

          elif eqptype=="Horizontal vessel":
               C0=690
               Lmax=100
               Lmin=4
               L0=4
               D0=3
               a=0.78
               b=0.98
               eqnum=math.ceil(height/Lmax)
               if height <=Lmin:
                    L_input=Lmin
               elif height>Lmin:
                    L_input=height/eqnum
               
               C=C0*((L_input/L0)**a)*((diameter/D0)**b)
               Cb=mpf*C*eqnum
               return round(Cb,0)

     elif equipment=="Furnace":
     #elif pressure > 1000:
          #return("Out of capacity - Pressure too high")
          fd=fd_furnace[eqptype]
          if pressure<=500:
               fp=0
          elif 500<pressure<=1000:
               fp=0.1
          elif 1000<pressure<=1500:
               fp=0.15
          elif 1500<pressure<=2000:
               fp=0.25
          elif 2000<pressure<=2500:
               fp=0.4
          elif 2500<pressure: #<=3000:
               fp=0.6
          mpf=fm+fp+fd

          C0=100*1000
          S=power*unit_mmbtu
          S0=30
          Smax=300
          Smin=10
          a=0.83
          eqnum=math.ceil(S/Smax)
          if S<=Smin:
               S_input=Smin
          else:
               S_input=S/eqnum
          C=C0*(S_input/S0)**a
          Cb=mpf*C*eqnum
          return round(Cb,0)
               
     elif equipment=="Heater":  
     #elif pressure > 1500:
          #return("Out of capacity - Pressure too high")
          fd=fd_heater[eqptype]
          if pressure<=500:
               fp=0
          elif 500<pressure<=1000:
               fp=0.15
          elif 1000<pressure: #<=1500:
               fp=0.2
          mpf=fm+fp+fd

          C0=20*1000
          S=power*unit_mmbtu
          S0=5
          Smax=40
          Smin=1
          a=0.77
          eqnum=math.ceil(S/Smax)
          if S<=Smin:
               S_input=Smin
          else:
               S_input=S/eqnum
          C=C0*(S_input/S0)**a
          Cb=mpf*C*eqnum
          return round(Cb,0)

     elif equipment=="Heat exchanger (shell and tube)":
     #elif pressure > 1000:
          #return("Out of capacity - Pressure too high")
          if area <=100:
               fm=fm_heatexchanger_100[material]
          elif 100<area <=500:
               fm=fm_heatexchanger_500[material]
          elif 500<area <=1000:
               fm=fm_heatexchanger_1000[material]
          elif 1000<area: #<=5000:
               fm=fm_heatexchanger_5000[material]
          fd=fd_heatexchanger[eqptype]
          if pressure<=150:
               fp=0
          elif 150<pressure<1000:
               fp=0.3155*math.log(pressure)-1.6279
          elif 1000<=pressure: #<=1000:
               fp=0.55
          mpf=fm*(fp+fd)
          if area<=100:
               C0=0.3*1000
               S=area
               S0=5.5
               Smax=100
               Smin=2
               a=0.024
          elif 100<area:
               C0=5*1000
               S=area
               S0=400
               Smax=10000
               Smin=100
               a=0.65
          eqnum=math.ceil(S/Smax)
          if S<=Smin:
               S_input=Smin
          else:
               S_input=S/eqnum
          C=C0*(S_input/S0)**a
          Cb=mpf*C*eqnum
          return round(Cb,0)

     elif equipment=="Heat exchanger (others)":
     #elif pressure > 1000:
          #return("Out of capacity - Pressure too high")
          if pressure<=150:
               fp=0
          elif 150<pressure<=300:
               fp=0.1
          elif 300<pressure<=400:
               fp=0.25
          elif 400<pressure<=800:
               fp=0.52
          elif 800<pressure: #<=1000:
               fp=0.55
          mpf=fm*fp
          C0=3*1000
          S=area/15.5
          S0=200
          Smax=10000
          Smin=100
          a=0.82
          eqnum=math.ceil(S/Smax)
          if S<=Smin:
               S_input=Smin
          else:
               S_input=S/eqnum

          C=C0*(S_input/S0)**a
          Cb=mpf*C*eqnum
          return round(Cb,0)

     elif equipment=="Pumps":
          volflow=volflow*unit_gal/60
          dP=abs(pressure-Pout)
          S=volflow*dP  #S=C/H factor(gpm*psi)  
          #elif pressure > 1000:
               #return("Out of capacity - Pressure too high")   
          if pressure<=150:
               fo=1
          elif 150<pressure<=1000:
               fo=0.000002*pressure**2+0.0004*pressure+0.9067
          elif 1000<pressure: #<=1000:
               fo=2.9
          mpf=fm*fo

          if S<=2000:
               C0=0.39*1000
               S0=10
               Smax=2000
               Smin=10
               a=0.17
          elif 2000<S<=20000:
               C0=0.65*1000
               S0=2000
               Smax=20000
               Smin=2000
               a=0.36
          elif 20000<S: #<=200000:
               C0=1.5*1000
               S0=20000
               Smax=200000
               Smin=20000
               a=0.64
          eqnum=math.ceil(S/Smax)
          if S<=Smin:
               S_input=Smin
          else:
               S_input=S/eqnum
          C=C0*(S_input/S0)**a
          Cb=mpf*C*eqnum
          return round(Cb,0)

     elif equipment=="Compressor":
          power=power*unit_hph
          S=power  
          if eqptype =="Centrifugal":
               if drive in ["Electric-explosion proof","Electric-totally enclosed", "Electric-open/drip proof"]:
                    fd=1
               elif drive in ["Gas turbine", "Steam turbine", "Intern comb.engine"]:
                    fd=1.15
               elif drive not in ["Gas turbine", "Steam turbine", "Intern comb.engine","Electric-explosion proof","Electric-totally enclosed", "Electric-open/drip proof" ]:
                    return(print(f"Error: The selected driver type '{drive}' is not available in this model. Available driver types: ['Gas turbine', 'Steam turbine', 'Intern comb.engine','Electric-explosion proof','Electric-totally enclosed', 'Electric-open/drip proof' ]"))
          elif eqptype=="Reciprocating":
               if drive in ["Steam turbine"]:
                    fd=1.07
               elif drive in ["Electric-explosion proof","Electric-totally enclosed", "Electric-open/drip proof"]:
                    fd=1.29
               elif drive in ["Gas turbine","Intern comb.engine"]:
                    fd=1.82
               elif drive not in ["Steam turbine", "Electric-explosion proof","Electric-totally enclosed", "Electric-open/drip proof", "Gas turbine","Intern comb.engine"]:
                    return(print(f"Error: The selected driver type '{drive}' is not available in this model. Available driver types: ['Steam turbine', 'Electric-explosion proof','Electric-totally enclosed', 'Electric-open/drip proof', 'Gas turbine','Intern comb.engine']"))
          mpf=fd
          C0=23*1000
          S0=100
          Smax=10000
          Smin=30
          a=0.77
          eqnum=math.ceil(S/Smax)
          if S<=Smin:
               S_input=Smin
          else:
               S_input=S/eqnum
          
          C=C0*(S_input/S0)**a
          Cb=mpf*C*eqnum
          return round(Cb,0)

