import random as r
import time
import csv
s1=45 # seed generazione prima etichetta
r.seed(s1)
stato1= r.getstate()
s2=33 # seed generazione luogo rilevamento
r.seed(s2)
stato2= r.getstate()
s3=56 #seed generazione verità seconda etichetta
r.seed(s3)
stato3= r.getstate()
s4=77 #seed generazione pr. prima etichetta
stato4= r.getstate()
s5= 89 #seed generazione orario
stato5= r.getstate()

prima_etichetta= ['VS', 'VCI', 'VCS', 'VTC']
verità_seconda_etichetta= {0:'Non sospetto', 1: 'Sospetto'}
luogo_rilevamento= ['A', 'B', 'C', 'D', 'E']
cs = [] # verità sulla seconda etichetta 
ts=""# tipo di situazione 
etichetta=""
v_etichetta=""
orario=time.time() #espresso in secondi rispetto all'ingresso precedente
luogo=""

# probabilità verità prima etichetta
pvVS=[1,25]
pvVCI=[26,50]
pvVCS=[51,75]
pvVTC=[76,100]

# probabilità prima etichetta
pVS=[] 
pVCI=[] 
pVCS=[] 
pVTC=[] 

# probabilità luogo
pA=[]
pB=[]
pC=[]
pD=[]
pE=[]

def probabilitàLuoghiSbilanciata():
    global pA, pB, pC, pD, pE
    pA=[1,40] # 40%
    pB=[41,60] # 20%
    pC=[61,80] # 20%
    pD=[81,95] # 15%
    pE=[96,100] # 5%

def probabilitàLuoghiUniforme():
    global pA, pB, pC, pD, pE
    pA=[1,20] # 20%
    pB=[21,40] # 20%
    pC=[41,60] # 20%
    pD=[61,80] # 20%
    pE=[81,100] # 20%

def situazioneNormale():
    global pVS, pVCI, pVCS, pVTC, cs,ts
    cs=[0,1,0,1]
    pVS=[1,7000] # 70%
    pVCI=[9000,9901] # 9%
    pVCS=[7001,9000] # 20%
    pVTC=[9901,10000] # 1%
    return "Situazione Normale"

def obbligoMascherina(): #entrata in vigore obbligo mascherina
    global pVS, pVCI, pVCS, pVTC, cs
    cs=[1,0,1,1]
    pVS=[1,1000] # 10%
    pVCI=[1001,9000] # 80%
    pVCS=[9001,9900] # 9%
    pVTC=[9901,10000] # 1%
    return "Obbligo mascherina"

def condizioniMeteoAvverse():
    global pVS, pVCI, pVCS, pVTC, cs
    cs=[1,0,0,0]
    pVS=[1,500] # 5%
    pVCI=[501,2500] # 20%
    pVCS=[2501,6000] # 35%
    pVTC=[6001,10000] # 40%
    return "Condizioni meteo avverse"

def genera_prima_etichetta():
    global stato1, stato3, stato4
    r.setstate(stato1)
    n1=r.randrange(1,10000)
    stato1=r.getstate()

    r.setstate(stato4)
    p=r.randrange(50,99,1)
    stato4=r.getstate()

    r.setstate(stato3)
    n2=r.randrange(1,100,1)
    stato3=r.getstate()
    return n1,p,n2

def genera_luogo():
    global stato2
    r.setstate(stato2)
    l=r.randrange(1,100,1)
    stato2= r.getstate()
    return l

def genera_orario():
    global stato5,orario
    r.setstate(stato5)
    d=r.randrange(1,5,1)
    stato5=r.getstate()
    orario=orario+d
    return orario

probabilitàLuoghiUniforme()
with open('dati.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Id", "Prima etichetta", "Pr. Prima etichetta", "Verità Prima etichetta", "Luogo", "Orario", "Verità Seconda etichetta","Tipo situazione"])
    for i in range(1,600,1):
        if i==1:
            ts=situazioneNormale()
        elif i==201:
            ts=obbligoMascherina()
        elif i==401:
            ts=situazioneNormale()
    
        n,p,n2=genera_prima_etichetta()

        if n>=pVS[0] and n<=pVS[1]:
            etichetta=prima_etichetta[0]

        elif n>=pVCI[0] and n<=pVCI[1]:
            etichetta=prima_etichetta[1]

        elif n>=pVCS[0] and n<=pVCS[1]:
            etichetta=prima_etichetta[2]

        elif n>=pVTC[0] and n<=pVTC[1]:
            etichetta=prima_etichetta[3]
        if p<65:
            if n2>=pvVS[0] and n2<=pvVS[1]:
                v_etichetta=prima_etichetta[0]

            elif n2>=pvVCI[0] and n2<=pvVCI[1]:
                v_etichetta=prima_etichetta[1]

            elif n2>=pvVCS[0] and n2<=pvVCS[1]:
                v_etichetta=prima_etichetta[2]

            elif n2>=pvVTC[0] and n2<=pvVTC[1]:
                v_etichetta=prima_etichetta[3]
        else:
            v_etichetta=etichetta

        l=genera_luogo()
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
        o=genera_orario()
        v_seconda_etichetta=verità_seconda_etichetta[cs[prima_etichetta.index(etichetta)]]
        writer.writerow([i,etichetta,p,v_etichetta,luogo,o,v_seconda_etichetta,ts])
    
