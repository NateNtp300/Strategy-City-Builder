import game_ui
import units
import enemy
from tkinter import *
import math
from tkinter.ttk import Progressbar
import random



ui = game_ui.GameUI()
main_window = ui.main_window

class City:
    def __init__(self, money,iron, population, populationPotential, populationUnused, populationCap):
        self.money = money
        self.iron = iron
        self.population = population
        self.populationPotential = populationPotential
        self.populationUnused = populationUnused
        self.populationCap = populationCap

class Property:
    def __init__(self, value, amount, ironCost):
        self.value = value
        self.amount = amount
        self.ironCost = ironCost
        

class Timer:
    def __init__(self, second, minute):
        self.second = second
        self.minute = minute
        


#declare soldiers
warrior = units.Soldiers(name="Warrior",
                   amount=0,
                   attack=5,
                   defence=5,
                   goldCost=5,
                   ironCost=1,
                   titaniumCost=0)
knight = units.Soldiers(name="Knight",
                  amount=0,
                  attack=10,
                  defence=10,
                  goldCost=10,
                  ironCost=2,
                  titaniumCost=0)

#declare properties
village = Property(value=20, amount=0, ironCost=0)
ironMine = Property(value=50, amount=0, ironCost=0)
barracks = Property(value=100, amount=0, ironCost=5)

plotList = []
plotRows = 10
plotColumns =10
global newWindow
global barracksWindow

pixel = PhotoImage(width=1, height=1)
build_img = PhotoImage(file='build.png')
village_img = PhotoImage(file='village.png')
mine_img = PhotoImage(file='mine.png')
barracks_img = PhotoImage(file='barracks.png')

timer = Timer(0,0)
city = City(money=100,
            iron=0,
            population=0,
            populationPotential=0,
            populationUnused=0,
            populationCap=100)

def calc_attack_power():
    total_attack = warrior.amount * warrior.attack + knight.amount * knight.attack + 10
    return total_attack

wave = enemy.Wave(enemy_attack_power=10, enemy_defense=5)

timer_paused = False
finished_game = True  # Game is not started yet

# Create "Start Game" button
def start_game():
    global finished_game
    finished_game = False  # Allow showTime to run
    start_btn.config(state=DISABLED)
    createGrid()
    showTime()

start_btn = Button(main_window, text="Start Game", bg='lightgreen', font=("Verdana", 12, "bold"), command=start_game)
start_btn.place(x=900, y=325)

def resume_timer():
    global timer_paused
    timer_paused = False

def showTime():
    global timer_paused, finished_game

    if finished_game:
        return

    if timer_paused:
        timeDisplay.after(1000, showTime)
        return

    timer.second += 1
    sec = 1000
    attack_interval = 60
    resource_interval = 5

    # Create label above the progress bar if not exists
    if not hasattr(showTime, "wave_label"):
        showTime.wave_label = Label(main_window, text="The next wave approaches...", font=("Verdana", 12, "bold"), bg='white')
        showTime.wave_label.place(x=500, y=630)

    # Create progress bar if not exists
    if not hasattr(showTime, "progress"):
        showTime.progress = Progressbar(main_window, orient="horizontal", length=200, mode="determinate", maximum=attack_interval)
        showTime.progress.place(x=500, y=660)

    if not wave.all_defeated:
        showTime.progress["value"] = timer.second % attack_interval
    else:
        showTime.progress["value"] = 0

    if timer.second % resource_interval == 0:
        addMoney()
        addIron()
        ui.show_money(city.money)
        ui.show_iron(city.iron)


    if timer.second % attack_interval == 0 and timer.second != 0:
        showTime.progress["value"] = 0
        

        if wave.check_defeat_wave(calc_attack_power(), ui):
            timer_paused = True
            if not finished_game:
                if wave.count == wave.total_waves:
                    ui.show_final_wave_result(on_close=resume_timer)
                    showTime.wave_label.config(text="All waves defeated!")
                    finished_game = True
                    disable_all_plots()
                else:
                    ui.show_wave_result(message="Wave defeated successfully!", on_close=resume_timer)
        else:
            ui.show_wave_result(message="You were defeated!")
            finished_game = True
            disable_all_plots()
            return

    if timer.second == 60:
        timer.second = 0
        timer.minute += 1

    time_str = f"Time: {timer.minute}:{timer.second:02d}"
    timeDisplay.config(text=time_str)
    timeDisplay.after(sec, showTime)
    ui.show_enemy_attack_power(wave.enemy_attack_power)
    ui.show_iron(city.iron)
    ui.show_money(city.money)
    ui.show_population(city.population)
    ui.show_attack_power(calc_attack_power())

