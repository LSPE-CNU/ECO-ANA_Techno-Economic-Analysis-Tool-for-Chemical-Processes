import math
import numbers
import warnings

CAPCOMO_list=["Hill", "Guthrie", "Timms", "Garrett", "Petley", "Lange 1", "Lange 2"]

# Model name: [basis CE, basis year, Capital cost type]
CE_basis_dict={"Hill": [86.1,"1954 year basis", "Installed total equipment cost"],
               "Guthrie": [394.1,"2000 year basis", "Fixed capital investment"],
               "Timms": [358.2,"1992 year basis", "Inside battery limits"],   # Petley (1997): existing methods evaluated on the battery-limits (ISBL) basis
               "Garrett": [478.6,"2006 year basis", "Inside battery limits"],   # January 2006, U.S. Gulf Coast (Towler Table 6.2, note 1)
               "Petley": [342.5,"1988 year basis", "Inside battery limits"],   # mid-1988 USD, plant built in West Germany (Petley 1997)
               "Lange 1": [359.2,"1993 year basis", "Fixed capital investment"],   # Lange (2001), notes [iii],[iv]: plant cost incl. off-sites (ISBL x 1.4), no working capital
               "Lange 2": [359.2,"1993 year basis", "Fixed capital investment"]
               }

#Model factor[process] - Guthrie===================================================================================================
# Source: Peters M.S., Timmerhaus K.D. and West R.E. (2003), Plant Design and Economics for Chemical Engineers, 5th ed.,
#         Table 6-11 "Capital cost data for chemical and petroleum processing plants (2000)", p. 255;
#         adapted from Guthrie K.M., Chem. Eng. 77(13): 140 (1970) and Process Plant Estimating, Evaluation, and Control (1974).
#   FCI [million USD, 2000] = Cbase * (Q/Qbase)^n
# Chemical plants: Qbase in t/y (10^3 kg/yr). Petroleum processing plants: Qbase in m3/d; scale_tpy (t/y) is converted
#   with the liquid density of the stream on which the capacity is defined and 365 operating days per year
#   (ECO-ANA assumptions; not given in the source). Feed-based units: pass the feed rate as scale_tpy.
# The power factors apply within roughly a 3-fold ratio either way from Qbase (Table 6-11, footnote).
#   Below Qbase/3 the correlation is extrapolated; above 3*Qbase the plant is estimated as identical parallel trains.
#   A UserWarning is issued in both cases.
_DAYS_Y_GUTHRIE = 365
def _tpy_to_m3pd(rho):      return 1/(rho*_DAYS_Y_GUTHRIE)
GUTHRIE_RANGE_RATIO = 3
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
               "Urea":10,
               "Alkylation (H2SO4)":23,
               "Coking (delayed)":31,
               "Coking (fluid)":19,
               "Cracking (fluid)":19,
               "Cracking (thermal)":6,
               "Distillation (atm.)":38,
               "Distillation (vac.)":23,
               "Hydrotreating":3.5,
               "Reforming":34,
               "Polymerization":6
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
               "Urea":55000,
               "Alkylation (H2SO4)":1600,   # m3/d
               "Coking (delayed)":1600,   # m3/d
               "Coking (fluid)":1600,   # m3/d
               "Cracking (fluid)":1600,   # m3/d
               "Cracking (thermal)":1600,   # m3/d
               "Distillation (atm.)":16000,   # m3/d
               "Distillation (vac.)":16000,   # m3/d
               "Hydrotreating":1600,   # m3/d
               "Reforming":1600,   # m3/d
               "Polymerization":1600   # m3/d
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
           "Urea":0.7,
           "Alkylation (H2SO4)":0.6,
           "Coking (delayed)":0.38,
           "Coking (fluid)":0.42,
           "Cracking (fluid)":0.7,
           "Cracking (thermal)":0.7,
           "Distillation (atm.)":0.9,
           "Distillation (vac.)":0.7,
           "Hydrotreating":0.65,
           "Reforming":0.6,
           "Polymerization":0.58
               }
