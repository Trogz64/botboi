import discord
from discord.ext import commands
import json
import datetime
import asyncio
import logging
import random
import string
import time
import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

with open(os.path.join(__location__, 'config.json')) as config_file:
        data = json.load(config_file)

TOKEN = data["token"]

COMMAND_CHARACTER = "--"

bot = commands.Bot(command_prefix=COMMAND_CHARACTER, help_command=None)

logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
handler =logging.FileHandler(filename=os.path.join(__location__, "BotBoiFiles/botLog.log"), encoding="utf-8",mode="w")
handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
logger.addHandler(handler)

@bot.event
async def on_ready():
        print("\nLogged in as {0.user}\n".format(bot))
        await bot.change_presence(activity = discord.Activity(type = discord.ActivityType.listening, name = COMMAND_CHARACTER + "help"))
        numberOfServers = len(bot.guilds)
        print("Connected to " + str(numberOfServers) + " servers")
        print("------\n")

# Help command
@bot.command()
async def help(ctx, *args):
        if len(args) > 0:
                exists = False
                for comm in bot.commands:
                        if args[0] == comm.name:
                                exists = True
                                em = discord.Embed(title="\"" + comm.name + "\"" + " help", description=comm.help + "\n\nUsage: " + comm.usage, colour=0x800020)
                                await ctx.send(embed=em)
                if not exists:
                        em = discord.Embed(descirption="Unknown command \"" + str(args[0] + "\""), colour=0x800020)
                        await ctx.send(embed=em)
        else:
                em = discord.Embed(title="~BotBoi Help~", description="Try the following commands:\n" 
                + COMMAND_CHARACTER + "hellobotboi\n" 
                + COMMAND_CHARACTER + "hellothere\n" 
                + COMMAND_CHARACTER + "heyyy\n" 
                + COMMAND_CHARACTER + "wednesday\n" 
                + COMMAND_CHARACTER + "goodbot\n" 
                + COMMAND_CHARACTER + "badbot\n" 
                + COMMAND_CHARACTER + "evaluate <numbers>\n" 
                + COMMAND_CHARACTER + "birthday [@mention/multiple @mentions]\n" 
                + COMMAND_CHARACTER + "servercount\n" 
                + COMMAND_CHARACTER + "roll d[Number of faces]\n" 
                + COMMAND_CHARACTER + "poll \"Question\" \"Option1\" \"Option2\" ... \"Option9\"\n"
                + COMMAND_CHARACTER + "eightball \"Question\"\n"
                + COMMAND_CHARACTER + "github\n"
                + COMMAND_CHARACTER + "invite\n"
                + "\n" + COMMAND_CHARACTER + "help [command] for more info about a command", colour=0x800020)
                await ctx.send(embed=em)

# Commands
@bot.command(help="Botboi greets you!", usage=COMMAND_CHARACTER + "hellobotboi")
async def hellobotboi(ctx):
        await ctx.send("Hello {0.author.mention}".format(ctx))

@bot.command(help="You are a bold one!", usage=COMMAND_CHARACTER + "hellothere")
async def hellothere(ctx):
        await ctx.send("General Kenobi!")

@bot.command(help="", usage=COMMAND_CHARACTER + "heyyy")
async def heyyy(ctx):
        await ctx.send("Queen Bee")
        
@bot.command(help="Give this a try on a Wednesday...", usage=COMMAND_CHARACTER + "wednesday")
async def wednesday(ctx):
        weekday = datetime.datetime.today().weekday()
        if weekday == 2:#monday=0 -> sunday=6
                await ctx.send(file = discord.File(fp = os.path.join(__location__, 'BotBoiFiles/ITSWEDNESDAY.jpg'), filename = 'WednesdayFrog.jpg'))
        else:
                await ctx.send("It is not Wednesday...\nIt is " + getDayName(weekday) + " my dudes!")

@bot.command(help="Increments Botboi's good counter", usage=COMMAND_CHARACTER + "goodbot")
async def goodbot(ctx):
        await ctx.send(":blush:")

        #increment the good counter
        evaluateFilesExist()
        goodFile = os.path.join(__location__, "BotBoiFiles/goodFile.txt")
        readAndWriteToFile(goodFile)