timeDisplay = Label(main_window, bg='white',  text="", font=("Verdana",16,"bold"))
timeDisplay.place(x=20, y=660)
showTime()

def createGrid():
    global c
    z= 0
    for i in range(plotColumns):
        for w in range(plotRows):
            cost = random.choice(range(20, 101, 10))
            plot = Button(main_window, text=f'${cost}', compound='center',
                          image=pixel,
                          height=50,
                          width=50,
                          padx=0,
                          pady=0,
                          command=lambda c=z, cost=cost: buy(c))
            plot.grid(row=w, column=i)
            plotList.append(plot)
            z=z+1

def disable_all_plots():
    global plotList
    for plot in plotList:
        plot.config(state=DISABLED)


def buildWindow():
    global newWindow
    newWindow = Toplevel()
    newWindow.geometry('400x600')
    def donothing():
        pass
    newWindow.protocol('WM_DELETE_WINDOW', donothing)
    #when build window opens all background buttons are disabled
    for all in range(plotRows*plotColumns):
            plotList[all]['state'] = DISABLED
    menuLabel = Label(newWindow,text="BUILD A PROPERTY")
    menuLabel.place(x=150,y=0)

def buildBarracksWindow():
    global barracksWindow
    barracksWindow = Toplevel()
    barracksWindow.geometry('400x600')
    def donothing():
        pass
    barracksWindow.protocol('WM_DELETE_WINDOW', donothing)
    for all in range(plotRows*plotColumns):
            plotList[all]['state'] = DISABLED
    menuLabel = Label(barracksWindow,text="TRAIN TROOPS")
    menuLabel.place(x=150,y=0)


    
    

def destroyWindow():
    global newWindow
    newWindow.destroy()
    #when build window is closed all background buttons are enabled
    for all in range(plotRows*plotColumns):
            plotList[all]['state'] = NORMAL

def destroyBarracksWindow():
    global barracksWindow
    barracksWindow.destroy()
    for all in range(plotRows*plotColumns):
            plotList[all]['state'] = NORMAL

#gain revenue depending on population size
def addMoney():
    city.money+=math.trunc((city.population/20))
#gain iron depending on amount of iron mines
def addIron():
    city.iron += (ironMine.amount)


