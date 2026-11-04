# *******Guthrie model(L. T. Biegler, 1997, "Systematic Methods of Chemical Process Design", 1st ed.)

import numpy as np
from math import pi
from numpy import log as ln
import math
from .unit_parameters import *
import warnings
from .WarningMessage import warn_below, warn_above


DESIGN_PRESSURE_FACTOR=1.5        # Biegler et al. (1997) p.112-113: P_rated = 1.5 P_actual

def _step(P, table, name=""):
     """'up to' step table [(P_max, factor), ...]; above the last entry the last factor is used with a warning"""
     for pmax,f in table:
          if P<=pmax:
               return f
     warnings.warn(f"The design pressure {P:,.0f} psig exceeds the Guthrie {name} pressure-factor table ({table[-1][0]:,} psig); the last factor was used.", UserWarning, stacklevel=3)
     return table[-1][1]

tblFp_vessel=[(50,1.00),(100,1.05),(200,1.15),(300,1.20),(400,1.35),(500,1.45),(600,1.60),(700,1.80),(800,1.90),(900,2.30),(1000,2.50)]   # Table 4.2
tblFp_hex=[(150,0.00),(300,0.10),(400,0.25),(800,0.52),(1000,0.55)]                                                           # Table 4.4
tblFp_furnace=[(500,0.00),(1000,0.10),(1500,0.15),(2000,0.25),(2500,0.40),(3000,0.60)]                                         # Table 4.5
tblFp_heater=[(500,0.00),(1000,0.15),(1500,0.20)]                                                                             # Table 4.6

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
     "Stainless steel":3.67,            # SS 316, solid
     "SS clad":2.25,                    # SS 316, clad (Table 4.2)
     "Monel":6.34, 
     "Nickel(alloy)":6.34,              #allowed
     "Inconel":6.34,                    #allowed
     "Hastelloy C":6.34,                #allowed
     "Titanium(alloy)":7.89}

fm_furnace={                            # radiant-tube material, Table 4.5
     "Carbon steel":0,
     "Cr-Mo steel":0.35,
     "Stainless steel":0.75}

fm_heater={                             # tube material, Table 4.6
     "Carbon steel":0,
     "Cr-Mo steel":0.45,
     "Stainless steel":0.5
     }

# available material factor set for heat exchanger area <=100
fm_heatexchanger_100={
     "CS shell/CS tube":1,
     "CS shell/Cu tube":1.05,           # CS/brass
     "CS shell/SS tube":1.54,
     "SS shell/SS tube":2.5,
     "CS shell/Monel tube":2,
     "Monel shell/Monel tube":3.2,
     "CS shell/Ti(alloy) tube":4.1,
     "Ti(alloy) shell/Ti(alloy) tube":10.28}
# available for area <=500
fm_heatexchanger_500={
     "CS shell/CS tube":1,
     "CS shell/Cu tube":1.1,
     "CS shell/SS tube":1.78,
     "SS shell/SS tube":3.1,
     "CS shell/Monel tube":2.3,
     "Monel shell/Monel tube":3.5,
     "CS shell/Ti(alloy) tube":5.2,
     "Ti(alloy) shell/Ti(alloy) tube":10.6}
# available for area <=1000
fm_heatexchanger_1000={
     "CS shell/CS tube":1,
     "CS shell/Cu tube":1.15,
     "CS shell/SS tube":2.25,
     "SS shell/SS tube":3.26,
     "CS shell/Monel tube":2.5,
     "Monel shell/Monel tube":3.65,
     "CS shell/Ti(alloy) tube":6.15,
     "Ti(alloy) shell/Ti(alloy) tube":10.75}
