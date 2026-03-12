import numpy as np
from unit_parameters import *
from eqp_spec_default import vessel_thick, pump_head, vessel_volume, mat_mapping
from MoLib_EQP_Turton import eqpcomo_Turton
from MoLib_EQP_Seider import eqpcomo_Seider
from MoLib_EQP_Smith import eqpcomo_Smith
from MoLib_EQP_Towler import eqpcomo_Towler
from MoLib_EQP_Peters import eqpcomo_Peters
from MoLib_EQP_Guthrie import eqpcomo_Guthrie


EQPCOMO_list=["Turton", "Seider", "Smith", "Towler", "Peters", "Guthrie"]
CE_basis_dict={"Turton": [397,"2001 year basis"],
               "Seider": [394, "2000 year basis"],
               "Smith": [394, "2000 year basis"], 
               "Towler": [478.6, "2006 year basis"], 
               "Peters":[394.3, "2002 year basis"], 
               "Guthrie":[113.7, "1968 year basis"]}


def eqpcomo(*,model="", equipment=None, material=None, eqptype=None, T_K=None, P_bar=None, Pout_bar=None,
            vol_cum=None, area_sqm=None, height_m=None, diameter_m=None, thickness_m=None, 
            volflow_cumph=None, massflow_kgph=None, power_kW=None, driver=None, num=None, packsize_in=None, pumphead_m=None):
     #Equipment material name normalize
     material=mat_mapping(material)
     basis_year=CE_basis_dict[model][1]
     # Provide variables default value=======================================================================
     # Vessel volume defination
     if equipment == "Vessel/Tower" and vol_cum==None:
          if height_m != None and diameter_m != None:
               vol_cum=vessel_volume(diameter_m, height_m)
     # Vessel thickness definition
     if equipment == "Vessel/Tower" and thickness_m==None:
          if P_bar != None and diameter_m != None and T_K !=None:
               thickness_m=vessel_thick(diameter_m,P_bar,T_K,material)
     # Error message: Model name is not defined.
     if model==None:
          return (print("Error: The 'model' must be defined for equipment cost estimation."))
     elif model not in EQPCOMO_list:
          return (print(f"Error: The model is not available in the equipment cost estimation model library. Available models: {EQPCOMO_list}"))
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
                    "Mixer":{"eqptype":eqptype, "material":material,"vol_cum":vol_cum},
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
                    "Liquid-liquid extractor": {"eqptype":eqptype, "material":material,"height_m":height_m, "diameter_m":diameter_m    } , 
                    "Mixer": {"eqptype":eqptype, "material":material, "vol_cum":vol_cum  } , 
                    "Storage tank": {"eqptype":eqptype, "material":material, "vol_cum":vol_cum,"P_bar":P_bar   } , 
                    "Turbines" : {"eqptype":eqptype, "material":material, "power_kW":power_kW,   } , 
                    "Centrifuge" : {"eqptype":eqptype, "material":material, "diameter_m":diameter_m   } , 
                    "Crystallizer-batch evaporative" : {"eqptype":eqptype, "material":material, "vol_cum":vol_cum   } , 
                    "Crystallizer-cooling" : {"eqptype":eqptype, "material":material, "height_m":height_m   } , 
                    "Dewatering press" : {"eqptype":eqptype, "material":material, "massflow_kgph":massflow_kgph   } ,

                    "Dryer" : {"eqptype":eqptype, "material":material, "area_sqm":area_sqm, "massflow_kgph":massflow_kgph   }, #area_sqm for eqptype=="Drum", "Rotary(gas fired)", "Rotary(steam tube)", "Tray"
                                                                                                                               # massflow_kgph for eqptype=="Spray"
                    "Adsorbent" : {"eqptype":eqptype, "vol_cum":vol_cum   } , 
                    "Autoclave": {"eqptype":eqptype, "material":material, "vol_cum":vol_cum   } , 
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
                    "Trays":{"eqptype":eqptype, "material":material,   "diameter_m":diameter_m       },
                    "Mixer":{"eqptype":eqptype, "material":material, "power_kW":power_kW          },
                    "Agitator":{ "eqptype":eqptype, "material":material,"power_kW":power_kW          },
                    "Heater":{"eqptype":eqptype, "material":material, "massflow_kgph":massflow_kgph          },
                    "Furnace":{"eqptype":eqptype, "material":material,"power_kW":power_kW           },
                    "Compressor":{  "eqptype":eqptype, "material":material, "power_kW":power_kW        },
                    "Conveyor":{ "eqptype":eqptype,  "area_sqm":area_sqm        },
                    "Size reduction equipment":{"eqptype":eqptype, "massflow_kgph":massflow_kgph          },
                    "Crystallizer-cooling":{"eqptype":eqptype, "material":material,  "height_m":height_m         }, 
                    "Vessel/Tower":{"eqptype":eqptype, "material":material, "diameter_m":diameter_m, "thickness_m":thickness_m, "height_m":height_m        }, 

                    "Dryer":{"eqptype":eqptype, "material":material, "area_sqm":area_sqm, "massflow_kgph":massflow_kgph    },#area_sqm for eqptype=="Drum", "Rotary(gas fired)", "Rotary(steam tube)", "Tray"
                                                                                                                                       # massflow_kgph for eqptype=="Spray"
                    "Evaporator":{"eqptype":eqptype, "material":material, "area_sqm":area_sqm          },
                    "Heat exchanger (shell and tube)" :{"eqptype":eqptype, "material":material, "area_sqm":area_sqm          },
                    "Heat exchanger (others)":{"eqptype":eqptype, "material":material,  "area_sqm":area_sqm         },

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
                    "Storage tank":{"eqptype":eqptype, "material":material, "vol_cum": vol_cum     }
                    },
               "Guthrie":{
                    "Vessel/Tower": { "eqptype":eqptype, "material":material, "P_bar":P_bar, "height_m":height_m, "diameter_m":diameter_m   }, 
                    "Furnace": { "eqptype":eqptype, "material":material, "P_bar":P_bar, "power_kW":power_kW,       }, 
                    "Heater": {  "eqptype":eqptype, "material":material, "P_bar":P_bar, "power_kW":power_kW   }, 
                    "Heat exchanger (others)": { "eqptype":eqptype, "material":material,"P_bar":P_bar, "area_sqm":area_sqm      },
                    "Heat exchanger (shell and tube)": { "eqptype":eqptype, "material":material,  "area_sqm":area_sqm, "P_bar":P_bar      }, 
                    "Pumps": {"eqptype":eqptype, "material":material, "volflow_cumph":volflow_cumph,  "P_bar":P_bar, "Pout_bar": Pout_bar  }, 
                    "Compressor": { "eqptype":eqptype, "material":material,  "power_kW":power_kW, "driver":driver}
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
          eqpo=eqpcomo_Towler(equipment,material,eqptype,P_bar,Pout_bar,vol_cum,power_kW,volflow_cumph,massflow_kgph,
                              area_sqm,packsize_in,height_m,diameter_m,thickness_m,T_K,num,driver)
     elif model == "Peters":
          eqpo=eqpcomo_Peters(equipment,material,eqptype,P_bar,Pout_bar,vol_cum,power_kW,volflow_cumph,massflow_kgph,
                              area_sqm,packsize_in,height_m,diameter_m,thickness_m,T_K,num,driver)
     elif model =="Guthrie":
          eqpo=eqpcomo_Guthrie(equipment,material,eqptype,P_bar,Pout_bar,vol_cum,power_kW,volflow_cumph,massflow_kgph,
                              area_sqm,packsize_in,height_m,diameter_m,thickness_m,T_K,num,driver)

     return (eqpco, basis_year)

