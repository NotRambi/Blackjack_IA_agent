# Come Eseguire

## Parte 1: Creare l'immagine Docker

Per creare l'immagine Docker per il progetto, seguire i passaggi seguenti:

1. Aprire il terminale Linux nella directory di questo file
2. Eseguire il seguente comando:

        docker build -t progetto-ia .
   
    Questo comando creerà un'immagine Docker con il nome "progetto-ia" utilizzando il Dockerfile e i codici presenti in questa directory

## Parte 2: Avviare il container Docker

Dopo aver creato l'immagine Docker, è possibile avviare il container utilizzando i seguenti passaggi:

1. Dai i permessi al file contenente il comando di esecuzione del container:

        chmod +x ./run.sh

2. Esegui il comando:

        ./run.sh

    Questo comando avvierà un nuovo container Docker utilizzando l'immagine "progetto-ia".

## Parte 3: Esecuzione del codice

Una volta avviato il container seguire i seguenti passaggi per provare il codice:

1. Entrare nella repo:

        cd Blackjack_IA_agent/
    
2. Avviare la simulazione:

        python3 Simulation.py IA=1 N=1 Mazzi=4 Sim=10 Mani=100

    Questo comando server per eseguire ad esempio 10 simulazioni da 100 mani con un agente IA ed uno Naive ognuno con 1000 (default) soldi iniziali, in un tavolo con 4 mazzi.

    Ci vorrà un pò di tempo prima che la simulazione finisca,
    verranno poi mostrati i risultati della simulazione.
   
    Per effettuare diverse tipologie di simulazioni modificare i seguenti parametri:
    - IA = numero di agenti IA
    - N = numero di agenti Naive
    - Mazzi = numero di mazzi usati dal Dealer
    - Soldi = numero di soldi iniziali per ogni giocatore
    - Sim = numero di simulazioni da effettuare
    - Mani = numero di mani da giocare per ogni simulazioneni modificare i seguenti parametri:
   

3. Avviare direttamente una partita:

        python3 GUI.py

    Questo comando avvia un interfaccia grafica utile per decidere i parametri di gioco e successivamente avviare una partita a Blackjack con giocatori umani e o agenti IA.
    
    Avvia l'interfaccia grafica nelle `Impostazioni` è possibile cambiare i parametri con il quale avviare il gioco, 
    infine cliccare su `Gioca` per avviare su un nuovo Thread la partita, essa partirà nel terminale da cui si è eseguito il codice.

## Documentation

- [Documentazione](documentazione/documentation.md)