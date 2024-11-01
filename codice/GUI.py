### LIBRERIE ###

from tkinter import *
from tkinter import messagebox
from threading import Thread
import tempfile
import matplotlib.pyplot as plt
import ast
import Game

### CLASSI ###

# Classe Principale

class GUI(object):
    def __init__(self):

        # cartella in User/AppData/Local/Temp per file temporanei
        self.tempfolder = tempfile.TemporaryDirectory() 

        # thread per la partita
        self.t = None

        # Parametri di gioco
        self.numPlayers = 0
        self.numIA = 1
        self.startingMoney = 1000
        self.numMazzi = 4 # da 2 a 6
        self.stats = False
        self.Video = False
        self.plot = None
        self.stats_f = None

        # Finestra GUI
        self.window = Tk()
        self.window.title("Blackjack")
        self.window.geometry("400x600")
        self.window.configure(bg="#222")
        self.window.resizable(False, False)
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.HomePage()

    def on_closing(self):
        if messagebox.askokcancel("Esci", "Vuoi uscire?"):
            if self.t is not None:
                self.stopGame()
                self.t.join()
            if self.stats:
                if self.plot is not None:
                    self.plot.close()
                if self.stats_f is not None:
                    self.stats_f.close()
            self.tempfolder.cleanup() # cancella la cartella temporanea
            self.window.destroy() # chiude la finestra

    def update(self):
        self.window.update()
        self.window.update_idletasks()

    def run(self):
        self.window.mainloop()

    # Home Page
    def HomePage(self):
        # titolo
        self.HP_title = Label(self.window, text="Blackjack", font=('Arial', 24), bg="#222", fg="#eee")
        self.HP_title.place(x=200, y=100, anchor="center")

        # buttons
        self.Play_Button = Button(self.window, text="Gioca",  font=('Arial', 14), command=self.PlayButton, bg="#333", fg="#eee", activebackground="#111", activeforeground="#eee", borderwidth=0)
        self.Play_Button.place(x=200, y=300, anchor="center", width=150)
        
        self.Settings_Button = Button(self.window, text="Impostazioni",  font=('Arial', 14), command=self.SettingsButton, bg="#333", fg="#eee", activebackground="#111", activeforeground="#eee", borderwidth=0)
        self.Settings_Button.place(x=200, y=375, anchor="center", width=150)
        
        self.QuitButton = Button(self.window, text="Esci",  font=('Arial', 14), command=self.on_closing, bg="#333", fg="#eee", activebackground="#111", activeforeground="#eee", borderwidth=0)
        self.QuitButton.place(x=200, y=450, anchor="center", width=150)

    def PlayButton(self):
        self.clearHome()
        self.GamePage()

    def SettingsButton(self):
        self.clearHome()
        self.SettingsPage()

    def clearHome(self):
        self.HP_title.destroy()
        self.Play_Button.destroy()
        self.Settings_Button.destroy()
        self.QuitButton.destroy()

    # Game Page
    def GamePage(self):
        # titolo
        self.Game_title = Label(self.window, text="Gioco", font=('Arial', 24), bg="#222", fg="#eee")
        self.Game_title.place(x=200, y=100, anchor="center")

        # buttons
        self.stop_btn = Button(self.window, text="Arresta", font=('Arial', 14), command=self.stopGame, bg="#333", fg="#eee", activebackground="#111", activeforeground="#eee", borderwidth=0)
        self.stop_btn.place(x=200, y=300, anchor="center", width=150)

        self.Back_Button = Button(self.window, text="Indietro", font=('Arial', 14), command=self.Game_backToHP, bg="#333", fg="#eee", activebackground="#111", activeforeground="#eee", borderwidth=0)
        self.Back_Button.place(x=70, y=560, anchor="center", width=100, height=40)
        
        # avvia partita
        self.startGame()

    def startGame(self):
        path = self.tempfolder.name + "/temp.txt"
        self.f = open(path, "w")
        self.f.write("0")  # questo valore indica che il gioco non deve fermarsi  
        self.f.close()    
        if self.t is None:
            NewGame = Game.Game(self.numPlayers, self.numIA, self.numMazzi, self.startingMoney, self.stats, self.Video, self.tempfolder.name, 0, 0, True)
            self.t = Thread(target=NewGame.RunGame)
            self.t.start()
        elif not self.t.is_alive():
            NewGame = Game.Game(self.numPlayers, self.numIA, self.numMazzi, self.startingMoney, self.stats, self.Video, self.tempfolder.name, 0, 0, True)
            self.t = Thread(target=NewGame.RunGame)
            self.t.start()      

    def stopGame(self):
        path = self.tempfolder.name + "/temp.txt"
        self.f = open(path, "w")
        self.f.write("1") # questo valore indica che il gioco deve fermarsi
        self.f.close()

    def Game_backToHP(self):
        if not self.t.is_alive():
            self.clearGame()
            self.HomePage()
            if self.stats:
                stats_path = self.tempfolder.name + "/stats.txt"
                self.stats_f = open(stats_path, "r")

                # Ignora la prima riga
                self.stats_f.readline()

                # Inizializza le liste per le ascisse e le ordinate
                hands = []
                money = [[] for _ in range(self.numPlayers + self.numIA)]

                # Leggi i dati dal file
                for line in self.stats_f:
                    data = ast.literal_eval(line.strip())
                    hands.append(data[0])
                    for i in range(len(data[1])):
                        money[i].append(data[1][i])

                # Crea il grafico
                self.plot = plt
                self.plot.figure(figsize=(10, 6))
                for i in range(self.numPlayers):
                    self.plot.plot(hands, money[i], label=f'Player {i+1}')
                for i in range(self.numPlayers, self.numPlayers + self.numIA):
                    self.plot.plot(hands, money[i], label=f'Agent {i-self.numPlayers+1}')

                self.plot.xlabel('Mano')
                self.plot.ylabel('Soldi')
                self.plot.title('Andamento dei Soldi per Mano')
                self.plot.legend()
                self.plot.grid(True)
                self.plot.show()
                self.stats_f.close()

    def clearGame(self):
        self.Game_title.destroy()
        self.stop_btn.destroy()
        self.Back_Button.destroy()

    # Settings Page
    def SettingsPage(self):
        # titolo
        self.Settings_title = Label(self.window, text="Impostazioni", font=("Arial", 24), bg="#222", fg="#eee")
        self.Settings_title.place(x=200, y=100, anchor="center")

        # calcolo bounds per gli slider
        if self.numPlayers + self.numIA > 2:
            if self.numPlayers == 0:
                lowerBoundP = 0
                lowerBoundIA = 1
            elif self.numIA == 0:
                lowerBoundP = 1
                lowerBoundIA = 0
            else:
                lowerBoundP = 0
                lowerBoundIA = 0
        elif self.numPlayers + self.numIA == 2:
            if self.numPlayers == 2:
                lowerBoundP = 1
                lowerBoundIA = 0
            elif self.numIA == 2:
                lowerBoundP = 0
                lowerBoundIA = 1
            else:
                lowerBoundP = 0
                lowerBoundIA = 0
        else:
            if self.numPlayers == 1:
                lowerBoundP = 1
                lowerBoundIA = 0
            else:
                lowerBoundP = 0
                lowerBoundIA = 1

        # sliders
        self.Players_label = Label(self.window, text="Giocatori", font=("Arial", 14), bg="#222", fg="#eee")
        self.Players_label.place(x=200, y=170, anchor="center")
        self.Players_slider = Scale(self.window, from_=lowerBoundP, to=7-self.numIA, orient=HORIZONTAL, length=200, command=self.updateSlider, bg="#222", fg="#eee", highlightbackground="#222", troughcolor="#333", sliderlength=50, sliderrelief="flat", borderwidth=1, relief="flat", activebackground="#111")
        self.Players_slider.set(self.numPlayers)
        self.Players_slider.place(x=200, y=200, anchor="center")

        self.IA_label = Label(self.window, text="IA", font=("Arial", 14), bg="#222", fg="#eee")
        self.IA_label.place(x=200, y=270, anchor="center")
        self.IA_slider = Scale(self.window, from_=lowerBoundIA, to=7-self.numPlayers, orient=HORIZONTAL, length=200, command=self.updateSlider, bg="#222", fg="#eee", highlightbackground="#222", troughcolor="#333", sliderlength=50, sliderrelief="flat", borderwidth=1, relief="flat", activebackground="#111")
        self.IA_slider.set(self.numIA)
        self.IA_slider.place(x=200, y=300, anchor="center")

        # input
        self.starting_money_label = Label(self.window, text="Soldi iniziali", font=("Arial", 14), bg="#222", fg="#eee")
        self.starting_money_label.place(x=70, y=380, anchor="center")
        self.starting_money_entry = Entry(self.window, font=("Arial", 14), bg="#333", fg="#eee", relief="flat", borderwidth=0, highlightbackground="#222", insertbackground="#eee")
        self.starting_money_entry.insert(0, self.startingMoney)
        self.starting_money_entry.place(x=160, y=380, anchor="center", width=60, height=35)

        self.numMazzi_label = Label(self.window, text="Num mazzi", font=("Arial", 14), bg="#222", fg="#eee")
        self.numMazzi_label.place(x=250, y=380, anchor="center")
        self.numMazzi_entry = Entry(self.window, font=("Arial", 14), bg="#333", fg="#eee", relief="flat", borderwidth=0, highlightbackground="#222", insertbackground="#eee")
        self.numMazzi_entry.insert(0, self.numMazzi)
        self.numMazzi_entry.place(x=340, y=380, anchor="center", width=60, height=35)

        # buttons
        self.stats_label = Label(self.window, text="Statistiche", font=("Arial", 14), bg="#222", fg="#eee")
        self.stats_label.place(x=150, y=430, anchor="center")
        if self.stats:
            self.statistics_btn  = Button(self.window, text="ON", font=("Arial", 14), command=self.statisticsBtn, bg="#333", fg="#eee", activebackground="#111", activeforeground="#eee", borderwidth=0)
        else:
            self.statistics_btn  = Button(self.window, text="OFF", font=("Arial", 14), command=self.statisticsBtn, bg="#333", fg="#eee", activebackground="#111", activeforeground="#eee", borderwidth=0)
        self.statistics_btn.place(x=250, y=430, anchor="center", width=60, height=35)

        self.anim_label = Label(self.window, text="Video", font=("Arial", 14), bg="#222", fg="#eee")
        self.anim_label.place(x=150, y=480, anchor="center")
        if self.Video:
            self.Video_btn  = Button(self.window, text="ON", font=("Arial", 14), command=self.VideoBtn, bg="#333", fg="#eee", activebackground="#111", activeforeground="#eee", borderwidth=0)
        else:
            self.Video_btn  = Button(self.window, text="OFF", font=("Arial", 14), command=self.VideoBtn, bg="#333", fg="#eee", activebackground="#111", activeforeground="#eee", borderwidth=0)
        self.Video_btn.place(x=250, y=480, anchor="center", width=60, height=35)

        self.Back_Button = Button(self.window, text="Indietro", font=("Arial", 14), command=self.Setting_backToHP, bg="#333", fg="#eee", activebackground="#111", activeforeground="#eee", borderwidth=0)
        self.Back_Button.place(x=70, y=560, anchor="center", width=100, height=40)

    def updateSlider(self, event):
        self.numPlayers = self.Players_slider.get()
        self.numIA = self.IA_slider.get()
        if self.numPlayers + self.numIA > 2:
            if self.numPlayers == 0:
                lowerBoundP = 0
                lowerBoundIA = 1
            elif self.numIA == 0:
                lowerBoundP = 1
                lowerBoundIA = 0
            else:
                lowerBoundP = 0
                lowerBoundIA = 0
        elif self.numPlayers + self.numIA == 2:
            if self.numPlayers == 2:
                lowerBoundP = 1
                lowerBoundIA = 0
            elif self.numIA == 2:
                lowerBoundP = 0
                lowerBoundIA = 1
            else:
                lowerBoundP = 0
                lowerBoundIA = 0
        else:
            if self.numPlayers == 1:
                lowerBoundP = 1
                lowerBoundIA = 0
            else:
                lowerBoundP = 0
                lowerBoundIA = 1
        self.Players_slider.config(from_=lowerBoundP, to=7-self.numIA)
        self.IA_slider.config(from_=lowerBoundIA, to=7-self.numPlayers)

    def statisticsBtn(self):
        self.stats = not self.stats
        if self.stats:
            self.statistics_btn.config(text="ON")
        else:
            self.statistics_btn.config(text="OFF")

    def VideoBtn(self):
        self.Video = not self.Video
        if self.Video:
            self.Video_btn.config(text="ON")
        else:
            self.Video_btn.config(text="OFF")

    def Setting_backToHP(self):
        self.startingMoney = int(self.starting_money_entry.get())
        self.numMazzi = int(self.numMazzi_entry.get())
        self.clearSettings()
        self.HomePage()

    def clearSettings(self):
        self.Settings_title.destroy()
        self.Players_label.destroy()
        self.Players_slider.destroy()
        self.IA_label.destroy()
        self.IA_slider.destroy()
        self.starting_money_label.destroy()
        self.starting_money_entry.destroy()
        self.numMazzi_label.destroy()
        self.numMazzi_entry.destroy()
        self.stats_label.destroy()
        self.statistics_btn.destroy()
        self.anim_label.destroy()
        self.Video_btn.destroy()
        self.Back_Button.destroy()


### MAIN ###

if __name__ == "__main__":
    RunGUI = GUI()
    RunGUI.run()