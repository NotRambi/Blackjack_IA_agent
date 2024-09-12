### VARAIBILI GLOBALI ###

mazzo = ['1c','1q','1f','1p','2c','2q','2f','2p','3c','3q','3f','3p','4c','4q','4f','4p','5c','5q','5f','5p','6c','6q','6f','6p','7c','7q','7f','7p','8c','8q','8f','8p','9c','9q','9f','9p','10c','10q','10f','10p','11c','11q','11f','11p','12c','12q','12f','12p','13c','13q','13f','13p']
mazzoIntero = ['1c','1q','1f','1p','2c','2q','2f','2p','3c','3q','3f','3p','4c','4q','4f','4p','5c','5q','5f','5p','6c','6q','6f','6p','7c','7q','7f','7p','8c','8q','8f','8p','9c','9q','9f','9p','10c','10q','10f','10p','11c','11q','11f','11p','12c','12q','12f','12p','13c','13q','13f','13p']
CarteUscite = []

### FUNZIONI ###

# Funzione che calcola il valore di una mano (usata in entrambi gli approcci)
def HandValue(hand):
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

## Approccio 1: funzione Carta() prova a calcolare la probabilità di vincere se pesco una carta o passo
# semplice brute force, testa tutte le combinazioni di carte e verifica in quante si vince/perde/pareggia in rapporto al totale
def Carta(YourHand, DealerHand):

    mazzo = mazzoIntero.copy()
    ValNewHand = HandValue(YourHand)

    mazzo.remove(YourHand[0])
    mazzo.remove(YourHand[1])
    mazzo.remove(DealerHand[0])

    CarteUscite.append(YourHand[0])
    CarteUscite.append(YourHand[1])
    CarteUscite.append(DealerHand[0])

    # calcolo probabilità di vincere se passo
    numWin = 0
    numLose = 0
    numDraw = 0
    cont = 0

    # Dealer con 2 carte
    for carta2 in mazzo:
        NewDealer = DealerHand.copy()
        NewDealer.append(carta2)
        ValNewDealer = HandValue(NewDealer)
        if ValNewDealer < 17:
            continue
        else:
            cont += 1
            if ValNewHand <= 21 and ValNewHand > ValNewDealer:
                numWin += 1
            elif ValNewHand <= 21 and ValNewDealer > 21:
                numWin += 1
            elif ValNewHand == ValNewDealer:
                numDraw += 1
            elif ValNewHand > 21 and ValNewDealer > 21:
                numDraw += 1
            else:
                numLose += 1

            
    # Dealer con 3 carte
    for i2 in range(0,len(mazzo)):
        NewDealer = DealerHand.copy()
        NewDealer.append(mazzo[i2])
        ValNewDealer = HandValue(NewDealer)
        if ValNewDealer >= 17:
            continue
        for i3 in range(0,len(mazzo)):
            NewDealer = DealerHand.copy()
            NewDealer.append(mazzo[i2])
            NewDealer.append(mazzo[i3])
            ValNewDealer = HandValue(NewDealer)
            if ValNewDealer < 17 or i2 == i3:
                continue
            else:
                cont += 1
                if ValNewHand <= 21 and ValNewHand > ValNewDealer:
                    numWin += 1
                elif ValNewHand <= 21 and ValNewDealer > 21:
                    numWin += 1
                elif ValNewHand == ValNewDealer:
                    numDraw += 1
                elif ValNewHand > 21 and ValNewDealer > 21:
                    numDraw += 1
                else:
                    numLose += 1

    # Dealer con 4 carte
    for i2 in range(0,len(mazzo)):
        NewDealer = DealerHand.copy()
        NewDealer.append(mazzo[i2])
        ValNewDealer = HandValue(NewDealer)
        if ValNewDealer >= 17:
            continue
        for i3 in range(0,len(mazzo)):
            NewDealer = DealerHand.copy()
            NewDealer.append(mazzo[i2])
            NewDealer.append(mazzo[i3])
            ValNewDealer = HandValue(NewDealer)
            if ValNewDealer >= 17 or i2 == i3:
                continue
            for i4 in range(0,len(mazzo)):
                NewDealer = DealerHand.copy()
                NewDealer.append(mazzo[i2])
                NewDealer.append(mazzo[i3])
                NewDealer.append(mazzo[i4])
                ValNewDealer = HandValue(NewDealer)
                if ValNewDealer < 17 or i2 == i4 or i3 == i4:
                    continue
                else:
                    cont += 1
                    if ValNewHand <= 21 and ValNewHand > ValNewDealer:
                        numWin += 1
                    elif ValNewHand <= 21 and ValNewDealer > 21:
                        numWin += 1
                    elif ValNewHand == ValNewDealer:
                        numDraw += 1
                    elif ValNewHand > 21 and ValNewDealer > 21:
                        numDraw += 1
                    else:
                        numLose += 1

    # Dealer con 5 carte
    for i2 in range(0,len(mazzo)):
        NewDealer = DealerHand.copy()
        NewDealer.append(mazzo[i2])
        ValNewDealer = HandValue(NewDealer)
        if ValNewDealer >= 17:
            continue
        for i3 in range(0,len(mazzo)):
            NewDealer = DealerHand.copy()
            NewDealer.append(mazzo[i2])
            NewDealer.append(mazzo[i3])
            ValNewDealer = HandValue(NewDealer)
            if ValNewDealer >= 17 or i2 == i3:
                continue
            for i4 in range(0,len(mazzo)):
                NewDealer = DealerHand.copy()
                NewDealer.append(mazzo[i2])
                NewDealer.append(mazzo[i3])
                NewDealer.append(mazzo[i4])
                ValNewDealer = HandValue(NewDealer)
                if ValNewDealer >= 17 or i2 == i4 or i3 == i4:
                    continue
                for i5 in range(0,len(mazzo)):
                    NewDealer = DealerHand.copy()
                    NewDealer.append(mazzo[i2])
                    NewDealer.append(mazzo[i3])
                    NewDealer.append(mazzo[i4])
                    NewDealer.append(mazzo[i5])
                    ValNewDealer = HandValue(NewDealer)
                    if ValNewDealer < 17 or i2 == i5 or i3 == i5 or i4 == i5:
                        continue
                    else:
                        cont += 1
                        if ValNewHand <= 21 and ValNewHand > ValNewDealer:
                            numWin += 1
                        elif ValNewHand <= 21 and ValNewDealer > 21:
                            numWin += 1
                        elif ValNewHand == ValNewDealer:
                            numDraw += 1
                        elif ValNewHand > 21 and ValNewDealer > 21:
                            numDraw += 1
                        else:
                            numLose += 1

    # Dealer con 6 carte
    for i2 in range(0,len(mazzo)):
        NewDealer = DealerHand.copy()
        NewDealer.append(mazzo[i2])
        ValNewDealer = HandValue(NewDealer)
        if ValNewDealer >= 17:
            continue
        for i3 in range(0,len(mazzo)):
            NewDealer = DealerHand.copy()
            NewDealer.append(mazzo[i2])
            NewDealer.append(mazzo[i3])
            ValNewDealer = HandValue(NewDealer)
            if ValNewDealer >= 17 or i2 == i3:
                continue
            for i4 in range(0,len(mazzo)):
                NewDealer = DealerHand.copy()
                NewDealer.append(mazzo[i2])
                NewDealer.append(mazzo[i3])
                NewDealer.append(mazzo[i4])
                ValNewDealer = HandValue(NewDealer)
                if ValNewDealer >= 17 or i2 == i4 or i3 == i4:
                    continue
                for i5 in range(0,len(mazzo)):
                    NewDealer = DealerHand.copy()
                    NewDealer.append(mazzo[i2])
                    NewDealer.append(mazzo[i3])
                    NewDealer.append(mazzo[i4])
                    NewDealer.append(mazzo[i5])
                    ValNewDealer = HandValue(NewDealer)
                    if ValNewDealer >= 17 or i2 == i5 or i3 == i5 or i4 == i5:
                        continue
                    for i6 in range(0,len(mazzo)):
                        NewDealer = DealerHand.copy()
                        NewDealer.append(mazzo[i2])
                        NewDealer.append(mazzo[i3])
                        NewDealer.append(mazzo[i4])
                        NewDealer.append(mazzo[i5])
                        NewDealer.append(mazzo[i6])
                        ValNewDealer = HandValue(NewDealer)
                        if ValNewDealer < 17 or i2 == i6 or i3 == i6 or i4 == i6 or i5 == i6:
                            continue
                        else:
                            cont += 1
                            if ValNewHand <= 21 and ValNewHand > ValNewDealer:
                                numWin += 1
                            elif ValNewHand <= 21 and ValNewDealer > 21:
                                numWin += 1
                            elif ValNewHand == ValNewDealer:
                                numDraw += 1
                            elif ValNewHand > 21 and ValNewDealer > 21:
                                numDraw += 1
                            else:
                                numLose += 1

    # Dealer con 7 carte
    for i2 in range(0,len(mazzo)):
        NewDealer = DealerHand.copy()
        NewDealer.append(mazzo[i2])
        ValNewDealer = HandValue(NewDealer)
        if ValNewDealer >= 17:
            continue
        for i3 in range(0,len(mazzo)):
            NewDealer = DealerHand.copy()
            NewDealer.append(mazzo[i2])
            NewDealer.append(mazzo[i3])
            ValNewDealer = HandValue(NewDealer)
            if ValNewDealer >= 17 or i2 == i3:
                continue
            for i4 in range(0,len(mazzo)):
                NewDealer = DealerHand.copy()
                NewDealer.append(mazzo[i2])
                NewDealer.append(mazzo[i3])
                NewDealer.append(mazzo[i4])
                ValNewDealer = HandValue(NewDealer)
                if ValNewDealer >= 17 or i2 == i4 or i3 == i4:
                    continue
                for i5 in range(0,len(mazzo)):
                    NewDealer = DealerHand.copy()
                    NewDealer.append(mazzo[i2])
                    NewDealer.append(mazzo[i3])
                    NewDealer.append(mazzo[i4])
                    NewDealer.append(mazzo[i5])
                    ValNewDealer = HandValue(NewDealer)
                    if ValNewDealer >= 17 or i2 == i5 or i3 == i5 or i4 == i5:
                        continue
                    for i6 in range(0,len(mazzo)):
                        NewDealer = DealerHand.copy()
                        NewDealer.append(mazzo[i2])
                        NewDealer.append(mazzo[i3])
                        NewDealer.append(mazzo[i4])
                        NewDealer.append(mazzo[i5])
                        NewDealer.append(mazzo[i6])
                        ValNewDealer = HandValue(NewDealer)
                        if ValNewDealer >= 17 or i2 == i6 or i3 == i6 or i4 == i6 or i5 == i6:
                            continue
                        for i7 in range(0,len(mazzo)):
                            NewDealer = DealerHand.copy()
                            NewDealer.append(mazzo[i2])
                            NewDealer.append(mazzo[i3])
                            NewDealer.append(mazzo[i4])
                            NewDealer.append(mazzo[i5])
                            NewDealer.append(mazzo[i6])
                            NewDealer.append(mazzo[i7])
                            ValNewDealer = HandValue(NewDealer)
                            if ValNewDealer < 17 or i2 == i7 or i3 == i7 or i4 == i7 or i5 == i7 or i6 == i7:
                                continue
                            else:
                                cont += 1
                                if ValNewHand <= 21 and ValNewHand > ValNewDealer:
                                    numWin += 1
                                elif ValNewHand <= 21 and ValNewDealer > 21:
                                    numWin += 1
                                elif ValNewHand == ValNewDealer:
                                    numDraw += 1
                                elif ValNewHand > 21 and ValNewDealer > 21:
                                    numDraw += 1
                                else:
                                    numLose += 1

    probWinPasso = numWin / cont
    probLosePasso = numLose / cont
    probDrawPasso = numDraw / cont

    # calcolo probabilità di vincere se pesco una carta
    numWin = 0
    numLose = 0
    numDraw = 0
    cont = 0

    for carta in mazzo:

        mazzo = mazzoIntero.copy()
        mazzo.remove(YourHand[0])
        mazzo.remove(YourHand[1])
        mazzo.remove(DealerHand[0])

        mazzo.remove(carta)
        NewHand = YourHand.copy()
        NewHand.append(carta)
        ValNewHand = HandValue(NewHand)

        # Dealer con 2 carte
        for carta2 in mazzo:
            NewDealer = DealerHand.copy()
            NewDealer.append(carta2)
            ValNewDealer = HandValue(NewDealer)
            if ValNewDealer < 17:
                continue
            else:
                cont += 1
                if ValNewHand <= 21 and ValNewHand > ValNewDealer:
                    numWin += 1
                elif ValNewHand <= 21 and ValNewDealer > 21:
                    numWin += 1
                elif ValNewHand == ValNewDealer:
                    numDraw += 1
                elif ValNewHand > 21 and ValNewDealer > 21:
                    numDraw += 1
                else:
                    numLose += 1
            
        # Dealer con 3 carte
        for i2 in range(0,len(mazzo)):
            NewDealer = DealerHand.copy()
            NewDealer.append(mazzo[i2])
            ValNewDealer = HandValue(NewDealer)
            if ValNewDealer >= 17:
                continue
            for i3 in range(0,len(mazzo)):
                NewDealer = DealerHand.copy()
                NewDealer.append(mazzo[i2])
                NewDealer.append(mazzo[i3])
                ValNewDealer = HandValue(NewDealer)
                if ValNewDealer < 17 or i2 == i3:
                    continue
                else:
                    cont += 1
                    if ValNewHand <= 21 and ValNewHand > ValNewDealer:
                        numWin += 1
                    elif ValNewHand <= 21 and ValNewDealer > 21:
                        numWin += 1
                    elif ValNewHand == ValNewDealer:
                        numDraw += 1
                    elif ValNewHand > 21 and ValNewDealer > 21:
                        numDraw += 1
                    else:
                        numLose += 1

        # Dealer con 4 carte
        for i2 in range(0,len(mazzo)):
            NewDealer = DealerHand.copy()
            NewDealer.append(mazzo[i2])
            ValNewDealer = HandValue(NewDealer)
            if ValNewDealer >= 17:
                continue
            for i3 in range(0,len(mazzo)):
                NewDealer = DealerHand.copy()
                NewDealer.append(mazzo[i2])
                NewDealer.append(mazzo[i3])
                ValNewDealer = HandValue(NewDealer)
                if ValNewDealer >= 17 or i2 == i3:
                    continue
                for i4 in range(0,len(mazzo)):
                    NewDealer = DealerHand.copy()
                    NewDealer.append(mazzo[i2])
                    NewDealer.append(mazzo[i3])
                    NewDealer.append(mazzo[i4])
                    ValNewDealer = HandValue(NewDealer)
                    if ValNewDealer < 17 or i2 == i4 or i3 == i4:
                        continue
                    else:
                        cont += 1
                        if ValNewHand <= 21 and ValNewHand > ValNewDealer:
                            numWin += 1
                        elif ValNewHand <= 21 and ValNewDealer > 21:
                            numWin += 1
                        elif ValNewHand == ValNewDealer:
                            numDraw += 1
                        elif ValNewHand > 21 and ValNewDealer > 21:
                            numDraw += 1
                        else:
                            numLose += 1

        # Dealer con 5 carte
        for i2 in range(0,len(mazzo)):
            NewDealer = DealerHand.copy()
            NewDealer.append(mazzo[i2])
            ValNewDealer = HandValue(NewDealer)
            if ValNewDealer >= 17:
                continue
            for i3 in range(0,len(mazzo)):
                NewDealer = DealerHand.copy()
                NewDealer.append(mazzo[i2])
                NewDealer.append(mazzo[i3])
                ValNewDealer = HandValue(NewDealer)
                if ValNewDealer >= 17 or i2 == i3:
                    continue
                for i4 in range(0,len(mazzo)):
                    NewDealer = DealerHand.copy()
                    NewDealer.append(mazzo[i2])
                    NewDealer.append(mazzo[i3])
                    NewDealer.append(mazzo[i4])
                    ValNewDealer = HandValue(NewDealer)
                    if ValNewDealer >= 17 or i2 == i4 or i3 == i4:
                        continue
                    for i5 in range(0,len(mazzo)):
                        NewDealer = DealerHand.copy()
                        NewDealer.append(mazzo[i2])
                        NewDealer.append(mazzo[i3])
                        NewDealer.append(mazzo[i4])
                        NewDealer.append(mazzo[i5])
                        ValNewDealer = HandValue(NewDealer)
                        if ValNewDealer < 17 or i2 == i5 or i3 == i5 or i4 == i5:
                            continue
                        else:
                            cont += 1
                            if ValNewHand <= 21 and ValNewHand > ValNewDealer:
                                numWin += 1
                            elif ValNewHand <= 21 and ValNewDealer > 21:
                                numWin += 1
                            elif ValNewHand == ValNewDealer:
                                numDraw += 1
                            elif ValNewHand > 21 and ValNewDealer > 21:
                                numDraw += 1
                            else:
                                numLose += 1

        # Dealer con 6 carte
        for i2 in range(0,len(mazzo)):
            NewDealer = DealerHand.copy()
            NewDealer.append(mazzo[i2])
            ValNewDealer = HandValue(NewDealer)
            if ValNewDealer >= 17:
                continue
            for i3 in range(0,len(mazzo)):
                NewDealer = DealerHand.copy()
                NewDealer.append(mazzo[i2])
                NewDealer.append(mazzo[i3])
                ValNewDealer = HandValue(NewDealer)
                if ValNewDealer >= 17 or i2 == i3:
                    continue
                for i4 in range(0,len(mazzo)):
                    NewDealer = DealerHand.copy()
                    NewDealer.append(mazzo[i2])
                    NewDealer.append(mazzo[i3])
                    NewDealer.append(mazzo[i4])
                    ValNewDealer = HandValue(NewDealer)
                    if ValNewDealer >= 17 or i2 == i4 or i3 == i4:
                        continue
                    for i5 in range(0,len(mazzo)):
                        NewDealer = DealerHand.copy()
                        NewDealer.append(mazzo[i2])
                        NewDealer.append(mazzo[i3])
                        NewDealer.append(mazzo[i4])
                        NewDealer.append(mazzo[i5])
                        ValNewDealer = HandValue(NewDealer)
                        if ValNewDealer >= 17 or i2 == i5 or i3 == i5 or i4 == i5:
                            continue
                        for i6 in range(0,len(mazzo)):
                            NewDealer = DealerHand.copy()
                            NewDealer.append(mazzo[i2])
                            NewDealer.append(mazzo[i3])
                            NewDealer.append(mazzo[i4])
                            NewDealer.append(mazzo[i5])
                            NewDealer.append(mazzo[i6])
                            ValNewDealer = HandValue(NewDealer)
                            if ValNewDealer < 17 or i2 == i6 or i3 == i6 or i4 == i6 or i5 == i6:
                                continue
                            else:
                                cont += 1
                                if ValNewHand <= 21 and ValNewHand > ValNewDealer:
                                    numWin += 1
                                elif ValNewHand <= 21 and ValNewDealer > 21:
                                    numWin += 1
                                elif ValNewHand == ValNewDealer:
                                    numDraw += 1
                                elif ValNewHand > 21 and ValNewDealer > 21:
                                    numDraw += 1
                                else:
                                    numLose += 1

        # Dealer con 7 carte
        for i2 in range(0,len(mazzo)):
            NewDealer = DealerHand.copy()
            NewDealer.append(mazzo[i2])
            ValNewDealer = HandValue(NewDealer)
            if ValNewDealer >= 17:
                continue
            for i3 in range(0,len(mazzo)):
                NewDealer = DealerHand.copy()
                NewDealer.append(mazzo[i2])
                NewDealer.append(mazzo[i3])
                ValNewDealer = HandValue(NewDealer)
                if ValNewDealer >= 17 or i2 == i3:
                    continue
                for i4 in range(0,len(mazzo)):
                    NewDealer = DealerHand.copy()
                    NewDealer.append(mazzo[i2])
                    NewDealer.append(mazzo[i3])
                    NewDealer.append(mazzo[i4])
                    ValNewDealer = HandValue(NewDealer)
                    if ValNewDealer >= 17 or i2 == i4 or i3 == i4:
                        continue
                    for i5 in range(0,len(mazzo)):
                        NewDealer = DealerHand.copy()
                        NewDealer.append(mazzo[i2])
                        NewDealer.append(mazzo[i3])
                        NewDealer.append(mazzo[i4])
                        NewDealer.append(mazzo[i5])
                        ValNewDealer = HandValue(NewDealer)
                        if ValNewDealer >= 17 or i2 == i5 or i3 == i5 or i4 == i5:
                            continue
                        for i6 in range(0,len(mazzo)):
                            NewDealer = DealerHand.copy()
                            NewDealer.append(mazzo[i2])
                            NewDealer.append(mazzo[i3])
                            NewDealer.append(mazzo[i4])
                            NewDealer.append(mazzo[i5])
                            NewDealer.append(mazzo[i6])
                            ValNewDealer = HandValue(NewDealer)
                            if ValNewDealer >= 17 or i2 == i6 or i3 == i6 or i4 == i6 or i5 == i6:
                                continue
                            for i7 in range(0,len(mazzo)):
                                NewDealer = DealerHand.copy()
                                NewDealer.append(mazzo[i2])
                                NewDealer.append(mazzo[i3])
                                NewDealer.append(mazzo[i4])
                                NewDealer.append(mazzo[i5])
                                NewDealer.append(mazzo[i6])
                                NewDealer.append(mazzo[i7])
                                ValNewDealer = HandValue(NewDealer)
                                if ValNewDealer < 17 or i2 == i7 or i3 == i7 or i4 == i7 or i5 == i7 or i6 == i7:
                                    continue
                                else:
                                    cont += 1
                                    if ValNewHand <= 21 and ValNewHand > ValNewDealer:
                                        numWin += 1
                                    elif ValNewHand <= 21 and ValNewDealer > 21:
                                        numWin += 1
                                    elif ValNewHand == ValNewDealer:
                                        numDraw += 1
                                    elif ValNewHand > 21 and ValNewDealer > 21:
                                        numDraw += 1
                                    else:
                                        numLose += 1

            

    probWinCarta = numWin / cont
    probLoseCarta = numLose / cont
    probDrawCarta = numDraw / cont

    chooseCarta = probWinCarta + probDrawCarta*0.5 - probLoseCarta
    choosePasso = probWinPasso + probDrawPasso*0.5 - probLosePasso

    if chooseCarta > choosePasso:
        choose = 'carta'
    else:
        choose = 'passo'

    return choose, probWinCarta, probWinPasso, probDrawCarta, probDrawPasso, probLoseCarta, probLosePasso
    

