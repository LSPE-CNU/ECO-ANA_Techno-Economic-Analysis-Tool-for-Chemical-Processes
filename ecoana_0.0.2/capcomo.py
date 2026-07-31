import numpy as np
import math

CAPCOMO_list=["Hill", "Guthrie", "Timms", "Garrett", "Petley", "Lange 1", "Lange 2"]

# Model name: [basis CE, basis year, Capital cost type]
CE_basis_dict={"Hill": [86.1,"1954 year basis", "Installed total equipment cost"],
               "Guthrie": [394.1,"2000 year basis", "Fixed capital investment"],
               "Timms": [358.2,"1992 year basis", "Total capital investment"],
               "Garrett": [478.6,"2006 year basis", "Inside battery limits"],
               "Petley": [323.7,"1987 year basis", "Inside battery limits"],
               "Lange 1": [359.2,"1993 year basis", "Total capital investment"],
               "Lange 2": [359.2,"1993 year basis", "Total capital investment"]
               }

#Model factor[process] - Guthrie===================================================================================================
Cbase_Guthrie={"Acetic acid":8,
               "Acetone":33,
               "Ammonia":29,
               "Ammonium nitrate":6,
               "Butanol":48,
               "Chlorine":33,
               "Ethylene":16,
               "Ethylene oxide":59,
               "Formaldehyde":19,
               "Glycol":18,
               "Hydrofluoric acid":10,
               "Methanol":15,
               "Nitric acid":8,
               "Phosphoric acid":4,
               "Polyethylene":19,
               "Propylene":4,
               "Sulfuric acid":4,
               "Urea":10
               }
Qbase_Guthrie={"Acetic acid":9000,
               "Acetone":90000,
               "Ammonia":90000,
               "Ammonium nitrate":90000,
               "Butanol":45000,
               "Chlorine":45000,
               "Ethylene":45000,
               "Ethylene oxide":45000,
               "Formaldehyde":9000,
               "Glycol":4500,
               "Hydrofluoric acid":9000,
               "Methanol":55000,
               "Nitric acid":90000,
               "Phosphoric acid":4500,
               "Polyethylene":4500,
               "Propylene":9000,
               "Sulfuric acid":90000,
               "Urea":55000
               }
n_Guthrie={"Acetic acid":0.68,
               "Acetone":0.45,
               "Ammonia":0.53,
               "Ammonium nitrate":0.65,
               "Butanol":0.4,
               "Chlorine":0.45,
               "Ethylene":0.83,
               "Ethylene oxide":0.78,
               "Formaldehyde":0.55,
               "Glycol":0.75,
               "Hydrofluoric acid":0.68,
               "Methanol":0.6,
               "Nitric acid":0.6,
               "Phosphoric acid":0.6,
               "Polyethylene":0.65,
               "Propylene":0.7,
               "Sulfuric acid":0.65,
               "Urea":0.7
               }
process_Guthrie={"Acetic acid":"Methanol and CO-catalytic",
               "Acetone":"Propylene-copper chloride",
               "Ammonia":"Steam reforming",
               "Ammonium nitrate":"Ammonia and nitric acid",
               "Butanol":"Propylene, CO, and H2O",
               "Chlorine":"Electrolysis of NaCl",
               "Ethylene":"Refinary gases",
               "Ethylene oxide":"Ethylene-catalytic",
               "Formaldehyde":"Methanol - catalytic",
               "Glycol":"Ethylene and chlorine",
               "Hydrofluoric acid":"Hydrogen fluoride and water",
               "Methanol":"CO2, natural gas, steam",
               "Nitric acid":"Ammonia-catalytic",
               "Phosphoric acid":"Calcium phosphate and H2SO4",
               "Polyethylene":"Ethylene-catalytic",
               "Propylene":"Refinery gases",
               "Sulfuric acid":"Sulfur-contact catalytic",
               "Urea":"Ammonia and CO2"
               }


