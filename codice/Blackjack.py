# File contenente le classi per la gestione del gioco del BlackJack

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
    
    def ValoreCarta(self, carta): # funzione per calcolare il valore di una carta
        if len(carta) == 3:
            return 10
        else:
            if carta[0] == '1':
                return 11
            else:
                return int(carta[0])
    
    def addCard(self, carta): # aggiunge una carta alla mano del giocatore e ne calcola il valore
        self.mano.append(carta)
        self.valoreMano += self.ValoreCarta(carta)
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
        self.numDiMazzi = num_mazzi
        self.mazzo = mazzo_intero.copy() * num_mazzi # mazzo_intero e num_mazzi compongono la KB iniziale dell'agente
        self.carteUscite = []                        # tutti gli altri parametri sono osservazioni della partita 
        self.manoDealer = []
        self.BetUnits = 0.01 * self.soldi

    def resetMazzo(self): # funzione per resettare il mazzo quando viene rimescolato raggiunta la taglia
        self.mazzo = self.mazzo_intero.copy() * self.numDiMazzi
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
        prob = dictProbHand[i]  # questa ricorsione ha nel calcolo finale peso "prop"
        for e in dictMazzo:     
            if dictMazzo[e] == 0:   
                continue
            flag = False    # flag asso per il ciclo
            flag2 = flagAsso    # flag asso per la chiamata ricorsiva   
            if len(e) == 3:     # se la carta è un 10 o una figura
                if i+10 <= 21:  # caso in cui non si sballa
                    dictProbHand[i+10] = dictProbHand[i+10] + prob*dictMazzo[e]/lenMazzo    # la probabilità di avere i+10 punti aumenta (dove i era il punteggio della chiamata ricorsiva precedente)
                    i2 = i+10
                elif flagAsso: # caso in cui c'è un asso che può essere considerato 1
                    flag2 = False
                    dictProbHand[i-10+10] = dictProbHand[i-10+10] + prob*dictMazzo[e]/lenMazzo
                    i2 = i-10+10
                else:   # caso in cui si sballa
                    dictProbHand[22] = dictProbHand[22] + prob*dictMazzo[e]/lenMazzo
                    i2 = 22
            elif e[0] == '1':   # se la carta è un asso
                if i+11 <= 21:  # caso in cui l'asso verrà considerato 11
                    dictProbHand[i+11] = dictProbHand[i+11] + prob*dictMazzo[e]/lenMazzo
                    i2 = i+11
                    flag = True
                elif i+1 <= 21: # caso in cui l'asso verrà considerato 1
                    dictProbHand[i+1] = dictProbHand[i+1] + prob*dictMazzo[e]/lenMazzo
                    i2 = i+1
                else:
                    dictProbHand[22] = dictProbHand[22] + prob*dictMazzo[e]/lenMazzo
                    i2 = 22
            else:   # se la carta è da 2 a 9
                if i+int(e[0]) <= 21:   # caso in cui non si sballa
                    dictProbHand[i+int(e[0])] = dictProbHand[i+int(e[0])] + prob*dictMazzo[e]/lenMazzo
                    i2 = i+int(e[0])
                elif flagAsso:  # caso in cui c'è un asso che può essere considerato 1
                    flag2 = False
                    dictProbHand[i-10+int(e[0])] = dictProbHand[i-10+int(e[0])] + prob*dictMazzo[e]/lenMazzo
                    i2 = i-10+int(e[0])
                else:   # caso in cui si sballa
                    dictProbHand[22] = dictProbHand[22] + prob*dictMazzo[e]/lenMazzo
                    i2 = 22
            dictProbHand[i] = dictProbHand[i] - prob*dictMazzo[e]/lenMazzo  # la probabilità di avere i punti diminuisce di quanto sono aumentate le probabilità di avere punteggi maggiori
            newMazzo = dictMazzo.copy()
            newMazzo[e] -= 1
            if flag:
                dictProbHand = self.InferenzaProbabilità(i2,newMazzo,lenMazzo-1,dictProbHand,True)  # chiamata ricorsiva
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

        chooseCarta = probWinCarta + probDrawCarta*0.2
        choosePasso = probWinPasso + probDrawPasso*0.2

        if chooseCarta > choosePasso:
            return 1 # carta
        else:
            return 0 # passo
        
    def chooseBet(self):
        RunningCount = 0
        for carta in self.carteUscite:
            if carta[0] == '1':
                RunningCount -= 1
            elif carta[0] == '2' or carta[0] == '3' or carta[0] == '4' or carta[0] == '5' or carta[0] == '6':
                RunningCount += 1
        numMazziRimanenti = len(self.mazzo)/52
        TrueCount = int(RunningCount/numMazziRimanenti)
        if TrueCount < 0:
            return 2
        if TrueCount == 0:
            return self.BetUnits
        else:
            return int((TrueCount+1)*self.BetUnits)
    
# definizione di agente naive, sotto-classe di giocatore
class AgenteNaive(Giocatore):
    def __init__(self, nome, soldi):
        super().__init__(nome, soldi)
        self.BetUnits = 0.01 * self.soldi
    
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
    
    def ChooseCarta(self, MyHand,DealerHand): # funzione chiamata per decidere se chiedere carta o passare arbitrariamente

        ValMyHand = self.HandValueCalc(MyHand)
        ValDealerHand = self.HandValueCalc(DealerHand)

        if ValMyHand < 12: # caso in cui si ha un 11 o meno (matematicamente impossibile sballare)
            return 1 # carta
        elif ValMyHand == 12:   # caso in cui si ha un 12
            if ValDealerHand < 4 or ValDealerHand > 6:
                return 1
            else:
                return 0
        elif ValMyHand < 17:    # caso in cui si ha da 13 a 16
            if ValDealerHand < 7:
                return 1
            else:
                return 0  
        else:   # caso in cui si ha un 17 o più
            return 0 # passo

    def chooseBet(self):    # funzione per decidere la puntata
        return self.BetUnits  # puntata fissa del 1% dei soldi iniziali
    
    def addCardToDealer(self, carta):   # funzione per aggiornare la mano del dealer (non considerata per il calcolo nell'agente naive)
        pass

    def updateMazzo(self, uscite):  # funzione per aggiornare il mazzo (non considerata per il calcolo nell'agente naive)
        pass    

    def resetMazzo(self):   # funzione per resettare il mazzo (non considerata per il calcolo nell'agente naive)
        pass
    

# definizione di dealer
class dealer:
    def __init__(self):
        self.mano = []
        self.valoreMano = 0
        self.blackjack = False
        self.sballa = False

    def ValoreCarta(self, carta): # funzione per calcolare il valore di una carta
        if len(carta) == 3:
            return 10
        else:
            if carta[0] == '1':
                return 11
            else:
                return int(carta[0])
    
    def addCard(self, carta): # aggiunge una carta alla mano del dealer e ne calcola il valore
        self.mano.append(carta)
        self.valoreMano += self.ValoreCarta(carta)
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

