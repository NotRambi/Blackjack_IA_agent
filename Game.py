import Blackjack
import Tavolo
import random
from threading import Thread

class Game:
    def __init__(self, np, nai, nm, sm, sts, vid, tmp):

        # Variabili globali
        self.numDiMazzi = nm # solitamente da 2 a 6 mazzi
        self.mazzo = ['1c','1q','1f','1p','2c','2q','2f','2p','3c','3q','3f','3p','4c','4q','4f','4p','5c','5q','5f','5p','6c','6q','6f','6p','7c','7q','7f','7p','8c','8q','8f','8p','9c','9q','9f','9p','10c','10q','10f','10p','11c','11q','11f','11p','12c','12q','12f','12p','13c','13q','13f','13p']
        self.Carte = []
        self.CarteUscite = []
        self.Taglia = 0
        self.Giocatori = []
        self.Agenti = []
        self.Dealer = Blackjack.dealer()

        self.contMani = 0

        # Parametri di gioco
        self.numGiocatori = np # giocatori umani
        self.numAgenti = nai # agenti ia
        self.soldiIniziali = sm # soldi iniziali per giocatori e agenti
        self.saveStats = sts # salvataggio statistiche
        self.video = vid # interfaccia grafica

        # cartella temporanea condivisa
        self.tmp = tmp 

    ## METODI DI GIOCO ##

    ## Funzioni del mazzo ##

    # creazione mazzo mischiato e taglia per rimescolamento
    def creaMazzo(self):
        self.Carte = self.mazzo * self.numDiMazzi # carte totali con valore e seme
        self.CarteUscite = [] # carte uscite
        random.shuffle(self.Carte) # mischia le carte
        random.shuffle(self.Carte)
        random.shuffle(self.Carte)
        lunghezzaMazzo = len(self.Carte)
        metaMazzo = lunghezzaMazzo/2
        self.Taglia = random.randint(int(metaMazzo-0.1*lunghezzaMazzo),int(metaMazzo+0.1*lunghezzaMazzo)) # taglia all'incirca a metà del mazzo +- 10%

    # pesca una carta dal mazzo mischiato
    def PescaCarta(self):
        carta = self.Carte.pop(0)
        self.CarteUscite.append(carta)
        return carta
    
    ## Funzioni per la partita ##

    # Puntata iniziale
    def PuntataIniziale(self):
        for i in range(0, len(self.Giocatori)):
            self.Giocatori[i].bet = 0
            while True:
                try:
                    self.Giocatori[i].bet = int(input(self.Giocatori[i].nome+', inserisci la tua puntata: ')) 
                    if self.Giocatori[i].bet < 0:
                        print('Inserisci una puntata non minore di 0')
                        continue
                    if self.Giocatori[i].bet > self.Giocatori[i].soldi:
                        print('Non hai abbastanza soldi per questa puntata')
                        continue
                    else:
                        self.Giocatori[i].soldi -= self.Giocatori[i].bet
                        break
                except:
                    print('Inserisci un numero intero')
                    continue
        for j in range(0, len(self.Agenti)):
            self.Agenti[j].bet = 0
            while True:
                try:
                    self.Agenti[j].bet = self.Agenti[j].chooseBet()
                    if self.Agenti[j].bet > self.Agenti[j].soldi:
                        print(self.Agenti[j].nome+' ha scommesso tutti i soldi')
                        self.Agenti[j].bet = self.Agenti[j].soldi
                        break
                    else:
                        self.Agenti[j].soldi -= self.Agenti[j].bet
                        break
                except:
                    continue

    # Controllo Vincite (controlla singole coppie giocatore-dealer e assegna soldi)
    def Vincite(self):
        if self.Dealer.blackjack:
            for i in range(0, len(self.Giocatori)):
                if self.Giocatori[i].bet == 0:
                    continue
                if i < self.numGiocatori: # se è un giocatore originale
                    if self.Giocatori[i].blackjack:
                        self.Giocatori[i].soldi += self.Giocatori[i].bet # se sia dealer che giocatore hanno un blackjack, il giocatore va in pari
                        print(self.Giocatori[i].nome+', pareggio BJ')
                        continue
                    elif self.Giocatori[i].assicurazione:
                        self.Giocatori[i].soldi += 1.5*self.Giocatori[i].bet # se il dealer ha un blackjack e il giocatore ha assicurato, il giocatore vince l'assicurazione
                        print(self.Giocatori[i].nome+', pareggio Assicurazione')
                        continue
                    print(self.Giocatori[i].nome+', sconfitta') # se il dealer ha un blackjack e il giocatore no, il giocatore perde (i soldi erano gia stati sottratti)
                else: # se è un giocatore clone generato da uno split
                    if self.Giocatori[i].blackjack: 
                        for j in range(0,self.numGiocatori):
                            if self.Giocatori[j].split:
                                if self.Giocatori[i].nome == self.Giocatori[j].nome+'_split':
                                    self.Giocatori[j].soldi += self.Giocatori[i].bet
                                    print(self.Giocatori[i].nome+', pareggio BJ')
                                    break
                        continue
                    elif self.Giocatori[i].assicurazione:
                        for j in range(0,self.numGiocatori):
                            if self.Giocatori[j].split:
                                if self.Giocatori[i].nome == self.Giocatori[j].nome+'_split':
                                    self.Giocatori[j].soldi += 1.5*self.Giocatori[i].bet
                                    print(self.Giocatori[i].nome+', pareggio Assicurazione')
                                    break
                        continue
                    print(self.Giocatori[i].nome+', sconfitta')
            # idem per gli agenti
            for j in range(0,len(self.Agenti)):
                if self.Agenti[j].bet == 0:
                    continue
                if self.Agenti[j].blackjack:
                    self.Agenti[j].soldi += self.Agenti[j].bet
                    print(self.Agenti[j].nome+', pareggio BJ')
                    continue
                elif self.Agenti[j].assicurazione:
                    self.Agenti[j].soldi += 1.5*self.Agenti[j].bet
                    print(self.Agenti[j].nome+', pareggio Assicurazione')
                    continue
                print(self.Agenti[j].nome+', sconfitta')
        else:
            for i in range(0, len(self.Giocatori)):
                if self.Giocatori[i].bet == 0:
                    continue
                if not self.Giocatori[i].sballa:
                    if i < self.numGiocatori: # caso giocatore originale
                        if self.Giocatori[i].blackjack:
                            self.Giocatori[i].soldi += 2.5*self.Giocatori[i].bet # se il giocatore ha un blackjack, vince 2.5 volte la puntata
                            print(self.Giocatori[i].nome+', vittoria BJ')
                            continue
                        elif self.Dealer.sballa:
                            self.Giocatori[i].soldi += 2*self.Giocatori[i].bet 
                            print(self.Giocatori[i].nome+', vittoria Dealer sballato')
                            continue
                        else:
                            if self.Giocatori[i].valoreMano > self.Dealer.valoreMano:
                                self.Giocatori[i].soldi += 2*self.Giocatori[i].bet
                                print(self.Giocatori[i].nome+', vittoria')
                                continue
                            elif self.Giocatori[i].valoreMano == self.Dealer.valoreMano:
                                self.Giocatori[i].soldi += self.Giocatori[i].bet
                                print(self.Giocatori[i].nome+', pareggio')
                                continue
                        print(self.Giocatori[i].nome+', sconfitta')
                    else: # caso giocatore clone generato da uno split
                        if self.Giocatori[i].blackjack:
                            for j in range(0,self.numGiocatori):
                                if self.Giocatori[j].split:
                                    if self.Giocatori[i].nome == self.Giocatori[j].nome+'_split':
                                        self.Giocatori[j].soldi += 2.5*self.Giocatori[i].bet
                                        print(self.Giocatori[i].nome+', vittoria BJ')
                                        break
                            continue
                        elif self.Dealer.sballa:
                            for j in range(0,self.numGiocatori):
                                if self.Giocatori[j].split:
                                    if self.Giocatori[i].nome == self.Giocatori[j].nome+'_split':
                                        self.Giocatori[j].soldi += 2*self.Giocatori[i].bet
                                        print(self.Giocatori[i].nome+', vittoria Dealer sballato')
                                        break
                            continue
                        else:
                            flag = False
                            for j in range(0,self.numGiocatori):
                                if self.Giocatori[j].split:
                                    if self.Giocatori[i].nome == self.Giocatori[j].nome+'_split':
                                        if self.Giocatori[i].valoreMano > self.Dealer.valoreMano:
                                            self.Giocatori[j].soldi += 2*self.Giocatori[i].bet
                                            print(self.Giocatori[i].nome+', vittoria')
                                            flag = True
                                            break
                                        elif self.Giocatori[i].valoreMano == self.Dealer.valoreMano:
                                            self.Giocatori[j].soldi += self.Giocatori[i].bet
                                            print(self.Giocatori[i].nome+', pareggio')
                                            flag = True
                                            break
                            if flag == False:
                                print(self.Giocatori[i].nome+', sconfitta')
                else:
                    print(self.Giocatori[i].nome+', sballato')

            # idem per gli agenti
            for j in range(0,len(self.Agenti)):
                if self.Agenti[j].bet == 0:
                    continue
                if not self.Agenti[j].sballa:
                    if self.Agenti[j].blackjack:
                        self.Agenti[j].soldi += 2.5*self.Agenti[j].bet
                        print(self.Agenti[j].nome+', vittoria BJ')
                        continue
                    elif self.Dealer.sballa:
                        self.Agenti[j].soldi += 2*self.Agenti[j].bet
                        print(self.Agenti[j].nome+', vittoria Dealer sballato')
                        continue
                    else:
                        if self.Agenti[j].valoreMano > self.Dealer.valoreMano:
                            self.Agenti[j].soldi += 2*self.Agenti[j].bet
                            print(self.Agenti[j].nome+', vittoria')
                            continue
                        elif self.Agenti[j].valoreMano == self.Dealer.valoreMano:
                            self.Agenti[j].soldi += self.Agenti[j].bet
                            print(self.Agenti[j].nome+', pareggio')
                            continue
                    print(self.Agenti[j].nome+', sconfitta')
                else:
                    print(self.Agenti[j].nome+', sballato')

    # Controllo Assicurazione
    def Assicurazione(self):
        if self.Dealer.mano[0][0] == '1' and len(self.Dealer.mano[0]) == 2: # si può assicurare solo se la carta scoperta del dealer è un asso
            for i in range(0, self.numGiocatori):
                if self.Giocatori[i].bet > 0:
                    if not self.Giocatori[i].blackjack and not self.Giocatori[i].split and self.Giocatori[i].soldi >= self.Giocatori[i].bet/2: # non deve avere un blackjack anche il giocatore
                        while True:
                            try:
                                assicura = input(self.Giocatori[i].nome+', vuoi assicurare la tua mano? (y/n): ')
                                if assicura == 'y':
                                    self.Giocatori[i].assicura() # sottrae metà della puntata e la mette in assicurazione
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
    def Raddoppio(self):
        for i in range(0, self.numGiocatori): # si può raddoppiare solo se il valore della mano è tra 9 e 11
            if self.Giocatori[i].bet > 0:
                if not self.Giocatori[i].blackjack and not self.Giocatori[i].split and self.Giocatori[i].soldi >= self.Giocatori[i].bet and self.Giocatori[i].valoreMano >= 9 and self.Giocatori[i].valoreMano <= 11:
                    while True:
                        try:
                            raddoppia = input(self.Giocatori[i].nome+', vuoi raddoppiare la tua puntata? (y/n): ')
                            if raddoppia == 'y':
                                self.Giocatori[i].raddoppia() # raddoppia la puntata e poi chiedi una sola carta
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
    def EffettuaSplit(self,Player):
        PlayerSplit = Blackjack.Giocatore(Player.nome+'_split', Player.soldi - Player.bet) # crea un giocatore clone con la stessa puntata
        PlayerSplit.bet = Player.bet                                             # aggiusta tutti i parametri del clone e dell'originale
        Player.soldi -= Player.bet
        PlayerSplit.mano = [Player.mano[1]]
        Player.mano = [Player.mano[0]]
        Player.mano[0] = '1c' if Player.mano[0] == '1C' else '1q' if Player.mano[0] == '1Q' else '1f' if Player.mano[0] == '1F' else '1p' 
        PlayerSplit.valoreMano = Player.valoreMano
        self.Giocatori.append(PlayerSplit)

    def Split(self):
        for i in range(0, self.numGiocatori):
            if self.Giocatori[i].bet > 0:
                if not self.Giocatori[i].blackjack and self.Giocatori[i].soldi >= self.Giocatori[i].bet: # si può splittare solo se il valore delle carte è uguale
                    if (len(self.Giocatori[i].mano[0]) == 2 and len(self.Giocatori[i].mano[1]) == 2 and self.Giocatori[i].mano[0][0] == self.Giocatori[i].mano[1][0]) or (len(self.Giocatori[i].mano[0]) == 3 and len(self.Giocatori[i].mano[1]) == 3 and self.Giocatori[i].mano[0][1] == self.Giocatori[i].mano[1][1]):
                        while True:
                            try:
                                split = input(self.Giocatori[i].nome+', vuoi dividere la tua mano? (y/n): ')
                                if split == 'y':
                                    self.Giocatori[i].split = True
                                    if self.Giocatori[i].mano[1] == '1c' or self.Giocatori[i].mano[1] == '1q 'or self.Giocatori[i].mano[1] == '1f' or self.Giocatori[i].mano[1] == '1p':
                                        self.Giocatori[i].valoreMano = 11 # se ha due assi passi da 12 a 11 dividendoli
                                    else:
                                        self.Giocatori[i].valoreMano = int(self.Giocatori[i].valoreMano/2) # negli altri casi il valore della mano si dimezza
                                    self.EffettuaSplit(self.Giocatori[i])
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

    def DelSplit(self):
        if len(self.Giocatori)>self.numGiocatori:
            for i in range(self.numGiocatori, len(self.Giocatori)): 
                self.Giocatori.pop(i) # elimina i giocatori clone generati dallo split

    # Funzione principale per il gioco

    def StartWindow(self, win):
        win.run()

    # Main
    def RunGame(self):
        # inizializzazione giocatori e agenti
        for i in range(0, self.numGiocatori):
            self.Giocatori.append(Blackjack.Giocatore('Giocatore_'+str(i+1), self.soldiIniziali))

        for i in range(0, self.numAgenti):
            self.Agenti.append(Blackjack.AgenteIA('Agente_'+str(i+1), self.soldiIniziali, self.mazzo, self.numDiMazzi))

        if self.video:
            # inizializzazione Finestra di gioco
            Win = Tavolo.Screen()
            Thread(target=self.StartWindow, args=(Win,)).start()
            tavolo = Win.getTable()
            tavolo.showCards(7, '1c')

        if self.saveStats:
            # inizializzazione statistiche
            self.statsFile = open(self.tmp + "/stats.txt", "w")
            titolo = "Mano|"
            for i in range(0, self.numGiocatori):
                titolo += self.Giocatori[i].nome+'|'
            for j in range(0, self.numAgenti):
                titolo += self.Agenti[j].nome+'|'
            self.statsFile.write(titolo+'\n')
            Mano = [self.contMani, []]
            for i in range(0, self.numGiocatori):
                Mano[1].append(self.Giocatori[i].soldi)
            for j in range(0, self.numAgenti):
                Mano[1].append(self.Agenti[j].soldi)
            self.statsFile.write(str(Mano)+'\n')

        # creazione mazzo 
        self.creaMazzo()

        ## Loop di gioco ##
        while True:
            print("inizio partita")
            self.PuntataIniziale() # fase di puntata iniziale
            flag_AtLeastOnePlayer = False
            for i in range(0, self.numGiocatori):
                if self.Giocatori[i].bet > 0:
                    flag_AtLeastOnePlayer = True
                    self.Giocatori[i].addCard(self.PescaCarta()) # distribuzione delle carte: giocatori, dealer, giocatori, dealer
            for j in range(0, self.numAgenti):
                if self.Agenti[j].bet > 0:
                    flag_AtLeastOnePlayer = True
                    self.Agenti[j].addCard(self.PescaCarta())
            if flag_AtLeastOnePlayer == False:
                print("nessun giocatore ha puntato, Arrivederci")
                if self.saveStats:
                    self.statsFile.close()
                return
            self.Dealer.addCard(self.PescaCarta())
            for i in range(0, self.numGiocatori):
                if self.Giocatori[i].bet > 0:
                    self.Giocatori[i].addCard(self.PescaCarta())
            for j in range(0, self.numAgenti):
                if self.Agenti[j].bet > 0:
                    self.Agenti[j].addCardToDealer(self.Dealer.mano[0])
                    self.Agenti[j].addCard(self.PescaCarta())
            self.Dealer.addCard(self.PescaCarta())
            print('Dealer: '+self.Dealer.mano[0]+', *')
            for i in range(0, self.numGiocatori):
                print(self.Giocatori[i].toStr()+', '+self.Giocatori[i].toStrMano())
            for j in range(0, self.numAgenti):
                print(self.Agenti[j].toStr()+', '+self.Agenti[j].toStrMano())
            
            if self.Dealer.blackjack: # blackjack del dealer
                self.Assicurazione()
                print('Dealer ha un blackjack') # in questo caso il dealer deve scoprire le carte e non permette ulteriori mosse ai giocatori
            else: # nessun blackjack del dealer
                self.Assicurazione()
                self.Split()
                self.Raddoppio()
                print("fine prima fase") # prima fase = possibili mosse precedenti alla distribuzione delle carte non iniziali
                for i in range(0, len(self.Giocatori)):
                    print(self.Giocatori[i].toStr()+', '+self.Giocatori[i].toStrMano())

                for i in range(0, self.numGiocatori): # fase di gioco in cui i giocatori chiedono carte
                    if self.Giocatori[i].bet > 0:
                        while True:
                            try:
                                if self.Giocatori[i].valoreMano == 21: # se il giocatore fa 21 non può chiedere altre carte (21 != bj)
                                    break
                                scelta = input(self.Giocatori[i].nome+', vuoi chiedere una carta? (y/n): ')
                                if scelta == 'y':
                                    self.Giocatori[i].addCard(self.PescaCarta())
                                    print(self.Giocatori[i].toStrMano())
                                    if self.Giocatori[i].sballa:
                                        print('Hai sballato') # idem se sballa (>21)
                                        break 
                                    elif self.Giocatori[i].doppio:
                                        break
                                elif scelta == 'n':
                                    break
                                else:
                                    print('Inserisci y o n')
                                    continue
                            except:
                                print('Inserisci y o n')
                                continue
                    if self.Giocatori[i].split: # finiti i giocatori originali, si passa ai giocatori clonati (ossia gli split)
                        for j in range(self.numGiocatori,len(self.Giocatori)):
                            if self.Giocatori[j].nome == self.Giocatori[i].nome+'_split':
                                while True:
                                    try:
                                        if self.Giocatori[j].valoreMano == 21:
                                            break
                                        scelta = input(self.Giocatori[j].nome+', vuoi chiedere una carta? (y/n): ')
                                        if scelta == 'y':
                                            self.Giocatori[j].addCard(self.PescaCarta())
                                            print(self.Giocatori[j].toStrMano())
                                            if self.Giocatori[j].sballa:
                                                print('Hai sballato')
                                                break
                                            elif self.Giocatori[i].doppio:
                                                break
                                        elif scelta == 'n':
                                            break
                                        else:
                                            print('Inserisci y o n')
                                            continue
                                    except:
                                        print('Inserisci y o n')
                                        continue

                for j in range(0, self.numAgenti):
                    if self.Agenti[j].bet > 0:
                        while True:
                            self.Agenti[j].updateMazzo(self.CarteUscite)
                            if self.Agenti[j].valoreMano == 21:
                                break
                            scelta = self.Agenti[j].ChooseCarta(self.Agenti[j].mano,self.Dealer.mano)
                            #print(Agenti[j].nome+', '+'carta' if scelta == 1 else 'passo')
                            if scelta == 1:
                                self.Agenti[j].addCard(self.PescaCarta())
                                #print(Agenti[j].toStrMano())
                                if self.Agenti[j].sballa:
                                    #print(Agenti[j].nome+', sballato')
                                    break
                                elif self.Agenti[j].doppio:
                                    break
                            else:
                                break

                #print('Dealer: '+Dealer.toStrMano())
                while self.Dealer.valoreMano < 17:
                    self.Dealer.addCard(self.PescaCarta())
                    #print('Dealer: '+Dealer.toStrMano())
                    if self.Dealer.sballa:
                        #print('Dealer sballato')
                        break

            self.Vincite() # finiti i turni si controllano le vincite

            # Reset fine mano
            self.DelSplit() # elimina i giocatori clonati
            for i in range(0, self.numGiocatori):
                self.Giocatori[i].resetMano() # resetta le mani dei giocatori
            for j in range(0, self.numAgenti):
                self.Agenti[j].resetMano() # resetta le mani degli agenti
            self.Dealer.resetMano() # resetta la mano del dealer

            for i in range(0, len(self.Giocatori)):
                print(self.Giocatori[i].toStr()) 
            for j in range(0, len(self.Agenti)):
                print(self.Agenti[j].toStr())

            # aggiunta statistiche
            self.contMani += 1
            if self.saveStats:
                Mano = [self.contMani, []]
                for i in range(0, self.numGiocatori):
                    Mano[1].append(self.Giocatori[i].soldi)
                for j in range(0, self.numAgenti):
                    Mano[1].append(self.Agenti[j].soldi)
                self.statsFile.write(str(Mano)+'\n')
            
            while True: # loop (provvisorio) per continuare a giocare o uscire dalla partita
                continua = True
                try:
                    f = open(self.tmp + "/temp.txt", "r")
                    parametroTemp = f.read()
                    f.close()
                    if parametroTemp == "1":
                        continua = False
                except:
                    print('Arrivederci')
                    if self.saveStats:
                        self.statsFile.close()
                    return
                if continua:
                    break
                print('Arrivederci')
                if self.saveStats:
                    self.statsFile.close()
                return

            if len(self.Carte) < self.Taglia: # controllo raggiungimento della taglia
                print("rimescola il mazzo")
                self.creaMazzo() # se raggiunta, rimescolamento del mazzo
                for j in range(0, self.numAgenti):
                    self.Agenti[j].resetMazzo()