#Model factor[prorcess]=[Qmin,Qmax,a,n,Qunitfactor] - Garrett===================================================================================================
Param_Garrett={
               "ABSResin (15%Rubber) (emulsion polymerization)":[50, 300, 12.146, 0.6, 0.002204623],
               "Acetic Acid (Cativa)":[500, 2000, 3.474, 0.6, 0.002204623],
               "Acetic Acid (Low Water Methanol Carbonylation)":[500, 2000, 2.772, 0.6, 0.002204623],
               "Acrolein (propylene oxidation with Bi/Mo catalyst)":[30, 150, 6.809, 0.6, 0.002204623],
               "Adipic acid (phenol)":[300, 1000, 3.533, 0.6, 0.002204623],
               #"Alkylation (sulfuric acid effluent refrigeration)":[4000, 20000, 0.16, 0.6, 0],
               #"Alkylation (HF)":[5000, 12000, 0.153, 0.6, 0],
               "Allyl chloride (propylene chlorination)":[80, 250, 7.581, 0.6, 0.002204623],
               "Alpha olefins (full-range, Chevron Phillips)":[400, 1200, 5.24, 0.6, 0.002204623],
               "Alpha olefins (full-range, Shell)":[400, 1000, 8.146, 0.6, 0.002204623],
               #"Benzene (Sulfolane extraction)":[50, 200, 7.793, 0.6, 0],
               #"Benzene (toluene hydrodealkylation)":[50, 200, 7.002, 0.6, 0],
               #"Benzene reduction (Bensat)":[8000, 15000, 0.0275, 0.6, 0],
               "Biodiesel(FAME) (vegetable oil)":[100, 500, 2.747, 0.6, 0.002204623],
               "bis-HET (Eastman Glycolysis)":[50, 200, 0.5, 0.6, 0.002204623],
               "BTX Aromatics (Cyclar)":[200000, 800000, 0.044, 0.6, 1],
               "BTX Aromatics (CCR Platforming)":[200000, 800000, 0.015, 0.6, 1],
               "Butadiene (extractive distillation)":[100, 500, 5.514, 0.6, 0.002204623],
               "Butadiene (Oxo-D plus extractive distillation)":[100, 500, 11.314, 0.6, 0.002204623],
               "Butene-1 (Alphabutol ethylene dimerization)":[5000, 30000, 0.0251, 0.6, 1],
               "Butene-1 (BP)":[20000, 80000, 0.169, 0.6, 1],
               "Caprolactam (nitration-grade toluene)":[40000, 120000, 0.321, 0.6, 1],
               #"Carbon monoxide (steam methane reforming)":[2000, 6000, 0.363, 0.6, 0],
               #"Catalytic Condensation (Gasoline Production)":[10000, 30000, 0.222, 0.6, 0],
               #"Catalytic reforming (CCR Platforming)":[15000, 60000, 0.179, 0.6, 0],
               #"Coking (Flexicoking including Fluid Coking)":[15000, 40000, 0.343, 0.6, 0],
               #"Coking (Selective Yield Delayed Coking)":[15000, 60000, 0.109, 0.68, 0],
               "Copolymer polypropylene (INNOVENE)":[300, 900, 3.43, 0.6, 0.002204623],
               "Copolymer polypropylene (Unipol)":[300, 900, 3.641, 0.6, 0.002204623],
               "Copolymer polypropylene (SPHERIPOL Bulk)":[300, 900, 3.649, 0.6, 0.002204623],
               "Copolymer polypropylene (BORSTAR)":[300, 900, 4.015, 0.6, 0.002204623],
               #"Crude distillation (D2000)":[150000, 300000, 0.151, 0.6, 0],
               "Cumene (Q-Max)":[150000, 450000, 0.012, 0.6, 1],
               "Cyclic Olefin Copolymer (Mitsui)":[60, 120, 12.243, 0.6, 0.002204623],
               "Cyclohexane (liq-phase hydrogenation of benzene)":[100000, 300000, 0.0061, 0.6, 1],
               #"Dewaxing (ISODEWAXING)":[6000, 15000, 0.256, 0.6, 0],
               "2,6-Dimethylnaphthalene (Methanol alkylation)":[50, 100, 7.712, 0.6, 0.002204623],
               "Dimethyl terephthalate (methanolysis)":[30, 80, 5.173, 0.6, 0.002204623],
               "Dimethyl terephthalate (Huels Oxidation)":[300, 800, 7.511, 0.6, 0.002204623],
               #"Ethanol (ethylene hydration)":[30, 90, 9.643, 0.6, 0],
               "Ethanol (fuel-grade) (Corn Dry Milling)":[100000, 300000, 0.0865, 0.6, 1],
               "Ethylbenzene (EBOne)":[300000, 700000, 0.0085, 0.6, 1],
               "Ethylene (ethane cracking)":[500, 2000, 9.574, 0.6, 0.002204623],
               "Ethylene (UOP Hydro MTO)":[500, 2000, 8.632, 0.6, 0.002204623],
               "Ethylene (light naphtha cracker)":[1000, 2000, 16.411, 0.6, 0.002204623],
               "Ethylene (ethane/propane cracker)":[1000, 2000, 7.878, 0.6, 0.002204623],
               "Ethylene (gas oil cracker)":[1000, 2000, 17.117, 0.6, 0.002204623],
               "Ethylene glycol (ethylene oxide hydrolysis)":[500, 1000, 5.792, 0.6, 0.002204623],
               "Expandable poly-styrene (suspension)":[50, 100, 3.466, 0.6, 0.002204623],
               "Fischer Tropsch (ExxonMobil)":[200000, 700000, 0.476, 0.6, 1],
               #"Fluid catalytic cracking (KBR)":[20000, 60000, 0.21, 0.6, 0],
               #"Fluid catalytic cracking (power recovery)":[20000, 60000, 0.302, 0.6, 0],
               #"Gas to liquids (Syntroleum)":[30000, 100000, 2.279, 0.6, 0],
               #"Gas sweetening (Amine Guard FS to pipeline spec)":[300, 800, 0.386, 0.6, 0],
               #"Gasification (GE Gasification Process Mayacrude)":[7000, 15000, 0.681, 0.6, 0],
               #"Gasoline desulfurization (Prime-Gþ)":[7000, 15000, 0.042, 0.58, 0],
               "Glucose(40%Solution) (basic wet cornmilling)":[300, 800, 3.317, 0.6, 0.002204623],
               "HDPE Pellets (BP Gas Phase)":[300, 700, 3.624, 0.6, 0.002204623],
               "HDPE Pellets (Phillips Slurry)":[300, 700, 3.37, 0.6, 0.002204623],
               "HDPE Pellets (Zeigler Slurry)":[300, 700, 4.488, 0.6, 0.002204623],
               "High impact polystyrene (bulk polymerization)":[70, 160, 2.97, 0.6, 0.002204623],
               #"Hydrocracking (ISOCRACKING)":[20000, 45000, 0.221, 0.6, 0],
               #"Hydrocracking (Unicracking, distillate)":[20000, 45000, 0.136, 0.66, 0],
               #"Hydrocracking (Axens)":[20000, 45000, 0.198, 0.6, 0],
               #"Hydrogen (steam methane reforming)":[10, 50, 1.759, 0.79, 0],
               #"Hydrotreating (Unionfining)":[10000, 40000, 0.0532, 0.68, 0],
               #"Isomerization (Once-through Penex)":[8000, 15000, 0.0454, 0.6, 0],
               #"Isomerization (Penex-Molex)":[8000, 15000, 0.12, 0.6, 0],
               "Isophthalic acid (m-Xylene oxidation)":[160, 300, 9.914, 0.6, 0.002204623],
               "Isoprene (isobutylene carbonylation)":[60, 200, 10.024, 0.6, 0.002204623],
               "Isoprene (propylene dimerization and pyrolysis)":[60, 200, 6.519, 0.6, 0.002204623],
               "Linear alkylbenzene (PACOL/DeFine/PEP/Detal)":[100, 250, 4.896, 0.6, 0.002204623],
               "Linear alpha olefins (Chevron)":[300, 700, 5.198, 0.6, 0.002204623],
               "Linear alpha olefins (Linear-1)":[200000, 300000, 0.122, 0.6, 1],
               "Maleic anhydride (fluid bed)":[70, 150, 7.957, 0.6, 0.002204623],
               "Methacrylic acid (isobutylene oxidation)":[70, 150, 7.691, 0.6, 0.002204623],
               #"Methanol (steam reforming & synthesis)":[3000, 7000, 2.775, 0.6, 0],
               "m-Xylene (MX Sorbex)":[150, 300, 4.326, 0.6, 0.002204623],
               "Naphthalene (3-stage fractional crystallizer)":[20, 50, 2.375, 0.6, 0.002204623],
               "N-Butanol (crude C4s)":[150, 300, 8.236, 0.6, 0.002204623],
               "Norbornene (Diels-Alder reaction)":[40, 90, 7.482, 0.6, 0.002204623],
               "Pentaerythritol (condensation)":[40, 90, 6.22, 0.6, 0.002204623],
               "PET resin chip (comonomer by NG3)":[150, 300, 4.755, 0.6, 0.002204623],
               "Phenol (cumene, zeolite catalyst basis)":[200, 600, 6.192, 0.6, 0.002204623],
               "Phthalic anhydride (catalytic oxidation)":[100, 200, 7.203, 0.6, 0.002204623],
               "Polycarbonate (interfacial polymerization)":[70, 150, 20.68, 0.6, 0.002204623],
               "Polyethylene terephthalate (meltphase)":[70, 200, 5.389, 0.6, 0.002204623],
               "Polystyrene (bulk polymerization, plugflow)":[70, 200, 2.551, 0.6, 0.002204623],
               "Propylene (Oleflex)":[150000, 350000, 0.0943, 0.6, 1],
               "Propylene (metathesis)":[500, 1000, 1.899, 0.6, 0.002204623],
               "Purified terphthalic acid (EniChem/Technimont)":[350, 700, 10.599, 0.6, 0.002204623],
               "p-Xylene (Isomar and Parex)":[300000, 700000, 0.023, 0.6, 1],
               #"p-Xylene (Tatoray)":[12000, 20000, 0.069, 0.6, 0],
               "Refined Glycerine (distillation/adsorption)":[30, 60, 2.878, 0.6, 0.002204623],
               "Sebaccic Acid (cyclododecanone route)":[8, 16, 13.445, 0.6, 0.002204623],
               "Sorbitol(70%) (continuous hydrogenation)":[50, 120, 4.444, 0.6, 0.002204623],
               "Styrene (SMART)":[300000, 700000, 0.0355, 0.6, 1],
               "Vinyl acetate (Cativa Integrated)":[300, 800, 7.597, 0.6, 0.002204623],
               "Vinyl acetate (Celanese VAntage)":[300, 800, 6.647, 0.6, 0.002204623],
               #"Visbreaking (coil-type visbreaker)":[6000, 15000, 0.278, 0.48, 0]
               }

