import discord
from discord.ext import commands
from discord.ext.commands import Bot
import json
import datetime
import asyncio
import logging

with open('config.json') as config_file:
        data = json.load(config_file)

TOKEN = data["token"]

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
        await client.change_presence(game=discord.Game(name="~help for help"))
        numberOfServers = len(client.servers)
        print("Connected to " + str(numberOfServers) + " servers")
        print("------\n")

@client.event
async def on_message(message):
        #this stops the bot from reacting to itself
        #if message.author == client.user:
                #return

#General commands and reactions
        if message.content.startswith("~hellobotboi"):
                msg = "Hello {0.author.mention}".format(message)
                await client.send_message(message.channel, msg)
                
        if message.content.startswith("~hellothere"):
                msg = "General Kenobi!"
                await client.send_message(message.channel, msg)

        if message.content.startswith("~heyyy"):
                msg = "Queen Bee"
                await client.send_message(message.channel, msg)

        if message.content.startswith("~goodbot"):
                msg = ":blush:"
                await client.send_message(message.channel, msg)

                #increment the good counter
                goodFile = "BotBoiFiles/goodFile.txt"
                readAndWriteToFile(goodFile)

        if message.content.startswith("~badbot"):
                msg = ":sob:"
                await client.send_message(message.channel, msg)

                #increment the bad counter
                badFile = "BotBoiFiles/badFile.txt"
                readAndWriteToFile(badFile)

        if message.content.startswith("~evaluate"):
                goodFile = open("BotBoiFiles/goodFile.txt", "r")
                goodCount = int(goodFile.read())
                badFile = open("BotBoiFiles/badFile.txt", "r")
                badCount = int(badFile.read())
                percent = (goodCount / (float(goodCount + badCount))) * 100
                msgReturn = "The results show that I am " + str(round(percent, 2)) + "% good!"
                if "NUMBERS" in message.content.upper():
                        msgReturn += "\nGood votes: " + str(goodCount) + "\nBad votes: " + str(badCount)
                
                await client.send_message(message.channel, msgReturn)

        if message.content.startswith("~chaostime"):
                msg = "@everyone <:kappa:522893572131913748>"
                await client.send_message(message.channel, msg)
        
        if message.content.startswith("~birthday"):
                msg = "Happy Birthday"
                mentionList = message.mentions
                for x in range(len(mentionList)):
                        msg += " " + mentionList[x].mention
                msg += "!\nhttp://i.imgur.com/P1vH64S.gif"
                await client.send_message(message.channel, msg)
                

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

#server count command
        if message.content.startswith("~servercount"):
                msg = "Currently connected to " + str(len(client.servers)) + " servers!"
                await client.send_message(message.channel, msg)

                serverNameOut = "Server names:\n\t"
                serverList = list(client.servers)
                for x in range(len(serverList)):
                        serverNameOut += serverList[x-1].name + " - " + serverList[x-1].owner.name + "\n\t"

                await client.send_message(message.channel, serverNameOut)

#Wednesday command
        if message.content.startswith("~wednesday"):
                weekday = datetime.datetime.today().weekday()
                if weekday == 2:#monday=0 -> sunday=6
                        await client.send_file(message.channel, "BotBoiFiles/ITSWEDNESDAY.jpg")
                else:
                        await client.send_message(message.channel, "It is not Wednesday...\nIt is " + getDayName(weekday) + " my dudes!")

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
                        msg = "**NOW PLAYING: **" + message.content[playIndex+6:len(message.content)] + " ~~-----~~o~~--------~~ :rewind: :pause_button: :fast_forward: 0:02/4:20"
                await client.send_message(message.channel, msg)

        if "AYY" in message.content.upper():
                msg = "lmao"
                await client.send_message(message.channel, msg)

#Help command
        if message.content.startswith("~help"):
                msg = "~BotBoi Help~\n\nTry the following commands:\n~hellobotboi\n~hellothere\n~heyyy\n~chaostime\n~wednesday\n~goodbot\n~badbot\n~evaluate"
                await client.send_message(message.channel, msg)

#Dad jokes                
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
                await client.send_message(message.channel, msg)

        if "BRAUM" in message.content.upper():
                if message.author == client.user:
                        return
                msg = "<:standbehindbraum:457164456846163969>"
                await client.send_message(message.channel, msg)

        if "KOZ" in message.content.upper():
                if message.author == client.user:
                        return
                msg = "<:ohdarn:457162626313617438>"
                await client.send_message(message.channel, msg)

        if "AHRI" in message.content.upper():
                if message.author == client.user:
                        return
                msg = "<:ahri:457199789591887872>"
                await client.send_message(message.channel, msg)

        if "SWAIN" in message.content.upper():
                if message.author == client.user:
                        return
                msg = "<:swain:457212057683492864>"
                await client.send_message(message.channel, msg)

        if "PYKE" in message.content.upper():
                if message.author == client.user:
                        return
                msg = "<:pyke:458619798117548042>"
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
##async def Wednesday():
##        await client.wait_until_ready()
##        while not client.is_closed:
##                weekday = datetime.datetime.today().weekday()
##                if weekday == 2:#monday=0 -> sunday=6
##                        #channel = client.get_channel("295972677276139520")#modchat
##                        channel = client.get_channel("135744167811874816")#allchat
##                        await client.send_file(channel, "ITSWEDNESDAY.jpg")
##                        while weekday == 2:
##                                await asyncio.sleep(60)
##                await asyncio.sleep(60)#this makes a check every minute (60 seconds)
##
##client.loop.create_task(Wednesday())
client.run(TOKEN)
