import discord
from discord import app_commands
import json
import datetime
import logging
import random
import string
import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

with open(os.path.join(__location__, 'config.json')) as config_file:
        data = json.load(config_file)

TOKEN = data["token"]

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents = intents)

commandTree = discord.app_commands.CommandTree(client = client)

logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
handler =logging.FileHandler(filename=os.path.join(__location__, "BotBoiFiles/botLog.log"), encoding="utf-8",mode="w")
handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
logger.addHandler(handler)

@client.event
async def on_ready():
        print("\nLogged in as {0.user}\n".format(client))
        await client.change_presence(activity = discord.Activity(type = discord.ActivityType.listening, name = "slash commands"))
        await commandTree.sync()
        numberOfServers = len(client.guilds)
        print("Connected to " + str(numberOfServers) + " servers")
        print("------\n")

# Commands
@commandTree.command(name="hellobotboi", description="Botboi greets you!")
async def hellobotboi(interaction: discord.Interaction):
        await interaction.response.send_message(f"Hello {interaction.user.mention}")

@commandTree.command(name="hellothere", description="You are a bold one!")
async def hellothere(interaction: discord.Interaction):
        await interaction.response.send_message("General Kenobi!")
        
@commandTree.command(name="wednesday", description="Give this a try on a Wednesday...")
async def wednesday(interaction: discord.Interaction):
        weekday = datetime.datetime.today().weekday()
        if weekday == 2:#monday=0 -> sunday=6
                await interaction.response.send_message(file = discord.File(fp = os.path.join(__location__, 'BotBoiFiles/ITSWEDNESDAY.jpg'), filename = 'WednesdayFrog.jpg'))
        else:
                await interaction.response.send_message("It is not Wednesday...\nIt is " + getDayName(weekday) + " my dudes!")

@commandTree.command(name="goodbot", description="Increments Botboi's good counter.")
async def goodbot(interaction: discord.Interaction):
        await interaction.response.send_message(":blush:")

        #increment the good counter
        evaluateFilesExist()
        goodFile = os.path.join(__location__, "BotBoiFiles/goodFile.txt")
        readAndWriteToFile(goodFile)

@commandTree.command(name="badbot", description="Increments Botboi's bad counter.")
async def badbot(interaction: discord.Interaction):
        await interaction.response.send_message(":sob:")

        #increment the bad counter
        evaluateFilesExist()
        badFile = os.path.join(__location__, "BotBoiFiles/badFile.txt")
        readAndWriteToFile(badFile)

@commandTree.command(name="evaluate", description="Returns the results of using goodbot and badbot commands.")
@app_commands.describe(numbers="[Optional] Whether to include the exact numbers in the response.")
async def evaluate(interaction: discord.Interaction, numbers: bool = False):
        evaluateFilesExist()
        goodFile = open(os.path.join(__location__, "BotBoiFiles/goodFile.txt"), "r")
        goodCount = int(goodFile.read())
        badFile = open(os.path.join(__location__, "BotBoiFiles/badFile.txt"), "r")
        badCount = int(badFile.read())
        percent = (goodCount / (float(goodCount + badCount))) * 100
        msgReturn = "The results show that I am " + str(round(percent, 2)) + "% good!"
        if numbers:
                msgReturn += "\nGood votes: " + str(goodCount) + "\nBad votes: " + str(badCount)
        
        em = discord.Embed(title="Evaluation", description=msgReturn, colour=0x800020)
        await interaction.response.send_message(embed=em)

@commandTree.command(name="birthday", description="Send a birthday message from Botboi.")
@app_commands.describe(member="[Optional] User to mention")
async def birthday(interaction: discord.Interaction, member: discord.Member = None):
        msg = "Happy Birthday"
        if member != None:
                msg += " " + member.mention
        msg += "!\nhttp://i.imgur.com/P1vH64S.gif"
        await interaction.response.send_message(msg)

@commandTree.command(name="servercount", description="Returns the number of servers that Botboi is currently connected to.")
async def servercount(interaction: discord.Interaction):
        em = discord.Embed(title="Server Count", description="Currently connected to " + str(len(client.guilds)) + " servers!", colour=0x800020)
        await interaction.response.send_message(embed=em)

@commandTree.command(name="roll", description="Rolls a die.")
@app_commands.describe(sides="The number of sides on the die.")
async def roll(interaction: discord.Interaction, sides: int):
        result = random.randint(1,sides)
        em = discord.Embed(title="", description="Rolled a d" + str(sides) + "...\n\nThe result is: **" + str(result) + "**", colour=0x800020)
        await interaction.response.send_message(embed=em)

