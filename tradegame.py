################################################################################
#
# Unnamed Tradeing Game
#
# Version 0.0.0.0 - Basic Prototype - Now With Comments (no thanks to old me)
#
################################################################################
################################################################################
#
# TO DO:
#
# Include limits to disallow player from spending more money than they have or
# buying more of a resource than is available in a given town
#
# Create a restoking mechanic so that towns will regain sold resources as well
# as lost bought recouces over time
#
# Create something to handle rumors as a way to hint to the player where there
# might be good deals to be had
#
# Give Towns an available money pool so that there is only so much that the
# player can sell to a single town at once
#
# Create events mechanic so that sometimes, randomly, prices in a certain town
# for a certain resource with change
#
# Make a GUI so that this is prettier than just using the command prompt
#
################################################################################
#
# POSSIBLE IDEAS
#
# Create inventory limit
#
# Player Upgrades
#
################################################################################

import random

import sys
import os
import pygame
from pygame.locals import *

pygame.init()

if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')

# resourcesGlobalMean = { "wheat"    : 1,   "salt"    : 1,   "salted meat"   : 1,
#                         "iron"     : 1,   "silver"  : 1,   "gold"          : 1,
#                         "cloth"    : 1,   "leather" : 1,   "furs"          : 1,
#                         "ale"      : 1,   "cider"   : 1,   "wine"          : 1,
#                         "pepper"   : 1,   "sugar"   : 1,   "saffron"       : 1,
#                         "tools"    : 1,   "weapons" : 1,   "armor"         : 1,
#                         "clothing" : 1,   "shoes"   : 1,   "fine clothing" : 1 }

# The base price of each resource, the price in each town should be different but trend towards these values
resourcesGlobalMean = { "wheat"    : 2,   "salt"    : 30,  "salted meat"   : 7,
                        "iron"     : 100, "silver"  : 300, "gold"          : 500,
                        "cloth"    : 12,  "leather" : 40,  "furs"          : 70,
                        "ale"      : 3,   "cider"   : 4,   "wine"          : 8,
                        "pepper"   : 6,   "sugar"   : 24,  "saffron"       : 180,
                        "tools"    : 10,  "weapons" : 6,   "armor"         : 360,
                        "clothing" : 8,   "shoes"   : 6,   "fine clothing" : 60 }

#An array of the names of each resource
resources = []
for i in resourcesGlobalMean:
    resources.append(i)

# Array of names used for each of the towns
# names from: https://en.wikipedia.org/wiki/List_of_lost_settlements_in_the_United_Kingdom
townNames = ["Stratton", "Sheep Lane", "Ruxox", "Kinwick", "Elvedon",
             "Ackhampstead", "Addingrove", "Doddershall", "Ekeney",
             "Fleet Marston", "Mardale", "Snittlegarth", "Agden Side",
             "Cottons", "Phoside", "Toxall", "Tyneham", "Maryland",
             "Winterborn Farringdon"]

# I *think* theis code *should* import a list of names to be used for the towns from a .txt tile in the same folder as this file which is named.  Don't know that I ever tested it though...
# townNames = []
# file = "villagenames.txt"
# path = dir_path + '\\' + file
# fp = open(path,"r")
# for i in fp:
#     townNames.append(i)
# fp.close()