@bot.command(help="Increments Botboi's bad counter", usage=COMMAND_CHARACTER + "badbot")
async def badbot(ctx):
        await ctx.send(":sob:")

        #increment the bad counter
        evaluateFilesExist()
        badFile = os.path.join(__location__, "BotBoiFiles/badFile.txt")
        readAndWriteToFile(badFile)

@bot.command(help="Returns the results of using goodbot and badbot commands as a percentage.\n"
        +"Include optional parameter 'number' to also return the exact numbers.", usage=COMMAND_CHARACTER + "evaluate <number>")
async def evaluate(ctx, *args):
        evaluateFilesExist()
        goodFile = open(os.path.join(__location__, "BotBoiFiles/goodFile.txt"), "r")
        goodCount = int(goodFile.read())
        badFile = open(os.path.join(__location__, "BotBoiFiles/badFile.txt"), "r")
        badCount = int(badFile.read())
        percent = (goodCount / (float(goodCount + badCount))) * 100
        msgReturn = "The results show that I am " + str(round(percent, 2)) + "% good!"
        if len(args) > 0:
                if "NUMBER" in args[0].upper():
                        msgReturn += "\nGood votes: " + str(goodCount) + "\nBad votes: " + str(badCount)
        
        em = discord.Embed(title="Evaluation", description=msgReturn, colour=0x800020)
        await ctx.send(embed=em)

@bot.command(help="Send your friends a Birthday message from Botboi.\n"
        +"Mention your friend, mention all your friends, mention no one, or mention yourself!", usage=COMMAND_CHARACTER + "birthday @mention/multiple @mentions")
async def birthday(ctx):
        msg = "Happy Birthday"
        mentionList = ctx.message.mentions
        for x in range(len(mentionList)):
                msg += " " + mentionList[x].mention
        msg += "!\nhttp://i.imgur.com/P1vH64S.gif"
        await ctx.send(msg)

@bot.command(help="Returns the number of servers that Botboi is currently connected to", usage=COMMAND_CHARACTER + "servercount")
async def servercount(ctx):
        em = discord.Embed(title="Server Count", description="Currently connected to " + str(len(bot.guilds)) + " servers!", colour=0x800020)
        await ctx.send(embed=em)

@bot.command(help="Rolls a die. You pick the number of sides (e.g. d6 = 6 sides, d20 = 20 sides, etc.)", usage=COMMAND_CHARACTER + "roll d[number of faces]")
async def roll(ctx, arg1):
        number = int(arg1.split("d")[1])
        result = random.randint(1,number)
        em = discord.Embed(title="", description="Rolled a d" + str(number) + "...\n\nThe result is: **" + str(result) + "**", colour=0x800020)
        await ctx.send(embed=em)

@bot.command(help="Create a poll for users to vote on.\nVote using the reactions added.\nYou can have up to nine (9) options in your poll.\n\n"
        +"Surround your question and options in quotation marks, and separate them with a space", usage=COMMAND_CHARACTER + "poll \"Question\" \"Option1\" \"Option2\" ... \"Option9\"")
async def poll(ctx, *args):
        if len(args) >= 1:
                question = args[0]
                numOfOptions = len(args)-1
                #check to see if enough options have been provided
                if numOfOptions < 2:
                        await ctx.send("Please provide at least two options for your poll")
                        return
                if numOfOptions > 9:
                        await ctx.send("You have exceeded the maximum number of options (9)")
                        return
        else:
                await ctx.send("Invalid syntax. Please provide a question and at least two options for your poll")
                return
        optionsString = ""
        for x in range(numOfOptions+1):
                if x > 0:
                        optionsString += getNumberEmote(x) + ": " + str(args[x]) + "\n"
        
        em = discord.Embed(title=question, description=optionsString, colour=0x800020)
        botMessage = await ctx.send(embed=em)

        # Add the reactions which users can vote with
        for i in range(numOfOptions+1):
                if i > 0:
                        await botMessage.add_reaction(getNumberEmote(i))