Qunit_Guthrie={"Acetic acid":1,
               "Acetone":1,
               "Ammonia":1,
               "Ammonium nitrate":1,
               "Butanol":1,
               "Chlorine":1,
               "Ethylene":1,
               "Ethylene oxide":1,
               "Formaldehyde":1,
               "Glycol":1,
               "Hydrofluoric acid":1,
               "Methanol":1,
               "Nitric acid":1,
               "Phosphoric acid":1,
               "Polyethylene":1,
               "Propylene":1,
               "Sulfuric acid":1,
               "Urea":1,
               "Alkylation (H2SO4)":_tpy_to_m3pd(0.70),   # m3/d of alkylate product (rho 0.70)
               "Coking (delayed)":_tpy_to_m3pd(1.00),   # m3/d of vacuum residue feed (rho 1.00)
               "Coking (fluid)":_tpy_to_m3pd(1.00),   # m3/d of vacuum residue feed (rho 1.00)
               "Cracking (fluid)":_tpy_to_m3pd(0.92),   # m3/d of gas oil feed (rho 0.92)
               "Cracking (thermal)":_tpy_to_m3pd(1.00),   # m3/d of residue feed (rho 1.00)
               "Distillation (atm.)":_tpy_to_m3pd(0.87),   # m3/d of crude oil feed (rho 0.87)
               "Distillation (vac.)":_tpy_to_m3pd(0.95),   # m3/d of atmospheric residue feed (rho 0.95)
               "Hydrotreating":_tpy_to_m3pd(0.85),   # m3/d of distillate feed (rho 0.85)
               "Reforming":_tpy_to_m3pd(0.74),   # m3/d of naphtha feed (rho 0.74)
               "Polymerization":_tpy_to_m3pd(0.73)   # m3/d of polymer gasoline product (rho 0.73)
               }
process_Guthrie={"Acetic acid":"CH3OH and CO - catalytic",
                 "Acetone":"Propylene-copper chloride catalyst",
                 "Ammonia":"Steam reforming",
                 "Ammonium nitrate":"Ammonia and nitric acid",
                 "Butanol":"Propylene, CO, and H2O - catalytic",
                 "Chlorine":"Electrolysis of NaCl",
                 "Ethylene":"Refinery gases",
                 "Ethylene oxide":"Ethylene - catalytic",
                 "Formaldehyde":"Methanol - catalytic; product: formaldehyde (37%)",
                 "Glycol":"Ethylene and chlorine",
                 "Hydrofluoric acid":"Hydrogen fluoride and H2O",
                 "Methanol":"CO2, natural gas, and steam",
                 "Nitric acid":"Ammonia - catalytic; product: high-strength nitric acid",
                 "Phosphoric acid":"Calcium phosphate and H2SO4",
                 "Polyethylene":"Ethylene - catalytic; product: high-density polyethylene",
                 "Propylene":"Refinery gases",
                 "Sulfuric acid":"Sulfur - contact catalytic",
                 "Urea":"Ammonia and CO2",
                 "Alkylation (H2SO4)":"Catalytic",
                 "Coking (delayed)":"Thermal",
                 "Coking (fluid)":"Thermal",
                 "Cracking (fluid)":"Catalytic",
                 "Cracking (thermal)":"Thermal",
                 "Distillation (atm.)":"65% vaporized",
                 "Distillation (vac.)":"65% vaporized",
                 "Hydrotreating":"Catalytic desulfurization",
                 "Reforming":"Catalytic",
                 "Polymerization":"Catalytic"
               }

#Model factor[process]=[Slower,Supper,a,n,Qunitfactor] - Garrett ==================================================================================================
# Sources: Garrett D.E. (2012), Chemical Engineering Economics, Springer Science & Business Media;
#          Towler G. and Sinnott R. (2008), Chemical Engineering Design, Table 6.2 (Process cost correlations).
#   ISBL [MM$, January 2006, USGC basis, CE 478.6] = a * S^n
#   S is the product rate for chemicals and the feed rate for fuels (Table 6.2, note 3).
#   Slower-Supper: range over which the correlation can be applied (note 2).
# The capacity units of Table 6.2 (MMlb/y, t/d, bpd, MMgal/y, MMscf/y, MMscf/d) are converted from scale_tpy (t/y).
# The densities, molar masses and the 365 operating days per year used for this conversion are
# ECO-ANA assumptions (they are not given in the source).
# Volume-based units need a liquid density rho (t/m3, ~15 degC) of the stream on which the capacity is defined.
_BBL_M3 = 0.158987          # m3 per barrel
_GAL_M3 = 3.785411784e-3    # m3 per US gallon
_DAYS_Y = 365               # operating days per year (calendar-day basis)
def _tpy_to_tpd():          return 1/_DAYS_Y
def _tpy_to_bpd(rho):       return 1/(rho*_BBL_M3*_DAYS_Y)
def _tpy_to_MMgalpy(rho):   return 1/(rho*_GAL_M3*1e6)
_T_PER_MMSCF_PER_M = 1.1953 # t per MMscf per (kg/kmol); ideal gas at 60 degF, 1 atm (379.49 scf/lbmol)
def _tpy_to_MMscfy(M):      return 1/(_T_PER_MMSCF_PER_M*M)
def _tpy_to_MMscfd(M):      return 1/(_T_PER_MMSCF_PER_M*M*_DAYS_Y)