# Hill (1956), Installed equipment cost
def capcomo_Hill(unit_num,scale_tpy):
     if unit_num==None:
          return(print("Error: The 'unit_num' must be defined for capital cost estimation (Hill model)."))
     elif scale_tpy == None: 
               return (print("Error: The 'scale_tpy' must be defined for capital cost estimation (Hill model)."))
     else:
        #Q=ton/y, IEC=1954 USD
        IEC=30000*unit_num*(scale_tpy/4540)**0.6
        return(round(IEC,1))

# Guthrie, conceptual (1970), FCI
def capcomo_Guthrie(process, scale_tpy):
     if process ==None:
          return (print("Error: The 'process' must be defined for capital cost estimation (Guthrie model)."))
     elif process not in Cbase_Guthrie:
          return(print(f"Error: The selected process '{process}' is not available for capital cost estimation (Guthrie model). Available processes: {list(Cbase_Guthrie.keys())}"))
     elif scale_tpy == None: 
          return (print("Error: The 'scale_tpy' must be defined for capital cost estimation (Guthrie model)."))
     
     else:
          Cbase=Cbase_Guthrie[process]
          Qbase=Qbase_Guthrie[process]
          n=n_Guthrie[process]
          FCI=Cbase*((scale_tpy/Qbase)**n)*(10**6)
          return(round(FCI, 1))

