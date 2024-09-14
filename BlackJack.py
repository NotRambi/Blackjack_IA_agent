### LIBRERIE ###
import random


### VARIABILI GLOBALI ###

numDiMazzi = 2 # solitamente da 2 a 6 mazzi
mazzo = ['1c','1q','1f','1p','2c','2q','2f','2p','3c','3q','3f','3p','4c','4q','4f','4p','5c','5q','5f','5p','6c','6q','6f','6p','7c','7q','7f','7p','8c','8q','8f','8p','9c','9q','9f','9p','10c','10q','10f','10p','11c','11q','11f','11p','12c','12q','12f','12p','13c','13q','13f','13p']
Carte = []
CarteUscite = []
ValoriCarte = []
ValoriCarteUscite = []
Taglia = 0

# solo per le simulazioni solo agente
numManiSimulazione = 10000


### FUNZIONI ###

## Funzioni del mazzo ## 

# creazione mazzo mischiato e taglia per rimescolamento
def creaMazzo():
    global Carte, CarteUscite, ValoriCarte, ValoriCarteUscite, Taglia
    Carte = mazzo * numDiMazzi # carte totali con valore e seme
    CarteUscite = [] # carte uscite
    ValoriCarteUscite = [] # valori delle carte uscite
    random.shuffle(Carte) # mischia le carte
    random.shuffle(Carte)
    random.shuffle(Carte)
    lunghezzaMazzo = len(Carte)
    metaMazzo = lunghezzaMazzo/2
    Taglia = random.randint(int(metaMazzo-0.1*lunghezzaMazzo),int(metaMazzo+0.1*lunghezzaMazzo)) # taglia all'incirca a metà del mazzo +- 10%

    ValoriCarte = [] # valori delle carte per i calcoli ## l'asso vale 11 di default ma verrà valutato 1 quando necessario
    for i in range(0, len(Carte)):
        if len(Carte[i]) == 3:
            ValoriCarte.append(10)
        else:
            if Carte[i][0] == '1':
                ValoriCarte.append(11)
            else:
                ValoriCarte.append(int(Carte[i][0]))

# pesca una carta dal mazzo mischiato
def PescaCarta():
    carta = Carte.pop(0)
    CarteUscite.append(carta)
    ValoriCarteUscite.append(ValoriCarte.pop(0))
    return carta


## Funzioni di gioco ##

# Puntata iniziale
def PuntataIniziale():
    for i in range(0, len(Giocatori)):
        Giocatori[i].bet = 0
        while True:
            try:
                Giocatori[i].bet = int(input(Giocatori[i].nome+', inserisci la tua puntata: ')) 
                if Giocatori[i].bet <= 0:
                    print('Inserisci una puntata maggiore di 0')
                    continue
                if Giocatori[i].bet > Giocatori[i].soldi:
                    print('Non hai abbastanza soldi per questa puntata')
                    continue
                else:
                    Giocatori[i].soldi -= Giocatori[i].bet
                    break
            except:
                print('Inserisci un numero intero')
                continue
    for j in range(0, len(Agenti)):
        Agenti[j].bet = 0
        while True:
            try:
                #Agenti[j].bet = int(input(Agenti[j].nome+', inserisci la sua puntata: ')) ## da ancora implementare scelta puntata agente
                Agenti[j].bet = 10
                if Agenti[j].bet <= 0:
                    continue
                if Agenti[j].bet > Agenti[j].soldi:
                    Agenti[j].bet = 0
                    #continue
                    break
                else:
                    Agenti[j].soldi -= Agenti[j].bet
                    break
            except:
                continue