Param_Garrett={
               "ABSResin (15%Rubber) (emulsion polymerization)":[50, 300, 12.146, 0.6, 0.002204623],
               "Acetic Acid (Cativa)":[500, 2000, 3.474, 0.6, 0.002204623],
               "Acetic Acid (Low Water Methanol Carbonylation)":[500, 2000, 2.772, 0.6, 0.002204623],
               "Acrolein (propylene oxidation with Bi/Mo catalyst)":[30, 150, 6.809, 0.6, 0.002204623],
               "Adipic acid (phenol)":[300, 1000, 3.533, 0.6, 0.002204623],
               "Alkylation (sulfuric acid effluent refrigeration)":[4000, 20000, 0.16, 0.6, _tpy_to_bpd(0.70)],   # bpd of alkylate (rho 0.70)
               "Alkylation (HF)":[5000, 12000, 0.153, 0.6, _tpy_to_bpd(0.70)],   # bpd of alkylate (rho 0.70)
               "Allyl chloride (propylene chlorination)":[80, 250, 7.581, 0.6, 0.002204623],
               "Alpha olefins (full-range, Chevron Phillips)":[400, 1200, 5.24, 0.6, 0.002204623],
               "Alpha olefins (full-range, Shell)":[400, 1000, 8.146, 0.6, 0.002204623],
               "Benzene (Sulfolane extraction)":[50, 200, 7.793, 0.6, _tpy_to_MMgalpy(0.879)],   # MMgal/y of benzene (rho 0.879)
               "Benzene (toluene hydrodealkylation)":[50, 200, 7.002, 0.6, _tpy_to_MMgalpy(0.879)],   # MMgal/y of benzene (rho 0.879)
               "Benzene reduction (Bensat)":[8000, 15000, 0.0275, 0.6, _tpy_to_bpd(0.70)],   # bpd of light reformate feed (rho 0.70)
               "Biodiesel(FAME) (vegetable oil)":[100, 500, 2.747, 0.6, 0.002204623],
               "bis-HET (Eastman Glycolysis)":[50, 200, 0.5, 0.6, 0.002204623],
               "BTX Aromatics (Cyclar)":[200000, 800000, 0.044, 0.6, 1],
               "BTX Aromatics (CCR Platforming)":[200000, 800000, 0.015, 0.6, 1],
               "Butadiene (extractive distillation)":[100, 500, 5.514, 0.6, 0.002204623],
               "Butadiene (Oxo-D plus extractive distillation)":[100, 500, 11.314, 0.6, 0.002204623],
               "Butene-1 (Alphabutol ethylene dimerization)":[5000, 30000, 0.0251, 0.6, 1],
               "Butene-1 (BP)":[20000, 80000, 0.169, 0.6, 1],
               "Caprolactam (nitration-grade toluene)":[40000, 120000, 0.321, 0.6, 1],
               "Carbon monoxide (steam methane reforming)":[2000, 6000, 0.363, 0.6, _tpy_to_MMscfy(28.01)],   # MMscf/y of CO (M 28.01)
               "Catalytic Condensation (Gasoline Production)":[10000, 30000, 0.222, 0.6, _tpy_to_bpd(0.73)],   # bpd of polymer gasoline (rho 0.73)
               "Catalytic reforming (CCR Platforming)":[15000, 60000, 0.179, 0.6, _tpy_to_bpd(0.74)],   # bpd of naphtha FEED (rho 0.74); scale_tpy = feed rate
               "Coking (Flexicoking including Fluid Coking)":[15000, 40000, 0.343, 0.6, _tpy_to_bpd(1.00)],   # bpd of vacuum residue FEED (rho 1.00); scale_tpy = feed rate
               "Coking (Selective Yield Delayed Coking)":[15000, 60000, 0.109, 0.68, _tpy_to_bpd(1.00)],   # bpd of vacuum residue FEED (rho 1.00); scale_tpy = feed rate
               "Copolymer polypropylene (INNOVENE)":[300, 900, 3.43, 0.6, 0.002204623],
               "Copolymer polypropylene (Unipol)":[300, 900, 3.641, 0.6, 0.002204623],
               "Copolymer polypropylene (SPHERIPOL Bulk)":[300, 900, 3.649, 0.6, 0.002204623],
               "Copolymer polypropylene (BORSTAR)":[300, 900, 4.015, 0.6, 0.002204623],
               "Crude distillation (D2000)":[150000, 300000, 0.151, 0.6, _tpy_to_bpd(0.87)],   # bpd of crude oil FEED (rho 0.87); scale_tpy = feed rate
               "Cumene (Q-Max)":[150000, 450000, 0.012, 0.6, 1],
               "Cyclic Olefin Copolymer (Mitsui)":[60, 120, 12.243, 0.6, 0.002204623],
               "Cyclohexane (liq-phase hydrogenation of benzene)":[100000, 300000, 0.0061, 0.6, 1],
               "Dewaxing (ISODEWAXING)":[6000, 15000, 0.256, 0.6, _tpy_to_bpd(0.87)],   # bpd of waxy lube oil FEED (rho 0.87); scale_tpy = feed rate
               "2,6-Dimethylnaphthalene (Methanol alkylation)":[50, 100, 7.712, 0.6, 0.002204623],
               "Dimethyl terephthalate (methanolysis)":[30, 80, 5.173, 0.6, 0.002204623],
               "Dimethyl terephthalate (Huels Oxidation)":[300, 800, 7.511, 0.6, 0.002204623],
               "Ethanol (ethylene hydration)":[30, 90, 9.643, 0.6, _tpy_to_MMgalpy(0.789)],   # million gal/y of ethanol (rho 0.789); Table 6.2 prints "Mgal/y", read as MMgal/y (30-90 thousand gal/y is not a realistic plant size)
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
               "Fluid catalytic cracking (KBR)":[20000, 60000, 0.21, 0.6, _tpy_to_bpd(0.92)],   # bpd of gas oil FEED (rho 0.92); scale_tpy = feed rate
               "Fluid catalytic cracking (power recovery)":[20000, 60000, 0.302, 0.6, _tpy_to_bpd(0.92)],   # bpd of gas oil FEED (rho 0.92); scale_tpy = feed rate
               "Gas to liquids (Syntroleum)":[30000, 100000, 2.279, 0.6, _tpy_to_bpd(0.77)],   # bpd of liquid product (rho 0.77)
               "Gas sweetening (Amine Guard FS to pipeline spec)":[300, 800, 0.386, 0.6, _tpy_to_MMscfd(17.4)],   # MMscf/d of natural gas FEED (M 17.4); scale_tpy = feed rate
               "Gasification (GE Gasification Process Mayacrude)":[7000, 15000, 0.681, 0.6, _tpy_to_bpd(0.92)],   # bpd of Maya crude FEED (rho 0.92); scale_tpy = feed rate
               "Gasoline desulfurization (Prime-G+)":[7000, 15000, 0.042, 0.58, _tpy_to_bpd(0.74)],   # bpd of FCC gasoline FEED (rho 0.74); scale_tpy = feed rate
               "Glucose(40%Solution) (basic wet cornmilling)":[300, 800, 3.317, 0.6, 0.002204623],
               "HDPE Pellets (BP Gas Phase)":[300, 700, 3.624, 0.6, 0.002204623],
               "HDPE Pellets (Phillips Slurry)":[300, 700, 3.37, 0.6, 0.002204623],
               "HDPE Pellets (Zeigler Slurry)":[300, 700, 4.488, 0.6, 0.002204623],
               "High impact polystyrene (bulk polymerization)":[70, 160, 2.97, 0.6, 0.002204623],
               "Hydrocracking (ISOCRACKING)":[20000, 45000, 0.221, 0.6, _tpy_to_bpd(0.92)],   # bpd of vacuum gas oil FEED (rho 0.92); scale_tpy = feed rate
               "Hydrocracking (Unicracking, distillate)":[20000, 45000, 0.136, 0.66, _tpy_to_bpd(0.92)],   # bpd of vacuum gas oil FEED (rho 0.92); scale_tpy = feed rate
               "Hydrocracking (Axens)":[20000, 45000, 0.198, 0.6, _tpy_to_bpd(0.92)],   # bpd of vacuum gas oil FEED (rho 0.92); scale_tpy = feed rate
               "Hydrogen (steam methane reforming)":[10, 50, 1.759, 0.79, _tpy_to_MMscfd(2.016)],   # MMscf/d of H2 (M 2.016)
               "Hydrotreating (Unionfining)":[10000, 40000, 0.0532, 0.68, _tpy_to_bpd(0.85)],   # bpd of distillate FEED (rho 0.85); scale_tpy = feed rate
               "Isomerization (Once-through Penex)":[8000, 15000, 0.0454, 0.6, _tpy_to_bpd(0.65)],   # bpd of light naphtha FEED (rho 0.65); scale_tpy = feed rate
               "Isomerization (Penex-Molex)":[8000, 15000, 0.12, 0.6, _tpy_to_bpd(0.65)],   # bpd of light naphtha FEED (rho 0.65); scale_tpy = feed rate
               "Isophthalic acid (m-Xylene oxidation)":[160, 300, 9.914, 0.6, 0.002204623],
               "Isoprene (isobutylene carbonylation)":[60, 200, 10.024, 0.6, 0.002204623],
               "Isoprene (propylene dimerization and pyrolysis)":[60, 200, 6.519, 0.6, 0.002204623],
               "Linear alkylbenzene (PACOL/DeFine/PEP/Detal)":[100, 250, 4.896, 0.6, 0.002204623],
               "Linear alpha olefins (Chevron)":[300, 700, 5.198, 0.6, 0.002204623],
               "Linear alpha olefins (Linear-1)":[200000, 300000, 0.122, 0.6, 1],
               "Maleic anhydride (fluid bed)":[70, 150, 7.957, 0.6, 0.002204623],
               "Methacrylic acid (isobutylene oxidation)":[70, 150, 7.691, 0.6, 0.002204623],
               "Methanol (steam reforming & synthesis)":[3000, 7000, 2.775, 0.6, _tpy_to_tpd()],   # t/d of methanol
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
               "p-Xylene (Tatoray)":[12000, 20000, 0.069, 0.6, _tpy_to_bpd(0.87)],   # bpd of toluene/C9 aromatics FEED (rho 0.87); scale_tpy = feed rate
               "Refined Glycerine (distillation/adsorption)":[30, 60, 2.878, 0.6, 0.002204623],
               "Sebaccic Acid (cyclododecanone route)":[8, 16, 13.445, 0.6, 0.002204623],
               "Sorbitol(70%) (continuous hydrogenation)":[50, 120, 4.444, 0.6, 0.002204623],
               "Styrene (SMART)":[300000, 700000, 0.0355, 0.6, 1],
               "Vinyl acetate (Cativa Integrated)":[300, 800, 7.597, 0.6, 0.002204623],
               "Vinyl acetate (Celanese VAntage)":[300, 800, 6.647, 0.6, 0.002204623],
               "Visbreaking (coil-type visbreaker)":[6000, 15000, 0.278, 0.48, _tpy_to_bpd(1.00)],   # bpd of vacuum residue FEED (rho 1.00); scale_tpy = feed rate
               }

