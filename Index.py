from tkinter import *
from tkinter import messagebox
from threading import Thread

class GUI:
    def __init__(self):

        self.numPlayers = 1
        self.numIA = 0

        self.window = Tk()
        self.window.title("Blackjack")
        self.window.geometry("400x600")
        self.window.configure(bg="black")
        self.window.resizable(False, False)
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.HomePage()

    def on_closing(self):
        if messagebox.askokcancel("Esci", "Vuoi uscire?"):
            self.window.destroy()

    def update(self):
        self.window.update()
        self.window.update_idletasks()

    def run(self):
        self.window.mainloop()

    # Home Page
    def HomePage(self):
        self.window.geometry("400x600")
        self.HP_title = Label(self.window, text="Blackjack", font=("Arial", 24), bg="black", fg="white")
        self.HP_title.place(x=200, y=100, anchor="center")
        self.Play_Button = Button(self.window, text="Gioca", font=("Arial", 14), command=self.PlayButton)
        self.Play_Button.place(x=200, y=300, anchor="center", width=150)
        self.Settings_Button = Button(self.window, text="Impostazioni", font=("Arial", 14), command=self.SettingsButton)
        self.Settings_Button.place(x=200, y=375, anchor="center", width=150)
        self.QuitButton = Button(self.window, text="Esci", font=("Arial", 14), command=self.on_closing)
        self.QuitButton.place(x=200, y=450, anchor="center", width=150)

    def PlayButton(self):
        print("Button1")

    def SettingsButton(self):
        self.clearHome()
        self.settings()

    def clearHome(self):
        self.HP_title.destroy()
        self.Play_Button.destroy()
        self.Settings_Button.destroy()
        self.QuitButton.destroy()

    # Game Page

    # Settings Page
    def settings(self):
        self.window.geometry("800x600")
        self.Settings_title = Label(self.window, text="Impostazioni", font=("Arial", 24), bg="black", fg="white")
        self.Settings_title.place(x=400, y=100, anchor="center")

        if self.numPlayers + self.numIA > 2:
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
        self.Players_label = Label(self.window, text="Giocatori", font=("Arial", 14), bg="black", fg="white")
        self.Players_label.place(x=200, y=150, anchor="center")
        self.Players_slider = Scale(self.window, from_=lowerBoundP, to=7-self.numIA, orient=HORIZONTAL, length=200, command=self.updateSlider)
        self.Players_slider.set(self.numPlayers)
        self.Players_slider.place(x=200, y=200, anchor="center")
        self.IA_label = Label(self.window, text="IA", font=("Arial", 14), bg="black", fg="white")
        self.IA_label.place(x=600, y=150, anchor="center")
        self.IA_slider = Scale(self.window, from_=lowerBoundIA, to=7-self.numPlayers, orient=HORIZONTAL, length=200, command=self.updateSlider)
        self.IA_slider.set(self.numIA)
        self.IA_slider.place(x=600, y=200, anchor="center")

        self.Back_Button = Button(self.window, text="Indietro", font=("Arial", 14), command=self.backToHP)
        self.Back_Button.place(x=400, y=500, anchor="center", width=150)

    def updateSlider(self, event):
        self.numPlayers = self.Players_slider.get()
        self.numIA = self.IA_slider.get()
        if self.numPlayers + self.numIA > 2:
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


    def backToHP(self):
        self.clearSettings()
        self.HomePage()

    def clearSettings(self):
        self.Settings_title.destroy()
        self.Players_label.destroy()
        self.Players_slider.destroy()
        self.IA_label.destroy()
        self.IA_slider.destroy()
        self.Back_Button.destroy()


if __name__ == "__main__":
    RunGUI = GUI()
    RunGUI.run()