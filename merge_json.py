import json
import datetime
import os

import pandas as pd


#insert : {complet, gates or qubit}
def combineJson(prefixe_name):
    folder = "data_json/"
    date = datetime.datetime.now().strftime("%Y-%m-%d_%H")
    elements = os.listdir(folder)
    files = []

    for name_file in elements:
        if prefixe_name in name_file and name_file.endswith(".json"):
            print(name_file)
            file = pd.read_json(folder+"/"+name_file)
            files.append(file)
    
    merged_file = pd.concat(files, ignore_index=True)
    output_folder = "data_hour/"
    name_file = output_folder+"ibm_backend_" + prefixe_name + "_hourly_total_" + date +".json"
    return merged_file.to_json(name_file, index=False)

if __name__=="__main__":
    combineJson("qubit")
    combineJson("complet")
    combineJson("gates")