def _check_positive(model, **inputs):
     # Returns an error message for the first input that is not a finite positive number, otherwise None.
     for name, value in inputs.items():
          if isinstance(value, bool) or not isinstance(value, numbers.Real):
               return f"Error: The '{name}' must be a number ({model} model); got {type(value).__name__} {value!r}."
          if not math.isfinite(value):
               return f"Error: The '{name}' must be a finite number ({model} model); got {value!r}."
          if value <= 0:
               return f"Error: The '{name}' must be a positive value ({model} model)."
     return None

# Hill (1956), Installed equipment cost
def capcomo_Hill(unit_num,scale_tpy):
     if unit_num==None:
          return(print("Error: The 'unit_num' must be defined for capital cost estimation (Hill model)."))
     elif scale_tpy == None: 
               return (print("Error: The 'scale_tpy' must be defined for capital cost estimation (Hill model)."))
     elif _check_positive("Hill", unit_num=unit_num, scale_tpy=scale_tpy):
          return (print(_check_positive("Hill", unit_num=unit_num, scale_tpy=scale_tpy)))
     else:
        #Q=ton/y, IEC=1954 USD
        IEC=30000*unit_num*(scale_tpy/4540)**0.6
        return(round(IEC,1))

# Guthrie: Peters, Timmerhaus & West (2003), Table 6-11 (2000 USD), adapted from Guthrie (1970), FCI
def capcomo_Guthrie(process, scale_tpy):
     if process ==None:
          return (print("Error: The 'process' must be defined for capital cost estimation (Guthrie model)."))
     elif process not in Cbase_Guthrie:
          return(print(f"Error: The selected process '{process}' is not available for capital cost estimation (Guthrie model). Available processes: {list(Cbase_Guthrie.keys())}"))
     elif scale_tpy == None: 
          return (print("Error: The 'scale_tpy' must be defined for capital cost estimation (Guthrie model)."))
     elif _check_positive("Guthrie", scale_tpy=scale_tpy):
          return (print(_check_positive("Guthrie", scale_tpy=scale_tpy)))
     else:
          Cbase=Cbase_Guthrie[process]
          Qbase=Qbase_Guthrie[process]
          n=n_Guthrie[process]
          Q=scale_tpy*Qunit_Guthrie[process]     # capacity in the unit of Qbase (t/y or m3/d)
          Qmin, Qmax = Qbase/GUTHRIE_RANGE_RATIO, Qbase*GUTHRIE_RANGE_RATIO
          train_num=1
          if Q < Qmin:
               warnings.warn(f"Guthrie model, '{process}': capacity {Q:.4g} is below the range of the power factor "
                             f"({Qmin:.4g}-{Qmax:.4g}, i.e. 1/3-3 x base size {Qbase:g}); the correlation is extrapolated.",
                             UserWarning, stacklevel=3)
          elif Q > Qmax:
               train_num=math.ceil(Q/Qmax)
               warnings.warn(f"Guthrie model, '{process}': capacity {Q:.4g} is above the range of the power factor "
                             f"({Qmin:.4g}-{Qmax:.4g}, i.e. 1/3-3 x base size {Qbase:g}); the plant is estimated as "
                             f"{train_num} parallel trains of {Q/train_num:.4g} each.", UserWarning, stacklevel=3)
          FCI=Cbase*(((Q/train_num)/Qbase)**n)*train_num*(10**6)
          return(round(FCI, 1))

