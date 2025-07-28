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

        instructions = """
        Build your city and defend it from waves of enemies!
        Buy a plot of land to build a village, mine, or barracks.
        Villages increase population and generate gold.
        Mines generate iron which is used to build barracks.
        Barracks increase attack power and are used to defend against waves of enemies.
        """

        # create a label that gives the instructions of the game
        instructions = Label(self.main_window, text=instructions, font=("Verdana", 12), justify=LEFT, anchor="w")
        instructions.place(x=520, y=20)

        # Initialize UI components
        self.init_ui()

    def init_ui(self):
        # Create and place UI elements here
        # create labels and keep them hidden for now
        self.moneyStatus = Label(self.main_window, font=("Verdana", 16, "bold"), bg='white', text='Gold: 0   ')
        self.moneyStatus.place_forget()
        self.populationStatus = Label(self.main_window, font=("Verdana", 16, "bold"), bg='white', text='Population: 0   ')
        self.populationStatus.place_forget()
        self.ironStatus = Label(self.main_window, font=("Verdana", 16, "bold"), bg='white', text='Iron: 0   ')
        self.ironStatus.place_forget()
        self.attackStatus = Label(self.main_window, font=("Verdana", 16, "bold"), bg='white', text='Attack Power: 0   ')
        self.attackStatus.place_forget()
        self.enemyAttackStatus = Label(self.main_window, font=("Verdana", 16, "bold"), bg='white', text='Enemy Attack Power: 0   ')
        self.enemyAttackStatus.place_forget()
        self.errorLabel = Label(self.main_window, font=("Verdana", 12, "bold"), bg='white', fg='red', text="")
        self.errorLabel.place_forget()

    def show_money(self, money):
        self.moneyStatus.config(text=f'Gold: {money}   ')
        self.moneyStatus.place(x=300, y=660)

    def show_population(self, population):
        self.populationStatus.config(text=f'Population: {population}   ')
        self.populationStatus.place(x=20, y=690)

    def show_iron(self, iron):
        self.ironStatus.config(text=f'Iron: {iron}   ')
        self.ironStatus.place(x=300, y=690)

    def show_attack_power(self, total_attack):
        self.attackStatus.config(text=f'Attack Power: {total_attack}   ')
        self.attackStatus.place(x=1000, y=630)

    def show_enemy_attack_power(self, total_attack):
        self.enemyAttackStatus.config(text=f'Enemy Attack Power: {total_attack}   ')
        self.enemyAttackStatus.place(x=910, y=660)

    def errorMoney(self, message="Not enough money"):
        self.errorLabel.config(text=message)
        self.errorLabel.place(x=900, y=690)
        # Remove the error after 2 seconds
        self.main_window.after(2000, self.errorLabel.place_forget)

    def show_wave_result(self, message, on_close=None):
        # create a new popup window that shows the wave was defeated with an ok button
        popup = Toplevel(self.main_window)
        popup.title("Notification")
        popup.geometry("400x200")
        label = Label(popup, text=message, font=("Verdana", 14, "bold"), bg='white')
        label.pack(pady=40)
        def close_popup():
            popup.destroy()
            if on_close:
                on_close()
        ok_button = Button(popup, text="OK", command=close_popup)
        ok_button.pack(pady=20)

    def show_final_wave_result(self, on_close=None):
        # create a new popup window that shows the final wave was defeated with an ok button
        popup = Toplevel(self.main_window)
        popup.title("Notification")
        popup.geometry("400x200")
        message = "Congratulations!\nYou have defeated all waves!"
        label = Label(popup, text=message, font=("Verdana", 14, "bold"), bg='white')
        label.pack(pady=40)
        def close_popup():
            popup.destroy()
            if on_close:
                on_close()
        ok_button = Button(popup, text="OK", command=close_popup)
        ok_button.pack(pady=20)