# Timms (1980), ISBL
def capcomo_Timms(unit_num,scale_tpy,Tmax_K,Pmax_bar):
     if unit_num==None:
          return(print("Error: The 'unit_num' must be defined for capital cost estimation (Timms model)."))
     elif scale_tpy == None: 
               return (print("Error: The 'scale_tpy' must be defined for capital cost estimation (Timms model)."))
     elif Tmax_K == None: 
               return (print("Error: The 'Tmax_K' must be defined for capital cost estimation (Timms model)."))
     elif Pmax_bar == None: 
               return (print("Error: The 'Pmax_bar' must be defined for capital cost estimation (Timms model)."))
     else:
          #Q=ton/y, TCI=1992 USD, T=K, P=bar
          TCI=2570*unit_num*(scale_tpy**0.639)*(Tmax_K**0.066)*(Pmax_bar**-0.016)
          return(round(TCI,1))

# Garrett (1989), ISBL
def capcomo_Garrett(process, scale_tpy):
     if process ==None:
          return (print("Error: The 'process' must be defined for capital cost estimation (Garrett model)."))
     elif process not in Param_Garrett:
          return(print(f"Error: The selected process '{process}' is not available for capital cost estimation (Garrett model). Available processes: {list(Param_Garrett.keys())}"))
     elif scale_tpy == None: 
          return (print("Error: The 'scale_tpy' must be defined for capital cost estimation (Garrett model)."))
     
     else:
          Qmin=Param_Garrett[process][0]
          Qmax=Param_Garrett[process][1]
          a=Param_Garrett[process][2]
          n=Param_Garrett[process][3]
          Qunit=Param_Garrett[process][4]
          Q=scale_tpy*Qunit

          if Q <= Qmin:
               Q=Qmin
               linear_num=1
          else:
               linear_num=math.ceil(Q/Qmax)
               Q=Q/linear_num
          ISBL=((a*(Q**n))*linear_num)*(10**6)
          return (round(ISBL,1))