# Controllo Vincite (controlla singole coppie giocatore-dealer e assegna soldi)
def Vincite():
    if Dealer.blackjack:
        for i in range(0, len(Giocatori)):
            if i < numGiocatori: # se è un giocatore originale
                if Giocatori[i].blackjack:
                    Giocatori[i].soldi += Giocatori[i].bet # se sia dealer che giocatore hanno un blackjack, il giocatore va in pari
                    print(Giocatori[i].nome+', pareggio BJ')
                    continue
                elif Giocatori[i].assicurazione:
                    Giocatori[i].soldi += 1.5*Giocatori[i].bet # se il dealer ha un blackjack e il giocatore ha assicurato, il giocatore vince l'assicurazione
                    print(Giocatori[i].nome+', pareggio Assicurazione')
                    continue
                print(Giocatori[i].nome+', sconfitta') # se il dealer ha un blackjack e il giocatore no, il giocatore perde (i soldi erano gia stati sottratti)
            else: # se è un giocatore clone generato da uno split
                if Giocatori[i].blackjack: 
                    for j in range(0,numGiocatori):
                        if Giocatori[j].split:
                            if Giocatori[i].nome == Giocatori[j].nome+'_split':
                                Giocatori[j].soldi += Giocatori[i].bet
                                print(Giocatori[i].nome+', pareggio BJ')
                                break
                    continue
                elif Giocatori[i].assicurazione:
                    for j in range(0,numGiocatori):
                        if Giocatori[j].split:
                            if Giocatori[i].nome == Giocatori[j].nome+'_split':
                                Giocatori[j].soldi += 1.5*Giocatori[i].bet
                                print(Giocatori[i].nome+', pareggio Assicurazione')
                                break
                    continue
                print(Giocatori[i].nome+', sconfitta')
        # idem per gli agenti
        for j in range(0,len(Agenti)):
            if Agenti[j].blackjack:
                Agenti[j].soldi += Agenti[j].bet
                print(Agenti[j].nome+', pareggio BJ')
                continue
            elif Agenti[j].assicurazione:
                Agenti[j].soldi += 1.5*Agenti[j].bet
                print(Agenti[j].nome+', pareggio Assicurazione')
                continue
            print(Agenti[j].nome+', sconfitta')
    else:
        for i in range(0, len(Giocatori)):
            if not Giocatori[i].sballa:
                if i < numGiocatori: # caso giocatore originale
                    if Giocatori[i].blackjack:
                        Giocatori[i].soldi += 2.5*Giocatori[i].bet # se il giocatore ha un blackjack, vince 2.5 volte la puntata
                        print(Giocatori[i].nome+', vittoria BJ')
                        continue
                    elif Dealer.sballa:
                        Giocatori[i].soldi += 2*Giocatori[i].bet 
                        print(Giocatori[i].nome+', vittoria Dealer sballato')
                        continue
                    else:
                        if Giocatori[i].valoreMano > Dealer.valoreMano:
                            Giocatori[i].soldi += 2*Giocatori[i].bet
                            print(Giocatori[i].nome+', vittoria')
                            continue
                        elif Giocatori[i].valoreMano == Dealer.valoreMano:
                            Giocatori[i].soldi += Giocatori[i].bet
                            print(Giocatori[i].nome+', pareggio')
                            continue
                    print(Giocatori[i].nome+', sconfitta')
                else: # caso giocatore clone generato da uno split
                    if Giocatori[i].blackjack:
                        for j in range(0,numGiocatori):
                            if Giocatori[j].split:
                                if Giocatori[i].nome == Giocatori[j].nome+'_split':
                                    Giocatori[j].soldi += 2.5*Giocatori[i].bet
                                    print(Giocatori[i].nome+', vittoria BJ')
                                    break
                        continue
                    elif Dealer.sballa:
                        for j in range(0,numGiocatori):
                            if Giocatori[j].split:
                                if Giocatori[i].nome == Giocatori[j].nome+'_split':
                                    Giocatori[j].soldi += 2*Giocatori[i].bet
                                    print(Giocatori[i].nome+', vittoria Dealer sballato')
                                    break
                        continue
                    else:
                        flag = False
                        for j in range(0,numGiocatori):
                            if Giocatori[j].split:
                                if Giocatori[i].nome == Giocatori[j].nome+'_split':
                                    if Giocatori[i].valoreMano > Dealer.valoreMano:
                                        Giocatori[j].soldi += 2*Giocatori[i].bet
                                        print(Giocatori[i].nome+', vittoria')
                                        flag = True
                                        break
                                    elif Giocatori[i].valoreMano == Dealer.valoreMano:
                                        Giocatori[j].soldi += Giocatori[i].bet
                                        print(Giocatori[i].nome+', pareggio')
                                        flag = True
                                        break
                        if flag == False:
                            print(Giocatori[i].nome+', sconfitta')
            else:
                if i < numGiocatori:
                    if Dealer.sballa:
                        Giocatori[i].soldi += Giocatori[i].bet
                        print(Giocatori[i].nome+', pareggio Dealer sballato')
                        continue
                    else:
                        print(Giocatori[i].nome+', sballato')
                        continue
                else: # caso giocatore clone generato da uno split
                    if Dealer.sballa:
                        for j in range(0,numGiocatori):
                            if Giocatori[j].split:
                                if Giocatori[i].nome == Giocatori[j].nome+'_split':
                                    Giocatori[j].soldi += Giocatori[i].bet
                                    print(Giocatori[i].nome+', pareggio Dealer sballato')
                                    break
                        continue
                    else:
                        print(Giocatori[i].nome+', sballato')
        # idem per gli agenti
        for j in range(0,len(Agenti)):
            if not Agenti[j].sballa:
                if Agenti[j].blackjack:
                    Agenti[j].soldi += 2.5*Agenti[j].bet
                    print(Agenti[j].nome+', vittoria BJ')
                    continue
                elif Dealer.sballa:
                    Agenti[j].soldi += 2*Agenti[j].bet
                    print(Agenti[j].nome+', vittoria Dealer sballato')
                    continue
                else:
                    if Agenti[j].valoreMano > Dealer.valoreMano:
                        Agenti[j].soldi += 2*Agenti[j].bet
                        print(Agenti[j].nome+', vittoria')
                        continue
                    elif Agenti[j].valoreMano == Dealer.valoreMano:
                        Agenti[j].soldi += Agenti[j].bet
                        print(Agenti[j].nome+', pareggio')
                        continue
                print(Agenti[j].nome+', sconfitta')
            else:
                if Dealer.sballa:
                    Agenti[j].soldi += Agenti[j].bet
                    print(Agenti[j].nome+', pareggio Dealer sballato')
                    continue
                else:
                    print(Agenti[j].nome+', sballato')

