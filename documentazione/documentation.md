# Documentation for the Blackjack Simulation Project

## Simulation.py

This script is responsible for running multiple simulations of the Blackjack game using multi-threading. It allows for the configuration of various parameters such as the number of AI agents, naive agents, decks, starting money, hands per simulation, and the number of simulations. The results of each simulation are collected and statistical analysis is performed.

### Functions

- `run_game_with_queue(game, queue)`: Runs a game instance and puts the result in a queue.

### Main Execution

- Parses command-line arguments to set simulation parameters.
- Initializes threads for each simulation.
- Starts and joins threads to run simulations concurrently.
- Collects results from the queue and calculates average results for each agent type.
- Prints the simulation results and statistics.

## Blackjack.py

This file contains the classes for managing the Blackjack game, including players, AI agents, naive agents, and the dealer. Each class has methods for handling game actions such as betting, drawing cards, calculating hand values, and making decisions based on game state.

### Classes

- `Giocatore`: Represents a player in the game.
    - Methods: 
        - `toStr()`: Returns a string representation of the player's state.
        - `ValoreCarta(carta)`: Calculates the value of a card.
        - `addCard(carta)`: Adds a card to the player's hand and updates the hand value.
        - `toStrMano()`: Returns a string representation of the player's hand.
        - `assicura()`: Ensures the player's hand.
        - `raddoppia()`: Doubles the player's bet.
        - `resetMano()`: Resets the player's hand at the end of a round.

- `AgenteIA`: Represents an AI agent, inherits from `Giocatore`.
    - Methods: 
        - `resetMazzo()`: Resets the deck when reshuffled.
        - `updateMazzo(uscite)`: Updates the deck with the cards that have been played.
        - `resetMano()`: Resets the agent's hand at the end of a round.
        - `addCardToDealer(carta)`: Updates the dealer's hand.
        - `HandValueCalc(hand)`: Calculates the value of a hand.
        - `InferenzaProbabilità(i, dictMazzo, lenMazzo, dictProbHand, flagAsso)`: Calculates the probability distribution of the dealer's hand.
        - `ChooseCarta(MyHand, DealerHand)`: Decides whether to draw a card or pass.
        - `chooseBet()`: Decides the bet amount based on the game state.

- `AgenteNaive`: Represents a naive agent, inherits from `Giocatore`.
    - Methods: 
        - `HandValueCalc(hand)`: Calculates the value of a hand.
        - `ChooseCarta(MyHand, DealerHand)`: Decides whether to draw a card or pass arbitrarily.
        - `chooseBet()`: Decides the bet amount (fixed at 1% of the initial money).
        - `addCardToDealer(carta)`: Updates the dealer's hand (not used in naive agent).
        - `updateMazzo(uscite)`: Updates the deck (not used in naive agent).
        - `resetMazzo()`: Resets the deck (not used in naive agent).

- `dealer`: Represents the dealer in the game.
    - Methods: 
        - `ValoreCarta(carta)`: Calculates the value of a card.
        - `addCard(carta)`: Adds a card to the dealer's hand and updates the hand value.
        - `toStrMano()`: Returns a string representation of the dealer's hand.
        - `resetMano()`: Resets the dealer's hand at the end of a round.

## GUI.py

This file manages the graphical user interface (GUI) for the Blackjack game using the Tkinter library. It allows users to start a game, adjust settings, and view game statistics.

### Classes

- `GUI`: Main class for the GUI.
    - Methods: 
        - `__init__()`: Initializes the GUI and its components.
        - `on_closing()`: Handles the closing event of the GUI.
        - `update()`: Updates the GUI.
        - `run()`: Runs the main loop of the GUI.
        - `HomePage()`: Displays the home page of the GUI.
        - `PlayButton()`: Handles the play button click event.
        - `SettingsButton()`: Handles the settings button click event.
        - `clearHome()`: Clears the home page components.
        - `GamePage()`: Displays the game page.
        - `startGame()`: Starts a new game.
        - `stopGame()`: Stops the current game.
        - `Game_backToHP()`: Returns to the home page from the game page.
        - `clearGame()`: Clears the game page components.
        - `SettingsPage()`: Displays the settings page.
        - `updateSlider(event)`: Updates the slider values for players and AI agents.
        - `statisticsBtn()`: Toggles the statistics option.
        - `VideoBtn()`: Toggles the video option.
        - `Setting_backToHP()`: Returns to the home page from the settings page.
        - `clearSettings()`: Clears the settings page components.

### Main Execution

- Initializes and runs the GUI.

## Game.py

This file contains the main game logic for the Blackjack game. It handles the initialization of players, agents, and the dealer, as well as the main game loop, including betting, drawing cards, checking for wins, and managing game state.

### Classes

- `Game`: Main class for the game logic.
    - Methods: 
        - `__init__(np, nai, nm, sm, sts, vid, tmp, naiv, nmani, print)`: Initializes the game with the specified parameters.
        - `creaMazzo()`: Creates and shuffles the deck.
        - `PescaCarta()`: Draws a card from the deck.
        - `PuntataIniziale()`: Handles the initial betting phase.
        - `Vincite()`: Checks for wins and assigns money to players.
        - `Assicurazione()`: Handles the insurance phase.
        - `Raddoppio()`: Handles the doubling phase.
        - `EffettuaSplit(Player)`: Handles the split action for a player.
        - `Split()`: Checks and performs split actions.
        - `DelSplit()`: Deletes split players.
        - `StartWindow(win)`: Starts the game window.
        - `RunGame()`: Runs the main game loop, handling all game actions and state management.

### Main Execution

- Initializes the game with the specified parameters.
- Runs the main game loop, handling all game actions and state management.
- Optionally saves game statistics and manages the graphical interface if enabled.