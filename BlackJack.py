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
                print(Giocatori[i].nome+', sballato')

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
        self.valoreManoDealer = 0

    def resetMazzo(self): # funzione per resettare il mazzo quando viene rimescolato raggiunta la taglia
        self.mazzo = self.mazzo_intero.copy() * numDiMazzi
        self.carteUscite = []
    
    def resetMano(self): # override del reset di giocatore
        self.mano = []
        self.valoreMano = 0
        self.manoDealer = []
        self.valoreManoDealer = 0
        self.bet = 0
        self.blackjack = False
        self.sballa = False
        self.assicurazione = False
        self.split = False
        self.doppio = False

    # da modificare: per il dealer non mi interessa aggiornare la mano ad ogni carta, mi serve solo la carta iniziale per inferire la probabilità durante la fase iniziale
    def addCardToDealer(self, carta): # aggiorna mano e valore del dealer
        self.manoDealer.append(carta)
        self.valoreManoDealer += ValoriCarteUscite[CarteUscite.index(carta)]
        if self.valoreManoDealer > 21:
            for i in range(0, len(self.manoDealer)):
                if self.manoDealer[i] == '1c' or self.manoDealer[i] == '1q' or self.manoDealer[i] == '1f' or self.manoDealer[i] == '1p':
                    self.manoDealer[i] = '1C' if self.manoDealer[i] == '1c' else '1Q' if self.manoDealer[i] == '1q' else '1F' if self.manoDealer[i] == '1f' else '1P'
                    self.valoreManoDealer -= 10
                    break
    
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
numGiocatori = 2 # giocatori umani (da terminale)
numAgenti = 0 # ancora da implementare
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
# da aggiungere agentiIA

while True:
    print("inizio partita")
    PuntataIniziale() # fase di puntata iniziale
    for i in range(0, numGiocatori):
        Giocatori[i].addCard(PescaCarta()) # distribuzione delle carte: giocatori, dealer, giocatori, dealer
    Dealer.addCard(PescaCarta())
    for i in range(0, numGiocatori):
        Giocatori[i].addCard(PescaCarta())
    Dealer.addCard(PescaCarta())
    print('Dealer: '+Dealer.mano[0]+', *')
    for i in range(0, numGiocatori):
        print(Giocatori[i].toStr()+', '+Giocatori[i].toStrMano())
    
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

        print('Dealer: '+Dealer.toStrMano())
        while Dealer.valoreMano < 17:
            Dealer.addCard(PescaCarta())
            print('Dealer: '+Dealer.toStrMano())
            if Dealer.sballa:
                print('Dealer sballato')
                break

    Vincite() # finiti i turni si controllano le vincite

    # Reset fine mano
    DelSplit() # elimina i giocatori clonati
    for i in range(0, numGiocatori):
        Giocatori[i].resetMano() # resetta le mani dei giocatori
    Dealer.resetMano() # resetta la mano del dealer

    for i in range(0, len(Giocatori)):
        print(Giocatori[i].toStr()) 
    
    while True: # loop (provvisorio) per continuare a giocare o uscire dalla partita
        continua = input('Vuoi continuare a giocare? (y/n): ') 
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