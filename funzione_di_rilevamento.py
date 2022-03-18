import numpy as np
import pandas as pd
import csv
risultati="risultati_2.csv"
dati_da_analizzare="dati_2.csv"
# FUNZIONE DI RILEVAMENTO 
T= 20 #voglio analizzare i dati ogni 20s
N= 50 #voglio conservare i dati relativi alle ultime 50 persone 
k= 0.6 # k può assumere valori [0;1] e permette di  assegnare piu o meno importanza alla distribuzione delle etichette tra i vari disp/luoghi.
s_min= 65 # scarta i dati con pr.etichetta inferiore al 65%
d_min= 0.1 #cambia in 'SOSPETTO' se sei inferiore a questa soglia
d_max=0.4 #cambia in 'NON SOSPETTO' se sei superiore a questa soglia
###
cs = [0,1,0,1]
prima_etichetta= ['VS', 'VCI', 'VCS', 'VTC']
seconda_etichetta= {0:'Non sospetto', 1: 'Sospetto'}
finestra=[]
pr_seconda_etichetta_NS=""
pr_seconda_etichetta_S=""
pr_seconda_etichetta=""
incertezza_sistema="" #1 -(P1* max(P_2S, P_2NS))
#valori di rilevamento per etichetta
sVS=(d_max-d_min)/2
sVCI=(d_max-d_min)/2
sVCS=(d_max-d_min)/2
sVTC=(d_max-d_min)/2

def get_parametri_rilevamento():
    return [T,N,k,s_min,d_min,d_max]

def get_dati_da_analizzare():
    return dati_da_analizzare

def get_risultati():
    return risultati

def calcolo_probabilita_NS(min,max,x):
        if x<=min and x>=0:
            m=(0-0.5)/(0-min)
            q=0
            y= m*x+q
            return round(y,2)
        elif x>min and x<max:
            y= 0.50
            return y
        else:
            m=(0.5-1)/(max-1)
            q=(max-0.5)/(max-1)
            y= m*x+q
            return round(y,2)

def calcolo_probabilita_S(min,max,x):
    return 1- calcolo_probabilita_NS(min,max,x)
       
    

dati= pd.read_csv(dati_da_analizzare ,usecols=["Id","Prima etichetta","Pr Prima etichetta","Luogo","Orario","Verita Seconda etichetta","Tipo situazione"])
dati_array= dati.to_numpy()
ultimo_orario= int(dati_array[0][4])
i=0

