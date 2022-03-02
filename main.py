#VARIABILI CONDIVISE
finestra=[]
cs = [0,1,0,1] # in che modo rispetto alla prima etichetta deve essere emessa la seconda, inizialmente vengono considerati sospetti i volti coperti inforiormente e totalmente coperti


#GENERATORE DATI SINTETICI
from random import randrange
import time
import threading
#time.strftime('%H:%M:%S', time.localtime())
#random.randrange(50,99,0.5) #probabilità etichetta
etichetta=[]
luogo=[]


#probabilità assegnazione prima etichetta
#random.randrange(1,10000)
pVS=[1,7000] # 70%
pVCI=[9897,9997] # 1%
pVCS=[7001,9897] # 28,97%
pVTC=[9998,10000] # 0,03%

# probabilità assegnazione luogo_rilevamento
#random.randrange(1,100)
pA=[1,20] # 20%
pB=[21,40] # 20%
pC=[41,60] # 20%
pD=[61,80] # 20%
pE=[81,100] # 20%


prima_etichetta= ['VS', 'VCI', 'VCS', 'VTC']
seconda_etichetta= {0:'Non sospetto', 1: 'Sospetto'}
luogo_rilevamento= ['A', 'B', 'C', 'D', 'E']

def cambioProbabilitàLuoghi():
    global pA, pB, pC, pD, pE
    pA=[1,40] # 40%
    pB=[41,60] # 20%
    pC=[61,80] # 20%
    pD=[81,95] # 15%
    pE=[96,100] # 5%


def obbligoMascherina(): #entrata in vigore obbligo mascherina
    global pVS, pVCI, pVCS, pVTC
    pVS=[1,2000] # 20%
    pVCI=[2001,9000] # 70%
    pVCS=[9001,9997] # 9,97%
    pVTC=[9998,10000] # 0,03%

def situazioneNormale():
    global pVS, pVCI, pVCS, pVTC
    pVS=[1,7000] # 70%
    pVCI=[9897,9997] # 1%
    pVCS=[7001,9897] # 28,97%
    pVTC=[9998,10000] # 0,03%

def condizioniMeteoAvverse():
    global pVS, pVCI, pVCS, pVTC
    pVS=[1,500] # 5%
    pVCI=[501,2500] # 20%
    pVCS=[2501,6000] # 35%
    pVTC=[6001,10000] # 40%

def generaDati():
    global finestra,etichetta,luogo
    for i in range(1,10801,1): #supponiamo nelle ore di punta tra le 7 e le 10 entri una persona al secondo
        lista_totale= open("lista_risultati","a")
        time.sleep(1) 
        #print("Genera dato")
        n= randrange(1,10000)
        if n>=pVS[0] and n<=pVS[1]:
            etichetta=prima_etichetta[0]

        elif n>=pVCI[0] and n<=pVCI[1]:
            etichetta=prima_etichetta[1]

        elif n>=pVCS[0] and n<=pVCS[1]:
            etichetta=prima_etichetta[2]

        elif n>=pVTC[0] and n<=pVTC[1]:
            etichetta=prima_etichetta[3]
        
        p= randrange(50,99,1) 
        l= randrange(1,100,1)

        if l>=pA[0] and l<=pA[1]:
            luogo=luogo_rilevamento[0]

        elif l>=pB[0] and l<=pB[1]:
            luogo=luogo_rilevamento[1]

        elif l>=pC[0] and l<=pC[1]:
            luogo=luogo_rilevamento[2]

        elif l>=pD[0] and l<=pD[1]:
            luogo=luogo_rilevamento[3]
        
        elif l>=pE[0] and l<=pE[1]:
            luogo=luogo_rilevamento[4]
        
        orario=time.strftime('%H:%M:%S', time.localtime())
        
        etichetta_rilevamento= seconda_etichetta[cs[prima_etichetta.index(etichetta)]]
        dato=[i,etichetta,p,luogo,orario,etichetta_rilevamento]
        
        if len(finestra)<N:
            finestra.append(dato)
        else:
            finestra=finestra.reverse()
            finestra.pop()
            finestra=finestra.reverse()
            finestra.append(dato)
        lista_totale.write("\n"+str(dato))
    lista_totale.close()
th = threading.Thread(target=generaDati, args=())
th.start()

# FUNZIONE DI RILEVAMENTO 
T= 20 #voglio analizzare i dati ogni 20s
N= 50 #voglio conservare i dati relativi alle ultime 50 persone 
k= 0.6 # k può assumere valori [0;1] e permette di  assegnare piu o meno importanza alla distribuzione delle etichette tra i vari disp/luoghi.
s= 65 # scarta i dati con pr.etichetta inferiore al 65%
d_min= 0.1 #cambia in 'SOSPETTO' se sei inferiore a questa soglia
d_max=0.4 #cambia in 'NON SOSPETTO' se sei superiore a questa soglia
def funzioneRilevamento():
    while True:
        #flag degli ingressi utilizzati
        cA=0 
        cB=0
        cC=0
        cD=0
        cE=0
        ##
        nIU=0 #numero di luoghi da cui proviene almeno un dato

        # contatori del numero di dati con una data etichetta
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
        ##
    
        #numero di luoghi da cui proviene almeno un dato con quell'etichetta
        nL_VS=0 
        nL_VCI=0
        nL_VCS=0
        nL_VTC=0

        # valori di rilevamento per etichetta
        sVS=0
        sVCI=0
        sVCS=0
        sVTC=0

        time.sleep(T)
        nTOT= len(finestra) # conta i dati totali
        for elem in range(0, nTOT-1, 1):
            if finestra[elem][2]>=65:
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
            
            print("Funzione di rilevamento...")
            print(f"\n sVS:{sVS}, sVCI:{sVCI}, sVCS:{sVCS}, sVTC:{sVTC}")

            if sVS<d_min:
                cs[0]=1 #etichetta come 'Sospetto'
            elif sVS>=d_max:
                cs[0]=0 #etichetta come 'Non Sospetto'
    
            if sVCI<d_min:
                cs[1]=1
            elif sVCI>=d_max:
                cs[1]=0

            if sVCS<d_min:
                cs[2]=1
            elif sVCS>=d_max:
                cs[2]=0

            if sVTC<d_min:
                cs[3]=1
            elif sVTC>=d_max:
                cs[3]=0 

            print(f"\n CS:{cs}")

        else:
            print("Nessun dato nella finestra da analizzare")

th = threading.Thread(target=funzioneRilevamento, args=())
th.start()
