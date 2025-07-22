from tkinter import *
from tkinter.ttk import Progressbar


class GameUI:
    def __init__(self):
        self.main_window = Tk()
        self.main_window.title("Strategy City Builder")
        self.main_window.geometry("1280x720")
        backdrop = Canvas(self.main_window, bg='white', width=1280, height=100)
        backdrop.place(x=0,y=620)
        self.main_window.resizable(False, False)
        
        # Initialize UI components
        self.init_ui()

    def init_ui(self):
        # Create and place UI elements here
        pass  # Placeholder for UI initialization code

    def show_money(self, money):
        font1 = ("Verdana", 16, "bold")
        moneyStatus = Label(self.main_window,font=font1, bg='white',text='Gold: '+str(money)+ '   ')
        moneyStatus.place(x=300,y=660)

    def show_population(self, population):
        font1 = ("Verdana", 16, "bold")
        populationStatus = Label(self.main_window,font=font1, bg='white',text='Population: '+str(population)+ '   ')
        populationStatus.place(x=20,y=690)

    def show_iron(self, iron):
        font1 = ("Verdana", 16, "bold")
        ironStatus = Label(self.main_window, font=font1, bg='white', text='Iron: ' + str(iron) + '   ')
        ironStatus.place(x=300, y=690)

    def show_attack_power(self, total_attack):
        font1 = ("Verdana", 16, "bold")
        attackStatus = Label(self.main_window, font=font1, bg='white', text='Attack Power: ' + str(total_attack) + '   ')
        attackStatus.place(x=1000, y=630)