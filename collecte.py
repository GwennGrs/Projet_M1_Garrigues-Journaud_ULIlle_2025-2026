#!/usr/bin/env python3

# Can be used with Qiskit
from qiskit_ibm_runtime import QiskitRuntimeService
import datetime
import pandas as pd
import numpy as np

def connect():
    QiskitRuntimeService.save_account(
    token="cFnkczqO_S0VNMuk-Ads-7JWIv8ims3hh3d04gFJtcJI",
    instance="open-instance",
    overwrite=True,
    set_as_default = True
    )
    service = QiskitRuntimeService()
    return service

def collect_data_qubit(qubit_props):
    t1 = qubit_props.get("T1", (None,))[0]
    t2 = qubit_props.get("T2", (None,))[0]
    frequency = qubit_props.get("frequency", (None,))[0]
    anharmonicity = qubit_props.get("anharmonicity", (None,))[0]
    readout_error = qubit_props.get("readout_error", (None,))[0]
    prob_meas0_prep1 = qubit_props.get("prob_meas0_prep1", (None,))[0]
    prob_meas1_prep0 = qubit_props.get("prob_meas1_prep0", (None,))[0]
    readout_length = qubit_props.get("readout_length", (None,))[0]
    return np.array([t1, t2, frequency, anharmonicity, readout_error, prob_meas0_prep1, prob_meas1_prep0, readout_length])
    
def collect_data_backend(backend):
    data = []
    name = backend.name
    nb_qubits =  backend.num_qubits
    date = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    col_nom = np.full((nb_qubits, 2), [name, date])

    for index in range(nb_qubits):
        data.append(
            collect_data_qubit(
                backend.properties().qubit_property(index)
                ))
    data = np.c_[col_nom, data]

    df = pd.DataFrame(
        data=data, 
        columns=["nom","time","T1", "T2", "frequency", "anharmonicity", "readout_error", "prob_meas0_prep1", "prob_meas1_prep0", "readout_length"]
        )
    return df

def full_collect(service):
    backends = service.backends(simulator=False, operational=True)
    
    datas = []
    for back in backends:
        datas.append(
            collect_data_backend(back)
        )
    df = pd.concat(datas, ignore_index=True)
    return df

def create_csv(data):
    folder = "/home/gwenn/Desktop/Projet/data"
    date = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    name_file = folder+"/ibm_backends_"+ date + ".csv"
    return data.to_csv(name_file, index=False)

if __name__=="__main__":
    service = connect()
    collected_data = full_collect(service)
    create_csv(collected_data)