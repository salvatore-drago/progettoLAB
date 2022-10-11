import sys
#from river import drift
import skmultiflow as sk
from pyod.models.lof import LOF
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import csv

#dataset e risultati
#dataset_np=[]
#verita=[]
#risultati=[]

#variabili architettura
#max_model=[]
#dim_finestra=[]

#stream dati
#data_stream=[]

#Concept Drift Detection Module
#old_data=[]
#new_data=[]
sintetica=[] #feature
#cd_d=[]
#cd_m=[]
#cd_d_flag=[]
#cd_m_flag=[]
#cl=[] #per ogni modello la lista delle confidance di previsione sui dati con cui è stato originariamente addestrato

#Anomaly Detection Module
#ml=[] #lista dei modelli LOF
n_neig=25 #numero vicini da considerare

#variabili utili
#n_feature=0
fine=False
#n_batch=0 
start_time=0
stop_time=0
time=0
#m=[] #modello attualmente in uso
#utilizzo_m=[] # numero di volte il cui quel modello è stato utilizzato
#score_m={}# score dei modelli
#n_modelli_usati=0
#n_riutilizzo_modello=0


def carica_dataset(dataset_name, usecols_feature, usecols_verita):
    dataset_np=pd.read_csv(dataset_name ,usecols=usecols_feature).to_numpy()
    verita=pd.read_csv(dataset_name ,usecols=usecols_verita).values.tolist()
    print(dataset_np[0])
    print(verita[0])
    return dataset_np,verita


def feature_sintetica(dataset):  #feature aggiuntiva per il rilevamento del concept drif sulle singole feature
    sintetica=[]
    for i in range(0, len(dataset)):
        new_f=0
        for j in range(0, len(dataset[i])):
            new_f=new_f+dataset[i][j]**2
        sintetica[i].append(new_f)
  
def prepara_stream_e_CD(dataset_np,n_feature,dim_finestra,max_model):
    cd_d=[]
    cd_m=[]
    cd_d_flag=[]
    cd_m_flag=[]
    data_stream= sk.data.DataStream(dataset_np,y=None)
    data_stream.print_df()
    data_stream.prepare_for_use()
    for i in range(0,n_feature+1):
        cd_d.append(sk.drift_detection.KSWIN(alpha=0.005, window_size=dim_finestra*2, stat_size=dim_finestra))
        cd_d_flag.append(False)
    for i in range(0,max_model):
        cd_m_flag.append(False)
    return data_stream, cd_d, cd_m, cd_d_flag, cd_m_flag

def reset_all_flag(cd_d_flag, cd_m_flag, cd_d, cd_m):
    for i in range(0, len(cd_d_flag)):
        cd_d_flag[i]=False
    for i in range(0, len(cd_m_flag)):
        cd_m_flag[i]=False
    for i in range(0, len(cd_d)):
        cd_d[i].reset()
    for i in range(0, len(cd_m)):
        cd_m[i].reset()

def sliding_window(data_stream,dim_finestra):
    data = data_stream.next_sample(batch_size=dim_finestra)[0]
    return data
    
        

def aggiungi_modello(max_model,ml,old_data,cl,utilizzo_m,n_batch,score_m):
    if(len(ml)>=max_model):
        elimina_modello(utilizzo_m,n_batch,score_m,ml,cl)
    ml.append(LOF(n_neighbors=n_neig, algorithm='ball_tree', leaf_size=30, metric='minkowski', p=3, metric_params=None, contamination=0.1, n_jobs=1))
    m=len(ml)-1
    ml[m].fit(old_data)
    y_pred,y_conf=ml[m].predict(old_data,return_confidence=True)
    cl.append(y_conf)
    utilizzo_m.append(0) #da fare
    print(f"\n Creato modello {m}, modelli presenti:{len(ml)}")
    return m

def score_modello(utilizzo_m,n_batch,score_m):
    for i in range(0, len(utilizzo_m)):
        s=utilizzo_m[i]+[(i*10*n_batch)/100] # Combinazione Utilizzo/Creazione recente
        score_m[i]=s

def elimina_modello(utilizzo_m,n_batch,score_m,ml,cl):
    score_modello(utilizzo_m,n_batch,score_m)
    scores=sorted(score_m.values())
    for key, value in score_m.items():
         if scores[0] == value:
            del ml[key]
            del utilizzo_m[key]
            del cl[key]

def predici_classe(new_model,ml,m,old_data,risultati,new_data,utilizzo_m,n_modelli_usati,n_riutilizzo_modello):
    if(new_model):
        y_pred,y_conf=ml[m].predict(old_data,return_confidence=True)
        #finestra_del_concetto.append(y_conf)
        with open(risultati, 'a', newline='\n') as file:
            for i in range(0, len(y_pred)):
                #kswin_lof_model[i_m].add_element(y_conf[i])
                writer = csv.writer(file)
                writer.writerow([y_pred[i],y_conf[i],m])
                #predizioni.append(y_pred[i])
        n_modelli_usati+=1
    else:
        y_pred,y_conf=ml[m].predict(new_data,return_confidence=True)
        #finestra_del_concetto.append(y_conf)
        with open(risultati, 'a', newline='\n') as file:
            for i in range(0, len(y_pred)):
                #kswin_lof_model[i_m].add_element(y_conf[i])
                writer = csv.writer(file)
                writer.writerow([y_pred[i],y_conf[i],m])
                #predizioni.append(y_pred[i])
        n_riutilizzo_modello+=1
    utilizzo_m[m]+=1
    return n_modelli_usati,n_riutilizzo_modello

