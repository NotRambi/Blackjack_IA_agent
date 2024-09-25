# Blackjack_IA_agent
Un agente intelligente in grado di giocare a blackjack sfruttando il calcolo dell'utilità attesa, realizzato come progetto di IA presso La Sapienza, Università di Roma

## How to run
Per avviare il programma eseguire il file GUI.py:

    python3 GUI.py

Nelle `Impostazioni` è possibile cambiare i parametri con il quale avviare il gioco, 

infine cliccare su `Gioca` per avviare su un nuovo Thread la partita,  
essa partirà (provvisoriamente) nel terminale da cui si è eseguito il codice.

## File

### Blackjack.py
file python che definisce le classi:
  - Giocatore
  - AgenteIA (che estende Giocatore)
  - Dealer

### Gioco.py
file python che definisce il tavolo da blackjack.  
Contiene tutte le funzioni ausiliarie utili allo svolgimento di una partita e la funzione che definisce il main loop.

### GUI.py
file python che oltre ad essere l'index dell'intero progetto definisce l'interfaccia grafica del menu di avvio,  
permette inoltre tramite l'interazione con l'utente la modifica dei parametri di gioco.
