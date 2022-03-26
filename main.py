# bot.py
import os

import discord
from dotenv import load_dotenv
import random

class potatoBot():
    def __init__(self):
        self.wildMagic = self.readWildMagic()

    #Reads the d10,000 list of wild magic options from the text file and saves it in a list
    #Inputs: N/A
    #Outputs: list
    def readWildMagic(self):
        wildMagic = []
        file = "./d10,000_table.txt"
        with open(file, "r+") as localFile:
            for line in localFile:
                wildMagic.append(line)
        localFile.close()
        return wildMagic

    #Getter for wildMagic array
    def getWildMagic(self):
        return self.wildMagic


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

    poap = potatoBot()
    wildMagic = poap.getWildMagic()

    if message.content == '99!':
        print(message.content.find("!roll"))
        response = random.choice(brooklyn_99_quotes)
        await message.channel.send(response)

    if message.content.find("!roll") == 0:
        response = message.content.split(" ")[1].split("d")

        await message.channel.send(response)
    if message.content.lower() == '!wild magic':
        response = random.choice(wildMagic)
        await message.channel.send(response)

    if message.content.find("!wild magic") == 0:
        pulls = message.content.split(" ")[2]
        pulls = int(pulls)
        print(pulls)
        for i in range(0, pulls):
            response = random.choice(wildMagic)
            await message.channel.send(response)
    
    if message.content.lower() == "!help":
        response = "Potato on a Pedestal takes the following commands:\n"
        response += "!roll XdY: Where X is the number of dice, and Y is the number of faces.\n"
        response += "!wild magic X: Where X is the number of draws from a 10,000 entry wild magic table. Default is 1 pull.\n"
        await message.channel.send(response)

client.run(TOKEN)
