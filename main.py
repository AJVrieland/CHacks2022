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

    def get_die_rolls(self, num_die, die_size):
        total = 0
        die_totals = []

        for i in range(int(num_die)):
            num = random.randint(1, int(die_size))
            die_totals.append(num)
            total += num
        return total, die_totals
        # if (int(num_die) > 1):
        #     die_totals.append(total)
        # print(die_totals)
        # if len(die_totals) == 1:
        #     return str(die_totals[0])
        # else:
        #     mystr = ""
        #     for i in range(len(die_totals) - 1):
        #         mystr += str(die_totals[i]) + " + "
        #     mystr += str(die_totals[-1])
        #     return mystr


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
        total, roll_list = poap.get_die_rolls(response[0], response[1])
        print(roll_list)
        if len(roll_list) > 1:
            tempstr = ""
            for i in range(len(roll_list) - 1):
                tempstr += str(roll_list[i]) + " + "
            tempstr += str(roll_list[-1])
            await message.channel.send(tempstr)
        await message.channel.send(total)


    if message.content == '!wild magic':
        response = random.choice(wildMagic)
        await message.channel.send(response)

client.run(TOKEN)