@bot.command(help="Ask the Magic 8-Ball a question", usage=COMMAND_CHARACTER + "eightball \"Question\"")
async def eightball(ctx, *args):
        if len(args) > 0:
                question = args[0]
        else:
                await ctx.send("You need to ask the Magic 8-Ball a question.")
                return
        
        response = get8BallResponse(random.randint(1,20))
        em = discord.Embed(title="", description="\U0001F3B1 " + response, colour=0x800020)
        await ctx.send(embed=em)

@bot.command(help="Returns the link to the Botboi Github repository", usage=COMMAND_CHARACTER + "github")
async def github(ctx):
        em = discord.Embed(title="Botboi Github", description="https://github.com/Trogz64/botboi", colour=0x800020)
        await ctx.send(embed=em)

@bot.command(help="Returns the link with which you can invite Botboi to your own server", usage=COMMAND_CHARACTER + "invite")
async def invite(ctx):
        em = discord.Embed(title="Botboi Invite Link", description="Use this link to invite me to your servers!\n"
        + "https://discord.com/api/oauth2/authorize?client_id=416406487024402432&permissions=523328&redirect_uri=https%3A%2F%2Fdiscordapp.com%2Fapi%2Foauth2%2Fauthorize%3Fclient_id%3D416406487024402432%26permissions%3D518208%26redirect_uri%3Dhttps%253A%252F%252Fdiscordapp.com%252Fapi%252Foauth2%252Fauthorize%253Fclient_&scope=bot", colour=0x800020)
        await ctx.send(embed=em)


