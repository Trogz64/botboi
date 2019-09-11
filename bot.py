import discord
from discord.ext import commands
from discord.ext.commands import Bot
import json
import datetime
import asyncio
import logging
import random
import time

with open('config.json') as config_file:
        data = json.load(config_file)

TOKEN = data["token"]

COMMAND_CHARACTER = "--"

client = discord.Client()

logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
handler =logging.FileHandler(filename="BotBoiFiles/botLog.log", encoding="utf-8",mode="w")
handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
logger.addHandler(handler)

@client.event
async def on_ready():
        print("\nLogged in as")
        print(client.user.name)
        print(client.user.id)
        print("")
        await client.change_presence(game = discord.Game(name = COMMAND_CHARACTER + "help for help"))
        numberOfServers = len(client.servers)
        print("Connected to " + str(numberOfServers) + " servers")
        print("------\n")

@client.event
async def on_message(message):
        #uncomment to stop the bot from reacting to itself
        # if message.author == client.user:
        #         return

#Help command
        if message.content.startswith(COMMAND_CHARACTER + "help"):
                em = discord.Embed(title="~BotBoi Help~", description="Try the following commands:\n"+COMMAND_CHARACTER + "hellobotboi\n"+COMMAND_CHARACTER + "hellothere\n"+COMMAND_CHARACTER + "heyyy\n"+COMMAND_CHARACTER + "chaostime\n"+COMMAND_CHARACTER + "wednesday\n"+COMMAND_CHARACTER + "goodbot\n"+COMMAND_CHARACTER + "badbot\n"+COMMAND_CHARACTER + "evaluate [numbers]\n"+COMMAND_CHARACTER + "birthday [@mention/multiple @mentions]\n"+COMMAND_CHARACTER + "servercount\n"+COMMAND_CHARACTER + "roll d[Number of faces]", colour=0x800020)
                await client.send_message(message.channel, embed=em)

#General commands
        if message.content.startswith(COMMAND_CHARACTER + "hellobotboi"):
                msg = "Hello {0.author.mention}".format(message)
                await client.send_message(message.channel, msg)
                
        if message.content.startswith(COMMAND_CHARACTER + "hellothere"):
                msg = "General Kenobi!"
                await client.send_message(message.channel, msg)

        if message.content.startswith(COMMAND_CHARACTER + "heyyy"):
                msg = "Queen Bee"
                await client.send_message(message.channel, msg)

        if message.content.startswith(COMMAND_CHARACTER + "chaostime"):
                msg = "@everyone <:kappa:522893572131913748>"
                await client.send_message(message.channel, msg)
        
        if message.content.startswith(COMMAND_CHARACTER + "wednesday"):
                weekday = datetime.datetime.today().weekday()
                if weekday == 2:#monday=0 -> sunday=6
                        await client.send_file(message.channel, "BotBoiFiles/ITSWEDNESDAY.jpg")
                else:
                        await client.send_message(message.channel, "It is not Wednesday...\nIt is " + getDayName(weekday) + " my dudes!")

        if message.content.startswith(COMMAND_CHARACTER + "goodbot"):
                msg = ":blush:"
                await client.send_message(message.channel, msg)

                #increment the good counter
                evaluateFilesExist()
                goodFile = "BotBoiFiles/goodFile.txt"
                readAndWriteToFile(goodFile)

        if message.content.startswith(COMMAND_CHARACTER + "badbot"):
                msg = ":sob:"
                await client.send_message(message.channel, msg)

                #increment the bad counter
                evaluateFilesExist()
                badFile = "BotBoiFiles/badFile.txt"
                readAndWriteToFile(badFile)

        if message.content.startswith(COMMAND_CHARACTER + "evaluate"):
                evaluateFilesExist()
                goodFile = open("BotBoiFiles/goodFile.txt", "r")
                goodCount = int(goodFile.read())
                badFile = open("BotBoiFiles/badFile.txt", "r")
                badCount = int(badFile.read())
                percent = (goodCount / (float(goodCount + badCount))) * 100
                msgReturn = "The results show that I am " + str(round(percent, 2)) + "% good!"
                if "NUMBERS" in message.content.upper():
                        msgReturn += "\nGood votes: " + str(goodCount) + "\nBad votes: " + str(badCount)
                
                em = discord.Embed(title="Evaluation", description=msgReturn, colour=0x800020)
                await client.send_message(message.channel, embed=em)

        if message.content.startswith(COMMAND_CHARACTER + "birthday"):
                msg = "Happy Birthday"
                mentionList = message.mentions
                for x in range(len(mentionList)):
                        msg += " " + mentionList[x].mention
                msg += "!\nhttp://i.imgur.com/P1vH64S.gif"
                await client.send_message(message.channel, msg)

        if message.content.startswith(COMMAND_CHARACTER + "servercount"):
                msg = "Currently connected to " + str(len(client.servers)) + " servers!"
                #Only output the names of the server if the correct parameter is passed
                if "NAME" in message.content.upper():
                        msg += "\nServer names:\n\t"
                        serverList = list(client.servers)
                        for x in range(len(serverList)):
                                msg += serverList[x-1].name + " - " + serverList[x-1].owner.name + "\n\t"
                em = discord.Embed(title="Server Count", description=msg, colour=0x800020)
                await client.send_message(message.channel, embed=em)

        if message.content.startswith(COMMAND_CHARACTER + "roll"):
                number = int(message.content.split("d")[1])
                result = random.randint(1,number)
                em = discord.Embed(title="", description="Rolled a d" + str(number) + "...\n\nThe result is: **" + str(result) + "**", colour=0x800020)
                await client.send_message(message.channel, embed=em)

