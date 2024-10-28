# Blackjack_IA_agent
Un agente intelligente in grado di giocare a blackjack sfruttando il calcolo dell'utilità attesa, realizzato come progetto di IA presso La Sapienza, Università di Roma

## How to run with GUI
Per avviare il programma normalmente eseguire il file GUI.py:

    python GUI.py
oppure

    py GUI.py
   
Nelle `Impostazioni` è possibile cambiare i parametri con il quale avviare il gioco, 

infine cliccare su `Gioca` per avviare su un nuovo Thread la partita,  
essa partirà (provvisoriamente) nel terminale da cui si è eseguito il codice.

## How to run with Simulation
Per avviare invece il Simulatore utile ad effettuare velocemente numerose partite in multithread eseguire Simulation.py con i seguenti parametri:
- IA = numero di agenti IA
- N = numero di agenti Naive
- Mazzi = numero di mazzi usati dal Dealer
- Soldi = numero di soldi iniziali per ogni giocatore
- Sim = numero di simulazioni da effettuare
- Mani = numero di mani da giocare per ogni simulazione
  
ad esempio :

    python Simulation.py IA=1 N=1 Mazzi=4 Sim=100 Mani=100
oppure

    py Simulation.py IA=1 N=1 Mazzi=4 Sim=100 Mani=100

per eseguire 100 simulazioni da 100 mani con un agente IA ed uno Naive ognuno con 1000 (default) soldi iniziali, in un tavolo con 4 mazzi.

## Documentation

- [Documentazione](documentazione/documentation.md)
