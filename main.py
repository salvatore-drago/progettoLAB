#VARIABILI CONDIVISE
lista_totale=[]
finestra=[]
cs = [0,1,0,1] # in che modo rispetto alla prima etichetta deve essere emessa la seconda, inizialmente vengono considerati sospetti i volti coperti inforiormente e totalmente coperti


#GENERATORE DATI SINTETICI
from random import randrange
import time
import threading
#time.strftime('%H:%M:%S', time.localtime())
#random.randrange(50,99,0.5) #probabilità etichetta

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
    for i in range(1,10801,1): #supponiamo nelle ore di punta tra le 7 e le 10 entri una persona al secondo
        time.sleep(1) 
        print("Genera dato")
        
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
        for elem in range(0, len(finestra)-1, -1):
            if finestra[elem][1]>=65:
                if finestra[elem][0]=='VS':
                    nVS+=1
                    if finestra[elem][2]=='A':
                        cA=1
                        nA_VS=1
                    elif finestra[elem][2]=='B':
                        cB=1
                        nB_VS=1
                    elif finestra[elem][2]=='C':
                        cC=1
                        nC_VS=1
                    elif finestra[elem][2]=='D':
                        cD=1
                        nD_VS=1
                    elif finestra[elem][2]=='E':
                        cE=1
                        nE_VS=1

                elif finestra[elem][0]=='VCI':
                    nVCI+=1
                    if finestra[elem][2]=='A':
                        cA=1
                        nA_VCI=1
                    elif finestra[elem][2]=='B':
                        cB=1
                        nB_VCI=1
                    elif finestra[elem][2]=='C':
                        cC=1
                        nC_VCI=1
                    elif finestra[elem][2]=='D':
                        cD=1
                        nD_VCI=1
                    elif finestra[elem][2]=='E':
                        cE=1
                        nE_VCI=1

                elif finestra[elem][0]=='VCS':
                    nVCS+=1
                    if finestra[elem][2]=='A':
                        cA=1
                        nA_VCS=1
                    elif finestra[elem][2]=='B':
                        cB=1
                        nB_VCS=1
                    elif finestra[elem][2]=='C':
                        cC=1
                        nC_VCS=1
                    elif finestra[elem][2]=='D':
                        cD=1
                        nD_VCS=1
                    elif finestra[elem][2]=='E':
                        cE=1
                        nE_VCS=1

                elif finestra[elem][0]=='VTC':
                    nVTC+=1
                    if finestra[elem][2]=='A':
                        cA=1
                        nA_VTC=1
                    elif finestra[elem][2]=='B':
                        cB=1
                        nB_VTC=1
                    elif finestra[elem][2]=='C':
                        cC=1
                        nC_VTC=1
                    elif finestra[elem][2]=='D':
                        cD=1
                        nD_VTC=1
                    elif finestra[elem][2]=='E':
                        cE=1
                        nE_VTC=1

        nIU=cA+cB+cC+cD+cE

        nL_VS=nA_VS+nB_VS+nC_VS+nD_VS+nE_VS
        sVS= (1-k)*(nVS/nTOT) + k*(nL_VS/nIU)

        nL_VCI=nA_VCI+nB_VCI+nC_VCI+nD_VCI+nE_VCI
        sVCI= (1-k)*(nVCI/nTOT) + k*(nL_VCI/nIU)     
            
        nL_VCS=nA_VCS+nB_VCS+nC_VCS+nD_VCS+nE_VCS
        sVCS= (1-k)*(nVCS/nTOT) + k*(nL_VCS/nIU)

        nL_VTC=nA_VTC+nB_VTC+nC_VTC+nD_VTC+nE_VTC
        sVTV= (1-k)*(nVTC/nTOT) + k*(nL_VTC/nIU)
            
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
    
th = threading.Thread(target=funzioneRilevamento, args=())
th.start()