def buy(c):
    global newWindow
    global barracksWindow
    #plotList[90].config(bg='blue')
    def buyVillage():
        if city.money >= village.value:
            city.money-=village.value
            ui.show_money(city.money)
            destroyWindow()
            village.amount +=1
            city.population+=100
            ui.show_population(city.population)
            plotList[c].config(image=village_img, bg='yellow', text='')
                
        else:
            ui.errorMoney()

    def buyIronMine():
        if city.money >= ironMine.value:
            city.money-=ironMine.value
            ui.show_money(city.money)
            destroyWindow()
            
            ironMine.amount+=1
            print('Iron Mine count: '+str(ironMine.amount))

            plotList[c].config(image=mine_img, bg='darkgrey', text='')

        else:
            ui.errorMoney()

    def buyBarracks():
        if city.money >= barracks.value and city.iron >= barracks.ironCost:
            city.money -= barracks.value
            city.iron -= barracks.ironCost
            ui.show_iron(city.iron)
            ui.show_money(city.money)
            plotList[c].config(image=barracks_img, bg='red', text='TRAIN')
            # destroyBarracksWindow()
            destroyWindow()
            
        else:
            ui.errorMoney("Not enough money and iron")


    #if you click on an empty piece of land then the build menu appears
    if plotList[c]['text'] == 'BUILD' and plotList[c]['bg'] == 'green':
        #print('already bought')
        buildWindow()
        closeBtn = Button(newWindow, bg='darkgrey', text='close', command=destroyWindow)
        closeBtn.place(x=20,y=550)

        villageBtn = Button(newWindow,text='CREATE', bg='darkgrey', command=buyVillage)
        villageBtn.place(x=20,y=50)
        villageLbl = Label(newWindow, text="Village")
        villageLbl.place(x=20,y=80)
        villageCostLbl = Label(newWindow, text=f"Cost: {village.value} gold")
        villageCostLbl.place(x=20, y=100)

        ironMineBtn = Button(newWindow,text='CREATE', bg='darkgrey', command=buyIronMine)
        ironMineBtn.place(x=200,y=50)
        ironMineLbl = Label(newWindow, text="Iron Mine")
        ironMineLbl.place(x=200,y=80)
        ironMineCostLbl = Label(newWindow, text=f"Cost: {ironMine.value} gold")
        ironMineCostLbl.place(x=200, y=100)

        barracksBtn = Button(newWindow, text='CREATE', bg='darkgrey', command=buyBarracks)
        barracksBtn.place(x=20, y=150)
        barracksLbl = Label(newWindow, text="Barracks")
        barracksLbl.place(x=20, y=180)
        barracksCostLbl = Label(newWindow, text=f"Cost: {barracks.value} gold, {barracks.ironCost} iron")
        barracksCostLbl.place(x=20, y=200)

    if plotList[c]['bg'] =='yellow':
        print('village')
    if plotList[c]['bg'] =='darkgrey':
        print('Iron Mine')

    def trainWarrior():
        if city.money >= warrior.goldCost and city.iron >= warrior.ironCost:
            city.money -= warrior.goldCost
            city.iron -= warrior.ironCost
            warrior.amount += 1
            ui.show_money(city.money)
            ui.show_iron(city.iron)
            ui.show_attack_power(calc_attack_power())
            print("Warriors: " + str(warrior.amount))
        else:
            ui.errorMoney("Not enough money or iron")

    def trainKnight():
            if city.money >= knight.goldCost and city.iron >= knight.ironCost:
                city.money -= knight.goldCost
                city.iron -= knight.ironCost
                knight.amount += 1
                ui.show_money(city.money)
                ui.show_iron(city.iron)
                ui.show_attack_power(calc_attack_power())
                print("Knights: " + str(knight.amount))
            else:
                ui.errorMoney("Not enough money or iron")

    if plotList[c]['bg'] =='red':
        buildBarracksWindow()
        closeBtn = Button(barracksWindow, bg='darkgrey', text='close', command=destroyBarracksWindow)
        closeBtn.place(x=20,y=550)
        warriorBtn = Button(barracksWindow, text='TRAIN', bg='darkgrey', command=trainWarrior)
        warriorBtn.place(x=20, y=50)
        WarriorLbl = Label(barracksWindow, text=f'Warrior: +{warrior.attack} attack')
        WarriorLbl.place(x=20, y=80)
        WarriorCostLbl = Label(barracksWindow, text=f'Cost: {warrior.goldCost} gold, {warrior.ironCost} iron')
        WarriorCostLbl.place(x=20, y=100)

        knightBtn = Button(barracksWindow, text='TRAIN', bg='darkgrey', command=trainKnight)
        knightBtn.place(x=200, y=50)
        KnightLbl = Label(barracksWindow, text=f'Knight: +{knight.attack} attack')
        KnightLbl.place(x=200, y=80)
        KnightCostLbl = Label(barracksWindow, text=f"Cost: {knight.goldCost} gold, {knight.ironCost} iron")
        KnightCostLbl.place(x=200, y=100)

            

    # Handle buying a plot with its actual cost
    if plotList[c]['text'].startswith('$') and not finished_game:
        try:
            cost = int(plotList[c]['text'][1:])
        except ValueError:
            cost = 0
        if city.money >= cost:
            plotList[c].config(image=build_img, bg='green', fg='white', text='BUILD')
            city.money -= cost
            ui.show_money(city.money)
        else:
            ui.errorMoney()


mainloop()