# Documentation for the Blackjack Simulation Project

## Simulation.py

Questo script è responsabile dell'esecuzione di più simulazioni del gioco del Blackjack utilizzando il multi-threading. Permette la configurazione di vari parametri come il numero di agenti AI, agenti ingenui, mazzi, denaro iniziale, mani per simulazione e il numero di simulazioni. I risultati di ogni simulazione vengono raccolti e viene eseguita un'analisi statistica.

### Funzioni

- `run_game_with_queue(game, queue)`: Esegue un'istanza di gioco e mette il risultato in una coda.

### Esecuzione Principale

- Analizza gli argomenti della riga di comando per impostare i parametri della simulazione.
- Inizializza i thread per ogni simulazione.
- Avvia e unisce i thread per eseguire le simulazioni contemporaneamente.
- Raccoglie i risultati dalla coda e calcola i risultati medi per ogni tipo di agente.
- Stampa i risultati e le statistiche della simulazione.

## Blackjack.py

Questo file contiene le classi per la gestione del gioco del Blackjack, inclusi giocatori, agenti AI, agenti ingenui e il dealer. Ogni classe ha metodi per gestire le azioni di gioco come scommettere, pescare carte, calcolare i valori delle mani e prendere decisioni in base allo stato del gioco.

### Classi

- `Giocatore`: Rappresenta un giocatore nel gioco.
    - Metodi: 
        - `toStr()`: Restituisce una rappresentazione in stringa dello stato del giocatore.
        - `ValoreCarta(carta)`: Calcola il valore di una carta.
        - `addCard(carta)`: Aggiunge una carta alla mano del giocatore e aggiorna il valore della mano.
        - `toStrMano()`: Restituisce una rappresentazione in stringa della mano del giocatore.
        - `assicura()`: Assicura la mano del giocatore.
        - `raddoppia()`: Raddoppia la scommessa del giocatore.
        - `resetMano()`: Resetta la mano del giocatore alla fine di un round.

- `AgenteIA`: Rappresenta un agente AI, eredita da `Giocatore`.
    - Metodi: 
        - `resetMazzo()`: Resetta il mazzo quando viene rimescolato.
        - `updateMazzo(uscite)`: Aggiorna il mazzo con le carte che sono state giocate.
        - `resetMano()`: Resetta la mano dell'agente alla fine di un round.
        - `addCardToDealer(carta)`: Aggiorna la mano del dealer.
        - `HandValueCalc(hand)`: Calcola il valore di una mano.
        - `InferenzaProbabilità(i, dictMazzo, lenMazzo, dictProbHand, flagAsso)`: Calcola la distribuzione di probabilità della mano del dealer.
        - `ChooseCarta(MyHand, DealerHand)`: Decide se pescare una carta o passare.
        - `chooseBet()`: Decide l'importo della scommessa in base allo stato del gioco.

- `AgenteNaive`: Rappresenta un agente ingenuo, eredita da `Giocatore`.
    - Metodi: 
        - `HandValueCalc(hand)`: Calcola il valore di una mano.
        - `ChooseCarta(MyHand, DealerHand)`: Decide arbitrariamente se pescare una carta o passare.
        - `chooseBet()`: Decide l'importo della scommessa (fissato all'1% del denaro iniziale).
        - `addCardToDealer(carta)`: Aggiorna la mano del dealer (non usato nell'agente ingenuo).
        - `updateMazzo(uscite)`: Aggiorna il mazzo (non usato nell'agente ingenuo).
        - `resetMazzo()`: Resetta il mazzo (non usato nell'agente ingenuo).

- `dealer`: Rappresenta il dealer nel gioco.
    - Metodi: 
        - `ValoreCarta(carta)`: Calcola il valore di una carta.
        - `addCard(carta)`: Aggiunge una carta alla mano del dealer e aggiorna il valore della mano.
        - `toStrMano()`: Restituisce una rappresentazione in stringa della mano del dealer.
        - `resetMano()`: Resetta la mano del dealer alla fine di un round.

## GUI.py

Questo file gestisce l'interfaccia grafica (GUI) per il gioco del Blackjack utilizzando la libreria Tkinter. Permette agli utenti di avviare un gioco, regolare le impostazioni e visualizzare le statistiche del gioco.

### Classi

- `GUI`: Classe principale per la GUI.
    - Metodi: 
        - `__init__()`: Inizializza la GUI e i suoi componenti.
        - `on_closing()`: Gestisce l'evento di chiusura della GUI.
        - `update()`: Aggiorna la GUI.
        - `run()`: Esegue il ciclo principale della GUI.
        - `HomePage()`: Visualizza la pagina iniziale della GUI.
        - `PlayButton()`: Gestisce l'evento di clic sul pulsante di gioco.
        - `SettingsButton()`: Gestisce l'evento di clic sul pulsante delle impostazioni.
        - `clearHome()`: Cancella i componenti della pagina iniziale.
        - `GamePage()`: Visualizza la pagina del gioco.
        - `startGame()`: Avvia un nuovo gioco.
        - `stopGame()`: Ferma il gioco corrente.
        - `Game_backToHP()`: Torna alla pagina iniziale dalla pagina del gioco.
        - `clearGame()`: Cancella i componenti della pagina del gioco.
        - `SettingsPage()`: Visualizza la pagina delle impostazioni.
        - `updateSlider(event)`: Aggiorna i valori dei cursori per i giocatori e gli agenti AI.
        - `statisticsBtn()`: Attiva/disattiva l'opzione delle statistiche.
        - `VideoBtn()`: Attiva/disattiva l'opzione video.
        - `Setting_backToHP()`: Torna alla pagina iniziale dalla pagina delle impostazioni.
        - `clearSettings()`: Cancella i componenti della pagina delle impostazioni.

### Esecuzione Principale

- Inizializza ed esegue la GUI.

## Game.py

Questo file contiene la logica principale del gioco del Blackjack. Gestisce l'inizializzazione dei giocatori, degli agenti e del dealer, nonché il ciclo principale del gioco, inclusi scommesse, pesca delle carte, verifica delle vincite e gestione dello stato del gioco.

### Classi

- `Game`: Classe principale per la logica del gioco.
    - Metodi: 
        - `__init__(np, nai, nm, sm, sts, vid, tmp, naiv, nmani, print)`: Inizializza il gioco con i parametri specificati.
        - `creaMazzo()`: Crea e mescola il mazzo.
        - `PescaCarta()`: Pesca una carta dal mazzo.
        - `PuntataIniziale()`: Gestisce la fase di scommessa iniziale.
        - `Vincite()`: Verifica le vincite e assegna denaro ai giocatori.
        - `Assicurazione()`: Gestisce la fase di assicurazione.
        - `Raddoppio()`: Gestisce la fase di raddoppio.
        - `EffettuaSplit(Player)`: Gestisce l'azione di split per un giocatore.
        - `Split()`: Verifica e esegue le azioni di split.
        - `DelSplit()`: Elimina i giocatori split.
        - `StartWindow(win)`: Avvia la finestra del gioco.
        - `RunGame()`: Esegue il ciclo principale del gioco, gestendo tutte le azioni e lo stato del gioco.

### Esecuzione Principale

- Inizializza il gioco con i parametri specificati.
- Esegue il ciclo principale del gioco, gestendo tutte le azioni e lo stato del gioco.
- Opzionalmente salva le statistiche del gioco e gestisce l'interfaccia grafica se abilitata.
