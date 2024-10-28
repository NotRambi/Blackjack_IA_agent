from threading import Thread
import queue
import sys
import time
import Game

def run_game_with_queue(game, queue):   # funzione per eseguire il gioco con una coda per i risultati
    result = game.RunGame()
    queue.put(result)

if __name__ == "__main__":
    
    #default values
    numIA = 1
    numAgentiNaive = 0

    numMazzi = 4
    startingMoney = 1000

    numMani = 100
    numSimulazioni = 1

    #input values
    # argomenti della chiamata da riga di comando

    if len(sys.argv) > 1:
        for attr in sys.argv:
            try:
                attr = attr.split('=')
                if attr[0] == "IA":
                    numIA = int(attr[1])
                elif attr[0] == "N":
                    numAgentiNaive = int(attr[1])
                elif attr[0] == "Mazzi":
                    numMazzi = int(attr[1])
                elif attr[0] == "Soldi":
                    startingMoney = int(attr[1])
                elif attr[0] == "Mani":
                    numMani = int(attr[1])
                elif attr[0] == "Sim":
                    numSimulazioni = int(attr[1])
            except:
                print("attributo", attr, "nel formato sbagliato")
                exit()
        print("\nValori di simulazione:\nNumero simulazioni:", numSimulazioni,"\nNumero mani per simulazione:", numMani)
        print("\nValori di gioco:\nNumero agentiIA:", numIA, "\nNumero agenti Naive:", numAgentiNaive, "\nNumero mazzi:", numMazzi, "\nSoldi iniziali:", startingMoney)
    else:
        print("\nValori di default senza argomenti:\nAgenti: 1\nMazzi: 4\nMani: 100\nSoldi: 1000\nSimulazioni: 1") 

    print("\nInizio simulazioni\n")
    
    Threads = []
    Risultati = []
    results_queue = queue.Queue()

    for i in range(numSimulazioni):
        NewGame = Game.Game(0, numIA, numMazzi, startingMoney, False, False, None, numAgentiNaive, numMani, False)
        t = Thread(target=run_game_with_queue, args=(NewGame, results_queue))
        Threads.append(t)

    startingTime = time.time()
    for t in Threads:
        t.start()   # avvia i thread

    for t in Threads:
        t.join()    # attende la fine dei thread
    
    endingTime = time.time()
    simulationTime = endingTime - startingTime 
    print("Simulazioni completate in", simulationTime, "secondi\n")

    # Recupera i risultati dalla coda
    while not results_queue.empty():
        Risultati.append(results_queue.get())

    # calcolo statistiche
    numRes = numAgentiNaive + numIA
    media = [0] * numRes
    for r in Risultati:
        for i in range(numRes):
            media[i] += int(r[i])
    media = [m / numSimulazioni for m in media]

    print("Risultati delle simulazioni:")
    for i in range(numIA):
        print("Agente IA", i+1, ":", media[i])
    for i in range(numAgentiNaive):
        print("Agente Naive", i+1, ":", media[i + numIA])

    print("\n")
