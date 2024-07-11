from tkinter import *
import math
import time
mainWindow = Tk()
mainWindow.geometry("1280x720")
backdrop = Canvas(mainWindow, bg='white', width=1280, height=100)
backdrop.place(x=0,y=620)

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

# class Property:
#     def __init__(self, villageValue,villageCount, ironMineValue, ironMineCount):
#         self.villageValue = villageValue
#         self.villageCount = villageCount
#         self.ironMineValue = ironMineValue
#         self.ironMineCount = ironMineCount
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
warrior = Soldiers("Warrior", 0, 5, 5, 5, 2, 0)
knight = Soldiers("Knight", 0, 10, 10, 10, 5, 0)

#declare properties
village = Property(20, 0, 0)
ironMine = Property(50, 0, 0)
barracks = Property(100, 0, 5)

plotList = []
plotRows = 10
plotColumns =10
global newWindow
global barracksWindow

timer = Timer(0,0)
city = City(100,0,0,0,0,100)
winOpen = windowHandler(FALSE)
#property = Property(20,0, 50,0)



def showTime():
    
    timer.second+=1
    sec = 1000
    if timer.second == 60:
        timer.second = 0
        timer.minute+=1
        print('add money')
        
        addMoney()
        addIron()
        
        showMoney()
        showIron()

    if timer.second < 10:
        timeDisplay.config(text="Time: " + str(timer.minute) + ":0"+ str(timer.second))
        timeDisplay.after(sec, showTime)
        
    else:
        timeDisplay.config(text="Time: " + str(timer.minute) + ":"+ str(timer.second))
        timeDisplay.after(sec, showTime)

    
    

def showMoney():
    font1 = ("Verdana", 16, "bold")
    moneyStatus = Label(mainWindow,font=font1, bg='white',text='Gold: '+str(city.money)+ '   ')
    moneyStatus.place(x=300,y=660)
def showPopulation():
    font1 = ("Verdana", 16, "bold")
    populationStatus = Label(mainWindow,font=font1, bg='white',text='Population: '+str(city.population)+ '   ')
    populationStatus.place(x=20,y=690)
def showIron():
    font1 = ("Verdana", 16, "bold")
    ironStatus = Label(mainWindow, font=font1, bg='white', text='Iron: ' +str(city.iron)+'   ')
    ironStatus.place(x=300,y=690)

showIron()
showMoney()
showPopulation()


timeDisplay = Label(mainWindow, bg='white',  text="", font=("Verdana",16,"bold"))
timeDisplay.place(x=20, y=660)
showTime()

# mainWindow.columnconfigure(0, weight=1)
# mainWindow.rowconfigure(0, weight=1)
def createGrid():
    global c
    z= 0
    for i in range(plotColumns):
        for w in range(plotRows):
            plot = Button(mainWindow, text='$20', height=3, width=7, command=lambda c=z:buy(c))
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
      
def buy(c):
    global newWindow
    global barracksWindow
    #plotList[90].config(bg='blue')
    def buyVillage():
        if city.money >= village.value:
            city.money-=village.value
            showMoney()
            destroyWindow()
            village.amount +=1
            city.population+=100
            showPopulation()
            # city.populationPotential = village.amount*100
            # print('Population Potential: '+str(city.populationPotential))
            plotList[c].config(bg='yellow')
            # if city.population < city.populationCap:
            #     city.population+=100
            #     showPopulation()
                
            # else:
            #     city.populationUnused +=100
            #     print('Unused population: '+ str(city.populationUnused))
        else:
            print('not enought money')
    
    def buyIronMine():
        if city.money >= ironMine.value:
            city.money-=ironMine.value
            showMoney()
            destroyWindow()
            
            ironMine.amount+=1
            print('Iron Mine count: '+str(ironMine.amount))
            #city.populationCap +=200
            #print('Population cap: '+str(city.populationCap))
            plotList[c].config(bg='darkgrey')
            #showPopulation()
            # if city.populationUnused >=100 and city.populationUnused <200:
            #     city.populationUnused -=100
            #     print('Unused population: '+ str(city.populationUnused))
            #     city.population+=100
            #     showPopulation()
            # if city.populationUnused >=200:
            #     city.populationUnused -=200
            #     print('Unused population: '+ str(city.populationUnused))
            #     city.population+=200
            #     showPopulation()
            
        else:
            print('not enough money')
    
    def buyBarracks():
        if city.money >= barracks.value and city.iron >= barracks.ironCost:
            city.money -= barracks.value
            city.iron -= barracks.ironCost
            showIron()
            showMoney()
            plotList[c].config(bg='red')
            # destroyBarracksWindow()
            destroyWindow()
            
        else:
            print('not enough')


    #if you click on an empty piece of land then the build menu appears
    if plotList[c]['text'] == '' and plotList[c]['bg'] == 'green':
        #print('already bought')
        buildWindow()
        closeBtn = Button(newWindow, bg='darkgrey', text='close', command=destroyWindow).place(x=20,y=550)

        villageBtn = Button(newWindow,text='CREATE', bg='darkgrey', command=buyVillage).place(x=20,y=50)
        villageLbl = Label(newWindow, text="Village").place(x=20,y=80)

        ironMineBtn = Button(newWindow,text='CREATE', bg='darkgrey', command=buyIronMine).place(x=200,y=50)
        ironMineLbl = Label(newWindow, text="Iron Mine").place(x=200,y=80)

        barracksBtn = Button(newWindow, text='CREATE', bg ='darkgrey', command=buyBarracks).place(x=20, y=100)
        barracksLbl = Label(newWindow, text="Barracks").place(x=20,y=130)

    if plotList[c]['bg'] =='yellow':
        print('village')
    if plotList[c]['bg'] =='darkgrey':
        print('Iron Mine')

    def trainWarrior():
        warrior.amount+=1
        print("Warriors: "+ str(warrior.amount))

    if plotList[c]['bg'] =='red':
        buildBarracksWindow()
        closeBtn = Button(barracksWindow, bg='darkgrey', text='close', command=destroyBarracksWindow).place(x=20,y=550)
        warriorBtn = Button(barracksWindow, text='TRAIN', bg='darkgrey', command=trainWarrior).place(x=20, y=50)
        WarriorLbl = Label(barracksWindow, text='Warrior').place(x=20,y=80)

        
            
            

    if plotList[c]['text'] == '$20':
        if city.money >= 20:
            plotList[c].config(bg='green', text='')
            city.money -=20
            showMoney()
        else:
            print('not enough money')


    

    

# money = 100
# def buy(c):
#     global money
#     if money >=50:
#         plotList[c].config(bg='green')
#         money -=50
#         print(money)


createGrid()

    
    

mainloop()