# Controllo Assicurazione
def Assicurazione():
    if Dealer.mano[1][0] == '1' and len(Dealer.mano[1]) == 2: # si può assicurare solo se la carta scoperta del dealer è un asso
        for i in range(0, numGiocatori):
            if not Giocatori[i].blackjack and not Giocatori[i].split and Giocatori[i].soldi >= Giocatori[i].bet/2: # non deve avere un blackjack anche il giocatore
                while True:
                    try:
                        assicura = input(Giocatori[i].nome+', vuoi assicurare la tua mano? (y/n): ')
                        if assicura == 'y':
                            Giocatori[i].assicura() # sottrae metà della puntata e la mette in assicurazione
                            break
                        elif assicura == 'n':
                            break
                        else:
                            print('Inserisci y o n')
                            continue
                    except:
                        print('Inserisci y o n')
                        continue

# Controllo Raddoppio
def Raddoppio():
    for i in range(0, numGiocatori): # si può raddoppiare solo se il valore della mano è tra 9 e 11
        if not Giocatori[i].blackjack and not Giocatori[i].split and Giocatori[i].soldi >= Giocatori[i].bet and Giocatori[i].valoreMano >= 9 and Giocatori[i].valoreMano <= 11:
            while True:
                try:
                    raddoppia = input(Giocatori[i].nome+', vuoi raddoppiare la tua puntata? (y/n): ')
                    if raddoppia == 'y':
                        Giocatori[i].raddoppia() # raddoppia la puntata e poi chiedi una sola carta
                        break
                    elif raddoppia == 'n':
                        break
                    else:
                        print('Inserisci y o n')
                        continue
                except:
                    print('Inserisci y o n')
                    continue

# Controllo Split
def EffettuaSplit(Player):
    PlayerSplit = Giocatore(Player.nome+'_split', Player.soldi - Player.bet) # crea un giocatore clone con la stessa puntata
    PlayerSplit.bet = Player.bet                                             # aggiusta tutti i parametri del clone e dell'originale
    Player.soldi -= Player.bet
    PlayerSplit.mano = [Player.mano[1]]
    Player.mano = [Player.mano[0]]
    Player.mano[0] = '1c' if Player.mano[0] == '1C' else '1q' if Player.mano[0] == '1Q' else '1f' if Player.mano[0] == '1F' else '1p' 
    PlayerSplit.valoreMano = Player.valoreMano
    Giocatori.append(PlayerSplit)

