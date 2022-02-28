#VARIABILI CONDIVISE
lista_totale=[]
finestra=[]
cs = [0,1,0,1] # in che modo rispetto alla prima etichetta deve essere emessa la seconda, inizialmente vengono considerati sospetti i volti coperti inforiormente e totalmente coperti


#GENERATORE DATI SINTETICI
from random import randrange
import time
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
    while True:
        time.sleep(1)
        

# funzione di rilevamento 