@commandTree.command(name="coinflip", description="Flip a coin.")
async def coinflip(interaction: discord.Interaction):
        result = random.randint(1,2)
        resultString: str = ""
        if result == 1:
                resultString = "heads!"
        else:
                resultString = "tails!"
        em = discord.Embed(title="", description="The result is: **" + resultString + "**", colour=0x800020)
        await interaction.response.send_message(embed=em)

@commandTree.command(name="poll", description="Create a poll for users to vote on.")
@app_commands.describe(
        question="Poll question.",
        option1="Poll option 1.",
        option2="Poll option 2.",
        option3="[Optional] Poll option 3.",
        option4="[Optional] Poll option 4.",
        option5="[Optional] Poll option 5.",
        option6="[Optional] Poll option 6.",
        option7="[Optional] Poll option 7.",
        option8="[Optional] Poll option 8.",
        option9="[Optional] Poll option 9."
)
async def poll(interaction: discord.Interaction, question: str, option1: str, option2: str, option3: str = None, option4: str = None, option5: str = None, option6: str = None, option7: str = None, option8: str = None, option9: str = None):
        if question == None or question == "":
                await interaction.response.send_message("Please provide a question for your poll.")
                return
        if (option1 == None or option1 == "") or (option2 == None or option2 == ""):
                await interaction.response.send_message("Please provide at least two options for your poll.")
                return
        optionsString = getNumberEmote(1) + ": " + option1 + "\n"
        optionsString += getNumberEmote(2) + ": " + option2 + "\n"
        optionsCount = 2
        if (option3 != None and option3 != ""):
                optionsCount += 1
                optionsString += getNumberEmote(optionsCount) + ": " + option3 + "\n"
        if (option4 != None and option4 != ""):
                optionsCount += 1
                optionsString += getNumberEmote(optionsCount) + ": " + option4 + "\n"
        if (option5 != None and option5 != ""):
                optionsCount += 1
                optionsString += getNumberEmote(optionsCount) + ": " + option5 + "\n"
        if (option6 != None and option6 != ""):
                optionsCount += 1
                optionsString += getNumberEmote(optionsCount) + ": " + option6 + "\n"
        if (option7 != None and option7 != ""):
                optionsCount += 1
                optionsString += getNumberEmote(optionsCount) + ": " + option7 + "\n"
        if (option8 != None and option8 != ""):
                optionsCount += 1
                optionsString += getNumberEmote(optionsCount) + ": " + option8 + "\n"
        if (option9 != None and option9 != ""):
                optionsCount += 1
                optionsString += getNumberEmote(optionsCount) + ": " + option9 + "\n"
        
        em = discord.Embed(title=question, description=optionsString, colour=0x800020)
        await interaction.response.send_message(embed=em)
        botmessage = await interaction.original_response()

        # Add the reactions which users can vote with
        for i in range(optionsCount+1):
                if i > 0:
                     await botmessage.add_reaction(getNumberEmote(i))

@commandTree.command(name="eightball", description="Ask the Magic 8-Ball a question.")
@app_commands.describe(question="Question to ask the Magic 8-Ball.")
async def eightball(interaction: discord.Interaction, question: str):
        if len(question) == 0:
                await interaction.response.send_message("You need to ask the Magic 8-Ball a question.")
                return
        response = get8BallResponse(random.randint(1,20))
        em = discord.Embed(title="", description="\U0001F464 *" + question + "*\n\U0001F3B1 " + response, colour=0x800020)
        await interaction.response.send_message(embed=em)

@commandTree.command(name="github", description="Returns the link to the Botboi Github repository.")
async def github(interaction: discord.Interaction):
        link: str = "https://github.com/Trogz64/botboi"
        em = discord.Embed(title="Botboi Github", description=link, colour=0x800020)
        await interaction.response.send_message(view=LinkButtons(link, em, "Visit GitHub"))

@commandTree.command(name="invite", description="Returns an invite link for Botboi.")
async def invite(interaction: discord.Interaction):
        inviteLink: str = "https://discord.com/api/oauth2/authorize?client_id=416406487024402432&permissions=414464863296&scope=applications.commands%20bot"
        em = discord.Embed(title="Botboi Invite Link", description="Use this link to invite me to your servers!\n" + inviteLink, colour=0x800020)
        await interaction.response.send_message(view=LinkButtons(inviteLink, em, "Add Botboi"))