def Split():
    for i in range(0, numGiocatori):
        if not Giocatori[i].blackjack and Giocatori[i].soldi >= Giocatori[i].bet: # si può splittare solo se il valore delle carte è uguale
            if (len(Giocatori[i].mano[0]) == 2 and len(Giocatori[i].mano[1]) == 2 and Giocatori[i].mano[0][0] == Giocatori[i].mano[1][0]) or (len(Giocatori[i].mano[0]) == 3 and len(Giocatori[i].mano[1]) == 3 and Giocatori[i].mano[0][1] == Giocatori[i].mano[1][1]):
                while True:
                    try:
                        split = input(Giocatori[i].nome+', vuoi dividere la tua mano? (y/n): ')
                        if split == 'y':
                            Giocatori[i].split = True
                            if Giocatori[i].mano[1] == '1c' or Giocatori[i].mano[1] == '1q 'or Giocatori[i].mano[1] == '1f' or Giocatori[i].mano[1] == '1p':
                                Giocatori[i].valoreMano = 11 # se ha due assi passi da 12 a 11 dividendoli
                            else:
                                Giocatori[i].valoreMano = int(Giocatori[i].valoreMano/2) # negli altri casi il valore della mano si dimezza
                            EffettuaSplit(Giocatori[i])
                            break
                        elif split == 'n':
                            break
                        else:
                            print('Inserisci y o n')
                            continue
                    except Exception as e:
                        print(e)
                        print('Inserisci y o n')
                        continue

def DelSplit():
    if len(Giocatori)>numGiocatori:
        for i in range(numGiocatori, len(Giocatori)): 
            Giocatori.pop(i) # elimina i giocatori clone generati dallo split


### CLASSI ###

# definizione di giocatore
class Giocatore:
    def __init__(self, nome, soldi):
        self.nome = nome
        self.soldi = soldi
        self.mano = [] 
        self.valoreMano = 0
        self.bet = 0
        self.blackjack = False # serie di flag per lo stato del giocatore
        self.sballa = False
        self.assicurazione = False
        self.split = False
        self.doppio = False

    def toStr(self): # funzione per stampare lo stato del giocatore
        return 'nome: '+self.nome+', soldi: '+str(self.soldi)
    
    def addCard(self, carta): # aggiunge una carta alla mano del giocatore e ne calcola il valore
        self.mano.append(carta)
        self.valoreMano += ValoriCarteUscite[CarteUscite.index(carta)]
        if self.valoreMano > 21:
            for i in range(0, len(self.mano)):
                if self.mano[i] == '1c' or self.mano[i] == '1q' or self.mano[i] == '1f' or self.mano[i] == '1p':
                    self.mano[i] = '1C' if self.mano[i] == '1c' else '1Q' if self.mano[i] == '1q' else '1F' if self.mano[i] == '1f' else '1P'
                    self.valoreMano -= 10
                    break
            if self.valoreMano > 21:
                self.sballa = True
        if len(self.mano) == 2 and self.valoreMano == 21:
            self.blackjack = True

    def toStrMano(self): # funzione per stampare la mano del giocatore
        return 'mano: '+str(self.mano)+', valore mano: '+str(self.valoreMano)+ (' B' if self.blackjack else '')+ (' S' if self.sballa else '')
    
    def assicura(self): # funzione per assicurare la mano
        self.assicurazione = True
        self.soldi -= self.bet/2

    def raddoppia(self): # funzione per raddoppiare la puntata
        self.doppio = True
        self.soldi -= self.bet
        self.bet *= 2
    
    def resetMano(self): # funzione di reset a fine mano
        self.mano = []
        self.valoreMano = 0
        self.bet = 0
        self.blackjack = False
        self.sballa = False
        self.assicurazione = False
        self.split = False
        self.doppio = False

