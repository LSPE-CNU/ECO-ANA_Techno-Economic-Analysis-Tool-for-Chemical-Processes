import numpy as np
from unit_parameters import *
from math import pi
##================================== Providing Undefined Equipment Specifiaction; Default Values==================================

# Vessel thick estimation (Warren D. Seider, 2016), “Product and Process Design Principles: Synthesis, Analysis and Evaluation”, 4th ed.(529 p.)))
def vessel_thick(diameter_m,pressure_bar,temperature_K,material):
        # required pressure unit=psi, diameter unit=inch, temp unit=F
        pressure_psi=pressure_bar*unit_psi
        diameter_in=diameter_m*unit_in
        temperature_F=(temperature_K-273.15)*1.8 + 32

        if material =="Carbon steel":
                if temperature_F<=500:
                        stress=12.9*1000
                elif 500<temperature_F<=700:
                        stress=11.5*1000
                elif 700<temperature_F:
                        stress=5.9*1000

        if material =="Stainless steel":
                if temperature_F<=100:
                        stress=18.6*1000
                elif 100<temperature_F<=300:
                        stress=17.8*1000
                elif 300<temperature_F<=500:
                        stress=17.2*1000
                elif 500<temperature_F<=700:
                        stress=16.2*1000
                elif 700<temperature_F:
                        stress=12.3*1000
        else:
                if temperature_F<=100:
                        stress=20*1000
                elif 100<temperature_F<=300:
                        stress=16.5*1000
                elif 300<temperature_F<=500:
                        stress=14.3*1000
                elif 500<temperature_F<=700:
                        stress=13*1000
                elif 700<temperature_F:
                        stress=12.3*1000
                weld_eff=1        
                thickness_in=(pressure_psi*diameter_in)/(2*stress*weld_eff-1.2*pressure_psi)  #unit: inch
                thickness_m=thickness_in/unit_in   # unit: m

                return(thickness_m)

# Pump head estimation
def pump_head(power_kW,volflow_m3ph,massflow_kgph):
        if volflow_m3ph == 0:
                head=0
        if massflow_kgph==0:
                head=0
        else: 
                density=massflow_kgph/volflow_m3ph    # density unit= kg/m3
                if power_kW <=40:
                        a=0.293847527
                        x0=-0.004211716
                        FHD=(power_kW*a+x0)*(10**6)           # f(power)=Flowrate*head*density/10^6
                elif power_kW>40:
                        a=1.69045E-06
                        b=-0.001769222
                        c=0.578576695
                        x0=-9.53526825
                        FHD=( a*power_kW**3 + b*power_kW**2 + c*power_kW + x0 )*(10**6) 
                head_m=FHD/volflow_m3ph/density     
        return (head_m)

# Vessel volume estimation
def vessel_volume(diameter_m, height_m):
        volume=((diameter_m*0.5)**2*pi)*height_m     # volume unit = cbm
        return(volume)

# Material name mapping
def mat_mapping(material,*, strict: bool = False):
    if material is None:
        return None
    # 입력값 내 앞뒤 공백을 없애고 모두 소문자로 변환
    key = "".join(c for c in str(material) if c.isalnum()).lower()
    # Material list
    MATERIAL_GROUPS = {
        "Cast iron":["castiron","ci"],
        "Carbon steel":["carbonsteel", "cs"],  
        "Stainless steel":["stainlesssteel", "ss"],
        "Nickel(alloy)":["nickel", "ni", "nickelalloy", "nialloy"],
        "Copper(alloy)":["copper", "cu", "copperalloy", "cualloy"],
        "Titanium(alloy)":["titanium", "ti", "tialloy", "titaniumalloy"],
        "Aluminum(alloy)":["aluminum", "al", "aluminumalloy", "alalloy"],
        "Monel":["monel", "nicu", 'nicualloy'],              #Ni(60-70%)-Cu(30%) alloy
        "Inconel":["inconel", 'nicr','nicralloy'],          #Ni-Cr alloy
        "Hastelloy C":['hastelloy','hastelloyc','nimocr','nimocralloy', 'nicrmo', 'nicrmoalloy'],     #Ni-Mo-Cr alloy
        "Polyethylene(plastic)":["polyethylene", 'pe', 'plastic'],
        "Ceramic":["ceramic"],
        "Fiberglass":["fiberglass", "glass"],
        "PVC":["pvc", "polyvinylchloride"],

        # Shell & tube type Heat exchanger materials
        "CS shell/CS tube":["cscs", "csshellcstube"],
        "CS shell/Cu tube":["cscu", "csshellcutube"],
        "Cu shell/Cu tube":["cucu", "cushellcutube"],
        "CS shell/SS tube":["csss", "csshellsstube"],
        "SS shell/SS tube":["ssss", "ssshellsstube"],
        "CS shell/Ni(alloy) tube":["csni","csnickel","csnickelalloy","csnialloy","csshellnitube","csshellnickeltube","csshellnialloytube", "csshellnickelalloytube"],
        "Ni(alloy) shell/Ni(alloy) tube":["nini","nialloynialloy", "nishellnitube", "nialloyshellnialloytube"],
        "CS shell/Ti(alloy) tube":["csti","cstialloy", "csshelltitube", "csshelltialloytube"],
        "Ti(alloy) shell/Ti(alloy) tube":["titi","tialloytialloy","tishelltitube", "tialloyshell/tialloytube"],
        "CS shell/Mo(alloy) tube":["csmo","csmoalloy","csshellmotube", "csshellmoalloytube"],
        "CS shell/Al(alloy) tube":["csal","csalalloy","csshellaltube", "csshellalalloytube"]
                                        }

    material_aliases = {
        alias: standard
        for standard, aliases in MATERIAL_GROUPS.items()
        for alias in aliases
    }

    if key in material_aliases:
        return material_aliases[key]

    if strict:
        raise ValueError(f"Unknown material: {material!r}")
    return str(material).strip()
    
def vessel_weight():
     dictMatDensity={
          "Carbon steel":7810,
          "Stainless steel":7930,
          "Titanium": 4507,
          "Monel":8800,
          "Inconel":8442.4,
          "Nickel":8900,
          "Ni alloy clad":8900,
          "Ti clad":4507,
          "SS clad":7930
          }  #density unit=kg/m3
       