# test approccio 1

# caso 1
YourHand1 = ['1c','1q']
DealerHand1 = ['10f']
#print("IA:",YourHand1, "Dealer:",DealerHand1)
#print(Carta(YourHand1, DealerHand1)) 

# caso 2
YourHand1 = ['5c','10q']
DealerHand1 = ['9f']
#print("IA:",YourHand1, "Dealer:",DealerHand1)
#print(Carta(YourHand1, DealerHand1)) 

# caso 3
YourHand1 = ['3c','6q']
DealerHand1 = ['7p']
#print("IA:",YourHand1, "Dealer:",DealerHand1)
#print(Carta(YourHand1, DealerHand1)) 

# caso 4
YourHand1 = ['10c','8q']
DealerHand1 = ['8c']
#print("IA:",YourHand1, "Dealer:",DealerHand1)
#print(Carta(YourHand1, DealerHand1)) 

# caso 5
YourHand1 = ['2c','2q']
DealerHand1 = ['7f']
#print("IA:",YourHand1, "Dealer:",DealerHand1)
#print(Carta(YourHand1, DealerHand1))

# RECAP Approccio 1 #
# codice poco leggibile, molto lungo e rindondante
# dai test sembra non funzionare perfettamente, le probabilità non sembrano corrette
# anche fosse preciso è poco efficente, soprattutto nei casi peggiori come un Dealer con una carta iniziale bassa ed un giocatore con carte basse
 



