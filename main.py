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
        file = "./d10,000.txt"
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
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    poap = potatoBot()
    wildMagic = poap.getWildMagic()

    if message.content == '99!':
        response = random.choice(brooklyn_99_quotes)
        await message.channel.send(response)

    if message.content == '!wild magic':
        response = random.choice(wildMagic)
        await message.channel.send(response)
    
    if message.content.lower() == "!help":
        response = "Commands:\n"
    


client.run(TOKEN)
