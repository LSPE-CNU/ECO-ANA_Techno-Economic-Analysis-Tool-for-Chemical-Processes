import numpy as np
from .unit_parameters import *
from .eqp_spec_default import vessel_thick, pump_head, vessel_volume, mat_mapping
from .MoLib_EQP_Turton import eqpcomo_Turton
from .MoLib_EQP_Seider import eqpcomo_Seider
from .MoLib_EQP_Smith import eqpcomo_Smith
from .MoLib_EQP_Towler import eqpcomo_Towler
from .MoLib_EQP_Peters import eqpcomo_Peters
from .MoLib_EQP_Guthrie import eqpcomo_Guthrie


EQPCOMO_list=["Turton", "Seider", "Smith", "Towler", "Peters", "Guthrie"]
CE_basis_dict={"Turton": [397,"2001 year basis"],
               "Seider": [394, "2000 year basis"],
               "Smith": [394, "2000 year basis"], 
               "Towler": [478.6, "2006 year basis"], 
               "Peters":[394.3, "2002 year basis"], 
               "Guthrie":[115, "1968 year basis"]}     # Biegler et al. (1997) p.133: CE = 115 for mid-1968 (Guthrie)


def eqpcomo(*,model="", equipment=None, material=None, eqptype=None, T_K=0, P_bar=0, Pout_bar=0,
            vol_cum=0, area_sqm=0, height_m=0, diameter_m=0, thickness_m=0, 
            volflow_cumph=0, massflow_kgph=0, power_kW=0, driver=None, num=0, packsize_in=None, pumphead_m=0, length_m=0):
     """Equipment purchase cost. Returns (cost in USD, basis year). On an input error an error message is printed
     and the cost is None; the result is always a 2-tuple, (None, None) when the model is missing or unknown."""
     result=_eqpcomo_impl(model=model, equipment=equipment, material=material, eqptype=eqptype, T_K=T_K, P_bar=P_bar,
                          Pout_bar=Pout_bar, vol_cum=vol_cum, area_sqm=area_sqm, height_m=height_m, diameter_m=diameter_m,
                          thickness_m=thickness_m, volflow_cumph=volflow_cumph, massflow_kgph=massflow_kgph,
                          power_kW=power_kW, driver=driver, num=num, packsize_in=packsize_in, pumphead_m=pumphead_m,
                          length_m=length_m)
     basis_year=CE_basis_dict[model][1] if isinstance(model, str) and model in CE_basis_dict else None
     if result is None:                       # error message already printed
          return (None, basis_year)
     cost=result[0]
     if cost is None:
          return (None, basis_year)
     if isinstance(cost, str):                # error message returned by a model module
          print(cost if cost.startswith("Error") else f"Error: {cost}")
          return (None, basis_year)
     if not np.isfinite(float(cost)) or float(cost)<0:
          print(f"Error: The estimated cost ({cost}) is not a finite non-negative value; check the inputs.")
          return (None, basis_year)
     return (cost, basis_year)


