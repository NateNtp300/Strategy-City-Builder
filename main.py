import game_ui
from tkinter import *
import math
from tkinter.ttk import Progressbar



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

class windowHandler:
    def __init__(self, open):
        self.open=open

class Property:
    def __init__(self, value, amount, ironCost):
        self.value = value
        self.amount = amount
        self.ironCost = ironCost
        

class Timer:
    def __init__(self, second, minute):
        self.second = second
        self.minute = minute
        
class Soldiers:
    def __init__(self,  name, amount, attack, defence, goldCost, ironCost, titaniumCost):
        self.name = name
        self.amount = amount
        self.attack = attack
        self.defence = defence
        self.goldCost = goldCost
        self.ironCost = ironCost
        self.titanmiumCost = titaniumCost

#declare soldiers
warrior = Soldiers(name="Warrior",
                   amount=0,
                   attack=5,
                   defence=5,
                   goldCost=5,
                   ironCost=2,
                   titaniumCost=0)
knight = Soldiers(name="Knight",
                  amount=0,
                  attack=10,
                  defence=10,
                  goldCost=10,
                  ironCost=5,
                  titaniumCost=0)

#declare properties
village = Property(20, 0, 0)
ironMine = Property(50, 0, 0)
barracks = Property(100, 0, 5)

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
city = City(money=1000,
            iron=100,
            population=0,
            populationPotential=0,
            populationUnused=0,
            populationCap=100)
winOpen = windowHandler(FALSE)

def calc_attack_power():
    total_attack = warrior.amount * warrior.attack + knight.amount * knight.attack
    return total_attack


def showTime():
    
    timer.second += 1
    sec = 1000

    # Create label above the progress bar
    if not hasattr(showTime, "wave_label"):
        showTime.wave_label = Label(main_window, text="the next wave approaches...", font=("Verdana", 12, "bold"), bg='white')
        showTime.wave_label.place(x=500, y=630)

    # Create progress bar if not exists
    if not hasattr(showTime, "progress"):
        showTime.progress = Progressbar(main_window, orient="horizontal", length=200, mode="determinate", maximum=60)
        showTime.progress.place(x=500, y=660)

    showTime.progress["value"] = timer.second

    if timer.second == 60:
        timer.second = 0
        timer.minute += 1
        showTime.progress["value"] = 0
        addMoney()
        addIron()
        ui.show_money(city.money)
        ui.show_iron(city.iron)

    if timer.second < 10:
        timeDisplay.config(text="Time: " + str(timer.minute) + ":0" + str(timer.second))
        timeDisplay.after(sec, showTime)
    else:
        timeDisplay.config(text="Time: " + str(timer.minute) + ":" + str(timer.second))
        timeDisplay.after(sec, showTime)

    
    







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
            plot = Button(main_window, text='$20', compound='center', 
                          image=pixel, 
                          height=50,
                          width=50,
                          padx=0,
                          pady=0, 
                          command=lambda c=z:buy(c))
            plot.grid(row=w, column=i)
            plotList.append(plot)
            z=z+1
            #print(plot['text'])


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
    city.money+=math.trunc((city.population/4))
#gain iron depending on amount of iron mines
def addIron():
    city.iron += (ironMine.amount*2)

def errorMoney():
    errorLabel = Label(main_window, font=("Verdana", 12, "bold"), bg='white', fg='red', text='Not enough money')
    errorLabel.place(x=1100, y=690)
    # Remove the error after 2 seconds
    main_window.after(2000, errorLabel.destroy)
      
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
            errorMoney()

    def buyIronMine():
        if city.money >= ironMine.value:
            city.money-=ironMine.value
            ui.show_money(city.money)
            destroyWindow()
            
            ironMine.amount+=1
            print('Iron Mine count: '+str(ironMine.amount))

            plotList[c].config(image=mine_img, bg='darkgrey', text='')

        else:
            errorMoney()

    def buyBarracks():
        if city.money >= barracks.value and city.iron >= barracks.ironCost:
            city.money -= barracks.value
            city.iron -= barracks.ironCost
            ui.show_iron(city.iron)
            ui.show_money(city.money)
            plotList[c].config(image=barracks_img, bg='red', text='')
            # destroyBarracksWindow()
            destroyWindow()
            
        else:
            print('not enough')


    #if you click on an empty piece of land then the build menu appears
    if plotList[c]['text'] == 'Build' and plotList[c]['bg'] == 'green':
        #print('already bought')
        buildWindow()
        closeBtn = Button(newWindow, bg='darkgrey', text='close', command=destroyWindow)
        closeBtn.place(x=20,y=550)

        villageBtn = Button(newWindow,text='CREATE', bg='darkgrey', command=buyVillage)
        villageBtn.place(x=20,y=50)
        villageLbl = Label(newWindow, text="Village")
        villageLbl.place(x=20,y=80)

        ironMineBtn = Button(newWindow,text='CREATE', bg='darkgrey', command=buyIronMine)
        ironMineBtn.place(x=200,y=50)
        ironMineLbl = Label(newWindow, text="Iron Mine")
        ironMineLbl.place(x=200,y=80)

        barracksBtn = Button(newWindow, text='CREATE', bg ='darkgrey', command=buyBarracks)
        barracksBtn.place(x=20, y=100)
        barracksLbl = Label(newWindow, text="Barracks")
        barracksLbl.place(x=20,y=130)

    if plotList[c]['bg'] =='yellow':
        print('village')
    if plotList[c]['bg'] =='darkgrey':
        print('Iron Mine')

    def trainWarrior():
        if city.money >= warrior.goldCost:
            city.money -= warrior.goldCost
            warrior.amount += 1
            ui.show_money(city.money)
            ui.show_attack_power(calc_attack_power())
            print("Warriors: " + str(warrior.amount))
        else:
            errorMoney()

    def trainKnight():
            if city.money >= knight.goldCost:
                city.money -= knight.goldCost
                knight.amount += 1
                ui.show_money(city.money)
                ui.show_attack_power(calc_attack_power())
                print("Knights: " + str(knight.amount))
            else:
                errorMoney()

    if plotList[c]['bg'] =='red':
        buildBarracksWindow()
        closeBtn = Button(barracksWindow, bg='darkgrey', text='close', command=destroyBarracksWindow)
        closeBtn.place(x=20,y=550)
        warriorBtn = Button(barracksWindow, text='TRAIN', bg='darkgrey', command=trainWarrior)
        warriorBtn.place(x=20, y=50)
        WarriorLbl = Label(barracksWindow, text='Warrior')
        WarriorLbl.place(x=20, y=80)

        knightBtn = Button(barracksWindow, text='TRAIN', bg='darkgrey', command=trainKnight)
        knightBtn.place(x=200, y=50)
        KnightLbl = Label(barracksWindow, text='Knight')
        KnightLbl.place(x=200, y=80)

            

    if plotList[c]['text'] == '$20':
        if city.money >= 20:
            plotList[c].config(image=build_img, bg='green', fg='white', text='Build')
            city.money -=20
            ui.show_money(city.money)
        else:
            errorMoney()

createGrid()
mainloop()