# Timms (1980), ISBL ==============================================================================================================
# Source: Timms S.R. (1980), M.Phil. thesis, Aston University; as given in Petley G.J. (1997), PhD thesis,
#         Loughborough University, eq. (3.20) (Method 2):
#   C [GBP, 1992] = 3860 * N * Q^0.639 * Fm * Tmax^0.066 * Pmax^-0.016
#   N = number of functional units, Q = capacity [t/y], Tmax = maximum temperature [K], Pmax = maximum pressure [bar],
#   Fm = materials-of-construction factor (Wilson factors, 1.0 carbon steel - 1.3 high-grade stainless steel).
# ECO-ANA uses Fm = 1.0 (carbon steel). The cost is the battery-limits (ISBL) capital cost.
# The 1992 GBP cost is converted to 1992 USD with GBP_TO_USD_1992.
GBP_TO_USD_1992=1.7643   # USD per GBP, 1992 (1377.36 KRW/GBP / 780.67 KRW/USD)

def capcomo_Timms(unit_num,scale_tpy,Tmax_K,Pmax_bar):
     if unit_num==None:
          return(print("Error: The 'unit_num' must be defined for capital cost estimation (Timms model)."))
     elif scale_tpy == None: 
               return (print("Error: The 'scale_tpy' must be defined for capital cost estimation (Timms model)."))
     elif Tmax_K == None: 
               return (print("Error: The 'Tmax_K' must be defined for capital cost estimation (Timms model)."))
     elif Pmax_bar == None: 
               return (print("Error: The 'Pmax_bar' must be defined for capital cost estimation (Timms model)."))
     elif _check_positive("Timms", unit_num=unit_num, scale_tpy=scale_tpy, Tmax_K=Tmax_K, Pmax_bar=Pmax_bar):
          return (print(_check_positive("Timms", unit_num=unit_num, scale_tpy=scale_tpy, Tmax_K=Tmax_K, Pmax_bar=Pmax_bar)))
     else:
          #Q=ton/y, T=K, P=bar, ISBL=1992 GBP (Fm = 1.0) -> 1992 USD
          ISBL_GBP=3860*unit_num*(scale_tpy**0.639)*(Tmax_K**0.066)*(Pmax_bar**-0.016)
          ISBL=ISBL_GBP*GBP_TO_USD_1992
          return(round(ISBL,1))

