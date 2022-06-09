# bot.py
from ast import Try, arg
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


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()
poap = potatoBot()
linkDict = {}
diePool = {}

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        'Hot damn!',
        'BONE!',
        'The Full Bull Pen!!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    wildMagic = poap.getWildMagic()

    if message.content == '99!':
        print(message.content.find("!roll"))
        response = random.choice(brooklyn_99_quotes)
        await message.channel.send(response)

    #Adding bulk list of initiative
    if message.content.find("!initiative") == 0:
        argv = message.content.split(" ")
        argv.pop(0)
        response = poap.processInit(argv)
        await message.channel.send("Current order:")
        for initiative in response:
            await message.channel.send(initiative[0] + ": " + str(initiative[1]) )

    #Rolling for initiative inside the app
    if message.content.find("!roll initiative") == 0:
        argv = message.content.split(" ")
        #Immediately popping twice should remove the !roll initiative and leave the arguments
        del argv[0:2]
        if len(argv) != 2:
            response = "Invalid syntax, roll initiative takes 2 arguments: Name and Initiative Modifier"
            await message.channel.send(response)
        else:
            response = poap.rollInitiative(argv)
            await message.channel.send("Current order:")
            for initiative in response:
                await message.channel.send(initiative[0] + ": " + str(initiative[1]) )

    elif message.content.find("!roll") == 0:
        response = message.content.split(" ")[1].split("d")
        total, roll_list = poap.get_die_rolls(response[0], response[1])
        print(roll_list)
        if len(roll_list) > 1:
            tempstr = ""
            for i in range(len(roll_list) - 1):
                tempstr += str(roll_list[i]) + " + "
            tempstr += str(roll_list[-1])
            await message.channel.send(tempstr)
        await message.channel.send(total)

    #Health tracker syntax: !health <mode(set, heal, damage, temp, mass)> <PlayerName> <health value> 
    #Special use case of !health mass <PlayerName>:<HealthValue> <PlayerName>:<HealthValue> <PlayerName>:<HealthValue>
    if message.content.find("!health") == 0:
        #Remove the phrase !health from the argument vector
        argv = message.content.split(" ")
        argv.pop(0)
        response = poap.healthTracker(argv)
        await message.channel.send(response)

    #Wild magic handler
    if message.content.find("!wild") == 0 and message.content.find("magic"):
        try:
            pulls = message.content.split(" ")[2]
            pulls = int(pulls)
        except:
            pulls = 1
        for i in range(0, pulls):
            response = random.choice(wildMagic) + str(message.author)
            await message.channel.send(response)

    if message.content.find("!map") == 0:
        message.channel.send("https://watabou.itch.io/medieval-fantasy-city-generator")

    if message.content.find("!link") == 0:
        name_link = message.content.split(" ")
        linkDict.update({name_link[1]: name_link[2]})

    if message.content.find("!get") == 0:
        link_name = message.content.split(" ")[1]
        await message.channel.send(linkDict.get(link_name))

    if message.content.find("!rg") == 0:
        die_array = poap.roll_genesys()
        die_string = ""
        for i in die_array:
            for j in i:
                die_string += j
        die_dict = {
            "Success": die_string.count("Success"),
            "Failure": die_string.count("Failure"),
            "Inspiration": die_string.count("Inspiration"),
            "Threat": die_string.count("Threat"),
            "Triumph": die_string.count("Triumph"),
            "Despair": die_string.count("Despair")

        }
        await message.channel.send(die_dict)
        diePool.clear()

    #!dp 3g 1y 3p 2b
    if message.content.find("!dp") == 0:
        message_array = message.content.split(" ")
        if len(message_array) > 1:
            for i in range(len(message_array) - 1):
                splt = message_array[i+1]
                diePool.update({splt[-1]: splt[0:-1]})
        else:
            await message.channel.send(diePool)

    if message.content.find("!xkcd") == 0:
        comic_str = message.content.split(" ")
        if len(comic_str) == 1:
            comic = xkcd.getLatestComic()
            print(comic)
            await message.channel.send(comic)
        elif comic_str[1] == "r":
            comic = xkcd.Comic(random.randint(1, xkcd.getLatestComicNum()))
            await message.channel.send(comic.imageLink)
        else:
            comic_num = int(comic_str[1])
            comic = xkcd.Comic(comic_num)
            await message.channel.send(comic.imageLink)

    # Initiative tracker
    if message.content.find("!initiative") == 0:
        argv = message.content.split(" ").pop()
        response = poap.processInit(argv)

    
    if message.content.find("!name") == 0:
        await message.channel.send("https://www.fantasynamegenerators.com/")
    
    if message.content.lower() == "!help":
        response = "Potato on a Pedestal takes the following commands:\n"
        response += "!roll XdY: Where X is the number of dice, and Y is the number of faces.\n"
        response += "!wild magic X: Where X is the number of draws from a 10,000 entry wild magic table. Default is 1 pull.\n"
        response += "!initiative: With no arguments, this command returns the current initiative order"
        response += "!initiative <name:score> <name:score> ... where name is a creature's name and score is their total initiative, roll + mod. "
        response += "This command supports an arbitrary amound of <name:score> pairs\n"
        response += "!initiative clear: This clears the initiative queue"
        response += "!roll initiative <name> <modifier>: Given a creature's name and initiative modifier,"
        response += " rolls 1d20 + modifier and adds the creature to the initiative queue\n"
        await message.channel.send(response)

client.run(TOKEN)
