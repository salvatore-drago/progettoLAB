import sys
#from river import drift
import skmultiflow as sk
from pyod.models.lof import LOF
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time

#dataset e risultati
dataset_np=[]
verita=[]
risultati=[]

#variabili architettura
max_model=[]
dim_finestra=[]

#stream dati
data_stream=[]

#Concept Drift Detection Module
cd_d=[]
cd_m=[]

#Anomaly Detection Module
Lof_model=[] #lista dei modelli LOF

#variabili utili
fine=False
n_batch=0 
time=[]

def carica_dataset(dataset_name, usecols_feature, usecols_verita):
    dataset_np=pd.read_csv(dataset_name ,usecols=usecols_feature).to_numpy()
    verita=pd.read_csv(dataset_name ,usecols=usecols_verita).values.tolist()
    print(dataset_np[0])
    print(verita[0])


def feature_sintetica(dataset):  #feature aggiuntiva per il rilevamento del concept drif sulle singole feature
    for i in range(0, len(dataset)):
        new_f=0
        for j in range(0, len(dataset[i])):
            new_f=new_f+dataset[i][j]**2
        dataset[i].append(new_f)
  
def prepara_stream(): 
    data_stream= sk.data.DataStream(dataset_np,y=None)
    data_stream.print_df()
    data_stream.prepare_for_use()

def start(dn,uf,uv):
    carica_dataset(dn,uf,uv)
    prepara_stream()
    while fine!=True:
        start_time=time.time*1000
        n_batch+=1


def main():
    if len(sys.argv)<7:
        print("Sono richiesti sei o più parametri: Nome del dataset da leggere, Nome del dataset da creare per memorizzare i risultati, numero massimo di modelli, dimensione finestra dati, nomi delle feature da utilizzare, nome della verita")
        print("Esempio: python anomaly_detection_under_concept_v2.py SRdrift.csv SRdrift_risultati_150_v2.csv 5 150 A B C V")
        return
    else:
        dn=sys.argv[1]
        risultati=sys.argv[2]
        max_model=sys.argv[3]
        dim_finestra=sys.argv[4]
        uf=[]
        for i in range(5,len(sys.argv)-1):
            uf.append(sys.argv[i])
        uv=[]
        uv.append(sys.argv[-1])
        print(dn,risultati,max_model,dim_finestra, uf,uv)
        #start(dn,uf,uv)
        return

if __name__ == "__main__":
    main()