## Approccio 2: si una una funzione ricorsiva per provare a generare una distribuzione di probabilità a partire da una mano
# la funzione ChooseWithDict() crea i dizionari usati come distribuzioni di probabilità e interpreta i risultati
# la funzione InferenzaProbabilità() è la funzione ricorsiva che calcola la distribuzione di probabilità 

# funzione per ora funzionante solo per calcolare la distr. di prob. del Dealer con la sua carta iniziale
def InferenzaProbabilità(i,dictMazzo,lenMazzo,dictProbHand,flagAsso):
    #print(i, flagAsso)
    #print(dictProbHand)
    #print(lenMazzo,dictMazzo)
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
            dictProbHand = InferenzaProbabilità(i2,newMazzo,lenMazzo-1,dictProbHand,True)
        else:
            dictProbHand = InferenzaProbabilità(i2,newMazzo,lenMazzo-1,dictProbHand,flag2)
    return dictProbHand
    
    
## funzione main dell'agente
# verrà chiamata quando all'agente verrà chiesto se chiedere una carta o passare
# deciderà una mossa alla volta, quindi verrà richiamata finchè non passa (da implementare esternamente)
def ChooseWithDict(MyHand,DealerHand):
    if HandValue(MyHand) > 20: # caso in cui si ha già un 21
        return 'passo'
    elif HandValue(MyHand) < 12: # caso in cui si ha un 11 o meno (matematicamente impossibile sballare)
        return 'carta'
    
    # creo dizionario con le carte del mazzo
    dictMazzo = {'1s':0, '2s':0, '3s':0, '4s':0, '5s':0, '6s':0, '7s':0, '8s':0, '9s':0, '10s':0} # rappresendo il mazzo come la quantità di carte presenti per valore
    for carta in mazzo:
        if len(carta) == 3: # è un 10 o una figura
            dictMazzo['10s'] += 1
        elif carta[0] == '1': # è un asso
            dictMazzo['1s'] += 1
        else: # è una carta da 2 a 9
            dictMazzo[carta[0]+'s'] += 1

    lenMazzo = len(mazzo)
    #print(dictMazzo)

    # distribuzione di probabilità della mano del giocatore e del dealer
    dictValMyHand = {2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0,13:0,14:0,15:0,16:0,17:0,18:0,19:0,20:0,21:0,22:0} # 22 è il caso in cui si sballa
    dictValDealerHand = {2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0,13:0,14:0,15:0,16:0,17:0,18:0,19:0,20:0,21:0,22:0}
    dictValMyHand[HandValue(MyHand)] = 1
    dictValDealerHand[HandValue(DealerHand)] = 1
    
    # caso in cui il dealer ha un asso
    if HandValue(DealerHand) == 11:
        dictValDealerHand = InferenzaProbabilità(HandValue(DealerHand),dictMazzo,lenMazzo,dictValDealerHand,True)
    else:
        dictValDealerHand = InferenzaProbabilità(HandValue(DealerHand),dictMazzo,lenMazzo,dictValDealerHand,False)

    # stampa distribuzioni di probabilità
    #for e in dictValDealerHand:
    #    dictValDealerHand[e] = round(dictValDealerHand[e],5) # arrotondo per maggiore leggibilità, poi non serivirà
    #print("Dealer: ",dictValDealerHand)

    # confronto tra dealer e mano personale
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

    #print("Passo:",probWinPasso,probDrawPasso,probLosePasso)

    # caso in cui si chiede carta
    probWinCarta = 0
    probDrawCarta = 0
    probLoseCarta = 0
    lenMazzo = len(mazzo)

    for carta in mazzo:
        newmazzo = mazzo.copy()
        newmazzo.remove(carta)
        myNewHand = MyHand.copy()
        myNewHand.append(carta)
        dictValMyHand2 = {2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0,13:0,14:0,15:0,16:0,17:0,18:0,19:0,20:0,21:0,22:0}
        if HandValue(myNewHand) <= 21:
            dictValMyHand2[HandValue(myNewHand)] = 1
        else:
            dictValMyHand2[22] = 1
        if HandValue(DealerHand) == 11:
            dictValDealerHand2 = InferenzaProbabilità(HandValue(DealerHand),dictMazzo,lenMazzo,dictValDealerHand,True)
        else:
            dictValDealerHand2 = InferenzaProbabilità(HandValue(DealerHand),dictMazzo,lenMazzo,dictValDealerHand,False)
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

    #print("Carta:",probWinCarta,probDrawCarta,probLoseCarta)

    chooseCarta = probWinCarta + probDrawCarta*0.2 - probLoseCarta
    choosePasso = probWinPasso + probDrawPasso*0.2 - probLosePasso

    if chooseCarta > choosePasso:
        choose = 'carta'
    else:
        choose = 'passo'

    return choose, probWinCarta, probWinPasso, probDrawCarta, probDrawPasso, probLoseCarta, probLosePasso




# test approccio 2

YourHand2 = ['8c','9q']
DealerHand2 = ['6f']
mazzo.remove(YourHand2[0])
mazzo.remove(YourHand2[1])
mazzo.remove(DealerHand2[0])
print(ChooseWithDict(YourHand2,DealerHand2)) # per ora testo solo il delaer, le carte del giocatore non vengono ancora conteggiate


# RECAP Approccio 2 #
# per ora sembra un approccio decisamente migliore
# la distribuzione di probabilità del dealer sembra funzionare correttamente per tutte le carte dal 2...10 all'asso
# l'inferenza è molto veloce (parliamo di ms non s come nel primo approccio)
# una volta aggiunto il caso in cui l'agente simula di chiedere carta la funzione rallenterà ma sarà comunque al peggio n*m, dove n sono le carte nel mazzo e m è il tempo della singola inferenza, quindi comunque molto veloce. O(n) non esponenziale