# definizione di agente IA, sotto-classe di giocatore
class AgenteIA(Giocatore):
    def __init__(self, nome, soldi, mazzo_intero, num_mazzi):
        super().__init__(nome, soldi) # eredita tutti i parametri di giocatore
        self.mazzo_intero = mazzo_intero
        self.mazzo = mazzo_intero.copy() * num_mazzi # mazzo_intero e num_mazzi compongono la KB iniziale dell'agente
        self.carteUscite = []                        # tutti gli altri parametri sono osservazioni della partita 
        self.manoDealer = []

    def resetMazzo(self): # funzione per resettare il mazzo quando viene rimescolato raggiunta la taglia
        self.mazzo = self.mazzo_intero.copy() * numDiMazzi
        self.carteUscite = []

    def updateMazzo(self, uscite):
        self.resetMazzo()
        self.carteUscite = uscite.copy()
        for carta in uscite:
            self.mazzo.remove(carta)
    
    def resetMano(self): # override del reset di giocatore
        self.mano = []
        self.valoreMano = 0
        self.manoDealer = []
        self.bet = 0
        self.blackjack = False
        self.sballa = False
        self.assicurazione = False
        self.split = False
        self.doppio = False

    def addCardToDealer(self, carta): # aggiorna mano e valore del dealer
        self.manoDealer.append(carta)

    def HandValueCalc(self, hand): # funzione per calcolare il valore di una mano
        Hand = hand.copy()
        Val = 0
        for card in Hand:
            if len(card) == 3:
                Val += 10
            elif card[0] == '1':
                Val += 11
            else:
                Val += int(card[0])
        
        while Val > 21:
            flag = False
            for card in Hand:
                if len(card) == 2 and card[0] == '1':
                    Val -= 10
                    Hand.remove(card)
                    flag = True
            if not flag:
                break
        return Val
    
    def InferenzaProbabilità(self,i,dictMazzo,lenMazzo,dictProbHand,flagAsso): # funzione ricorsiva per calcolare la distribuzione di probabilità del dealer
        if i >= 17: # caso base
            return dictProbHand
        prob = dictProbHand[i]
        for e in dictMazzo:
            if dictMazzo[e] == 0:
                continue
            flag = False
            flag2 = flagAsso
            if len(e) == 3:
                if i+10 <= 21:
                    dictProbHand[i+10] = dictProbHand[i+10] + prob*dictMazzo[e]/lenMazzo
                    i2 = i+10
                elif flagAsso:
                    flag2 = False
                    dictProbHand[i-10+10] = dictProbHand[i-10+10] + prob*dictMazzo[e]/lenMazzo
                    i2 = i-10+10
                else:
                    dictProbHand[22] = dictProbHand[22] + prob*dictMazzo[e]/lenMazzo
                    i2 = 22
            elif e[0] == '1':
                if i+11 <= 21:
                    dictProbHand[i+11] = dictProbHand[i+11] + prob*dictMazzo[e]/lenMazzo
                    i2 = i+11
                    flag = True
                elif i+1 <= 21:
                    dictProbHand[i+1] = dictProbHand[i+1] + prob*dictMazzo[e]/lenMazzo
                    i2 = i+1
                else:
                    dictProbHand[22] = dictProbHand[22] + prob*dictMazzo[e]/lenMazzo
                    i2 = 22
            else:
                if i+int(e[0]) <= 21:
                    dictProbHand[i+int(e[0])] = dictProbHand[i+int(e[0])] + prob*dictMazzo[e]/lenMazzo
                    i2 = i+int(e[0])
                elif flagAsso:
                    flag2 = False
                    dictProbHand[i-10+int(e[0])] = dictProbHand[i-10+int(e[0])] + prob*dictMazzo[e]/lenMazzo
                    i2 = i-10+int(e[0])
                else:
                    dictProbHand[22] = dictProbHand[22] + prob*dictMazzo[e]/lenMazzo
                    i2 = 22
            dictProbHand[i] = dictProbHand[i] - prob*dictMazzo[e]/lenMazzo
            newMazzo = dictMazzo.copy()
            newMazzo[e] -= 1
            if flag:
                dictProbHand = self.InferenzaProbabilità(i2,newMazzo,lenMazzo-1,dictProbHand,True)
            else:
                dictProbHand = self.InferenzaProbabilità(i2,newMazzo,lenMazzo-1,dictProbHand,flag2)
        return dictProbHand
    
    def ChooseCarta(self, MyHand,DealerHand): # funzione chiamata per decidere se chiedere carta o passare

        # casi base
        if self.HandValueCalc(MyHand) > 20: # caso in cui si ha già un 21
            return 0 # passo
        elif self.HandValueCalc(MyHand) < 12: # caso in cui si ha un 11 o meno (matematicamente impossibile sballare)
            return 1 # carta
        
        # creo dizionario con le carte del mazzo
        dictMazzo = {'1s':0, '2s':0, '3s':0, '4s':0, '5s':0, '6s':0, '7s':0, '8s':0, '9s':0, '10s':0} # rappresendo il mazzo come la quantità di carte presenti per valore
        for carta in self.mazzo:
            if len(carta) == 3: # è un 10 o una figura
                dictMazzo['10s'] += 1
            elif carta[0] == '1': # è un asso
                dictMazzo['1s'] += 1
            else: # è una carta da 2 a 9
                dictMazzo[carta[0]+'s'] += 1

        lenMazzo = len(self.mazzo)

        # distribuzione di probabilità della mano del giocatore e del dealer
        dictValMyHand = {2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0,13:0,14:0,15:0,16:0,17:0,18:0,19:0,20:0,21:0,22:0} # 22 è il caso in cui si sballa
        dictValDealerHand = {2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0,13:0,14:0,15:0,16:0,17:0,18:0,19:0,20:0,21:0,22:0}
        dictValMyHand[self.HandValueCalc(MyHand)] = 1
        dictValDealerHand[self.HandValueCalc(DealerHand)] = 1
        
        # caso in cui il dealer ha un asso
        if self.HandValueCalc(DealerHand) == 11:
            dictValDealerHand = self.InferenzaProbabilità(self.HandValueCalc(DealerHand),dictMazzo,lenMazzo,dictValDealerHand,True)
        else:
            dictValDealerHand = self.InferenzaProbabilità(self.HandValueCalc(DealerHand),dictMazzo,lenMazzo,dictValDealerHand,False)


        # confronto tra dealer e mano personale se passo
        probWinPasso = 0
        probDrawPasso = 0
        probLosePasso = 0
        for m in dictValMyHand:
            for d in dictValDealerHand:
                if m == 22:
                    if d == 22:
                        probDrawPasso += dictValMyHand[m]*dictValDealerHand[d]
                    else:
                        probLosePasso += dictValMyHand[m]*dictValDealerHand[d]
                elif d == 22:
                    probWinPasso += dictValMyHand[m]*dictValDealerHand[d]
                else:
                    if m > d:
                        probWinPasso += dictValMyHand[m]*dictValDealerHand[d]
                    elif m == d:
                        probDrawPasso += dictValMyHand[m]*dictValDealerHand[d]
                    else:
                        probLosePasso += dictValMyHand[m]*dictValDealerHand[d]

        # caso in cui si chiede carta
        probWinCarta = 0
        probDrawCarta = 0
        probLoseCarta = 0

        for carta in self.mazzo:
            newmazzo = self.mazzo.copy()
            newmazzo.remove(carta)
            myNewHand = MyHand.copy()
            myNewHand.append(carta)
            dictValMyHand2 = {2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0,13:0,14:0,15:0,16:0,17:0,18:0,19:0,20:0,21:0,22:0}
            if self.HandValueCalc(myNewHand) <= 21:
                dictValMyHand2[self.HandValueCalc(myNewHand)] = 1
            else:
                dictValMyHand2[22] = 1
            if self.HandValueCalc(DealerHand) == 11:
                dictValDealerHand2 = self.InferenzaProbabilità(self.HandValueCalc(DealerHand),dictMazzo,lenMazzo,dictValDealerHand,True)
            else:
                dictValDealerHand2 = self.InferenzaProbabilità(self.HandValueCalc(DealerHand),dictMazzo,lenMazzo,dictValDealerHand,False)
            for m in dictValMyHand2:
                for d in dictValDealerHand2:
                    if m == 22:
                        if d == 22:
                            probDrawCarta += dictValMyHand2[m]*dictValDealerHand2[d]/lenMazzo
                        else:
                            probLoseCarta += dictValMyHand2[m]*dictValDealerHand2[d]/lenMazzo
                    elif d == 22:
                        probWinCarta += dictValMyHand2[m]*dictValDealerHand2[d]/lenMazzo
                    else:
                        if m > d:
                            probWinCarta += dictValMyHand2[m]*dictValDealerHand2[d]/lenMazzo
                        elif m == d:
                            probDrawCarta += dictValMyHand2[m]*dictValDealerHand2[d]/lenMazzo
                        else:
                            probLoseCarta += dictValMyHand2[m]*dictValDealerHand2[d]/lenMazzo

        chooseCarta = probWinCarta + probDrawCarta*0.2 - probLoseCarta
        choosePasso = probWinPasso + probDrawPasso*0.2 - probLosePasso

        if chooseCarta > choosePasso:
            return 1 # carta
        else:
            return 0 # passo
    