#reaction to an @everyone
        if message.mention_everyone:
                msg = "<:pingsock:522894414356414475>"
                sent = False
                for x in client.get_all_emojis():
                        if x.name == "pingsock":        #adds the reaction if the emoji is found
                                await client.add_reaction(message, x)
                                sent = True
                if sent != True:        #after the for, if it is not found then it will just send the emoji as a message instead
                        await client.send_message(message.channel, msg)

#Wave reaction to mention
        if client.user in message.mentions:
                emoji = "\U0001F44B"
                await client.add_reaction(message, emoji)

#Special reactions
        if "SLUT" in message.content.upper():
                if message.author == client.user:
                        return
                msg = "no u"
                await client.send_message(message.channel, msg)

        if "ALEXA" in message.content.upper():
                if message.author == client.user:
                        return
                playIndex = message.content.upper().find("PLAY")
                if(playIndex > 0):
                        msg = "**NOW PLAYING: **" + message.content[playIndex+5:len(message.content)] + " ~~-----~~o~~--------~~ :rewind: :pause_button: :fast_forward: 0:02/4:20"
                else:
                        playIndex = message.content.upper().find("ALEXA")
                        msg = "I'm SoRrY, I dIdN't UnDeRsTaNd YoUr QuEsTiOn..."
                await client.send_message(message.channel, msg)

        if "AYY" in message.content.upper():
                msg = "lmao"
                await client.send_message(message.channel, msg)

#Dad joke
        if len(message.content.split().size()) == 2:
                if message.content.startswith("im") or message.content.startswith("Im") or message.content.startswith("IM"):
                        messageLength = len(message.content)
                        returnMessage = message.content[3:messageLength]
                        msg = "Hello " + returnMessage + ", I'm dad!"
                        await client.send_message(message.channel, msg)

                if message.content.startswith("i'm") or message.content.startswith("I'm") or message.content.startswith("I'M"):
                        messageLength = len(message.content)
                        returnMessage = message.content[4:messageLength]
                        msg = "Hello " + returnMessage + ", I'm dad!"
                        await client.send_message(message.channel, msg)