# Garrett model (Garrett, 2012; Towler and Sinnott, 2008, Table 6.2), ISBL
def capcomo_Garrett(process, scale_tpy):
     if process ==None:
          return (print("Error: The 'process' must be defined for capital cost estimation (Garrett model)."))
     elif process not in Param_Garrett:
          return(print(f"Error: The selected process '{process}' is not available for capital cost estimation (Garrett model). Available processes: {list(Param_Garrett.keys())}"))
     elif scale_tpy == None: 
          return (print("Error: The 'scale_tpy' must be defined for capital cost estimation (Garrett model)."))
     elif _check_positive("Garrett", scale_tpy=scale_tpy):
          return (print(_check_positive("Garrett", scale_tpy=scale_tpy)))
     else:
          Slower, Supper, a, n, Qunit = Param_Garrett[process]
          Q=scale_tpy*Qunit          # capacity in the unit of the correlation
          train_num=1
          if Q < Slower:
               # Below the range: extrapolate the correlation (n = 0.6 correlations are themselves
               # an extrapolation around a single cost point; Table 6.2, note 4).
               warnings.warn(f"Garrett model, '{process}': capacity {Q:.4g} is below the lower bound of the correlation "
                             f"({Slower:g}); the correlation is extrapolated.", UserWarning, stacklevel=3)
          elif Q > Supper:
               # Above the range: split into identical parallel trains, each within the range.
               train_num=math.ceil(Q/Supper)
               warnings.warn(f"Garrett model, '{process}': capacity {Q:.4g} is above the upper bound of the correlation "
                             f"({Supper:g}); the plant is estimated as {train_num} parallel trains of {Q/train_num:.4g} each.",
                             UserWarning, stacklevel=3)
          ISBL=a*((Q/train_num)**n)*train_num*(10**6)
          return (round(ISBL,1))

