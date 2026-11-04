# *******Peters model, (M.S. Peters, K.D. Timmerhaus, R.E. West, 2003, “Plant Design and Economics for Chemical Engineers”, 5th ed.)********************
import numpy as np
from math import pi
import math
import warnings
from .unit_parameters import *
from .peters_digitized import PETERS_DIGITIZED
from .WarningMessage import warn_below, warn_above

# Material density (density unit=kg/m3) ===================================================================================================================
dictMatDensity={
     "Carbon steel":7810,
     "Stainless steel":7930,
     "Stainless steel(316)":7980,
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
dictMaterial_pump = {             # centrifugal pumps, Fig. 12-23 (relative to cast iron)
    "Cast iron":1,
    "Carbon steel":1.8,           # cast steel
    "Stainless steel":2.4,
    "Nickel(alloy)":5.0,
    "Monel":5.0,       #allowed
    "Inconel":5.0,     #allowed
    "Hastelloy C":5.0  #allowed
    }
dictMaterial_recpump = {"Cast iron":1, "Carbon steel":1, "Stainless steel":1, "Stainless steel(316)":1}   # Fig. 12-21: material selects the curve
# Material factor(fm): "Vessel/Tower" =====================================================================================================================
dictMaterial_vessel = {          # horizontal vessels, Fig. 12-54 (relative to carbon steel)
     "Carbon steel":1,
     "Nickel(alloy)":7.4,
     "Monel":7.4,       #allowed
     "Inconel":7.4,     #allowed
     "Hastelloy C":7.4,  #allowed
     "Stainless steel":3,
     "Stainless steel(316)":3
    }
# vertical vessels (columns), Fig. 15-10: material selects the weight-based curve; Ni alloys = CS curve x 7.4 (Fig. 15-11)
dictMaterial_vvessel = {"Carbon steel":1, "Stainless steel":1, "Stainless steel(316)":1,
                        "Nickel(alloy)":7.4, "Monel":7.4, "Inconel":7.4, "Hastelloy C":7.4}
# Material factor(fm): "Storage tank" =====================================================================================================================
dictMaterial_tank = {   # field-erected tanks, Figs. 12-55/12-56: CS, 304 SS and 316 SS curves (small) or factors (large);
     "Carbon steel": 1,  # other alloys relative to 316 SS (Fig. 12-55 table)
     "Stainless steel": 1,
     "Stainless steel(316)": 1,
     "Monel": 2.0,
     "Nickel(alloy)":2.0,
     "Inconel":2.0,
     "Hastelloy C":3.8,
     "Titanium(alloy)":3.2
    }

#==================================Digitized Peters correlations (v1.0.0 additions)==========================================================================
# All curves below were digitized from Peters, Timmerhaus & West (5th ed.) figures (Jan. 2002 cost basis) and fitted
# either as a power law  C = a*X^b  or as a log-polynomial  C = exp(c0 + c1*lnX + c2*(lnX)^2 + ...).
# Max. deviation from the digitized curve is reported next to each fit.

# Pressure factor tables (pressure in kPa, factor) ---------------------------------------------------------------------------
tblP_doublepipe=[(4135,1.0),(6205,1.1),(10340,1.3),(20680,2.0),(30000,3.0)]           # Fig. 14-15 / 14-16
tblP_spiraltube=[(200,1.0),(10000,1.05),(20000,1.10),(30000,1.15),(40000,1.20)]        # Fig. 14-26 (spiral)
tblP_scrapedwall=[(200,1.0),(10000,1.3),(20000,2.4),(30000,4.5)]                       # Fig. 14-26 (scraped wall)
tblP_vaporizer=[(505,1.6),(1115,3.2),(2130,4.6),(4150,8.7),(16300,12.2),(30000,15.8)]  # Fig. 14-32 (base curve below 505 kPa)
tblP_evaporator=[(1035,1.0),(4135,1.1),(5170,1.3),(10340,2.0),(15300,3.0)]             # Fig. 14-33

# Material factor(fm): scraped wall / spiral tube exchangers (Fig. 14-26) ----------------------------------------------------
dictMaterial_hex_scraped = {
        "CS shell/CS tube":1,
        "CS shell/Cu tube":1.25,
        "CS shell/SS tube":2.3,
        "CS shell/Ni(alloy) tube":2.8,
        "SS shell/SS tube":3.0,
        "CS shell/Ti(alloy) tube":7.2,
    }
# Double-pipe / multiple-pipe exchangers: material selects the curve (Fig. 14-15, 14-16) ------------------------------------
dictMaterial_hex_pipe = {"CS shell/CS tube":1, "CS shell/Cu tube":1, "CS shell/SS tube":1}   # Cu tube = Admiralty tube
# Spiral plate (Fig. 14-27, same table as flat plate) ----------------------------------------------------------------------
dictMaterial_spiralplate = dictmaterial_hexelse["Flat plate"]
# Evaporators (Fig. 14-33) -------------------------------------------------------------------------------------------------
dictMaterial_evap = {"Carbon steel":1, "Copper(alloy)":1.5, "Stainless steel":2.1, "Nickel(alloy)":2.5,
                     "Monel":2.5, "Inconel":2.5, "Hastelloy C":2.5}   #allowed: Ni alloys
# Vaporizers (Fig. 14-32) ---------------------------------------------------------------------------------------------------
dictMaterial_vapor = {"Carbon steel":1, "SS clad":1.6, "Glass-lined steel":2.0, "Stainless steel":2.0, "Nickel(alloy)":5.0,
                      "Monel":5.0, "Inconel":5.0, "Hastelloy C":5.0}   #allowed: Ni alloys
# Packing (Fig. 15-14) ------------------------------------------------------------------------------------------------------
dictMaterial_packing = {"Carbon steel":1.2, "Polyethylene(plastic)":1.0, "Ceramic":1.0, "Stainless steel":2.2, "Stainless steel(316)":4.2}
# Curve-selecting materials (factor 1; the material picks the curve) --------------------------------------------------------
dictMaterial_reactor   = {"Carbon steel":1, "Stainless steel":1, "Glass-lined steel":1}      # Fig. 13-15
dictMaterial_autoclave = {"Carbon steel":1, "Stainless steel":1, "Glass-lined steel":1}      # Fig. 13-16
dictMaterial_heatercyl = {"Carbon steel":1, "Cr-Mo steel":1, "Stainless steel":1}           # Fig. 14-38
dictMaterial_trays     = {"Carbon steel":1, "Stainless steel":1}                            # Fig. 15-13
dictMaterial_turbogrid = {"Stainless steel":1}                                              # Fig. 15-13

# Fitted curve coefficients -------------------------------------------------------------------------------------------------
# [a, b, Xmin, Xmax] for power laws, [coeffs..] for log-polynomials
coef_doublepipe={"CS shell/CS tube":[1040.2,0.0631,0.25,28], "CS shell/Cu tube":[1301.4,0.0736,0.25,19], "CS shell/SS tube":[1954.7,0.0710,0.25,14]}  # m2, max dev. 3%
coef_multipipe ={"CS shell/CS tube":[131.48,0.96967,10,200], "CS shell/Cu tube":[154.65,0.97724,10,200], "CS shell/SS tube":[229.41,0.96829,10,200]} # m2, max dev. 3%
coef_furnace   ={"Reformer furnace":[527.13,0.82253,2000,100000],      # SS tubes, 13,790 kPa
                 "Pyrolysis furnace":[299.95,0.85435,2000,100000],     # Cr-Mo tubes, 6,895 kPa
                 "Nonreactive furnace":[202.28,0.86456,2000,100000]}   # CS tubes, 3,450 kPa (process-fired heater); kW, max dev. 2%
coef_heatercyl ={"Stainless steel":[1475.09,0.67981,100,10000],        # 10,340 kPa
                 "Cr-Mo steel":[1420.14,0.66817,100,10000],            # 6,895 kPa
                 "Carbon steel":[936.32,0.67505,100,10000],            # 3,450 kPa
                 "Carbon steel(690kPa)":[175.13,0.76509,200,10000]}    # 690 kPa; kW, max dev. 2%
coef_reactor   ={"Carbon steel":[(345,11979.27,0.54455,0.1,15),(2070,14701.31,0.54672,0.1,15),(10350,96632.47,0.56997,0.4,2)],
                 "Stainless steel":[(345,21105.01,0.52961,0.1,15),(2070,38741.33,0.55499,0.4,4),(10350,145690.78,0.54434,0.4,2)],
                 "Glass-lined steel":[(690,29368.04,0.53375,0.1,15)]}  # (design P kPa, a, b, Vmin, Vmax) m3, max dev. 1%
coef_autoclave ={"Carbon steel":[33598.16,0.32246,1.2,13], "Stainless steel":[82485.55,0.21841,0.4,8], "Glass-lined steel":[34133.92,0.55185,0.4,22]}  # m3, max dev. 1%
coef_evap      ={"Agitated film(scraped wall)":[33309.89,0.56956,1,20], "Forced circulation(pumped)":[118370.79,0.69185,10,1000],
                 "Falling film":[34810.39,0.55796,30,300], "Vertical tube":[17793.13,0.52970,10,1000], "Horizontal tube":[9848.30,0.53868,8,1000]}  # m2, max dev. 3.5%
coef_vapor     ={"Jacketed vessels":[9.09364,0.08419,0.10230], "Internal coils/jackets":[9.34229,0.06549,0.12532]}   # log-poly, m3 (1-100), max dev. 3%
coef_fans      ={"Centrifugal straight-radial":[7.93178,0.26496,0.05083,0.01123], "Centrifugal backward-curved":[7.57538,0.24233,0.08697],
                 "Axial vane":[7.05558,0.29689,0.09631], "Axial tube":[6.58144,0.32277,0.09516]}   # log-poly, m3/s (0.5-50), max dev. 4%
coef_blower    ={"Centrifugal":[44934.23,0.62278,0.3,9], "Rotary straight-lobo":[41449.43,0.77599,0.05,1.6],
                 "Centrifugal(turbo)":[(21,16373.33,0.57046,0.05,5),(69,57729.85,0.58875,0.45,14),(207,169219.92,0.49141,1,7.5)]}  # m3/s, max dev. 3% (turbo: max discharge kPa)
coef_blower_hd =[7.90296,0.31168,0.18110,-0.10667,0.03514]   # heavy-duty blower, log-poly, m3/s (0.5-18), max dev. 5%
coef_trays     ={("Bubble cap","Stainless steel"):[7.05813,0.90671,0.51280], ("Valve","Stainless steel"):[6.90188,0.77237,0.49861],
                 ("Sieve","Stainless steel"):[6.80617,0.76174,0.24296], ("Bubble cap","Carbon steel"):[6.80617,0.76174,0.24296],
                 ("Turbogrid","Stainless steel"):[6.49025,0.76026,0.30329], ("Valve","Carbon steel"):[6.20831,0.79231,0.42828],
                 ("Sieve","Carbon steel"):[6.11163,0.75743,0.19229]}   # log-poly, $/tray vs diameter m (0.6-3.8), max dev. 5%
tray_quantity_factor={1:3.00,2:2.80,3:2.65,4:2.50,5:2.30,6:2.15,7:2.00,8:1.80,9:1.65,10:1.50,11:1.45,12:1.40,13:1.35,14:1.30,
                      15:1.25,16:1.20,17:1.15,18:1.10,19:1.05}   # 20-29: 1.00, 30-39: 0.98, 40+: 0.97
coef_packing   ={0.3:[150.25,0.96393,1.15,19.7], 0.5:[343.90,0.96530,1.55,24.6], 1.0:[1066.89,0.98984,2.5,36], 1.5:[1692.91,0.98326,2.9,39],
                 2.0:[2468.26,0.98316,3.6,45], 2.5:[4038.66,0.96188,4.3,49], 3.0:[6437.57,0.96689,5.3,58], 4.0:[11023.15,0.96004,6.6,62]}  # vs packed height m, max dev. 1.5%

# ---- Peters remaining refits (v1.0.0) ------------------------------------------------------------------------------------
coef_floatinghead={int(k):v for k,v in {"6895": [8.62802, -0.04664, 0.07553], "3105": [8.42567, -0.04649, 0.07492], "2070": [8.38222, -0.05347, 0.07335], "1035": [8.35276, -0.09362, 0.07696], "690": [7.79737, 0.08265, 0.05852]}.items()}   # Fig. 14-19, log-poly vs area m2 (10-1000) per design pressure kPa; max dev. 3%
coef_tank_small={"Carbon steel":[11.30307, -0.60812, 0.08749], "Stainless steel":[12.70942, -0.87466, 0.11409], "Stainless steel(316)":[12.6496, -0.80602, 0.10975]}   # Fig. 12-55, log-poly vs m3 (80-3000); max dev. 2%
coef_tank_large=[12.87169, -0.71739, 0.08038]                       # Fig. 12-56, CS, log-poly vs m3 (3000-50000); max dev. 1.5%
fm_tank_large={"Carbon steel":1, "Stainless steel":2.0, "Stainless steel(316)":3.0}   # Fig. 12-56 table
coef_recpump={"Cast iron":([12.865624, 1.697894, 0.160887, 0.005873],1e-4,0.0635), "Carbon steel":([12.539999, 1.365331, 0.086379],1e-3,0.02),
              "Stainless steel(316)":([13.881812, 1.796786, 0.17783, 0.006803],1e-4,0.058)}   # Fig. 12-21, log-poly vs m3/s; max dev. 3%
coef_recpump["Stainless steel"]=coef_recpump["Stainless steel(316)"]   # only a 316 SS curve is given
coef_vvessel={"Carbon steel":("pow",[245.59,0.6132],512,25000), "Stainless steel":("logpoly",[7.15913,0.35352,0.01775],250,41500),
              "Stainless steel(316)":("logpoly",[7.10166,0.39673,0.01617],110,41500)}   # Fig. 15-10, vs shell weight kg; max dev. 3% (CS), 2% (SS)
tblP_horvessel=[(101.3,1.0),(1035,1.6),(5000,3.2),(10000,4.6),(20000,8.7),(30000,12.2),(40000,15.8)]   # Fig. 12-54 (kPa abs); 1.0 at atmospheric
tblP_recpump=[(1035,1.0),(5000,1.6),(10000,1.8),(20000,2.1),(50000,2.4),(100000,2.7)]                    # Fig. 12-21
tblP_cenpump=[(1035,1.0),(5000,2.1),(10000,2.8),(20000,3.5),(30000,4.0)]                                  # Fig. 12-23, centrifugal

def _logpoly(c, x):
     lx=math.log(x)
     return math.exp(sum(ci*lx**i for i,ci in enumerate(c)))

def _size(capacity, capa_min, capa_max, equipment="", unit=""):
     # same convention as the other Peters correlations: below the lower limit -> evaluated at the lower limit,
     # above the upper limit -> identical parallel units
     if capacity<capa_min:
          warn_below(capacity, capa_min, equipment, None, "Peters", unit=unit)
          capacity=capa_min
     eqnum=math.ceil(capacity/capa_max)
     if eqnum>=2:
          warn_above(capacity, capa_max, equipment, None, "Peters", unit=unit, eqnum=eqnum)
     return eqnum, capacity/eqnum

def _pfactor(P_kPa, table, equipment=""):
     # piecewise-linear interpolation of a tabulated pressure factor; below the first entry -> first factor
     if P_kPa<=table[0][0]:
          return table[0][1]
     if P_kPa>table[-1][0]:
          warnings.warn(f"The pressure {P_kPa/unit_kPa:,.1f} bar exceeds the highest tabulated pressure for Peters {equipment} "
                        f"({table[-1][0]/unit_kPa:,.1f} bar); the factor at that pressure was used.", UserWarning, stacklevel=3)
          return table[-1][1]
     for (p0,f0),(p1,f1) in zip(table[:-1],table[1:]):
          if p0<=P_kPa<=p1:
               return f0+(f1-f0)*(P_kPa-p0)/(p1-p0)

#==================================Material parameters mapping=============================================================================================
# None: Peters gives no material adjustment for this equipment -> the material does not affect the cost (factor 1)
lst_FMaterial={
     "Turbines":{"Axial gas turbines":dictMaterial_turbine, "Radial expanders":dictMaterial_turbine, "Liquid expanders":dictMaterial_turbine},
     "Compressor":{"Centrifugal":dictMaterial_comp, "Reciprocating":dictMaterial_comp},
     "Heat exchanger (shell and tube)":{"Fixed tube":dictMaterial_hex, "U-tube (shell and tube)":dictMaterial_hex, "Floating head":dictMaterial_hex,
                                        "Double pipe":dictMaterial_hex_pipe, "Multiple pipe":dictMaterial_hex_pipe,
                                        "Scraped wall":dictMaterial_hex_scraped, "Spiral tube (shell and tube)":dictMaterial_hex_scraped},
     "Heat exchanger (others)":{"Gasket plate":dictmaterial_hexelse["Gasket plate"], "Flat plate":dictmaterial_hexelse["Flat plate"], "Air cooler":dictmaterial_hexelse["Air cooler"],
                                "Spiral plate":dictMaterial_spiralplate, "Welded plate":None},   # material factors depend on the type
     "Pumps":{"Centrifugal":dictMaterial_pump, "Reciprocating":dictMaterial_recpump},
     "Vessel/Tower":{"Horizontal vessel":dictMaterial_vessel, "Vertical vessel":dictMaterial_vvessel},
     "Storage tank":{"Open":dictMaterial_tank, "Cone roof":dictMaterial_tank, "Floating roof":dictMaterial_tank, "Spherical":dictMaterial_tank, "Gas holder":dictMaterial_tank},
     "Evaporator":{t:dictMaterial_evap for t in coef_evap},
     "Vaporizer":{"Jacketed vessels":dictMaterial_vapor, "Internal coils/jackets":dictMaterial_vapor},
     "Furnace":{t:None for t in coef_furnace},
     "Heater":{"Cylindrical":dictMaterial_heatercyl},
     "Reactor":{"Jacketed agitated":dictMaterial_reactor},
     "Autoclave":{"None":dictMaterial_autoclave},
     "Fans":{t:None for t in coef_fans},
     "Blower":{"Centrifugal":None, "Centrifugal(turbo)":None, "Rotary straight-lobo":None, "Heavy-duty":None},
     "Trays":{"Sieve":dictMaterial_trays, "Valve":dictMaterial_trays, "Bubble cap":dictMaterial_trays, "Turbogrid":dictMaterial_turbogrid},
     "Packing":{t:dictMaterial_packing for t in ["Raschig rings","Pall rings","Intalox saddles","Berl saddles","Cascade mini-rings"]}   # Fig. 15-14 does not distinguish ring/saddle shapes
}
lst_nontypeEq=["Autoclave"]

# Equipment from the second digitization batch (data in peters_digitized.py) ---------------------------------------------
def _digi_mat_table(spec):
     if not spec.get("mat"):
          return None
     tbl={m:1 for m in spec["mat"] if m!="*"}
     tbl.update(spec.get("fm") or {})
     return tbl
for _eq,_types in PETERS_DIGITIZED.items():
     lst_FMaterial.setdefault(_eq,{})
     for _t,_spec in _types.items():
          lst_FMaterial[_eq][_t]=_digi_mat_table(_spec)

def _curve(c, x):
     if c["form"]=="pow":
          return c["coef"][0]*x**c["coef"][1]
     return _logpoly(c["coef"], x)

def _digi_cost(equipment, eqptype, material, X, length, param_value):
     """Cost from a digitized Peters curve. X: size variable in the curve unit; length: conveyor length (m);
     param_value: conveyor width/diameter (m) or solids flow (kg/s)."""
     spec=PETERS_DIGITIZED[equipment][eqptype]
     if "pcurves" in spec:                                    # conveyors: cost vs length, parameter interpolated log-log
          pc={float(k):v for k,v in spec["pcurves"].items()}
          ps=sorted(pc)
          q=min(max(param_value,ps[0]),ps[-1])
          if q!=param_value:
               warnings.warn(f"The {spec['pname']} {param_value:,.3g} is outside the Peters {eqptype} curves ({ps[0]:g}-{ps[-1]:g}); the cost was evaluated at {q:g}.", UserWarning, stacklevel=3)
          def one(k):
               c=pc[k]; eqnum,xin=_size(length,c["range"][0],c["range"][1],eqptype,"m")
               return _curve(c,xin)*eqnum
          lo=max(k for k in ps if k<=q); hi=min(k for k in ps if k>=q)
          if lo==hi:
               return one(lo)
          w=(math.log(q)-math.log(lo))/(math.log(hi)-math.log(lo))
          return math.exp((1-w)*math.log(one(lo))+w*math.log(one(hi)))
     mat=spec.get("mat")
     key=next(iter(spec["curves"])) if not mat else mat.get(material, mat.get("*"))
     c=spec["curves"][key]
     lo_,hi_=c["range"]
     if spec["x"]=="diameter" and X>hi_:
          # a larger diameter cannot be represented by parallel units: extrapolate with the local slope at the limit
          warnings.warn(f"The diameter {X:,.2f} m exceeds the Peters {eqptype} curve ({hi_:g} m); the cost was extrapolated.", UserWarning, stacklevel=3)
          slope=(math.log(_curve(c,hi_))-math.log(_curve(c,hi_*0.95)))/(math.log(hi_)-math.log(hi_*0.95))
          return _curve(c,hi_)*(X/hi_)**max(slope,0)
     eqnum,xin=_size(X,lo_,hi_,eqptype,"")
     return _curve(c,xin)*eqnum


def eqpcomo_Peters(equipment,material,eqptype,pressure,Pout,volume,power,volflow,massflow,area,packsize,height,diameter,thick,temperature,num,drive,length=0):
     Cb=0    #2002 basis
     f_material=1
     f_pressure=1
     f_diameter=1
     # Error message: Not available equipment spec. for model supporting list & Material factor mapping
     if equipment in lst_nontypeEq:
          eqptype="None"
     eqp_type_list=lst_FMaterial[equipment].keys()

     if eqptype not in eqp_type_list:
          return(print(f"Error: The selected equipment type '{eqptype}' is not available for '{equipment}' in the cost estimation model. Available types for '{equipment}': {list(eqp_type_list)}"))  
     mat_table=lst_FMaterial[equipment][eqptype]
     if mat_table is None:          # no material adjustment in Peters for this equipment
          f_material=1
     elif material not in mat_table:
          return(f"Error: The selected equipment material '{material}' is not available for '{equipment}, {eqptype}' in the cost estimation model. Available materials: {list(mat_table.keys())}")
     else:
          f_material=mat_table[material]

     if equipment in PETERS_DIGITIZED:
          spec=PETERS_DIGITIZED[equipment][eqptype]
          xs={"massflow":(massflow/unit_sec,"massflow_kgph"),"power":(abs(power),"power_kW"),"volume":(volume,"vol_cum"),"area":(area,"area_sqm"),
              "diameter":(diameter,"diameter_m"),"volflow":(volflow/unit_sec,"volflow_cumph"),"length":(length,"length_m")}
          X,varname=xs[spec["x"]]
          if X is None or X<=0:
               return(print(f"Error: '{varname}' (> 0) is required for Peters '{equipment}, {eqptype}'."))
          pv=0
          if "param" in spec:
               pv,pname=xs[spec["param"]]
               if pv is None or pv<=0:
                    return(print(f"Error: '{pname}' (> 0) is required for Peters '{equipment}, {eqptype}' ({spec['pname']})."))
          Cb=_digi_cost(equipment,eqptype,material,X,X,pv)
          Cp=Cb*f_material

     elif equipment =="Storage tank":
          capacity=volume #unit=m3
          base_mat = material if material in ("Carbon steel","Stainless steel","Stainless steel(316)") else "Stainless steel(316)"
          f_alloy = 1 if base_mat==material else f_material      # other alloys: factor relative to 316 SS
          if capacity <=3000:   # small field-erected tank, Fig. 12-55 (CS / 304 SS / 316 SS curves)
               eqnum,capa_input=_size(capacity,80,3000,equipment,"m3")
               Cb=_logpoly(coef_tank_small[base_mat],capa_input)*eqnum
          else:                 # large field-erected tank, Fig. 12-56 (CS curve x material factor)
               eqnum,capa_input=_size(capacity,3000,50000,equipment,"m3")
               Cb=_logpoly(coef_tank_large,capa_input)*fm_tank_large[base_mat]*eqnum
          Cp=Cb*f_alloy

     elif equipment =="Turbines":
          capacity=abs(power) #unit=kW
          if eqptype=="Axial gas turbines":
               capa_min=100
               capa_max=4000
               if capacity<capa_min:
                    warn_below(capacity, capa_min, equipment, eqptype, "Peters")
                    capacity=capa_min
               eqnum=math.ceil(capacity/capa_max)
               if eqnum>=2: warn_above(capacity, capa_max, equipment, eqptype, "Peters", eqnum=eqnum)
               capa_input=capacity/eqnum
               Cb=(3167.9*capa_input**0.5989)*eqnum
               Cp=Cb*f_material
          elif eqptype in ["Radial expanders","Liquid expanders"]:   # Fig. 12-34, radial expander (gas and liquid)
               eqnum,capa_input=_size(capacity,100,1000,eqptype,"kW")
               Cb=(1310.39*capa_input**0.69387)*eqnum                # max dev. 1%
               Cp=Cb*f_material

     elif equipment=="Heat exchanger (others)":
          capacity=area #unit=m2
          if eqptype =="Gasket plate":
               capa_min=1
               capa_max=1500
               if capacity<capa_min:
                    warn_below(capacity, capa_min, equipment, eqptype, "Peters")
                    capacity=capa_min
               eqnum=math.ceil(capacity/capa_max)
               if eqnum>=2: warn_above(capacity, capa_max, equipment, eqptype, "Peters", eqnum=eqnum)
               capa_input=capacity/eqnum
               Cb=(12.228*capa_input+612.02)*eqnum
               Cp=Cb*f_material
          elif eqptype=="Flat plate": 
               capa_min=10     
               capa_max=1500
               if capacity<capa_min:
                    warn_below(capacity, capa_min, equipment, eqptype, "Peters")
                    capacity=capa_min
               eqnum=math.ceil(capacity/capa_max)
               if eqnum>=2: warn_above(capacity, capa_max, equipment, eqptype, "Peters", eqnum=eqnum)
               capa_input=capacity/eqnum
               Cb=(8501*capa_input**0.3605)*eqnum   # power-law fit to Peters Fig. 14-27 (flat plate, CS, 10-1500 m2)
               Cp=Cb*f_material
          elif eqptype=="Air cooler": 
               capa_min=3.5
               capa_max=10000
               if capacity<capa_min:
                    warn_below(capacity, capa_min, equipment, eqptype, "Peters")
                    capacity=capa_min
               eqnum=math.ceil(capacity/capa_max)
               if eqnum>=2: warn_above(capacity, capa_max, equipment, eqptype, "Peters", eqnum=eqnum)
               capa_input=capacity/eqnum
               Cb=(3406*capa_input**0.4367)*eqnum
               Cp=Cb*f_material
          elif eqptype=="Spiral plate":                         # Fig. 14-27, carbon steel, max. 2,000 kPa
               eqnum,capa_input=_size(capacity,1,200,eqptype,"m2")
               Cb=(4824.63*capa_input**0.44141)*eqnum                # max dev. 2%
               Cp=Cb*f_material
          elif eqptype=="Welded plate":                         # Fig. 14-25
               eqnum,capa_input=_size(capacity,1,1200,eqptype,"m2")
               Cb=(1939.0+27.543*capa_input**1.00194)*eqnum          # max dev. 2.5%
               Cp=Cb*f_material

     elif equipment =="Compressor":
          capacity=power # power unit = m3/s*kPa = kW
          if eqptype=="Centrifugal":
               capa_min=75
               capa_max=6000
               if capacity<capa_min:
                    warn_below(capacity, capa_min, equipment, eqptype, "Peters")
                    capacity=capa_min
               eqnum=math.ceil(capacity/capa_max)
               if eqnum>=2: warn_above(capacity, capa_max, equipment, eqptype, "Peters", eqnum=eqnum)
               capa_input=capacity/eqnum
               Cb=(-0.0185*capa_input**2 + 609.97*capa_input + 7616.3)*eqnum          
          elif eqptype=="Reciprocating" and drive not in ["Steam turbine","Electric-open/drip proof","Electric-explosion proof","Electric-totally enclosed"] :
               return(print(f"Error: The selected driver type '{drive}' is not available in this model. Available driver types: ['Steam turbine','Electric-open/drip proof','Electric-explosion proof','Electric-totally enclosed']"))
          elif eqptype=="Reciprocating" and drive=="Steam turbine":
               capa_min=75
               capa_max=6000
               if capacity<capa_min:
                    warn_below(capacity, capa_min, equipment, eqptype, "Peters")
                    capacity=capa_min
               eqnum=math.ceil(capacity/capa_max)
               if eqnum>=2: warn_above(capacity, capa_max, equipment, eqptype, "Peters", eqnum=eqnum)
               capa_input=capacity/eqnum
               Cb=(-0.0146*capa_input**2 + 672.09*capa_input + 4112)*eqnum
          elif eqptype=="Reciprocating" and drive in ["Electric-open/drip proof","Electric-explosion proof","Electric-totally enclosed"]:
               capa_min=75
               capa_max=6000
               if capacity<capa_min:
                    warn_below(capacity, capa_min, equipment, eqptype, "Peters")
                    capacity=capa_min
               eqnum=math.ceil(capacity/capa_max)
               if eqnum>=2: warn_above(capacity, capa_max, equipment, eqptype, "Peters", eqnum=eqnum)
               capa_input=capacity/eqnum
               Cb=(-0.0249*capa_input**2 + 813.46*capa_input + 15098)*eqnum
          
          Cp=Cb*f_material

     elif equipment=="Heat exchanger (shell and tube)" and eqptype in ["Double pipe","Multiple pipe","Scraped wall","Spiral tube (shell and tube)"]:
          capacity=area   #unit=m2
          P_kPa=pressure*unit_kPa
          if eqptype in ["Double pipe","Multiple pipe"]:            # Fig. 14-15, 14-16: tube material selects the curve
               a,b,capa_min,capa_max=(coef_doublepipe if eqptype=="Double pipe" else coef_multipipe)[material]
               f_pressure=_pfactor(P_kPa, tblP_doublepipe, eqptype)
               eqnum,capa_input=_size(capacity,capa_min,capa_max,eqptype,"m2")
               Cb=(a*capa_input**b)*eqnum
          elif eqptype=="Scraped wall":                             # Fig. 14-26, carbon steel
               f_pressure=_pfactor(P_kPa, tblP_scrapedwall, eqptype)
               eqnum,capa_input=_size(capacity,2,20,eqptype,"m2")
               Cb=(5562.63*capa_input**0.92545)*eqnum               # max dev. 2%
          elif eqptype=="Spiral tube (shell and tube)":             # Fig. 14-26, carbon steel
               f_pressure=_pfactor(P_kPa, tblP_spiraltube, eqptype)
               eqnum,capa_input=_size(capacity,0.1,45,eqptype,"m2")
               Cb=_logpoly([8.02662,0.56786,0.00773,0.00864],capa_input)*eqnum   # max dev. 3.5%
          Cp=Cb*f_material*f_pressure

     elif equipment=="Evaporator":                                  # Fig. 14-33, single effect
          a,b,capa_min,capa_max=coef_evap[eqptype]
          f_pressure=_pfactor(pressure*unit_kPa, tblP_evaporator, equipment)
          eqnum,capa_input=_size(area,capa_min,capa_max,eqptype,"m2")
          Cb=(a*capa_input**b)*eqnum
          Cp=Cb*f_material*f_pressure

     elif equipment=="Vaporizer":                                   # Fig. 14-32
          P_kPa=pressure*unit_kPa
          f_pressure=1 if P_kPa<tblP_vaporizer[0][0] else _pfactor(P_kPa, tblP_vaporizer, equipment)
          eqnum,capa_input=_size(volume,1,100,equipment,"m3")
          Cb=_logpoly(coef_vapor[eqptype],capa_input)*eqnum
          Cp=Cb*f_material*f_pressure

     elif equipment=="Furnace":                                     # Fig. 14-37, box type; tube material & design pressure fixed by type
          a,b,capa_min,capa_max=coef_furnace[eqptype]
          eqnum,capa_input=_size(abs(power),capa_min,capa_max,equipment,"kW")
          Cb=(a*capa_input**b)*eqnum
          Cp=Cb

     elif equipment=="Heater":                                      # Fig. 14-38, cylindrical direct-fired heater
          key=material
          if material=="Carbon steel" and pressure*unit_kPa<=690:  # low-pressure CS curve (690 kPa)
               key="Carbon steel(690kPa)"
          a,b,capa_min,capa_max=coef_heatercyl[key]
          Pmax={"Carbon steel":3450,"Cr-Mo steel":6895,"Stainless steel":10340}[material]
          if pressure*unit_kPa>Pmax:
               warnings.warn(f"The pressure {pressure:,.1f} bar exceeds the design pressure of the Peters cylindrical heater curve for {material} ({Pmax/unit_kPa:,.1f} bar).", UserWarning, stacklevel=2)
          eqnum,capa_input=_size(abs(power),capa_min,capa_max,equipment,"kW")
          Cb=(a*capa_input**b)*eqnum
          Cp=Cb

     elif equipment=="Reactor":                                     # Fig. 13-15, jacketed & stirred; design pressure selects the curve
          curves=coef_reactor[material]
          P_kPa=pressure*unit_kPa
          sel=[c for c in curves if P_kPa<=c[0]]
          if not sel:
               warnings.warn(f"The pressure {pressure:,.1f} bar exceeds the highest design pressure of the Peters reactor curves for {material} ({curves[-1][0]/unit_kPa:,.1f} bar); that curve was used.", UserWarning, stacklevel=2)
               sel=[curves[-1]]
          _,a,b,capa_min,capa_max=sel[0]
          eqnum,capa_input=_size(volume,capa_min,capa_max,equipment,"m3")
          Cb=(a*capa_input**b)*eqnum
          Cp=Cb

     elif equipment=="Autoclave":                                   # Fig. 13-16
          a,b,capa_min,capa_max=coef_autoclave[material]
          eqnum,capa_input=_size(volume,capa_min,capa_max,equipment,"m3")
          Cb=(a*capa_input**b)*eqnum
          Cp=Cb

     elif equipment=="Fans":                                        # Fig. 12-31, with electric drive
          eqnum,capa_input=_size(volflow/unit_sec,0.5,50,eqptype,"m3/s")          # m3/s
          Cb=_logpoly(coef_fans[eqptype],capa_input)*eqnum
          Cp=Cb

     elif equipment=="Blower":                                      # Fig. 12-32
          capacity=volflow/unit_sec                                 # m3/s
          if eqptype=="Heavy-duty":
               eqnum,capa_input=_size(capacity,0.6,18,eqptype,"m3/s")   # the fit has a shallow minimum just below 0.6 m3/s
               Cb=_logpoly(coef_blower_hd,capa_input)*eqnum
          else:
               if eqptype=="Centrifugal(turbo)":                    # max. discharge pressure (rise) selects the curve
                    dP_kPa=abs(Pout-pressure)*unit_kPa
                    curves=coef_blower[eqptype]
                    sel=[c for c in curves if dP_kPa<=c[0]]
                    if not sel:
                         warnings.warn(f"The pressure rise {dP_kPa/unit_kPa:,.2f} bar exceeds the maximum discharge pressure of the Peters turbo blower curves (2.07 bar); that curve was used.", UserWarning, stacklevel=2)
                         sel=[curves[-1]]
                    _,a,b,capa_min,capa_max=sel[0]
               else:
                    a,b,capa_min,capa_max=coef_blower[eqptype]
               eqnum,capa_input=_size(capacity,capa_min,capa_max,eqptype,"m3/s")
               Cb=(a*capa_input**b)*eqnum
          Cp=Cb

     elif equipment=="Trays":                                       # Fig. 15-13, cost per tray x quantity factor x number of trays
          if num is None or num<1:
               return(print("Error: The number of trays 'num' must be at least 1."))
          n=int(math.ceil(num))
          f_quantity=tray_quantity_factor.get(n, 1.00 if n<30 else (0.98 if n<40 else 0.97))
          d=min(max(diameter,0.6),3.8)                              # curves cover 0.6-3.8 m
          if d!=diameter:
               warnings.warn(f"The diameter {diameter:,.2f} m is outside the range of the Peters tray curves (0.6-3.8 m); the cost was evaluated at {d:,.2f} m.", UserWarning, stacklevel=2)
          Cb=_logpoly(coef_trays[(eqptype,material)],d)*f_quantity*n
          Cp=Cb

     elif equipment=="Packing":                                     # Fig. 15-14, incl. internal support and distributor
          Ds=sorted(coef_packing)
          d=min(max(diameter,Ds[0]),Ds[-1])
          if d!=diameter:
               warnings.warn(f"The diameter {diameter:,.2f} m is outside the range of the Peters packing curves (0.3-4.0 m); the cost was evaluated at {d:,.1f} m.", UserWarning, stacklevel=2)
          def _pack(D,H):
               a,b,hmin,hmax=coef_packing[D]
               eqnum,h=_size(H,hmin,hmax,"packing","m")
               return a*h**b*eqnum
          lo=max(x for x in Ds if x<=d); hi=min(x for x in Ds if x>=d)
          if lo==hi:
               Cb=_pack(lo,height)
          else:                                                     # log-log interpolation between the tabulated diameters
               w=(math.log(d)-math.log(lo))/(math.log(hi)-math.log(lo))
               Cb=math.exp((1-w)*math.log(_pack(lo,height))+w*math.log(_pack(hi,height)))
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
               if capacity<capa_min:
                    warn_below(capacity, capa_min, equipment, eqptype, "Peters")
                    capacity=capa_min
               eqnum=math.ceil(capacity/capa_max)
               if eqnum>=2: warn_above(capacity, capa_max, equipment, eqptype, "Peters", eqnum=eqnum)
               capa_input=capacity/eqnum
               Cb=(-0.0358*capa_input**2 + 81.708*capa_input + 3615.8)*eqnum

          elif eqptype=="U-tube (shell and tube)":
               capa_max=400    
               capa_min=3
               if capacity<capa_min:
                    warn_below(capacity, capa_min, equipment, eqptype, "Peters")
                    capacity=capa_min
               eqnum=math.ceil(capacity/capa_max)
               if eqnum>=2: warn_above(capacity, capa_max, equipment, eqptype, "Peters", eqnum=eqnum)
               capa_input=capacity/eqnum
               Cb=(-0.0873*capa_input**2 + 104.2*capa_input + 2292.6)*eqnum

          elif eqptype=="Floating head":
               # Fig. 14-19: separate curves for design pressures 690-6895 kPa (interpolated log-log); no extra pressure factor
               eqnum,capa_input=_size(capacity,10,1000,eqptype,"m2")
               P_kPa=pressure*unit_kPa
               ps=sorted(coef_floatinghead)
               Pq=min(max(P_kPa,ps[0]),ps[-1])
               if P_kPa>ps[-1]:
                    warnings.warn(f"The pressure {pressure:,.1f} bar exceeds the highest design pressure of Peters Fig. 14-19 (68.95 bar); that curve was used.", UserWarning, stacklevel=2)
               lo=max(p for p in ps if p<=Pq); hi=min(p for p in ps if p>=Pq)
               c_lo=_logpoly(coef_floatinghead[lo],capa_input); c_hi=_logpoly(coef_floatinghead[hi],capa_input)
               w=0 if lo==hi else (math.log(Pq)-math.log(lo))/(math.log(hi)-math.log(lo))
               Cb=math.exp((1-w)*math.log(c_lo)+w*math.log(c_hi))*eqnum
               f_pressure=1
          Cp=Cb*f_material*f_pressure

     elif equipment =="Pumps":          
          P_kPa=pressure*unit_kPa
          if eqptype=="Centrifugal":
               # Fig. 12-20 (capacity factor Q*P, m3/s*kPa); material and pressure factors of Fig. 12-23
               f_pressure=_pfactor(P_kPa, tblP_cenpump, "centrifugal pump")
               capacity=volflow/unit_sec*pressure*unit_kPa         #unit=m3/s*kPa
               capa_max=200
               capa_min=6
               if capacity<capa_min:
                    warn_below(capacity, capa_min, equipment, eqptype, "Peters")
                    capacity=capa_min
               eqnum=math.ceil(capacity/capa_max)
               if eqnum>=2: warn_above(capacity, capa_max, equipment, eqptype, "Peters", eqnum=eqnum)
               capa_input=capacity/eqnum
               Cb_fn=lambda q: 1.054*q**2 + 117.48*q + 8449
               Cb=Cb_fn(capa_input)*eqnum
               if eqnum>1:
                    Cb=max(Cb, Cb_fn(capa_max))      # the convex curve would make parallel units cheaper than one unit at the limit
          if eqptype=="Reciprocating":
               # Fig. 12-21: cast iron, cast steel and 316 SS curves; tabulated pressure factors
               f_pressure=_pfactor(P_kPa, tblP_recpump, "reciprocating pump")
               coef,qmin,qmax=coef_recpump[material]
               eqnum,capa_input=_size(volflow/unit_sec,qmin,qmax,eqptype,"m3/s")
               Cb=_logpoly(coef,capa_input)*eqnum
          Cp=Cb*f_material*f_pressure

     elif equipment =="Vessel/Tower":
          density=dictMatDensity.get(material, 8890)      # Ni-based alloys not listed: ~8890 kg/m3
          weight=pi*diameter*thick*height*density   #unit=kg
          
          if eqptype=="Vertical vessel":
               # Fig. 15-10: cost vs shell weight per material; the weight already reflects the pressure (wall
               # thickness), so no pressure factor is applied
               f_diameter=1
               f_pressure=1
               base_mat = material if material in coef_vvessel else "Carbon steel"     # Ni alloys: CS curve x 7.4 (Fig. 15-11)
               form,coef,wmin,wmax=coef_vvessel[base_mat]
               eqnum,capa_input=_size(weight,wmin,wmax,eqptype,"kg")
               Cb=(coef[0]*capa_input**coef[1] if form=="pow" else _logpoly(coef,capa_input))*eqnum


          if eqptype== "Horizontal vessel":
               # Fig. 12-54 pressure factors (kPa abs), 1.0 at atmospheric pressure, interpolated linearly
               f_pressure=_pfactor(pressure*unit_kPa, tblP_horvessel, "horizontal vessel")
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
               if capacity<capa_min:
                    warn_below(capacity, capa_min, equipment, eqptype, "Peters")
                    capacity=capa_min
               eqnum=math.ceil(capacity/capa_max)
               if eqnum>=2: warn_above(capacity, capa_max, equipment, eqptype, "Peters", eqnum=eqnum)
               capa_input=capacity/eqnum
               Cb=(2.954*capa_input**2 + 1150.3*capa_input + 4908.8)*eqnum
          
          Cp=Cb*f_material*f_pressure*f_diameter

     return round(Cp,0)