#League emotes
        if "BARD" in message.content.upper():
                if message.author == client.user:
                        return
                msg = "<:ootay:456893214880825354>"
                sent = False
                for x in client.get_all_emojis():
                        if x.name == "ootay":        #adds the reaction if the emoji is found
                                await client.add_reaction(message, x)
                                sent = True
                if sent != True:        #after the for, if it is not found then it will just send the emoji as a message instead
                        await client.send_message(message.channel, msg)

        if "BRAUM" in message.content.upper():
                if message.author == client.user:
                        return
                msg = "<:standbehindbraum:457164456846163969>"
                sent = False
                for x in client.get_all_emojis():
                        if x.name == "standbehindbraum":        #adds the reaction if the emoji is found
                                await client.add_reaction(message, x)
                                sent = True
                if sent != True:        #after the for, if it is not found then it will just send the emoji as a message instead
                        await client.send_message(message.channel, msg)

        if "KOZ" in message.content.upper():
                if message.author == client.user:
                        return
                msg = "<:ohdarn:457162626313617438>"
                sent = False
                for x in client.get_all_emojis():
                        if x.name == "ohdarn":        #adds the reaction if the emoji is found
                                await client.add_reaction(message, x)
                                sent = True
                if sent != True:        #after the for, if it is not found then it will just send the emoji as a message instead
                        await client.send_message(message.channel, msg)

        if "AHRI" in message.content.upper():
                if message.author == client.user:
                        return
                msg = "<:ahri:457199789591887872>"
                sent = False
                for x in client.get_all_emojis():
                        if x.name == "ahri":        #adds the reaction if the emoji is found
                                await client.add_reaction(message, x)
                                sent = True
                if sent != True:        #after the for, if it is not found then it will just send the emoji as a message instead
                        await client.send_message(message.channel, msg)

        if "SWAIN" in message.content.upper():
                if message.author == client.user:
                        return
                msg = "<:swain:457212057683492864>"
                sent = False
                for x in client.get_all_emojis():
                        if x.name == "swain":        #adds the reaction if the emoji is found
                                await client.add_reaction(message, x)
                                sent = True
                if sent != True:        #after the for, if it is not found then it will just send the emoji as a message instead
                        await client.send_message(message.channel, msg)

        if "PYKE" in message.content.upper():
                if message.author == client.user:
                        return
                msg = "<:pyke:458619798117548042>"
                sent = False
                for x in client.get_all_emojis():
                        if x.name == "pyke":        #adds the reaction if the emoji is found
                                await client.add_reaction(message, x)
                                sent = True
                if sent != True:        #after the for, if it is not found then it will just send the emoji as a message instead
                        await client.send_message(message.channel, msg)
        
        if "YORICK" in message.content.upper():
                if message.author == client.user:
                        return
                msg = "<:yorick:619544222068113408>"
                sent = False
                for x in client.get_all_emojis():
                        if x.name == "yorick":        #adds the reaction if the emoji is found
                                await client.add_reaction(message, x)
                                sent = True
                if sent != True:        #after the for, if it is not found then it will just send the emoji as a message instead
                        await client.send_message(message.channel, msg)

        if "LUX" in message.content.upper():
                if message.author == client.user:
                        return
                msg = "<:lux:619545161604792320>"
                sent = False
                for x in client.get_all_emojis():
                        if x.name == "lux":        #adds the reaction if the emoji is found
                                await client.add_reaction(message, x)
                                sent = True
                if sent != True:        #after the for, if it is not found then it will just send the emoji as a message instead
                        await client.send_message(message.channel, msg)
        
        if "NAMI" in message.content.upper():
                if message.author == client.user:
                        return
                msg = "<:nami:619545130566811661>"
                sent = False
                for x in client.get_all_emojis():
                        if x.name == "nami":        #adds the reaction if the emoji is found
                                await client.add_reaction(message, x)
                                sent = True
                if sent != True:        #after the for, if it is not found then it will just send the emoji as a message instead
                        await client.send_message(message.channel, msg)

#this is as close to a switch statement in python as possible. this uses dictionary mapping to return the name of the day from the number given by the date/time format
def getDayName(dayNumber):
        switcher = {
                0: "Monday",
                1: "Tuesday",
                2: "Wednesday",
                3: "Thursday",
                4: "Friday",
                5: "Saturday",
                6: "Sunday",
                }
        return switcher.get(dayNumber, "INVALID DAY")

#Methods

def evaluateFilesExist():
        #make sure that the required text files exist
        #try to open the file. If it cannot be found then create it
        try:
                goodFile = open("BotBoiFiles/goodFile.txt", "r")
                goodFile.close()
        except FileNotFoundError:
                createGoodFile = open("BotBoiFiles/goodFile.txt", "w")
                createGoodFile.write("0")
                createGoodFile.close()
        try:
                badFile = open("BotBoiFiles/badFile.txt", "r")
                badFile.close()
        except FileNotFoundError:
                createBadFile = open("BotBoiFiles/badFile.txt", "w")
                createBadFile.write("0")
                createBadFile.close()

def readAndWriteToFile(myFile):
        try:
                readFile = open(myFile, "r")
                data = int(readFile.read())
                readFile.close()
                data += 1
                writeFile = open(myFile, "w")
                writeFile.write(str(data))
                writeFile.close()
        except:
                print("File read/write error")

# async def Wednesday():
#        await client.wait_until_ready()
#        while not client.is_closed:
#                weekday = datetime.datetime.today().weekday()
#                if weekday == 2:#monday=0 -> sunday=6
#                        #channel = client.get_channel("295972677276139520")#modchat
#                        channel = client.get_channel("135744167811874816")#allchat
#                        await client.send_file(channel, "ITSWEDNESDAY.jpg")
#                        while weekday == 2:
#                                await asyncio.sleep(60)
#                await asyncio.sleep(60)#this makes a check every minute (60 seconds)

# client.loop.create_task(Wednesday())
client.run(TOKEN)