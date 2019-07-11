#!/usr/bin/env python

# dictionary of residue names and their corresponding chemical names as they will be dispalyed in the table
res_to_name = {}
res_to_name["ACN"] = "Acetamide"
res_to_name["ACH"] = "Acetic Acid"
res_to_name["ATO"] = "Acetone"
res_to_name["BUT"] = "Butanol"
res_to_name["DMF"] = "Dimethyl Formamide"
res_to_name["DMS"] = "Dimethyl Sulfoxide"
res_to_name["DMP"] = "2,3-Dimercapto-1-propanol"
res_to_name["EAC"] = "Ethyl Acetate"
res_to_name["ETH"] = "Ethanol"
res_to_name["GCL"] = "Ethylene Glycol"
res_to_name["GLY"] = "Glycerol"
res_to_name["MET"] = "Methanol"
res_to_name["PR"] = "Propanol"
res_to_name["PCB"] = "Propylene Carbonate"
res_to_name["PG"] = "Propylene Glycol"
res_to_name["RIB"] = "Ribose"
res_to_name["SOH"] = "Mercaptoethanol"
res_to_name["TET"] = "Tetrose"
res_to_name["THF"] = "Tetrahydrofuran"
res_to_name["URE"] = "Urea"

abbreviation = {}
abbreviation["Acetamide"] = "AcN"
abbreviation["ACN"] = "AcN"
abbreviation["Acetic Acid"] = "AcOH"
abbreviation["ACH"] = "AcOH"
abbreviation["Acetone"] = "ACE"
abbreviation["ATO"] = "ACE"
abbreviation["Butanol"] = "BuOH"
abbreviation["BUT"] = "BuOH"
abbreviation["Dimethyl Formamide"] = "DMF"
abbreviation["DMF"] = "DMF"
abbreviation["Dimethyl Sulfoxide"] = "DMSO"
abbreviation["DMS"] = "DMSO"
abbreviation["2,3-Dimercapto-1-propanol"] = "DMP"
abbreviation["DMP"] = "DMP"
abbreviation["Ethyl Acetate"] = "EAC"
abbreviation["EAC"] = "EAC"
abbreviation["Ethanol"] = "EtOH"
abbreviation["ETH"] = "EtOH"
abbreviation["Ethylene Glycol"] = "EG"
abbreviation["GCL"] = "EG"
abbreviation["Glycerol"] = "GLY"
abbreviation["GLY"] = "GLY"
abbreviation["Methanol"] = "MeOH"
abbreviation["MET"] = "MeOH"
abbreviation["Propanol"] = "PrOH"
abbreviation["PR"] = "PrOH"
abbreviation["Propylene Carbonate"] = "PC"
abbreviation["PCB"] = "PC"
abbreviation["Propylene Glycol"] = "PG"
abbreviation["PG"] = "PG"
abbreviation["Ribose"] = "RIB"
abbreviation["RIB"] = "RIB"
abbreviation["Mercaptoethanol"] = "ME"
abbreviation["SOH"] = "ME"
abbreviation["Tetrose"] = "TET"
abbreviation["TET"] = "TET"
abbreviation["Tetrahydrofuran"] = "THF"
abbreviation["THF"] = "THF"
abbreviation["Urea"] = "URE"
abbreviation["URE"] = "URE"

colors = ['blue', 'red', 'xkcd:green', 'xkcd:orange', 'xkcd:goldenrod']
color_dict = {}
color_dict['MET'] = colors[0]
color_dict['ETH'] = colors[0]
color_dict['PR'] = colors[0]
color_dict['BUT'] = colors[0]
color_dict['GCL'] = colors[1]
color_dict['PG'] = colors[1]
color_dict['GLY'] = colors[1]
color_dict['TET'] = colors[1]
color_dict['RIB'] = colors[1]
color_dict['ACH'] = colors[2]
color_dict['URE'] = colors[2]
color_dict['ACN'] = colors[2]
color_dict['ATO'] = colors[2]
color_dict['SOH'] = colors[3]
color_dict['DMP'] = colors[3]
color_dict['DMS'] = colors[3]
color_dict['THF'] = colors[4]
color_dict['PCB'] = colors[4]
color_dict['EAC'] = colors[4]
color_dict['DMF'] = colors[4]