def CD_d(): # ATTENZIONE: finestra fissa(old_concept) e finestra scorrevole(new_concept)! NON PIU FINESTRE ADIACENTI
    for i in range(0, len(cd_d)-1):
        for dato in old_data:
            cd_d[i].add_element(dato[i])
        for dato in new_data:
            cd_d[i].add_element(dato[i])
        if cd_d[i].detected_change()==True: #IN QUESTO CASO UNA SOLA VOLTA
            cd_d_flag[i]=True
            
    feature_sintetica(old_data)
    for i in range(0, len(sintetica)):
        cd_d[-1].add_element(sintetica[i])
    feature_sintetica(new_data)
    for i in range(0, len(sintetica)):
        cd_d[-1].add_element(sintetica[i])
    if cd_d[-1].detected_change()==True:
        cd_d_flag[-1]=True
        
    for i in range(0, len(cd_d)):
        if cd_d_flag[i]==True:
            print(f'Drift zone has been detected on feature {i} in batch {n_batch} with kswin')
            return True
        else:
            print(f'No Drift zone has been detected on feature {i} in batch {n_batch} with kswin')
            return False
def CD_m():
    for i in range(0, len(ml)):
        print(f"Predizione e test modello:{i}")
        y_pred_val,y_conf_val=ml[i].predict(new_data,return_confidence=True)
        for j in range(0, len(cl[i])): #inserisco i dati delle confidence originali (old_data)
            cd_m[i].add_element(cl[i][j])
        for j in range(0, len(y_conf_val)): #inserisco le confidence sulle nuove previsioni (new_data)
            cd_m[i].add_element(y_conf_val[j]) #dovra essere fatto append
        if cd_m[i].detected_change()==True:
            cd_m_flag[i]=True
    for i in range(0, len(ml)):
        if cd_m_flag[i]==False:
            print(f'Il modello {i} è quello adatto al concetto!')
            return i
        else:
            print(f'Nessun modello tra quelli presenti è adatto per il nuovo concetto')
            return -1

def rilevato_nuovo_concetto():
    old_data=new_data #la finestra fissa è cambiata perchè è stato rilevato un nuovo concetto


def start(dn,uf,uv,risultati,max_model,dim_finestra,n_feature):
    old_data=[]
    new_data=[]
    ml=[]
    cl=[]
    n_batch=0
    utilizzo_m=[]
    score_m={}
    m=[]
    n_modelli_usati=0
    n_riutilizzo_modello=0
    dataset_np, verita=carica_dataset(dn,uf,uv)
    data_stream, cd_d, cd_m, cd_d_flag, cd_m_flag=prepara_stream_e_CD(dataset_np,n_feature,dim_finestra,max_model)
    start_time=time.time*1000
    while fine!=True:
        reset_all_flag(cd_d_flag, cd_m_flag, cd_d, cd_m)
        data=sliding_window(data_stream,dim_finestra)
        if(len(data)!=0):
            n_batch+=1
            #da qui in poi segue come scaletta SEZ.3 Proposed Architecture(articolo)
            if n_batch==1: # STEP 1
                old_data=data
                print(f"\nPrimo batch")
                m=aggiungi_modello(max_model,ml,old_data,cl,utilizzo_m,n_batch,score_m)
                n_modelli_usati,n_riutilizzo_modello=predici_classe(True,ml,m,old_data,risultati,new_data,utilizzo_m,n_modelli_usati,n_riutilizzo_modello) #STEP 8
            else: # STEP 2
                print(f"\nBatch numero:{n_batch}")
                if(CD_d()): # STEP 4
                    f=CD_m()
                    if(f==-1): #STEP 6-7
                        rilevato_nuovo_concetto()
                        aggiungi_modello()
                        predici_classe(True) #STEP 8
                    else:
                        m=f #STEP 5
                        predici_classe(False) #STEP 8
                else: #STEP 3
                    predici_classe(False) #STEP 8
        else:
            print("Fine")
            fine=True
    stop_time=time.time()*1000
    time=stop_time-start_time


def main():
    if len(sys.argv)<7:
        print("Sono richiesti sei o più parametri: Nome del dataset da leggere, Nome del dataset da creare per memorizzare i risultati, numero massimo di modelli, dimensione finestra dati, nomi delle feature da utilizzare, nome della verita")
        print("Esempio: python anomaly_detection_under_concept_v2.py SRdrift.csv SRdrift_risultati_150_v2.csv 5 150 A B C V")
        return
    else:
        n_feature=0
        dn=sys.argv[1]
        risultati=sys.argv[2]
        max_model=sys.argv[3]
        dim_finestra=sys.argv[4]
        uf=[]
        for i in range(5,len(sys.argv)-1):
            n_feature+=1
            uf.append(sys.argv[i])
        uv=[]
        uv.append(sys.argv[-1])
        print(dn,risultati,max_model,dim_finestra, uf,uv)
        start(dn,uf,uv,risultati,max_model,dim_finestra,n_feature)
        return

'''def prova():
    score=[1,2,3]
    aumenta(score)
    diminuisci(score)
    print(score)
    a=0
    n=[1,2,3]
    m=[1,1,1]
    i,o=aumenta(n,m)
    print(n,m,i,o)
    for i in range(1,5):
        a+=1
    print(a)
    
def aumenta(score):
    score.append(1)

def diminuisci(score):
    del score[0]'''

if __name__ == "__main__":
    main()
    #prova()