# Petley (1997), ISBL ==============================================================================================================
# Source: Petley G.J. (1997), PhD thesis, Loughborough University, eq. (5.6):
#   ISBL [USD, mid-1988, plant constructed in West Germany] = 55882 * Q^0.44 * N^0.486 * Tmax^0.038 * Pmax^-0.02 * Fm^0.341
#   Q = capacity [t/y], N = number of functional units, Tmax [K], Pmax [bar], Fm = materials-of-construction (Wilson) factor.
# ECO-ANA uses Fm = 1.0 (carbon steel). The cost is the battery-limits capital cost (BLCC = ISBL).
# Capacity range of the correlation data (79 plants; Table 1.1 of the source): 2,250 - 990,000 t/y.
#   Below the range the capacity is set to the lower bound; above the range the plant is estimated as identical
#   parallel trains within the range. A UserWarning is issued in both cases.
PETLEY_RANGE_TPY=[2250, 990000]

def capcomo_Petley(unit_num,scale_tpy,Tmax_K,Pmax_bar):
     if unit_num==None:
          return(print("Error: The 'unit_num' must be defined for capital cost estimation (Petley model)."))
     elif scale_tpy == None: 
               return (print("Error: The 'scale_tpy' must be defined for capital cost estimation (Petley model)."))
     elif Tmax_K == None: 
               return (print("Error: The 'Tmax_K' must be defined for capital cost estimation (Petley model)."))
     elif Pmax_bar == None: 
               return (print("Error: The 'Pmax_bar' must be defined for capital cost estimation (Petley model)."))
     elif _check_positive("Petley", unit_num=unit_num, scale_tpy=scale_tpy, Tmax_K=Tmax_K, Pmax_bar=Pmax_bar):
          return (print(_check_positive("Petley", unit_num=unit_num, scale_tpy=scale_tpy, Tmax_K=Tmax_K, Pmax_bar=Pmax_bar)))
     else: 
        #Q=ton/y, ISBL=mid-1988 USD (West Germany), T=K, P=bar, Fm = 1.0
        Qmin, Qmax = PETLEY_RANGE_TPY
        Q=scale_tpy
        train_num=1
        if Q < Qmin:
             warnings.warn(f"Petley model: scale_tpy = {Q:g} t/y is below the capacity range of the correlation data "
                           f"({Qmin:g}-{Qmax:g} t/y); the lower bound {Qmin:g} t/y is used.", UserWarning, stacklevel=3)
             Q=Qmin
        elif Q > Qmax:
             train_num=math.ceil(Q/Qmax)
             warnings.warn(f"Petley model: scale_tpy = {Q:g} t/y is above the capacity range of the correlation data "
                           f"({Qmin:g}-{Qmax:g} t/y); the plant is estimated as {train_num} parallel trains of {Q/train_num:.4g} t/y each.",
                           UserWarning, stacklevel=3)
        ISBL=55882*(unit_num**0.486)*((Q/train_num)**0.44)*(Tmax_K**0.038)*(Pmax_bar**-0.02)*train_num
        return(round(ISBL,1))

# Lange 1 and Lange 2 =============================================================================================================
# Source: Lange J.-P. (2001), Fuels and chemicals manufacturing: guidelines for understanding and minimizing the
#         production costs, CATTECH 5(2), 82-95.
# Cost type: FCI (Fixed capital investment), USD 1993. The investment data of both correlations include the
#         plant and its off-sites (Lange 1: ISBL costs multiplied by 1.4, note [iii]); working capital is not included.
# Applicable range (read from the data in Figures 4 and 6 of the source):
#   Lange 1: energy loss 3 - 8,000 MW (below ~3 MW the plants deviate from the correlation and were excluded)
#   Lange 2: energy transfer duty 2 - 650 MW (per process segment)
#   Below the range the correlation is extrapolated; above the range the estimate is split into identical
#   parallel units within the range. A UserWarning is issued in both cases.
LANGE_RANGE_MW={"Lange 1":[3, 8000], "Lange 2":[2, 650]}