# available for area <=5000
fm_heatexchanger_5000={
     "CS shell/CS tube":1,
     "CS shell/Cu tube":1.3,
     "CS shell/SS tube":2.81,
     "SS shell/SS tube":3.75,
     "CS shell/Monel tube":3.1,
     "Monel shell/Monel tube":4.25,
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
     "Copper(alloy)":1.28,              # bronze (Table 4.8)
     "Carbon steel":1,                  #allowed
     "Stainless steel":1.93,
     "Hastelloy C":2.89,
     "Monel":3.23,
     "Inconel":3.23,                    #allowed
     "Nickel(alloy)":3.48,
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
          if equipment=="Pumps" and not Pout:
               return("Error: 'Pout_bar' (discharge pressure) is required for Guthrie pumps.")
          # Biegler/Guthrie factor tables are in psig; P_bar is taken as absolute pressure
          pressure=max(pressure*unit_psi-14.696,0)      # psig
          Pout=max(Pout*unit_psi-14.696,0)              # psig
          temperature_F=(temperature-273.15)*1.8+32 if temperature else None
          # design pressure for vessels, exchangers, furnaces and heaters: P_rated = 1.5 P_actual (Biegler, p. 112-113)
          P_design=DESIGN_PRESSURE_FACTOR*pressure
          height=height*unit_ft
          diameter=diameter*unit_ft
          area=area*unit_ft2
          # Error message: Not available equipment spec. for model supporting list & Material factor mapping
          eqp_type_list=lst_alltype[equipment]
          eqp_mat_list=lst_FMaterial[equipment].keys()
          if eqptype not in eqp_type_list:
               return((f"Error: The selected equipment type '{eqptype}' is not available for '{equipment}' in the cost estimation model. Available types for '{equipment}': {eqp_type_list}"))  
          if equipment== "Compressor":
               fm=1
          elif material not in eqp_mat_list:
               return(f"Error: The selected equipment material '{material}' is not available for '{equipment}, {eqptype}' in the cost estimation model. Available materials: {list(eqp_mat_list)}")
          else:
               fm = lst_FMaterial[equipment][material]

          if equipment=="Vessel/Tower":  
          #elif pressure > 1000:
               #return("Out of capacity - Pressure too high")
               fp=_step(P_design, tblFp_vessel, "vessel")
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
                         if height<Lmin: warn_below(height, Lmin, equipment, eqptype, "Guthrie", unit="ft (length)")
                         L_input=Lmin
                    elif height>Lmin:
                         if eqnum>=2: warn_above(height, Lmax, equipment, eqptype, "Guthrie", unit="ft (length)", eqnum=eqnum)
                         L_input=height/eqnum
                    if diameter<1: warn_below(diameter, 1, equipment, eqptype, "Guthrie", unit="ft (diameter)", extrapolated=True)
                    elif diameter>10: warn_above(diameter, 10, equipment, eqptype, "Guthrie", unit="ft (diameter)")
                    C=C0*((L_input/L0)**a)*((diameter/D0)**b)
                    Cb=mpf*C*eqnum
                    

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
                         if height<Lmin: warn_below(height, Lmin, equipment, eqptype, "Guthrie", unit="ft (length)")
                         L_input=Lmin
                    elif height>Lmin:
                         if eqnum>=2: warn_above(height, Lmax, equipment, eqptype, "Guthrie", unit="ft (length)", eqnum=eqnum)
                         L_input=height/eqnum
                    if diameter<1: warn_below(diameter, 1, equipment, eqptype, "Guthrie", unit="ft (diameter)", extrapolated=True)
                    elif diameter>10: warn_above(diameter, 10, equipment, eqptype, "Guthrie", unit="ft (diameter)")
                    
                    C=C0*((L_input/L0)**a)*((diameter/D0)**b)
                    Cb=mpf*C*eqnum

          elif equipment=="Furnace":
          #elif pressure > 1000:
               #return("Out of capacity - Pressure too high")
               fd=fd_furnace[eqptype]
               fp=_step(P_design, tblFp_furnace, "furnace")
               mpf=fm+fp+fd

               C0=100*1000
               S=power*unit_mmbtu
               S0=30
               Smax=300
               Smin=10
               a=0.83
               eqnum=math.ceil(S/Smax)
               if S<=Smin:
                    if S<Smin: warn_below(S, Smin, equipment, eqptype, "Guthrie", unit="(Guthrie size unit, US)")
                    S_input=Smin
               else:
                    if eqnum>=2: warn_above(S, Smax, equipment, eqptype, "Guthrie", unit="(Guthrie size unit, US)", eqnum=eqnum)
                    S_input=S/eqnum
               C=C0*(S_input/S0)**a
               Cb=mpf*C*eqnum
                    
          elif equipment=="Heater":  
          #elif pressure > 1500:
               #return("Out of capacity - Pressure too high")
               fd=fd_heater[eqptype]
               fp=_step(P_design, tblFp_heater, "fired heater")
               mpf=fm+fp+fd

               C0=20*1000
               S=power*unit_mmbtu
               S0=5
               Smax=40
               Smin=1
               a=0.77
               eqnum=math.ceil(S/Smax)
               if S<=Smin:
                    if S<Smin: warn_below(S, Smin, equipment, eqptype, "Guthrie", unit="(Guthrie size unit, US)")
                    S_input=Smin
               else:
                    if eqnum>=2: warn_above(S, Smax, equipment, eqptype, "Guthrie", unit="(Guthrie size unit, US)", eqnum=eqnum)
                    S_input=S/eqnum
               C=C0*(S_input/S0)**a
               Cb=mpf*C*eqnum

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
               fp=_step(P_design, tblFp_hex, "heat exchanger")
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
                    if S<Smin: warn_below(S, Smin, equipment, eqptype, "Guthrie", unit="(Guthrie size unit, US)")
                    S_input=Smin
               else:
                    if eqnum>=2: warn_above(S, Smax, equipment, eqptype, "Guthrie", unit="(Guthrie size unit, US)", eqnum=eqnum)
                    S_input=S/eqnum
               C=C0*(S_input/S0)**a
               Cb=mpf*C*eqnum

          elif equipment=="Heat exchanger (others)":
          #elif pressure > 1000:
               #return("Out of capacity - Pressure too high")
               #if pressure<=150:
               #     fp=0
               # Biegler gives no material or pressure factors for air coolers; by analogy with Table 4.4 the
               # exchanger pressure adders are added to a design factor of 1 and multiplied by the material factor
               fp=_step(P_design, tblFp_hex, "air cooler")
               mpf=fm*(1+fp)
               C0=3*1000
               S=area/15.5       # Table 4.12: S = [calculated area (ft2)]/15.5
               S0=200
               Smax=10000
               Smin=100
               a=0.82
               eqnum=math.ceil(S/Smax)
               if S<=Smin:
                    if S<Smin: warn_below(S, Smin, equipment, eqptype, "Guthrie", unit="(Guthrie size unit, US)")
                    S_input=Smin
               else:
                    if eqnum>=2: warn_above(S, Smax, equipment, eqptype, "Guthrie", unit="(Guthrie size unit, US)", eqnum=eqnum)
                    S_input=S/eqnum

               C=C0*(S_input/S0)**a
               Cb=mpf*C*eqnum

          elif equipment=="Pumps":
               volflow=volflow*unit_gal/60
               dP=abs(pressure-Pout)
               S=volflow*dP  #S=C/H factor(gpm*psi)  
               #elif pressure > 1000:
                    #return("Out of capacity - Pressure too high")   
               # operating-limit factor Fo, Table 4.8: max. suction pressure 150/500/1000 psig and
               # max. temperature 250/550/850 F -> 1.0/1.5/2.9 (the more severe limit governs)
               lv_p=0 if pressure<=150 else (1 if pressure<=500 else 2)
               lv_t=0 if (temperature_F is None or temperature_F<=250) else (1 if temperature_F<=550 else 2)
               if pressure>1000 or (temperature_F is not None and temperature_F>850):
                    warnings.warn("The pump suction pressure/temperature exceeds the Guthrie operating limits (1000 psig, 850 F); Fo = 2.9 was used.", UserWarning, stacklevel=2)
               fo=[1.0,1.5,2.9][max(lv_p,lv_t)]
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
                    if S<Smin: warn_below(S, Smin, equipment, eqptype, "Guthrie", unit="(Guthrie size unit, US)")
                    S_input=Smin
               else:
                    if eqnum>=2: warn_above(S, Smax, equipment, eqptype, "Guthrie", unit="(Guthrie size unit, US)", eqnum=eqnum)
                    S_input=S/eqnum
               C=C0*(S_input/S0)**a
               Cb=mpf*C*eqnum

          elif equipment=="Compressor":
               power=power*unit_hph
               S=power  
               if eqptype =="Centrifugal":
                    # Table 4.9: centrifugal/motor 1.00, centrifugal/turbine 1.15
                    if drive in ["Electric-explosion proof","Electric-totally enclosed", "Electric-open/drip proof"]:
                         fd=1
                    elif drive in ["Gas turbine", "Steam turbine"]:
                         fd=1.15
                    else:
                         return(f"Error: The selected driver type '{drive}' is not available in this model. Available driver types: ['Gas turbine', 'Steam turbine', 'Electric-explosion proof','Electric-totally enclosed', 'Electric-open/drip proof' ]")
               elif eqptype=="Reciprocating":
                    # Table 4.9: reciprocating/steam 1.07, reciprocating/motor 1.29, reciprocating/gas engine 1.82
                    if drive in ["Steam turbine"]:
                         fd=1.07
                    elif drive in ["Electric-explosion proof","Electric-totally enclosed", "Electric-open/drip proof"]:
                         fd=1.29
                    elif drive in ["Intern comb.engine"]:
                         fd=1.82
                    else:
                         return(f"Error: The selected driver type '{drive}' is not available in this model. Available driver types: ['Steam turbine', 'Electric-explosion proof','Electric-totally enclosed', 'Electric-open/drip proof', 'Intern comb.engine']")
               mpf=fd
               C0=23*1000
               S0=100
               Smax=10000
               Smin=30
               a=0.77
               eqnum=math.ceil(S/Smax)
               if S<=Smin:
                    if S<Smin: warn_below(S, Smin, equipment, eqptype, "Guthrie", unit="(Guthrie size unit, US)")
                    S_input=Smin
               else:
                    if eqnum>=2: warn_above(S, Smax, equipment, eqptype, "Guthrie", unit="(Guthrie size unit, US)", eqnum=eqnum)
                    S_input=S/eqnum
               
               C=C0*(S_input/S0)**a
               Cb=mpf*C*eqnum

          return(round (Cb,0))
          



