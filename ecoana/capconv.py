
# plant cost factors [model][processtype]
Fplantcost={"Peters and Timmerhaus":{"Fluid":{"install":0.47,
                                                  "instru":0.18,
                                                  "pipe":0.66,
                                                  "elec":0.11,
                                                  "building":0.18,
                                                  "yard":0.1,
                                                  "service":0.7,
                                                  "land":0.06,
                                                  "engineering":0.33,
                                                  "construction":0.41,
                                                  "contract":0.21,
                                                  "contingency":0.42,
                                                  "equipment":1},

                                          "Solids-fluid":{"install":0.39,
                                                          "instru":0.13,
                                                          "pipe":0.31,
                                                          "elec":0.1,
                                                          "building":0.29,
                                                          "yard":0.1,
                                                          "service":0.55,
                                                          "land":0.06,
                                                          "engineering":0.32,
                                                          "construction":0.34,
                                                          "contract":0.18,
                                                          "contingency":0.36,
                                                          "equipment":1},

                                          "Solid":{"install":0.45,
                                                  "instru":0.09,
                                                  "pipe":0.16,
                                                  "elec":0.1,
                                                  "building":0.25,
                                                  "yard":0.13,
                                                  "service":0.4,
                                                  "land":0.06,
                                                  "engineering":0.33,
                                                  "construction":0.39,
                                                  "contract":0.17,
                                                  "contingency":0.34,
                                                  "equipment":1}
                                                          }
                 }

CAP_list=["Equipment cost","Installed equipment cost","Inside battery limits","Fixed capital investment","Total capital investment"]

# Capital cost type mapping
def cap_mapping(capcost):
     if capcost is None:
          return None
     # 입력값 내 앞뒤 공백을 없애고 모두 소문자로 변환
     key = "".join(c for c in str(capcost) if c.isalnum()).lower()
     # Cost list
     CAP_KEYS = {
          "Equipment cost":["tpec","equipmentcost","totalequipmentcost","totalequipmentpurchasecost","equipment","totalequipment"],
          "Installed equipment cost":["tiec","installedequipmentcost","totalinstalledequipmentcost","totalinstalledequipment","installedequipment",],
          "Inside battery limits":["isbl","insidebatterylimits","insidebatterylimitscost","isblcost"],
          "Fixed capital investment":["fci","fixedcapital","fixedcapitalinvestment","fixedcapitalcost"],
          "Total capital investment":["tci","totalcapital","totalcapitalcost","totalcapitalinvetsment","totalcapitalinvetsmentcost"]
     }

     cap_aliases = {
          alias: standard
          for standard, aliases in CAP_KEYS.items()
          for alias in aliases
     }

     if key in cap_aliases:
          return cap_aliases[key]

     elif key not in cap_aliases:
          return (print(f"Error: That capital cost type '{capcost!r}' is not available. Available capital cost type: {CAP_list}"))



def capconv(*,model=None,phase_processing=None,cap_in=None, cap_out=None, base_cost=None, rate_WC=0.15):
     if model==None:
          return (print("Error: The 'model' must be defined for capital cost estimation."))
     elif base_cost==None:
          return (print("Error: The 'base_cost' must be defined for capital cost estimation."))
     elif model not in list(Fplantcost.keys()):
          return (print(f"Error: The model is not available in the capital cost estimation model library. Available models: {list(Fplantcost.keys())}"))
     elif cap_in==None or cap_out==None:
          return (print("Error: The 'cap_in' and 'cap_out' must be defined for capital cost estimation."))
     elif model=="Peters and Timmerhaus":
          if phase_processing == None:
               return (print("Error: The 'phase_processing' must be defined for plant capital estimation (Peters and Timmerhaus model)."))
          elif phase_processing not in list(Fplantcost[model].keys()):
               return(print(f"Error: The selected phase processing '{phase_processing}' is not available for plant capital estimation (Peters and Timmerhaus model). Available processes: {list(Fplantcost[model].keys())}"))
          cap_in=cap_mapping(cap_in)
          cap_out=cap_mapping(cap_out)

          key_IEC=["equipment","install"]
          key_ISBL=["equipment","install","instru","pipe","elec","building"]
          key_OSBL=["yard","service","land"]
          key_DC=key_ISBL+key_OSBL
          key_IDC=["engineering","construction","contract","contingency"]
          key_FCI=key_DC+key_IDC

          factors = Fplantcost[model][phase_processing]

          f_EC   = factors["equipment"]                          
          f_IEC  = sum(factors[k] for k in key_IEC)              
          f_ISBL = sum(factors[k] for k in key_ISBL)             
          f_OSBL = sum(factors[k] for k in key_OSBL)             
          f_DC   = f_ISBL + f_OSBL                                
          f_IDC  = sum(factors[k] for k in key_IDC)             
          f_FCI  = f_DC + f_IDC                          
          f_TCI  = f_FCI * (1 + rate_WC)                  

          f_map = {
               "Equipment cost": f_EC,
               "Installed equipment cost": f_IEC,
               "Inside battery limits": f_ISBL,
               "Fixed capital investment": f_FCI,
               "Total capital investment": f_TCI,
          }

          return (base_cost*f_map[cap_out]/f_map[cap_in])


          

          
     