# Reactions to messages
@bot.listen('on_message')
async def messageReactions(message):
        # uncomment to stop the bot from reacting to itself
        # if message.author == client.user:
        #         return

        #reaction to an @everyone
        if message.mention_everyone:
                msg = "<:pingsock:522894414356414475>"
                sent = False
                for x in bot.emojis:
                        if x.name == "pingsock":        #adds the reaction if the emoji is found
                                await message.add_reaction(x)
                                sent = True
                if sent != True:        #after the for, if it is not found then it will just send the emoji as a message instead
                        await message.channel.send(msg)

        #Wave reaction to mention
        if bot.user in message.mentions:
                emoji = "\U0001F44B"
                await message.add_reaction(emoji)

        #Special reactions
        if "ALEXA" in message.content.upper().translate(str.maketrans('', '', string.punctuation)).split():
                if message.author == bot.user:
                        return
                playIndex = message.content.upper().find("PLAY")
                if(playIndex > 0):
                        msg = "**NOW PLAYING: **" + message.content[playIndex+5:len(message.content)] + " ~~-----~~o~~--------~~ :rewind: :pause_button: :fast_forward: 0:02/4:20"
                else:
                        msg = "I'm SoRrY, I dIdN't UnDeRsTaNd YoUr QuEsTiOn..."
                await message.channel.send(msg)

        if message.content == "F":
                if message.author == bot.user:
                        return
                await message.channel.send("F")

        if message.content == "f":
                if message.author == bot.user:
                        return
                await message.channel.send("f")

        #League emotes
        #We need to make sure that the intended trigger is a word in itself, and not a substring in a different word
        if "BARD" in message.content.upper().translate(str.maketrans('', '', string.punctuation)).split() or "BARDS" in message.content.upper().translate(str.maketrans('', '', string.punctuation)).split():
                if message.author == bot.user:
                        return
                msg = "<:ootay:456893214880825354>"
                sent = False
                for x in bot.emojis:
                        if x.name == "ootay":        #adds the reaction if the emoji is found
                                await message.add_reaction(x)
                                sent = True
                if sent != True:        #after the for, if it is not found then it will just send the emoji as a message instead
                        await message.channel.send(msg)

        if "MEEP" in message.content.upper().translate(str.maketrans('', '', string.punctuation)).split() or "MEEPS" in message.content.upper().translate(str.maketrans('', '', string.punctuation)).split():
                if message.author == bot.user:
                        return
                msg = "<:meep:797893845819457567>"
                sent = False
                for x in bot.emojis:
                        if x.name == "meep":        #adds the reaction if the emoji is found
                                await message.add_reaction(x)
                                sent = True
                if sent != True:        #after the for, if it is not found then it will just send the emoji as a message instead
                        await message.channel.send(msg)

        if "BRAUM" in message.content.upper().translate(str.maketrans('', '', string.punctuation)).split() or "BRAUMS" in message.content.upper().translate(str.maketrans('', '', string.punctuation)).split():
                if message.author == bot.user:
                        return
                msg = "<:standbehindbraum:457164456846163969>"
                sent = False
                for x in bot.emojis:
                        if x.name == "standbehindbraum":        #adds the reaction if the emoji is found
                                await message.add_reaction(x)
                                sent = True
                if sent != True:        #after the for, if it is not found then it will just send the emoji as a message instead
                        await message.channel.send(msg)

        if "VEL" in message.content.upper().translate(str.maketrans('', '', string.punctuation)).split() or "VELS" in message.content.upper().translate(str.maketrans('', '', string.punctuation)).split() or "KOZ" in message.content.upper().translate(str.maketrans('', '', string.punctuation)).split() or "KOZS" in message.content.upper().translate(str.maketrans('', '', string.punctuation)).split() or "VELKOZ" in message.content.upper().translate(str.maketrans('', '', string.punctuation)).split() or "VELKOZS" in message.content.upper().translate(str.maketrans('', '', string.punctuation)).split():
                if message.author == bot.user:
                        return
                msg = "<:ohdarn:457162626313617438>"
                sent = False
                for x in bot.emojis:
                        if x.name == "ohdarn":        #adds the reaction if the emoji is found
                                await message.add_reaction(x)
                                sent = True
                if sent != True:        #after the for, if it is not found then it will just send the emoji as a message instead
                        await message.channel.send(msg)

        if "AHRI" in message.content.upper().translate(str.maketrans('', '', string.punctuation)).split() or "AHRIS" in message.content.upper().translate(str.maketrans('', '', string.punctuation)).split():
                if message.author == bot.user:
                        return
                msg = "<:ahri:457199789591887872>"
                sent = False
                for x in bot.emojis:
                        if x.name == "ahri":        #adds the reaction if the emoji is found
                                await message.add_reaction(x)
                                sent = True
                if sent != True:        #after the for, if it is not found then it will just send the emoji as a message instead
                        await message.channel.send(msg)

        if "SWAIN" in message.content.upper().translate(str.maketrans('', '', string.punctuation)).split() or "SWAINS" in message.content.upper().translate(str.maketrans('', '', string.punctuation)).split():
                if message.author == bot.user:
                        return
                msg = "<:swain:457212057683492864>"
                sent = False
                for x in bot.emojis:
                        if x.name == "swain":        #adds the reaction if the emoji is found
                                await message.add_reaction(x)
                                sent = True
                if sent != True:        #after the for, if it is not found then it will just send the emoji as a message instead
                        await message.channel.send(msg)

        if "PYKE" in message.content.upper().translate(str.maketrans('', '', string.punctuation)).split() or "PYKES" in message.content.upper().translate(str.maketrans('', '', string.punctuation)).split():
                if message.author == bot.user:
                        return
                msg = "<:pyke:458619798117548042>"
                sent = False
                for x in bot.emojis:
                        if x.name == "pyke":        #adds the reaction if the emoji is found
                                await message.add_reaction(x)
                                sent = True
                if sent != True:        #after the for, if it is not found then it will just send the emoji as a message instead
                        await message.channel.send(msg)
        
        if "YORICK" in message.content.upper().translate(str.maketrans('', '', string.punctuation)).split() or "YORICKS" in message.content.upper().translate(str.maketrans('', '', string.punctuation)).split():
                if message.author == bot.user:
                        return
                msg = "<:yorick:619544222068113408>"
                sent = False
                for x in bot.emojis:
                        if x.name == "yorick":        #adds the reaction if the emoji is found
                                await message.add_reaction(x)
                                sent = True
                if sent != True:        #after the for, if it is not found then it will just send the emoji as a message instead
                        await message.channel.send(msg)

        if "LUX" in message.content.upper().translate(str.maketrans('', '', string.punctuation)).split() or "LUXS" in message.content.upper().translate(str.maketrans('', '', string.punctuation)).split():
                if message.author == bot.user:
                        return
                msg = "<:lux:619545161604792320>"
                sent = False
                for x in bot.emojis:
                        if x.name == "lux":        #adds the reaction if the emoji is found
                                await message.add_reaction(x)
                                sent = True
                if sent != True:        #after the for, if it is not found then it will just send the emoji as a message instead
                        await message.channel.send(msg)
        
        if "NAMI" in message.content.upper().translate(str.maketrans('', '', string.punctuation)).split() or "NAMIS" in message.content.upper().translate(str.maketrans('', '', string.punctuation)).split():
                if message.author == bot.user:
                        return
                msg = "<:nami:619545130566811661>"
                sent = False
                for x in bot.emojis:
                        if x.name == "nami":        #adds the reaction if the emoji is found
                                await message.add_reaction(x)
                                sent = True
                if sent != True:        #after the for, if it is not found then it will just send the emoji as a message instead
                        await message.channel.send(msg)
        
        if "KDA" in message.content.upper().translate(str.maketrans('', '', string.punctuation)).split():
                if message.author == bot.user:
                        return
                msg = "<:KDA:771168104968486962>"
                sent = False
                for x in bot.emojis:
                        if x.name == "KDA":        #adds the reaction if the emoji is found
                                await message.add_reaction(x)
                                sent = True
                if sent != True:        #after the for, if it is not found then it will just send the emoji as a message instead
                        await message.channel.send(msg)

        #Food related reactions
        if "FOOD" in message.channel.name.upper() or "COOKING" in message.channel.name.upper():
                if len(message.attachments) > 0:
                        await message.add_reaction("\U0001F373")
                        await message.add_reaction("\U0001F37D")
                if "MEAT" in message.content.upper():
                        await message.channel.send("https://media.giphy.com/media/w8g5zUCbH215kUjycc/giphy.gif")

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