# Petley (1997), ISBL
def capcomo_Petley(unit_num,scale_tpy,Tmax_K,Pmax_bar):
     if unit_num==None:
          return(print("Error: The 'unit_num' must be defined for capital cost estimation (Petley model)."))
     elif scale_tpy == None: 
               return (print("Error: The 'scale_tpy' must be defined for capital cost estimation (Petley model)."))
     elif Tmax_K == None: 
               return (print("Error: The 'Tmax_K' must be defined for capital cost estimation (Petley model)."))
     elif Pmax_bar == None: 
               return (print("Error: The 'Pmax_bar' must be defined for capital cost estimation (Petley model)."))
     else: 
        #Q=ton/y, ISBL=1987 USD, T=K, P=bar
        ISBL=55882*(unit_num**0.486)*(scale_tpy**0.44)*(Tmax_K**0.038)*(Pmax_bar**-0.02)
        return(round(ISBL,1))

# Lange 1 (2001), TCI
def capcomo_Lange1(energyloss_MW):
     if energyloss_MW==None:
          return(print("Error: The 'energyloss_MW' must be defined for capital cost estimation (Lange 1 model)."))
     else:
          #Energyloss=MW, TCI=1993 MMUSD
          TCI=3*(energyloss_MW**0.84)
          return(round(TCI*(10**6),1))

# Lange 2 (2001), TCI
def capcomo_Lange2(energytransfer_MW):
     if energytransfer_MW==None:
          return(print("Error: The 'energytransfer_MW' must be defined for capital cost estimation (Lange 2 model)."))
     else:
          #Total energy transfer=MW, TCI=1993 MMUSD
          TCI=12.9*(energytransfer_MW**0.55)
          return(round(TCI*(10**6),1))
    

def capcomo(*,model=None, process=None, scale_tpy=None, unit_num=None,Tmax_K=None,Pmax_bar=None,energytransfer_MW=None, energyloss_MW=None):
     # Error message: Model name is not defined.
     if model==None:
          return (print("Error: The 'model' must be defined for capital cost estimation."))
     elif model not in CAPCOMO_list:
          return (print(f"Error: The model is not available in the capital cost estimation model library. Available models: {CAPCOMO_list}"))
     ## Mapping model & Capital cost estimation
     elif model == "Hill":
          capco=capcomo_Hill(unit_num, scale_tpy)
     elif model == "Guthrie":
          capco=capcomo_Guthrie(process, scale_tpy)
     elif model == "Timms":
          capco=capcomo_Timms(unit_num,scale_tpy,Tmax_K,Pmax_bar)
     elif model == "Garrett":
          capco=capcomo_Garrett(process, scale_tpy)
     elif model == "Petley":
          capco=capcomo_Petley(unit_num,scale_tpy,Tmax_K,Pmax_bar)
     elif model == "Lange 1":
          capco=capcomo_Lange1(energyloss_MW)
     elif model == "Lange 2":
          capco=capcomo_Lange2(energytransfer_MW)
     
     basis_year=CE_basis_dict[model][1]
     capco_type=CE_basis_dict[model][2]
     
     return (capco, basis_year, capco_type)


