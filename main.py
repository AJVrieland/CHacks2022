# bot.py
import os

import discord
from dotenv import load_dotenv

class potatoBot():
    def __init__(self):
        self.wildMagic = self.readWildMagic()

    #Reads the d10,000 list of wild magic options from the text file and saves it in a list
    #Inputs: N/A
    #Outputs: list
    def readWildMagic(self):
        wildMagic = []
        file = ".\\d10,000 table.txt"
        with open(file, "r+") as localFile:
            for line in localFile:
                wildMagic.append(line)
        localFile.close()
        return wildMagic

    
    #Simulates a roll on the wild magic table and returns the result
    #Inputs: N/A
    #Outputs: String
    def rollWildMagic(self):
        #Roll a random number, 0 to 9999, and use that to index the list
        pass


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

client.run(TOKEN)