# definizione di dealer
class dealer:
    def __init__(self):
        self.mano = []
        self.valoreMano = 0
        self.blackjack = False
        self.sballa = False
    
    def addCard(self, carta): # aggiunge una carta alla mano del dealer e ne calcola il valore
        self.mano.append(carta)
        self.valoreMano += ValoriCarteUscite[CarteUscite.index(carta)]
        if self.valoreMano > 21:
            for i in range(0, len(self.mano)):
                if self.mano[i] == '1c' or self.mano[i] == '1q' or self.mano[i] == '1f' or self.mano[i] == '1p':
                    self.mano[i] = '1C' if self.mano[i] == '1c' else '1Q' if self.mano[i] == '1q' else '1F' if self.mano[i] == '1f' else '1P'
                    self.valoreMano -= 10
                    break
            if self.valoreMano > 21:
                self.sballa = True
        if len(self.mano) == 2 and self.valoreMano == 21: # condizione per il blackjack
            self.blackjack = True

    def toStrMano(self):
        return 'mano: '+str(self.mano)+', valore mano: '+str(self.valoreMano)+ (' B' if self.blackjack else '')+ (' S' if self.sballa else '')
    
    def resetMano(self):
        self.mano = []
        self.valoreMano = 0
        self.blackjack = False
        self.sballa = False
    

