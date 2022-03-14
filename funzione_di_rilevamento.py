import numpy as np
import pandas as pd

# FUNZIONE DI RILEVAMENTO 
T= 20 #voglio analizzare i dati ogni 20s
N= 50 #voglio conservare i dati relativi alle ultime 50 persone 
k= 0.6 # k può assumere valori [0;1] e permette di  assegnare piu o meno importanza alla distribuzione delle etichette tra i vari disp/luoghi.
s= 65 # scarta i dati con pr.etichetta inferiore al 65%
d_min= 0.1 #cambia in 'SOSPETTO' se sei inferiore a questa soglia
d_max=0.4 #cambia in 'NON SOSPETTO' se sei superiore a questa soglia
cs = [0,1,0,1]
seconda_etichetta= {0:'Non sospetto', 1: 'Sospetto'}
finestra=[]

dati= pd.read_csv('dati.csv' ,usecols=["Id","Prima etichetta","Pr. Prima etichetta","Luogo","Orario"])
dati_array= dati.to_numpy()
ultimo_orario= int(dati_array[0][4])
i=0

while i<len(dati_array):
    if dati_array[i][4]<= ultimo_orario+T:
        if len(finestra)<N:
            finestra.append(dati_array[i])
        else:
            finestra.reverse()
            finestra.pop()
            finestra.reverse()
            finestra.append(dati_array[i])
    else:
        i=i-1
        ultimo_orario=dati_array[i][4]
        print("\n",finestra,len(finestra),ultimo_orario)
        #code
    i=i+1
     
    


        


    