class Town:
    def __init__(self, id, name, size):
        self.name = name            #The Name of the Town
        self.size = size            #The Size of the Town (should effect how many resources are available)

        # WHAT DOES THIS DO AGAIN?
        self.resourcesQuantity = dict.fromkeys(resourcesGlobalMean, 0)
        for i in random.sample(self.resourcesQuantity.keys(), self.size // 10 + 1):
            if size // 2 <= 1:
                self.resourcesQuantity[i] = random.randrange(1, 2)
            else:
                self.resourcesQuantity[i] = random.randrange(1, size // 2)
        self.resourcesPrice = dict(resourcesGlobalMean)

        # inital randomizing of price
        for i in self.resourcesPrice:
            self.resourcesPrice[i] = self.resourcesPrice[i] * random.triangular(0.5, 1.5)   # Randomizes the value of each resource between 50% and 150% the base price, with a bell curve of the likelyhood of values with 100% being most common and the extreams being least common
            self.resourcesPrice[i] = int(self.resourcesPrice[i])    # Casts the price to an int, removing any decimals left over

        self.roads = dict()     # Creates a dictonary of all the roads that lead out of this town, the towns they lead to, and how far away they are
        self.id = id            # Creates a value, id, which should be a unique identifier

    def getName(self):                          # Returns the town name
        return self.name
    def getSize(self):                          # Returns the town size
        return self.size
    def getResourcesQuantity(self, item):       # Takes one of the resources and returns the number of that item available in the town
        return self.resourcesQuantity[item]
    def getResourcesPrice(self, item):          # Takes one of the resources and returns the price of that item in this town
        return self.resourcesPrice[item]
    def getResourceList(self):                  # Returns an array of all the resources which are available in this town in a quantity grater than 0
        r = []
        for i in self.resourcesQuantity:
            if self.resourcesQuantity[i] != 0:
                r.append(i)
        return r
    def setRoads(self, location, distance):     # Takes another town (in the form of its id) and a value and creates a road between this town and that one with a distance equal to the value
        self.roads[location] = distance

    def getRoads(self):                         # Returns the array of all the towns that this town has a road to
        return self.roads
    def getID(self):                            # Returns this town's id
        return self.id
    def buyStuff(self, stuff, ammount):             # Takes a resource by name and a value and reduces the amount of that resource available in this town by that much
        self.resourcesQuantity[stuff] -= ammount
    def sellStuff(self, stuff, ammount):            # Takes a resource by name and a value and increases the amount of that resource available in this town by that much
        self.resourcesQuantity[stuff] += ammount

class PlayerChar:
    def __init__(self):
        self.location = 1                                           # Starts the player in the town with id of 1
        # FOR TESTING PURPOSES WILL REMOVE OR EDIT LATER
        self.bag = {el:random.randrange(0,2) for el in resources}   # starts the player with either 1 or 0 of each resource
        self.money = 100                                            # Starts the player with 100 money
        self.totalLifetimeMoney = self.money
    def getLocation(self):                                          # Returns the player's current location
        return self.location
    def getMoney(self):                                             # Returns the player's current money
        return self.money
    def goToLocation(self, newloc, cost):                           # Takes a new town's id and its distance and moves the player to that town charging them 1 money per distance
        self.location = newloc
        self.spendMoney(cost)
    def getTotalLifetimeMoney(self):                                # Returns the player's lifetime money
        return self.totalLifetimeMoney
    def getBag(self):                                               # Returns a dictionary of all the resources in the player's inventory in a quantity greater than 0
        stuff = dict()
        for i in self.bag:
            if self.bag[i] != 0:
                stuff[i] = self.bag[i]
        return stuff
    def spendMoney(self, ammount):                                  # Takes a value and reduces the player's money by that ammount
        self.money -= ammount
    def makeMoney(self, ammount):                                   # Takes a value and increases the player's money by that ammount as well as their lifetime money
        self.money += ammount
        if(self.money > self.totalLifetimeMoney):
            self.totalLifetimeMoney = self.money
            return True
        else:
            return False
    def buyStuff(self, stuff, amount, pricePerUnit):                # Takes a resource, an amount of that resourece, and a price then adds an the ammount of the resource to the player's inventory and subtracts money from them based on the price and ammount
        self.bag[stuff] += amount
        self.spendMoney(pricePerUnit * amount)
    def sellStuff(self, stuff, amount, pricePerUnit):               # Takes a resource, an amount of that resourece, and a price then subtracts an the ammount of the resource to the player's inventory and gives them money them based on the price and ammount
        self.bag[stuff] += amount
        self.bag[stuff] -= amount
        self.makeMoney(pricePerUnit * amount)

class PlayGameTest:
    def __init__(self):
        n = random.sample(townNames, 6)                 # Creates an array of 6 town names from the list
        self.towns = []                                 # An array of all the towns in this instance of the game
        for i in range(len(n)):                         # Populates the towns array with created towns with the previously picked names and a random size between 1 and 100
            self.towns.append(Town(i, n[i], random.randrange(1, 100)))
        self.autoSetRoads()                             # Automatically sets roads between the towns

        self.char = PlayerChar()                        # Initiates the player character

        userInput = ""

        while userInput != "quit":                      # Until the player enters "quit" continue the gameplay loop
            b = False
            t = self.towns[self.char.getLocation()]     # the player's current location
            print("Welcome to", t.getName())
            if t.getSize() >= 66:
                print("It is a large city")
            elif t.getSize() <= 33:
                print("It is a small village")
            else:
                print("It is an average sized town")
            print()
            userInput = input("What do you want to do?\n1. Buy at the Market\n2. Sell at the Market\n3. Listen to Rumors\n4. Leave Town\n")
            print()

            # Buy - allows the player to buy the resources availablein the town at the town's price
            if userInput == "1":
                while(not b):
                    print("you have", self.char.getMoney(), "coins")

                    # Prints an aligned table with all avalable recources, now many are available in this town, and their price in this town
                    print('{:>15}  {:>15}  {:>15}'.format("Items", "Price per Unit", "Units Available"))
                    #print("Items\t\tPrice per Unit\t\tUnits Available")
                    for i in t.getResourceList():
                        print('{:>15}  {:>15}  {:>15}'.format(i, str(t.getResourcesPrice(i)), str(t.getResourcesQuantity(i))))
                        #print(i + "\t\t" + str(t.getResourcesPrice(i)) + "\t\t\t" + str(t.getResourcesQuantity(i)))

                    userInput2 = input("\nWhat do you want to buy?\n")      # Player enters name of an availble recource or "back" to continue
                    if userInput2 == "back":                                # If "back" in inputed break current look and go back to the 4 town options
                        b = True
                    else:
                        for i in t.getResourceList():
                            if userInput2 == i:                             # Checks if the input is the name of an availavle recource
                                userInput3 = input("\nThere are " + str(t.getResourcesQuantity(i)) + " units of " + i + ".\nHow many do you want to buy for " + str(t.getResourcesPrice(i)) + " coins each?\n")
                                try:
                                   userInput4 = int(userInput3)
                                except ValueError:
                                   print("That is not a valid number")      # Checks if input is a number
                                else:                                       # Transfers an appropreate number of the chosen recource from the town's availbe amount to the player's inventory and charges the player an approprate ammount of money
                                    t.buyStuff(i, userInput4)
                                    self.char.buyStuff(i, userInput4, t.getResourcesPrice(i))
                    print()

            # Sell - allows the player to sell the resources in their inventory at the town's price
            elif userInput == "2":
                while(not b):
                    print("you have", self.char.getMoney(), "coins")

                    # Prints an aligned table with all avalable recources, now many are available in this town, and their price in this town
                    print('{:>15}  {:>15}  {:>15}'.format("Items", "Price per Unit", "Units Available"))
                    #print("Items\t\tPrice per Unit\t\tUnits Available")
                    for i in self.char.getBag():
                        print('{:>15}  {:>15}  {:>15}'.format(i, str(t.getResourcesPrice(i)), str(self.char.getBag()[i])))
                        #print(i + "\t\t" + str(t.getResourcesPrice(i)) + "\t\t\t" + str(self.char.getBag()[i]))

                    userInput2 = input("\nWhat do you want to sell?\n")     # Player enters name of an availble recource or "back" to continue
                    if userInput2 == "back":                                # If "back" in inputed break current look and go back to the 4 town options
                        b = True
                    else:
                        for i in self.char.getBag():
                            if userInput2 == i:                             # Checks if the input is the name of an availavle recource
                                userInput3 = input("\nYou have " + str(self.char.getBag()[i]) + " units of " + i + ".\nHow many do you want to sell for " + str(t.getResourcesPrice(i)) + " coins each?\n")
                                try:
                                   userInput4 = int(userInput3)
                                except ValueError:
                                   print("That is not a valid number")      # Checks if input is a number
                                else:                                       # Transfers an appropreate number of the chosen recource from the player's inventory to the town's availbe amount and gives the player an approprate ammount of money
                                    t.sellStuff(i, userInput4)
                                    self.char.sellStuff(i, userInput4, t.getResourcesPrice(i))
                    print()

            # Rumors - not implimented, gotta get on that eventually
            elif userInput == "3":
                print("The rumors in this town are:")
                print("rumors not yet implemented")
                input()
                print()

            # Leave Town - lists the towns connected to the one the player is currently is in and lets them travel to one of them
            elif userInput == "4":
                print("The roads lead to these villages:")
                for i in t.getRoads():                                          # Goes through the towns connected to the one the player is currently in and prints them and their distance
                    print(self.towns[i].getName(), "\t\t", t.getRoads()[i], "days away")
                userInput2 = input("\nWhich village do you want to go to?\n")
                for i in t.getRoads():                                          # Checks if the input is the name of an avaible town
                    if userInput2.lower() == self.towns[i].getName().lower():
                        userInput3 = input("\nYou want to go to " + str(self.towns[i].getName()) + " for " + str(t.getRoads()[i]) + " coins?\n")
                        if userInput3.lower() == "yes":
                            self.char.goToLocation(i, t.getRoads()[i])
                print()



    # A function that sets a road between those towns in both town's road dictionary
    def setRoads(self, town1, town2, distance):
        town1.setRoads(town2.getID(), distance)
        town2.setRoads(town1.getID(), distance)

    # Automatically sets roads randomly between towns
    def autoSetRoads(self):
        for i in range(len(self.towns) - 1):                                                # goes through each town that exists in the town array
            limiter = 0                                                                     # to keep from throwing infinite loop when at end and out of towns to link to
            while len(self.towns[i].getRoads()) < 3 and limiter < 100:                      # Will continue to give a town new towns to be connected to until it either has 3 towns connected or it has tried and failed to find a town to connect it to 100 times
                l = random.randrange(i, len(self.towns))                                    # Picks a random town that is further down the list than the current town
                if len(self.towns[l].getRoads()) < 3:                                       # Checks if the picked town already has 3 other towns connected to it and skips it if it does
                    self.setRoads(self.towns[i], self.towns[l], random.randrange(1, 4))     # Connects the two towns with a distance randomly chossen between 1 and 4
                limiter += 1



PlayGameTest()  # Runs the Game