def getNumberEmote(number):
        switcher = {
                1: "\U0001F534",
                2: "\U0001F7E0",
                3: "\U0001F7E1",
                4: "\U0001F7E2",
                5: "\U0001F535",
                6: "\U0001F7E3",
                7: "\U0001F7E4",
                8: "\U000026AB",
                9: "\U000026AA",
                }
        return switcher.get(number, "INVALID NUMBER")

def get8BallResponse(number):
        switcher = {
                1: "It is Certain.",
                2: "It is decidedly so.",
                3: "Without a doubt.",
                4: "Yes definitely.",
                5: "You may rely on it.",
                6: "As I see it, yes.",
                7: "Most likely.",
                8: "Outlook good.",
                9: "Yes.",
                10: "Signs point to yes.",
                11: "Reply hazy, try again.",
                12: "Ask again later.",
                13: "Better not tell you now.",
                14: "Cannot predict now.",
                15: "Concentrate and ask again.",
                16: "Don't count on it.",
                17: "My reply is no.",
                18: "My sources say no.",
                19: "Outlook not so good.",
                20: "Very doubtful.",
                }
        return switcher.get(number, "INVALID SELECTION")

#Methods
def evaluateFilesExist():
        #make sure that the required text files exist
        #try to open the file. If it cannot be found then create it
        try:
                goodFile = open(os.path.join(__location__, "BotBoiFiles/goodFile.txt"), "r")
                goodFile.close()
        except FileNotFoundError:
                createGoodFile = open(os.path.join(__location__, "BotBoiFiles/goodFile.txt"), "w")
                createGoodFile.write("0")
                createGoodFile.close()
        try:
                badFile = open(os.path.join(__location__, "BotBoiFiles/badFile.txt"), "r")
                badFile.close()
        except FileNotFoundError:
                createBadFile = open(os.path.join(__location__, "BotBoiFiles/badFile.txt"), "w")
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

bot.run(TOKEN)
