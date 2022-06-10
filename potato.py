import os
import xkcd
import discord
from dotenv import load_dotenv
import random

class potatoBot():
    def __init__(self):
        self.wildMagic = self.readWildMagic()
        self.initiativeOrder = []
        self.genesys_die = [
            [
                ["Blank"],
                ["Success"],
                ["Success"],
                ["Inspiration"],
                ["Inspiration"],
                ["Success", "Inspiration"],
                ["Inspiration", "Inspiration"]
            ],
            [
                ["Blank"],
                ["Success"],
                ["Success"],
                ["Success", "Success"],
                ["Success", "Success"],
                ["Inspiration"],
                ["Success", "Inspiration"],
                ["Success", "Inspiration"],
                ["Success", "Inspiration"],
                ["Inspiration", "Inspiration"],
                ["Inspiration", "Inspiration"],
                ["Triumph"]
            ],
            [
                ["Blank"],
                ["Blank"],
                ["Success"],
                ["Success", "Inspiration"],
                ["Inspiration", "Inspiration"],
                ["Inspiration"]
            ],
            [
                ["Blank"],
                ["Failure"],
                ["Failure", "Failure"],
                ["Threat"],
                ["Threat"],
                ["Threat"],
                ["Threat", "Threat"],
                ["Failure", "Threat"]
            ],
            [
                ["Blank"],
                ["Failure"],
                ["Failure"],
                ["Failure", "Failure"],
                ["Failure", "Failure"],
                ["Threat"],
                ["Threat"],
                ["Failure", "Threat"],
                ["Failure", "Threat"],
                ["Threat", "Threat"],
                ["Threat", "Threat"],
                ["Despair"]
            ],
            [
                ["Blank"],
                ["Blank"],
                ["Failure"],
                ["Failure"],
                ["Threat"],
                ["Threat"]
            ],
        ]
        self.healthList = []

    # Reads the d10,000 list of wild magic options from the text file and saves it in a list
    # Inputs: N/A
    # Outputs: list
    def readWildMagic(self):
        pass
        # wildMagic = []
        # file = "./d10,000_table.txt"
        # with open(file, "r+") as localFile:
        #     for line in localFile:
        #         wildMagic.append(line)
        # localFile.close()
        # return wildMagic

    # Getter for wildMagic array
    def getWildMagic(self):
        return self.wildMagic

    def initSort(self, index):
        return int(index[1])

    # argv is a vector of variable length, if it's 0, the only thing in the message was !initiative
    def processInit(self, argv):
        # if argv has a length of 0, it's asking for the current order, else add other arguments to initiativeOrder list
        # Idea: make intiative order a list of list, where the inner list has creature name and their initiative score, and sort the
        # outer list by the initiative score
        if len(argv) == 0:
            return self.initiativeOrder
        else:
            #If the first item in argv is "clear", return the blank list
            if(argv[0].lower() == "clear"):
                return self.initiativeOrder
            # if not, process the rest of the arguments
            for arg in argv:
                splitArgs = arg.split(":")
                self.initiativeOrder.append(splitArgs)
            # Sort initiativeOrder and return
            self.initiativeOrder.sort(reverse=True, key=self.initSort)
            return self.initiativeOrder

    # !roll initiative <name> <modifier> rolls 1d20, adds the modifier, and adds the name-value pair to initiativeOrder list, and sorts
    # intiative: list, first value is a name, second value is an initiative modifier
    def rollInitiative(self, initiative):
        total, dieList = self.get_die_rolls(1,20)
        initiative[1] = int(initiative[1]) + total
        self.initiativeOrder.append(initiative)
        self.initiativeOrder.sort(reverse=True, key=self.initSort)
        return self.initiativeOrder

    #Store, modify, and track player health
    #Input: argv: array. Argv[0] is mode: set, heal, damage, or temp, argv[1] is player name,
    #argv[2] is a number that is set to, added to, or removed from player total
    #If no health value is given alongside player, player health is set to 100, and healed or damaged by 5
    def healthTracker(self, argv):
        try:
            mode = argv[0]
        except:
            return self.healthList
        #Remove the mode argument from argv
        argv.pop(0)
        #Set the value in argv to be an int instead of a str, unless the mode is mass or clear, as they use different syntax
        try:
            argv[1] = int(argv[1])
        except:
            pass
        if( mode == "set"):
            self.healthList.append(argv)
        elif( mode == "heal"):
            for player in self.healthList:
                if player.count(argv[0]) == 1:
                    player[1] += int(argv[1])
        elif( mode == "damage"):
            for player in self.healthList:
                if player.count(argv[0]) == 1:
                    player[1] -= int(argv[1])
        elif( mode == "mass"):
            for kvPair in argv:
                argList = kvPair.split(":")
                argList[1] = int(argList[1])
                self.healthList.append(argList)
        elif( mode =="clear"):
            self.healthList = []
        else:
            return "Mode not found"
        #Regardless of the mode, the last action is to return the healthList
        return self.healthList


    def get_die_rolls(self, num_die, die_size):
        total = 0
        die_totals = []

        for i in range(int(num_die)):
            num = random.randint(1, int(die_size))
            die_totals.append(num)
            total += num
        return total, die_totals

    def roll_genesys(self):
        result_array = []
        for key in diePool:
            for i in range(int(diePool.get(key))):
                if key == "g":
                    result_array.append(random.choice(self.genesys_die[0]))
                if key == "y":
                    result_array.append(random.choice(self.genesys_die[1]))
                if key == "u":
                    result_array.append(random.choice(self.genesys_die[2]))
                if key == "p":
                    result_array.append(random.choice(self.genesys_die[3]))
                if key == "r":
                    result_array.append(random.choice(self.genesys_die[4]))
                if key == "l":
                    result_array.append(random.choice(self.genesys_die[5]))
        return result_array

    def get_schedule(self):
        return self.schedule

    def create_schedule(self, person_list):
        days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        self.schedule = {}
        for i in person_list:
            self.schedule.update({i: days_of_week})
        print(self.schedule)

    def update_schedule(self, person, day_list):
        self.schedule.update({person: day_list})
        print(self.schedule)