# bot.py
from ast import Try, arg
import os
import xkcd
import discord
from dotenv import load_dotenv
import random
from potato import potatoBot


if __name__ == '__main__':
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

        if message.content.find("!s") == 0:
            await message.channel.send(poap.get_schedule())

        if message.content.find("!cs") == 0:
            argv = message.content.split(" ")
            print(discord.user)

        if message.content.find("!us") == 0:
            argv = message.content.split(" ")
            week_list = argv[2:]
            poap.update_schedule(argv[1], week_list)
            await message.channel.send(poap.get_schedule())

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