def _lange_ranged(model, E, a, n, varname):
     lo, hi = LANGE_RANGE_MW[model]
     unit_num=1
     if E < lo:
          warnings.warn(f"{model} model: {varname} = {E:g} MW is below the range of the correlation data ({lo:g}-{hi:g} MW); "
                        f"the correlation is extrapolated.", UserWarning, stacklevel=4)
     elif E > hi:
          unit_num=math.ceil(E/hi)
          warnings.warn(f"{model} model: {varname} = {E:g} MW is above the range of the correlation data ({lo:g}-{hi:g} MW); "
                        f"the cost is estimated as {unit_num} parallel units of {E/unit_num:.4g} MW each.", UserWarning, stacklevel=4)
     return a*((E/unit_num)**n)*unit_num      # MMUSD

# Lange 1 (2001), FCI
def capcomo_Lange1(energyloss_MW):
     # energyloss_MW = LHV(feed + fuel) - LHV(product) of the whole plant [MW] (Lange 2001, Figure 4 and note [ii]);
     #   it covers the losses through the heat of reaction, the combustion of fuel and the heating value of purge streams.
     if energyloss_MW==None:
          return(print("Error: The 'energyloss_MW' must be defined for capital cost estimation (Lange 1 model)."))
     elif _check_positive("Lange 1", energyloss_MW=energyloss_MW):
          return (print(_check_positive("Lange 1", energyloss_MW=energyloss_MW)))
     else:
          #Energy loss=MW, FCI=1993 MMUSD, eq. (2): FCI = 3.0*(energy loss)^0.84
          FCI=_lange_ranged("Lange 1", energyloss_MW, 3.0, 0.84, "energyloss_MW")
          return(round(FCI*(10**6),1))

# Lange 2 (2001), FCI
def capcomo_Lange2(energytransfer_MW):
     # energytransfer_MW = energy transfer duty [MW]: sum of the duties of all heat- and impulse- (momentum-) transfer
     #   units in a process segment, taken from a detailed process flowsheet (Lange 2001, p. 86). It is generally
     #   dominated by the heat-transfer duties related to the heat of reaction and the feed-effluent heat exchange;
     #   gas compression is significant for high-pressure gas-phase processes; liquid pumping is negligible.
     #   Process segments of the correlation data (note [iv]): steam reforming, partial oxidation and combined
     #   reforming, methanol and Fischer-Tropsch synthesis, hydrocracking, paraffin alkylation, hydrodesulfurization,
     #   platforming, ethene oxide synthesis and hydration; auxiliary units: distillation trains, large multistep
     #   compressors, cryogenic air separation units, boilers and diesel engines.
     if energytransfer_MW==None:
          return(print("Error: The 'energytransfer_MW' must be defined for capital cost estimation (Lange 2 model)."))
     elif _check_positive("Lange 2", energytransfer_MW=energytransfer_MW):
          return (print(_check_positive("Lange 2", energytransfer_MW=energytransfer_MW)))
     else:
          #Energy transfer duty=MW, FCI=1993 MMUSD, eq. (3): FCI = 2.9*(energy transfer)^0.55
          FCI=_lange_ranged("Lange 2", energytransfer_MW, 2.9, 0.55, "energytransfer_MW")
          return(round(FCI*(10**6),1))
    

def _norm_model(name):
     return "".join(ch for ch in name.lower() if ch not in " -_")
_CAPCOMO_KEYS={_norm_model(m): m for m in CAPCOMO_list}

def capcomo(*,model=None, process=None, scale_tpy=None, unit_num=None,Tmax_K=None,Pmax_bar=None,energytransfer_MW=None, energyloss_MW=None):
     # Error message: Model name is not defined or not available. The result keeps the (cost, basis, type) form.
     if model==None:
          print("Error: The 'model' must be defined for capital cost estimation.")
          return (None, None, None)
     # Model names are matched ignoring letter case, spaces, hyphens and underscores (e.g. "lange1" -> "Lange 1").
     model=_CAPCOMO_KEYS.get(_norm_model(model), model) if isinstance(model, str) else model
     if model not in CAPCOMO_list:
          print(f"Error: The model is not available in the capital cost estimation model library. Available models: {CAPCOMO_list}")
          return (None, None, None)
     ## Mapping model & Capital cost estimation
     if model == "Hill":
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