### MAIN ###

## Inizializzazioni ##

# inizializzazione dealer
Dealer = dealer()

# inizializzazione giocatori e agenti (da 1 a 3 tra agenti e giocatori)
numGiocatori = 0 # giocatori umani (da terminale)
numAgenti = 3 # ancora da implementare
Giocatori = []
Agenti = []
soldiIniziali = 1000 # soldi iniziali per giocatori e agenti

for i in range(0, numGiocatori):
    Giocatori.append(Giocatore('Giocatore_'+str(i+1), soldiIniziali))

for i in range(0, numAgenti):
    Agenti.append(AgenteIA('Agente_'+str(i+1), soldiIniziali, mazzo, numDiMazzi))

# creazione mazzo 
creaMazzo()

## Loop di gioco ##
# da finire di aggiungere agentiIA: assicurazione, split, raddoppio.

while True:
    print("inizio partita")
    PuntataIniziale() # fase di puntata iniziale
    for i in range(0, numGiocatori):
        Giocatori[i].addCard(PescaCarta()) # distribuzione delle carte: giocatori, dealer, giocatori, dealer
    for j in range(0, numAgenti):
        Agenti[j].addCard(PescaCarta())
    Dealer.addCard(PescaCarta())
    for i in range(0, numGiocatori):
        Giocatori[i].addCard(PescaCarta())
    for j in range(0, numAgenti):
        Agenti[j].addCardToDealer(Dealer.mano[0])
        Agenti[j].addCard(PescaCarta())
    Dealer.addCard(PescaCarta())
    print('Dealer: '+Dealer.mano[0]+', *')
    for i in range(0, numGiocatori):
        print(Giocatori[i].toStr()+', '+Giocatori[i].toStrMano())
    for j in range(0, numAgenti):
        print(Agenti[j].toStr()+', '+Agenti[j].toStrMano())
    
    if Dealer.blackjack: # blackjack del dealer
        Assicurazione()
        print('Dealer ha un blackjack') # in questo caso il dealer deve scoprire le carte e non permette ulteriori mosse ai giocatori
    else: # nessun blackjack del dealer
        Assicurazione()
        Split()
        Raddoppio()
        print("fine prima fase") # prima fase = possibili mosse precedenti alla distribuzione delle carte non iniziali
        for i in range(0, len(Giocatori)):
            print(Giocatori[i].toStr()+', '+Giocatori[i].toStrMano())

        for i in range(0, numGiocatori): # fase di gioco in cui i giocatori chiedono carte
            while True:
                try:
                    if Giocatori[i].valoreMano == 21: # se il giocatore fa 21 non può chiedere altre carte (21 != bj)
                        break
                    scelta = input(Giocatori[i].nome+', vuoi chiedere una carta? (y/n): ')
                    if scelta == 'y':
                        Giocatori[i].addCard(PescaCarta())
                        print(Giocatori[i].toStrMano())
                        if Giocatori[i].sballa:
                            print('Hai sballato') # idem se sballa (>21)
                            break 
                        elif Giocatori[i].doppio:
                            break
                    elif scelta == 'n':
                        break
                    else:
                        print('Inserisci y o n')
                        continue
                except:
                    print('Inserisci y o n')
                    continue
            if Giocatori[i].split: # finiti i giocatori originali, si passa ai giocatori clonati (ossia gli split)
                for j in range(numGiocatori,len(Giocatori)):
                    if Giocatori[j].nome == Giocatori[i].nome+'_split':
                        while True:
                            try:
                                if Giocatori[j].valoreMano == 21:
                                    break
                                scelta = input(Giocatori[j].nome+', vuoi chiedere una carta? (y/n): ')
                                if scelta == 'y':
                                    Giocatori[j].addCard(PescaCarta())
                                    print(Giocatori[j].toStrMano())
                                    if Giocatori[j].sballa:
                                        print('Hai sballato')
                                        break
                                    elif Giocatori[i].doppio:
                                        break
                                elif scelta == 'n':
                                    break
                                else:
                                    print('Inserisci y o n')
                                    continue
                            except:
                                print('Inserisci y o n')
                                continue

        for j in range(0, numAgenti):
            while True:
                Agenti[j].updateMazzo(CarteUscite)
                if Agenti[j].valoreMano == 21:
                    break
                scelta = Agenti[j].ChooseCarta(Agenti[j].mano,Dealer.mano)
                #print(Agenti[j].nome+', '+'carta' if scelta == 1 else 'passo')
                if scelta == 1:
                    Agenti[j].addCard(PescaCarta())
                    #print(Agenti[j].toStrMano())
                    if Agenti[j].sballa:
                        #print(Agenti[j].nome+', sballato')
                        break
                    elif Agenti[j].doppio:
                        break
                else:
                    break

        #print('Dealer: '+Dealer.toStrMano())
        while Dealer.valoreMano < 17:
            Dealer.addCard(PescaCarta())
            #print('Dealer: '+Dealer.toStrMano())
            if Dealer.sballa:
                #print('Dealer sballato')
                break

    Vincite() # finiti i turni si controllano le vincite

    # Reset fine mano
    DelSplit() # elimina i giocatori clonati
    for i in range(0, numGiocatori):
        Giocatori[i].resetMano() # resetta le mani dei giocatori
    for j in range(0, numAgenti):
        Agenti[j].resetMano()
    Dealer.resetMano() # resetta la mano del dealer

    for i in range(0, len(Giocatori)):
        print(Giocatori[i].toStr()) 
    for j in range(0, len(Agenti)):
        print(Agenti[j].toStr())
    
    while True: # loop (provvisorio) per continuare a giocare o uscire dalla partita
        #continua = input('Vuoi continuare a giocare? (y/n): ') 
        continua = 'y'
        if numManiSimulazione == 0:
            continua = 'n'
        else:
            numManiSimulazione -= 1

        if continua == 'y':
            break
        elif continua == 'n':
            print('Arrivederci')
            exit()
        else:
            print('Inserisci y o n')
            continue

    if len(Carte) < Taglia: # controllo raggiungimento della taglia
        print("rimescola il mazzo")
        creaMazzo() # se raggiunta, rimescolamento del mazzo

# fine partita

## Note: ##
# - da finire la classe AgenteIA
#    - implementare il codice in agente.py nella classe agenteIA come motore di decisione
#    - valutare se implementarlo in un unico file o se importarlo come file esterno
# - effettuare ulteriori debugging per testare se tutte le funzioni di gioco funzionano bene
# - implementare nel loop di gioco tutte le fasi dell'agenteIA
# - decidere come permettere all'agenteIA di osservare le carte sul tavolo
#    - o si implementano come variabili globali
#    - o si passano come parametri ogni volta che c'è un cambiamento nel loop di gioco (ad esempio quando il dealer pesca una carta la si manda sia all'agente che al dealer)