class LinkButtons(discord.ui.View):
        def __init__(self, inv: str, em: discord.Embed, linkLabel: str):
                super().__init__()
                self.inv = inv
                self.em = em
                self.linkLabel = linkLabel
                self.add_item(discord.ui.Button(label=self.linkLabel, url=self.inv))
        
        @discord.ui.button(label="View link", style=discord.ButtonStyle.blurple)
        async def viewLinkBtn(self, interaction: discord.Interaction, button: discord.ui.Button):
                await interaction.response.send_message(embed=self.em, ephemeral=True)


# Reactions to messages
@client.event
async def on_message(message):
        # Uncomment to stop the bot from reacting to itself. Currently handled under individual responses.
        # if message.author == client.user:
        #         return

        #reaction to an @everyone
        if message.mention_everyone:
                msg = "<:pingsock:522894414356414475>"
                sent = False
                for x in client.emojis:
                        if x.name == "pingsock":        #adds the reaction if the emoji is found
                                await message.add_reaction(x)
                                sent = True
                if sent != True:        #after the for, if it is not found then it will just send the emoji as a message instead
                        await message.channel.send(msg)

        #Wave reaction to mention
        if client.user in message.mentions:
                emoji = "\U0001F44B"
                await message.add_reaction(emoji)

        #Special reactions
        if "ALEXA" in message.content.upper().translate(str.maketrans('', '', string.punctuation)).split():
                if message.author != client.user:
                        playIndex = message.content.upper().find("PLAY")
                        if(playIndex > 0):
                                msg = "**NOW PLAYING: **" + message.content[playIndex+5:len(message.content)] + " ~~-----~~o~~--------~~ :rewind: :pause_button: :fast_forward: 0:02/4:20"
                        else:
                                msg = "I'm SoRrY, I dIdN't UnDeRsTaNd YoUr QuEsTiOn..."
                        await message.channel.send(msg)

        if message.content == "F":
                if message.author != client.user:
                        await message.channel.send("F")

        if message.content == "f":
                if message.author != client.user:
                        await message.channel.send("f")

        #League emotes
        #We need to make sure that the intended trigger is a word in itself, and not a substring in a different word
        if "BARD" in message.content.upper().translate(str.maketrans('', '', string.punctuation)).split() or "BARDS" in message.content.upper().translate(str.maketrans('', '', string.punctuation)).split():
                if message.author != client.user:
                        msg = "<:ootay:456893214880825354>"
                        sent = False
                        for x in client.emojis:
                                if x.name == "ootay":        #adds the reaction if the emoji is found
                                        await message.add_reaction(x)
                                        sent = True
                        if sent != True:        #after the for, if it is not found then it will just send the emoji as a message instead
                                await message.channel.send(msg)

        if "MEEP" in message.content.upper().translate(str.maketrans('', '', string.punctuation)).split() or "MEEPS" in message.content.upper().translate(str.maketrans('', '', string.punctuation)).split():
                if message.author != client.user:
                        msg = "<:meep:797893845819457567>"
                        sent = False
                        for x in client.emojis:
                                if x.name == "meep":        #adds the reaction if the emoji is found
                                        await message.add_reaction(x)
                                        sent = True
                        if sent != True:        #after the for, if it is not found then it will just send the emoji as a message instead
                                await message.channel.send(msg)

        if "BRAUM" in message.content.upper().translate(str.maketrans('', '', string.punctuation)).split() or "BRAUMS" in message.content.upper().translate(str.maketrans('', '', string.punctuation)).split():
                if message.author != client.user:
                        msg = "<:standbehindbraum:457164456846163969>"
                        sent = False
                        for x in client.emojis:
                                if x.name == "standbehindbraum":        #adds the reaction if the emoji is found
                                        await message.add_reaction(x)
                                        sent = True
                        if sent != True:        #after the for, if it is not found then it will just send the emoji as a message instead
                                await message.channel.send(msg)

        if "VEL" in message.content.upper().translate(str.maketrans('', '', string.punctuation)).split() or "VELS" in message.content.upper().translate(str.maketrans('', '', string.punctuation)).split() or "KOZ" in message.content.upper().translate(str.maketrans('', '', string.punctuation)).split() or "KOZS" in message.content.upper().translate(str.maketrans('', '', string.punctuation)).split() or "VELKOZ" in message.content.upper().translate(str.maketrans('', '', string.punctuation)).split() or "VELKOZS" in message.content.upper().translate(str.maketrans('', '', string.punctuation)).split():
                if message.author != client.user:
                        msg = "<:ohdarn:457162626313617438>"
                        sent = False
                        for x in client.emojis:
                                if x.name == "ohdarn":        #adds the reaction if the emoji is found
                                        await message.add_reaction(x)
                                        sent = True
                        if sent != True:        #after the for, if it is not found then it will just send the emoji as a message instead
                                await message.channel.send(msg)

        if "AHRI" in message.content.upper().translate(str.maketrans('', '', string.punctuation)).split() or "AHRIS" in message.content.upper().translate(str.maketrans('', '', string.punctuation)).split():
                if message.author != client.user:
                        msg = "<:ahri:457199789591887872>"
                        sent = False
                        for x in client.emojis:
                                if x.name == "ahri":        #adds the reaction if the emoji is found
                                        await message.add_reaction(x)
                                        sent = True
                        if sent != True:        #after the for, if it is not found then it will just send the emoji as a message instead
                                await message.channel.send(msg)

        if "SWAIN" in message.content.upper().translate(str.maketrans('', '', string.punctuation)).split() or "SWAINS" in message.content.upper().translate(str.maketrans('', '', string.punctuation)).split():
                if message.author != client.user:
                        msg = "<:swain:457212057683492864>"
                        sent = False
                        for x in client.emojis:
                                if x.name == "swain":        #adds the reaction if the emoji is found
                                        await message.add_reaction(x)
                                        sent = True
                        if sent != True:        #after the for, if it is not found then it will just send the emoji as a message instead
                                await message.channel.send(msg)

        if "PYKE" in message.content.upper().translate(str.maketrans('', '', string.punctuation)).split() or "PYKES" in message.content.upper().translate(str.maketrans('', '', string.punctuation)).split():
                if message.author != client.user:
                        msg = "<:pyke:458619798117548042>"
                        sent = False
                        for x in client.emojis:
                                if x.name == "pyke":        #adds the reaction if the emoji is found
                                        await message.add_reaction(x)
                                        sent = True
                        if sent != True:        #after the for, if it is not found then it will just send the emoji as a message instead
                                await message.channel.send(msg)
        
        if "YORICK" in message.content.upper().translate(str.maketrans('', '', string.punctuation)).split() or "YORICKS" in message.content.upper().translate(str.maketrans('', '', string.punctuation)).split():
                if message.author != client.user:
                        msg = "<:yorick:619544222068113408>"
                        sent = False
                        for x in client.emojis:
                                if x.name == "yorick":        #adds the reaction if the emoji is found
                                        await message.add_reaction(x)
                                        sent = True
                        if sent != True:        #after the for, if it is not found then it will just send the emoji as a message instead
                                await message.channel.send(msg)

        if "LUX" in message.content.upper().translate(str.maketrans('', '', string.punctuation)).split() or "LUXS" in message.content.upper().translate(str.maketrans('', '', string.punctuation)).split():
                if message.author != client.user:
                        msg = "<:lux:619545161604792320>"
                        sent = False
                        for x in client.emojis:
                                if x.name == "lux":        #adds the reaction if the emoji is found
                                        await message.add_reaction(x)
                                        sent = True
                        if sent != True:        #after the for, if it is not found then it will just send the emoji as a message instead
                                await message.channel.send(msg)
        
        if "NAMI" in message.content.upper().translate(str.maketrans('', '', string.punctuation)).split() or "NAMIS" in message.content.upper().translate(str.maketrans('', '', string.punctuation)).split():
                if message.author != client.user:
                        msg = "<:nami:619545130566811661>"
                        sent = False
                        for x in client.emojis:
                                if x.name == "nami":        #adds the reaction if the emoji is found
                                        await message.add_reaction(x)
                                        sent = True
                        if sent != True:        #after the for, if it is not found then it will just send the emoji as a message instead
                                await message.channel.send(msg)
        
        if "KDA" in message.content.upper().translate(str.maketrans('', '', string.punctuation)).split():
                if message.author != client.user:
                        msg = "<:KDA:771168104968486962>"
                        sent = False
                        for x in client.emojis:
                                if x.name == "KDA":        #adds the reaction if the emoji is found
                                        await message.add_reaction(x)
                                        sent = True
                        if sent != True:        #after the for, if it is not found then it will just send the emoji as a message instead
                                await message.channel.send(msg)

        #Food related reactions
        #DMChannel does not have name attribute so these should not be checked 
        if isinstance(message.channel, discord.DMChannel):
                return
        else:
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

client.run(TOKEN)