with open(risultati, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Id","Prima etichetta","Pr Prima etichetta","Luogo","Orario","Verita Seconda etichetta","Tipo situazione","Seconda etichetta", "Pr Seconda etichetta","Incertezza Sistema"])
    while i<len(dati_array):
        se= seconda_etichetta[cs[prima_etichetta.index(dati_array[i][1])]]
        if dati_array[i][1]=="VS":
            pr_seconda_etichetta_NS= calcolo_probabilita_NS(d_min,d_max,sVS)
            pr_seconda_etichetta_S= calcolo_probabilita_S(d_min,d_max,sVS)
        elif dati_array[i][1]=="VCI":
            pr_seconda_etichetta_NS= calcolo_probabilita_NS(d_min,d_max,sVCI)
            pr_seconda_etichetta_S= calcolo_probabilita_S(d_min,d_max,sVCI)
        elif dati_array[i][1]=="VCS":
            pr_seconda_etichetta_NS= calcolo_probabilita_NS(d_min,d_max,sVCS)
            pr_seconda_etichetta_S= calcolo_probabilita_S(d_min,d_max,sVCS)
        elif dati_array[i][1]=="VTC":
            pr_seconda_etichetta_NS= calcolo_probabilita_NS(d_min,d_max,sVTC)
            pr_seconda_etichetta_S= calcolo_probabilita_S(d_min,d_max,sVTC)
        if se=="Non sospetto":
            pr_seconda_etichetta=pr_seconda_etichetta_NS
        else:
            pr_seconda_etichetta=pr_seconda_etichetta_S           
        incertezza_sistema=1-((dati_array[i][2]/100)* max(pr_seconda_etichetta_NS,pr_seconda_etichetta_S))       
        writer.writerow([dati_array[i][0],dati_array[i][1],dati_array[i][2],dati_array[i][3],dati_array[i][4],dati_array[i][5],dati_array[i][6], se , int(pr_seconda_etichetta*100),round(incertezza_sistema,2)])

        if dati_array[i][4]<= ultimo_orario+T:
            if len(finestra)<N:
                finestra.append(dati_array[i])
            else:
                finestra.reverse()
                finestra.pop()
                finestra.reverse()
                finestra.append(dati_array[i])
        else:
            ultimo_orario=dati_array[i][4]
            print("\n",finestra,len(finestra),ultimo_orario)
            nTOT= len(finestra) # conta i dati totali
            #flag degli ingressi utilizzati
            cA=0 
            cB=0
            cC=0
            cD=0
            cE=0
            ##

            nIU=0 #numero di luoghi da cui proviene almeno un dato

            #contatori del numero di dati con una data etichetta
            nVS=0
            nVCI=0
            nVCS=0
            nVTC=0

            #flag dei luoghi da cui proviene almeno un dato con quell'etichetta
            nA_VS=0
            nB_VS=0
            nC_VS=0
            nD_VS=0
            nE_VS=0
            nA_VCI=0
            nB_VCI=0
            nC_VCI=0
            nD_VCI=0
            nE_VCI=0
            nA_VCS=0
            nB_VCS=0
            nC_VCS=0
            nD_VCS=0
            nE_VCS=0
            nA_VTC=0
            nB_VTC=0
            nC_VTC=0
            nD_VTC=0
            nE_VTC=0

            #numero di luoghi da cui proviene almeno un dato con quell'etichetta
            nL_VS=0 
            nL_VCI=0
            nL_VCS=0
            nL_VTC=0

            
            for elem in range(0, nTOT-1, 1):
                if finestra[elem][2]>=s_min:
                    if finestra[elem][1]=='VS':
                        nVS+=1
                        if finestra[elem][3]=='A':
                            cA=1
                            nA_VS=1
                        elif finestra[elem][3]=='B':
                            cB=1
                            nB_VS=1
                        elif finestra[elem][3]=='C':
                            cC=1
                            nC_VS=1
                        elif finestra[elem][3]=='D':
                            cD=1
                            nD_VS=1
                        elif finestra[elem][3]=='E':
                            cE=1
                            nE_VS=1

                    elif finestra[elem][1]=='VCI':
                        nVCI+=1
                        if finestra[elem][3]=='A':
                            cA=1
                            nA_VCI=1
                        elif finestra[elem][3]=='B':
                            cB=1
                            nB_VCI=1
                        elif finestra[elem][3]=='C':
                            cC=1
                            nC_VCI=1
                        elif finestra[elem][3]=='D':
                            cD=1
                            nD_VCI=1
                        elif finestra[elem][3]=='E':
                            cE=1
                            nE_VCI=1

                    elif finestra[elem][1]=='VCS':
                        nVCS+=1
                        if finestra[elem][3]=='A':
                            cA=1
                            nA_VCS=1
                        elif finestra[elem][3]=='B':
                            cB=1
                            nB_VCS=1
                        elif finestra[elem][3]=='C':
                            cC=1
                            nC_VCS=1
                        elif finestra[elem][3]=='D':
                            cD=1
                            nD_VCS=1
                        elif finestra[elem][3]=='E':
                            cE=1
                            nE_VCS=1

                    elif finestra[elem][1]=='VTC':
                        nVTC+=1
                        if finestra[elem][3]=='A':
                            cA=1
                            nA_VTC=1
                        elif finestra[elem][3]=='B':
                            cB=1
                            nB_VTC=1
                        elif finestra[elem][3]=='C':
                            cC=1
                            nC_VTC=1
                        elif finestra[elem][3]=='D':
                            cD=1
                            nD_VTC=1
                        elif finestra[elem][3]=='E':
                            cE=1
                            nE_VTC=1

            if(nTOT>0):
                nIU=cA+cB+cC+cD+cE

                nL_VS=nA_VS+nB_VS+nC_VS+nD_VS+nE_VS
                sVS= (1-k)*(nVS/nTOT) + k*(nL_VS/nIU)

                nL_VCI=nA_VCI+nB_VCI+nC_VCI+nD_VCI+nE_VCI
                sVCI= (1-k)*(nVCI/nTOT) + k*(nL_VCI/nIU)     
                
                nL_VCS=nA_VCS+nB_VCS+nC_VCS+nD_VCS+nE_VCS
                sVCS= (1-k)*(nVCS/nTOT) + k*(nL_VCS/nIU)

                nL_VTC=nA_VTC+nB_VTC+nC_VTC+nD_VTC+nE_VTC
                sVTC= (1-k)*(nVTC/nTOT) + k*(nL_VTC/nIU)
                
                print("\n Funzione di rilevamento...")
                print(f"\n Elementi finestra:{nTOT}")
                print(f"\n nVS: {nVS}, nVCI: {nVCI}, nVCS: {nVCS}, nVTC: {nVTC}")
                print(f"\n nL_VS: {nL_VS}, nL_VCI: {nL_VCI}, nL_VCS: {nL_VCS}, nL_VTC: {nL_VTC}")
                print(f"\n sVS:{sVS}, sVCI:{sVCI}, sVCS:{sVCS}, sVTC:{sVTC}")

                if sVS<=d_min:
                    cs[0]=1 #etichetta come 'Sospetto'
                elif sVS>=d_max:
                    cs[0]=0 #etichetta come 'Non Sospetto'
        
                if sVCI<=d_min:
                    cs[1]=1
                elif sVCI>=d_max:
                    cs[1]=0

                if sVCS<=d_min:
                    cs[2]=1
                elif sVCS>=d_max:
                    cs[2]=0

                if sVTC<=d_min:
                    cs[3]=1
                elif sVTC>=d_max:
                    cs[3]=0 

                print(f"\n CS:{cs}")
                report= open("r_rilevamento","a")
                report.write(f"REPORT_ORA:{ultimo_orario}\n Elementi finestra:{nTOT}\n [nVS: {nVS}, nVCI: {nVCI}, nVCS: {nVCS}, nVTC: {nVTC}]\n [nL_VS: {nL_VS}, nL_VCI: {nL_VCI}, nL_VCS: {nL_VCS}, nL_VTC: {nL_VTC}] \n [sVS:{sVS}, sVCI:{sVCI}, sVCS:{sVCS}, sVTC:{sVTC}]\n CS:{cs}\n\n\n")
                report.close()
            else:
                print("Nessun dato nella finestra da analizzare")
        i=i+1
     
    


        


    