def _eqpcomo_impl(*,model="", equipment=None, material=None, eqptype=None, T_K=0, P_bar=0, Pout_bar=0,
            vol_cum=0, area_sqm=0, height_m=0, diameter_m=0, thickness_m=0, 
            volflow_cumph=0, massflow_kgph=0, power_kW=0, driver=None, num=0, packsize_in=None, pumphead_m=0, length_m=0):
     #Equipment material name normalize
     material=mat_mapping(material)
     # Provide variables default value=======================================================================
     # Vessel volume defination
     # vol_cum and thickness_m are optional for vessels: when they are not given (None or 0, the default),
     # they are estimated from the diameter, height, pressure and temperature
     if equipment == "Vessel/Tower" and not vol_cum:
          if height_m and diameter_m:
               vol_cum=vessel_volume(diameter_m, height_m)
     # Vessel thickness definition
     if equipment == "Vessel/Tower" and not thickness_m:
          if P_bar is not None and diameter_m and T_K:
               thickness_m=vessel_thick(diameter_m,P_bar,T_K,material)
               if thickness_m is None or thickness_m<=1e-4:
                    import warnings
                    warnings.warn("The estimated vessel wall thickness is ~0 (pressure 0 or not given); provide 'thickness_m' for weight-based vessel correlations.", UserWarning, stacklevel=2)
     # Error message: Model name is not defined.
     if model==None:
          return (print("Error: The 'model' must be defined for equipment cost estimation."))
     elif model not in EQPCOMO_list:
          return (print(f"Error: The model is not available in the equipment cost estimation model library. Available models: {EQPCOMO_list}"))
     basis_year=CE_basis_dict[model][1]
     required_var={
               "Turton":{
                    "Blender":{"eqptype":eqptype, "material":material, "vol_cum":vol_cum},
                    "Centrifuge":{"eqptype":eqptype, "material":material, "diameter_m":diameter_m},
                    "Compressor":{"eqptype":eqptype, "power_kW":power_kW, "P_bar":P_bar, "material":material, "driver":driver},
                    "Conveyor":{"eqptype":eqptype, "material":material, "area_sqm":area_sqm},
                    "Crystallizer-batch evaporative":{"eqptype":eqptype, "material":material, "vol_cum":vol_cum},
                    "Dryer":{"eqptype":eqptype, "material":material, "area_sqm":area_sqm},
                    "Dust collector":{"eqptype":eqptype, "material":material, "vol_cum":vol_cum},
                    "Evaporator":{"eqptype":eqptype, "area_sqm":area_sqm, "P_bar":P_bar, "material":material},
                    "Fans":{"eqptype":eqptype, "volflow_cumph":volflow_cumph, "P_bar":P_bar, "material":material, "Pout_bar":Pout_bar},
                    "Furnace":{"eqptype":eqptype, "power_kW":power_kW, "P_bar":P_bar, "material":material},
                    "Filters":{"eqptype":eqptype, "material":material,"area_sqm":area_sqm},
                    "Mixer":{"eqptype":eqptype, "material":material,"power_kW":power_kW},   # Turton Table A.1: mixer size = power, kW
                    "Heater":{"eqptype":eqptype, "power_kW":power_kW, "P_bar":P_bar, "material":material},
                    "Packing":{"eqptype":eqptype, "vol_cum":vol_cum, "P_bar":P_bar, "material":material},
                    "Vessel/Tower":{"eqptype":eqptype, "vol_cum":vol_cum, "P_bar":P_bar, "material":material, "diameter_m":diameter_m, "height_m":height_m },
                    "Pumps":{"eqptype":eqptype, "power_kW":power_kW, "P_bar":P_bar, "material":material},
                    "Reactor":{"eqptype":eqptype, "material":material, "vol_cum":vol_cum},
                    "Storage tank":{"eqptype":eqptype, "vol_cum":vol_cum, "P_bar":P_bar, "material":material},
                    "Screens":{"eqptype":eqptype, "material":material,"area_sqm":area_sqm},
                    "Trays":{"eqptype":eqptype, "area_sqm":area_sqm, "P_bar":P_bar, "material":material, "diameter_m":diameter_m, "num":num },
                    "Turbines":{"eqptype":eqptype, "material":material,"power_kW":power_kW},
                    "Vaporizer":{"eqptype":eqptype, "vol_cum":vol_cum, "P_bar":P_bar, "material":material},
                    "Heat exchanger (shell and tube)":{"eqptype":eqptype, "area_sqm":area_sqm, "P_bar":P_bar, "material":material},
                    "Heat exchanger (others)":{"eqptype":eqptype, "area_sqm":area_sqm, "P_bar":P_bar, "material":material}
                                             },
               "Seider":{
                    "Pumps":{"eqptype":eqptype, "material":material,"volflow_cumph":volflow_cumph, "pumphead_m":pumphead_m, "power_kW":power_kW, "driver":driver   },
                    "Agitator": {"eqptype":eqptype, "material":material, "power_kW":power_kW     } , 
                    "Crystallizer-continuous evaporative": {"eqptype":eqptype, "material":material, "massflow_kgph":massflow_kgph,   } , 
                    "Dust collector": {"eqptype":eqptype, "material":material, "volflow_cumph":volflow_cumph   } , 
                    "Evaporator": {"eqptype":eqptype, "material":material, "area_sqm":area_sqm   } , 
                    "Furnace": {"eqptype":eqptype, "material":material, "power_kW":power_kW,"P_bar":P_bar   } , 
                    "Liquid-liquid extractor": {"material":material,"height_m":height_m, "diameter_m":diameter_m    } ,   # no eqptype in Seider 
                    "Mixer": {"eqptype":eqptype, "material":material, "vol_cum":vol_cum  } , 
                    "Storage tank": {"eqptype":eqptype, "material":material, "vol_cum":vol_cum,"P_bar":P_bar   } , 
                    "Turbines" : {"eqptype":eqptype, "material":material, "power_kW":power_kW,   } , 
                    "Centrifuge" : {"eqptype":eqptype, "material":material, "diameter_m":diameter_m   } , 
                    "Crystallizer-batch evaporative" : {"material":material, "vol_cum":vol_cum   } ,   # no eqptype in Seider 
                    "Crystallizer-cooling" : {"eqptype":eqptype, "material":material, "height_m":height_m   } , 
                    "Dewatering press" : {"eqptype":eqptype, "material":material, "massflow_kgph":massflow_kgph   } ,

                    "Dryer" : {"eqptype":eqptype, "material":material, "area_sqm":area_sqm, "massflow_kgph":massflow_kgph   }, #area_sqm for eqptype=="Drum", "Rotary(gas fired)", "Rotary(steam tube)", "Tray"
                                                                                                                               # massflow_kgph for eqptype=="Spray"
                    "Adsorbent" : {"eqptype":eqptype, "vol_cum":vol_cum   } , 
                    "Autoclave": {"material":material, "vol_cum":vol_cum   } ,   # no eqptype in Seider 
                    "Blower" : {"eqptype":eqptype, "material":material, "power_kW":power_kW   } , 
                    "Compressor" : {"eqptype":eqptype, "material":material, "power_kW":power_kW,"driver":driver   } , 
                    "Fans" : {"eqptype":eqptype, "material":material, "Pout_bar":Pout_bar, "P_bar":P_bar, "volflow_cumph":volflow_cumph  } , 
                    "Filters" : {"eqptype":eqptype, "area_sqm":area_sqm   } , 
                    "Heat exchanger (others)" : {"eqptype":eqptype, "material":material, "area_sqm":area_sqm,    } , 
                    "Heat exchanger (shell and tube)" : {"eqptype":eqptype, "material":material, "P_bar":P_bar, "area_sqm":area_sqm,"height_m":height_m    } , 
                    "Heater" : {"eqptype":eqptype, "power_kW":power_kW,    } , 

                    "Membrane (for reverse osmosis)": {"eqptype":eqptype, "volflow_cumph":volflow_cumph   } , 
                    "Membrane" : {"eqptype":eqptype, "area_sqm":area_sqm   } , 

                    "Packing" : {"eqptype":eqptype, "material":material, "vol_cum":vol_cum, "packsize_in":packsize_in    } , 
                    "Size enlargement equipment" : {"eqptype":eqptype, "material":material,"massflow_kgph":massflow_kgph    } , 
                    "Size reduction equipment" : {"eqptype":eqptype,  "massflow_kgph":massflow_kgph  } , 
                    "Solid-liquid separator": {"eqptype":eqptype,  "area_sqm":area_sqm  } , 
                    "Trays": {"eqptype":eqptype, "material":material,"diameter_m":diameter_m , "num":num   } , 
                    "Vacuum system" : {"eqptype":eqptype,  "volflow_cumph":volflow_cumph  } , 
                    "Vessel/Tower" : {"eqptype":eqptype, "material":material, "diameter_m":diameter_m ,"height_m":height_m, "thickness_m":thickness_m } 
                    },
               "Smith":{
                    "Vessel/Tower":{"eqptype":eqptype,"T_K":T_K,"P_bar":P_bar,"material":material, "diameter_m":diameter_m,"thickness_m":thickness_m,"height_m":height_m  },
                    "Filters":{ "eqptype":eqptype,"T_K":T_K,"P_bar":P_bar,"area_sqm":area_sqm   },
                    "Storage tank":{ "eqptype":eqptype,"T_K":T_K,"P_bar":P_bar,  "vol_cum":vol_cum},
                    "Heater":{"eqptype":eqptype,"T_K":T_K,"P_bar":P_bar,"massflow_kgph":massflow_kgph   },
                    "Reactor":{ "eqptype":eqptype,"T_K":T_K,"P_bar":P_bar,"material":material, "vol_cum":vol_cum  },
                    "Trays":{ "eqptype":eqptype,"T_K":T_K,"P_bar":P_bar,"material":material, "diameter_m":diameter_m , "num":num },
                    "Packing (Structured)":{ "eqptype":eqptype,"T_K":T_K,"P_bar":P_bar,"material":material, "diameter_m":diameter_m , "height_m":height_m },
                    "Heat exchanger (others)":{ "eqptype":eqptype,"T_K":T_K,"P_bar":P_bar,"material":material,"area_sqm":area_sqm   },
                    "Pumps":{ "eqptype":eqptype,"T_K":T_K,"P_bar":P_bar,"material":material, "power_kW":power_kW  },
                    "Compressor":{  "eqptype":eqptype,"T_K":T_K,"P_bar":P_bar,"material":material, "power_kW":power_kW },
                    "Fans":{ "eqptype":eqptype,"T_K":T_K,"P_bar":P_bar,"material":material, "power_kW":power_kW  },
                    "Dryer":{ "eqptype":eqptype,"T_K":T_K,"P_bar":P_bar,"material":material,"massflow_kgph":massflow_kgph   },
                    "Heat exchanger (shell and tube)":{ "eqptype":eqptype,"T_K":T_K,"P_bar":P_bar,"material":material,"area_sqm":area_sqm   }},
               "Towler":{
                    "Trays":{"eqptype":eqptype, "material":material,   "diameter_m":diameter_m, "num":num       },
                    "Mixer":{"eqptype":eqptype, "material":material, "power_kW":power_kW          },
                    "Agitator":{ "eqptype":eqptype, "material":material,"power_kW":power_kW          },
                    "Heater":{"eqptype":eqptype, "material":material, "massflow_kgph":massflow_kgph          },
                    "Furnace":{"eqptype":eqptype, "material":material,"power_kW":power_kW           },
                    "Compressor":{  "eqptype":eqptype, "material":material, "power_kW":power_kW        },
                    "Conveyor":{ "eqptype":eqptype,  "length_m":length_m        },      # belt length; width via diameter_m (0.5-1.0 m, default 1.0)
                    "Size reduction equipment":{"eqptype":eqptype, "massflow_kgph":massflow_kgph          },
                    "Crystallizer-cooling":{"eqptype":eqptype, "material":material,  "height_m":height_m         }, 
                    "Vessel/Tower":{"eqptype":eqptype, "material":material, "diameter_m":diameter_m, "thickness_m":thickness_m, "height_m":height_m        }, 

                    "Dryer":{"eqptype":eqptype, "material":material, "area_sqm":area_sqm, "massflow_kgph":massflow_kgph    },#area_sqm for eqptype=="Drum", "Rotary(gas fired)", "Rotary(steam tube)", "Tray"
                                                                                                                                       # massflow_kgph for eqptype=="Spray"
                    "Evaporator":{"eqptype":eqptype, "material":material, "area_sqm":area_sqm          },
                    "Heat exchanger (shell and tube)" :{"eqptype":eqptype, "material":material, "area_sqm":area_sqm          },
                    "Heat exchanger (others)" :{"eqptype":eqptype, "material":material, "area_sqm":area_sqm          },   # plate-and-frame exchanger

                    "Filters" :{ "eqptype":eqptype, "vol_cum":vol_cum , "area_sqm":area_sqm   }, 		# vol_cum for eqptype=="Plate and frame",  # area_sqm for eqptype=="Vacuum filter"
                    "Packing":{ "eqptype":eqptype,  "material":material , "vol_cum":vol_cum       },
                    "Packing (Structured)":{"eqptype":eqptype, "material":material,   "diameter_m":diameter_m,   "height_m":height_m      } ,
                    "Pumps":{ "eqptype":eqptype, "material":material,  "volflow_cumph":volflow_cumph        },
                    "Reactor":{ "eqptype":eqptype, "material":material,   "vol_cum":vol_cum       }, 
                    "Storage tank":{   "eqptype":eqptype, "material":material,  "vol_cum":vol_cum      },
                    "Water ion exchanger":{   "volflow_cumph":volflow_cumph       }
                    },
               "Peters":{
                    "Turbines":{"eqptype":eqptype, "material":material,"power_kW":power_kW        },
                    "Compressor":{"eqptype":eqptype, "material":material,  "power_kW":power_kW, "driver":driver      },
                    "Heat exchanger (shell and tube)":{"eqptype":eqptype, "material":material,  "area_sqm":area_sqm      },
                    "Heat exchanger (others)":{"eqptype":eqptype, "material":material,  "area_sqm":area_sqm      },
                    "Pumps":{"eqptype":eqptype, "material":material, "P_bar":P_bar , "volflow_cumph":volflow_cumph      },
                    "Vessel/Tower":{"eqptype":eqptype, "material":material, "P_bar":P_bar, "diameter_m":diameter_m,   "height_m":height_m,  "thickness_m":thickness_m  },
                    "Storage tank":{"eqptype":eqptype, "material":material, "vol_cum": vol_cum     },
                    "Evaporator":{"eqptype":eqptype, "material":material, "area_sqm":area_sqm, "P_bar":P_bar      },
                    "Vaporizer":{"eqptype":eqptype, "material":material, "vol_cum":vol_cum, "P_bar":P_bar      },
                    "Furnace":{"eqptype":eqptype, "power_kW":power_kW      },
                    "Heater":{"eqptype":eqptype, "material":material, "power_kW":power_kW, "P_bar":P_bar      },
                    "Reactor":{"eqptype":eqptype, "material":material, "vol_cum":vol_cum, "P_bar":P_bar      },
                    "Autoclave":{"material":material, "vol_cum":vol_cum      },   # no eqptype in Peters
                    "Fans":{"eqptype":eqptype, "volflow_cumph":volflow_cumph      },
                    "Blower":{"eqptype":eqptype, "volflow_cumph":volflow_cumph, "P_bar":P_bar, "Pout_bar":Pout_bar      },
                    "Trays":{"eqptype":eqptype, "material":material, "diameter_m":diameter_m, "num":num      },
                    "Packing":{"eqptype":eqptype, "material":material, "diameter_m":diameter_m, "height_m":height_m      },
                    # second digitization batch: the size variable depends on the type (checked in MoLib_EQP_Peters)
                    "Vacuum system":{"eqptype":eqptype, "material":material, "massflow_kgph":massflow_kgph      },     # air load
                    "Agitator":{"eqptype":eqptype, "material":material, "power_kW":power_kW      },
                    "Mixer":{"eqptype":eqptype, "material":material      },                                       # vol_cum, power_kW or diameter_m
                    "Blender":{"eqptype":eqptype, "material":material, "vol_cum":vol_cum      },
                    "Size enlargement equipment":{"eqptype":eqptype, "massflow_kgph":massflow_kgph      },
                    "Dewatering press":{"eqptype":eqptype, "massflow_kgph":massflow_kgph      },
                    "Conveyor":{"eqptype":eqptype, "length_m":length_m      },                                    # + diameter_m (width) or massflow_kgph (pneumatic)
                    "Size reduction equipment":{"eqptype":eqptype, "massflow_kgph":massflow_kgph      },
                    "Dryer":{"eqptype":eqptype, "material":material, "area_sqm":area_sqm      },
                    "Filters":{"eqptype":eqptype, "material":material, "area_sqm":area_sqm      },
                    "Screens":{"eqptype":eqptype, "material":material, "area_sqm":area_sqm      },
                    "Centrifuge":{"eqptype":eqptype, "material":material, "diameter_m":diameter_m      },
                    "Dust collector":{"eqptype":eqptype, "volflow_cumph":volflow_cumph      }   # material: required only for dry collectors (Fig. 15-48)
                    },
               "Guthrie":{
                    "Vessel/Tower": { "eqptype":eqptype, "material":material, "P_bar":P_bar, "height_m":height_m, "diameter_m":diameter_m   }, 
                    "Furnace": { "eqptype":eqptype, "material":material, "P_bar":P_bar, "power_kW":power_kW,       }, 
                    "Heater": {  "eqptype":eqptype, "material":material, "P_bar":P_bar, "power_kW":power_kW   }, 
                    "Heat exchanger (others)": { "eqptype":eqptype, "material":material,"P_bar":P_bar, "area_sqm":area_sqm      },
                    "Heat exchanger (shell and tube)": { "eqptype":eqptype, "material":material,  "area_sqm":area_sqm, "P_bar":P_bar      }, 
                    "Pumps": {"eqptype":eqptype, "material":material, "volflow_cumph":volflow_cumph,  "P_bar":P_bar, "Pout_bar": Pout_bar  }, 
                    "Compressor": { "eqptype":eqptype, "power_kW":power_kW, "driver":driver}
               }
               }

     # Error message: A equipment not supported by the model has been selected.
     lst_EQPavail=required_var[model].keys()
     if equipment not in lst_EQPavail:
          return(print(f"Error: The selected equipment '{equipment}' is not available in the equipment cost estimation model. Available equipment options: {list(lst_EQPavail)}"))
     
     # Error message: Validate that all required variable inputs are not provided.
     model_required_var = required_var[model][equipment]
     missing_var = [k for k, v in model_required_var.items() if v is None]
     if missing_var and equipment =="Vessel/Tower":
          return (print(f"Error: Missing required input variables for the selected model and equipment. Missing variables: {missing_var}. The variable 'vol_cum' and 'thickness_m' are optional."))
     elif missing_var and equipment =="Dryer" and model in ["Seider", "Towler"]:
          return (print(f"Error: Missing required input variables for the selected model and equipment. Missing variables: {missing_var}. The variable 'massflow_kgph' is only need for 'eqptype'=='Spray'."))
     elif missing_var and equipment =="Filters" and model in ["Towler"]:
          return (print(f"Error: Missing required input variables for the selected model and equipment. Missing variables: {missing_var}. The variable 'vol_cum' is only need for 'eqptype'=='Plate and frame'."))
     elif missing_var:
          return (print(f"Error: Missing required input variables for the selected model and equipment. Missing variables: {missing_var}"))
     
     # Mapping model & Equipment cost estimation
     if model == "Turton":
          eqpco=eqpcomo_Turton(equipment, material, eqptype, P_bar, Pout_bar, vol_cum, power_kW, volflow_cumph, massflow_kgph, 
                              area_sqm, packsize_in, height_m, diameter_m, thickness_m, T_K, num, driver)
     elif model == "Seider":
          eqpco=eqpcomo_Seider(equipment,material,eqptype,P_bar, Pout_bar,vol_cum,power_kW,volflow_cumph,massflow_kgph,
                               area_sqm,packsize_in,height_m,diameter_m,thickness_m,T_K,num,driver, pumphead_m)
     elif model == "Smith":
          eqpco=eqpcomo_Smith(equipment,material,eqptype,P_bar,Pout_bar,vol_cum,power_kW,volflow_cumph,massflow_kgph,
                              area_sqm,packsize_in,height_m,diameter_m,thickness_m,T_K,num,driver)
     elif model == "Towler":
          eqpco=eqpcomo_Towler(equipment,material,eqptype,P_bar,Pout_bar,vol_cum,power_kW,volflow_cumph,massflow_kgph,
                              area_sqm,packsize_in,height_m,diameter_m,thickness_m,T_K,num,driver, length_m)
     elif model == "Peters":
          eqpco=eqpcomo_Peters(equipment,material,eqptype,P_bar,Pout_bar,vol_cum,power_kW,volflow_cumph,massflow_kgph,
                              area_sqm,packsize_in,height_m,diameter_m,thickness_m,T_K,num,driver, length_m)
     elif model =="Guthrie":
          eqpco=eqpcomo_Guthrie(equipment,material,eqptype,P_bar,Pout_bar,vol_cum,power_kW,volflow_cumph,massflow_kgph,
                              area_sqm,packsize_in,height_m,diameter_m,thickness_m,T_K,num,driver)

     return (eqpco, basis_year)


