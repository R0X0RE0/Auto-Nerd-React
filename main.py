import discord
import random

# import slash command functionality
from discord import app_commands

import processcsv as pcsv

import os

intents = discord.Intents.default()
intents.message_content = True
token = open("bottoken.txt").read()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

helpText = open("help.txt").read()
serverInvite = "https://discord.com/api/oauth2/authorize?client_id=1026651311233572884&permissions=67648&scope=applications.commands%20bot"

# globalList = [
#     # general terms
#     "ackchually","arcane","nerd","you leveled up","gay","ackshually","dibs",
    
#     # linux related
#     "linux","debian","ubuntu","gentoo","lfs","i3","dwm","kde","lxde","xfce","pop!_os","asahi",
    
#     # programming
#     "c++","c#","python","java","perl","lua","toml","xml","js","css","rustlang","golang","lua",
    
#     # text editors
#     "vim","emacs","notepad++","visual studio","eclipse",
    
#     # crypto related
#     "monero","crypto","bitcoin","nft","ethereum",

#     # music related
#     "fantano","weezer","radiohead","tally hall",

#     # STEM related
#     "arduino","rpi","raspberry pi","segment display","dot matrix","hexadecimal","logic gate","binary","dozenal","ternary operator","redstone",

#     # slang
#     "rizz","mid","fell off"
#     ]
nerdList = pcsv.csv2arr("globallists\\nerd.csv")
cornDogList = pcsv.csv2arr("globallists\\corndog.csv")
blacklist = pcsv.csv2arr("globallists\\blacklist.csv")
# disabledChannels = [543136681180659722]

nerdReactList = [u"\U0001f913", "<:nerdreactbotemote:1057685886634045460>"]
blacklistEmoji = u"\U0000274c"
cornDogReact = ":corndog:1058392601872576624"

async def reaction(strList, reactEmote, prompt, message: discord.Message):
    noReact = False
    for i in strList:
        for j in i:
            if j in message.content.lower():
                for row in blacklist:
                    for column in row:
                        if column in message.content.lower():
                            print("^^ blacklisted word detected! this message is immune\n")
                            noReact = True
                            break
                if noReact == True: break
                else:
                    print(prompt)
                    await message.add_reaction(reactEmote)
                    break

def listItems(strList, emote, strIn: str):
    strOut = strIn
    newEmote = emote
    if ':' in newEmote:
        newEmote = "<" + emote + ">"
    strOut += newEmote + ": \n"
    for i in strList:
                for j in i:
                    strOut += (strOut == "" if "" else ", ") + j
    strOut += "\n\n"
    return strOut

# slash commands
# /help
@tree.command(name = "help", description = "sends a message containing documentation on how to use the bot")
async def helpCommand(interaction):
    await interaction.response.send_message(helpText)

# /help
@tree.command(name = "invite", description = "sends a link so that you can invite the bot to your guild")
async def helpCommand(interaction):
    message = "Add me to your server using this link\n"+serverInvite
    await interaction.response.send_message(message)

# /globaltriggers
@tree.command(name = "globaltriggers", description = "list global triggers activated by the bot")
async def globaltriggers(interaction):
    listOfItems = ""
    listOfItems = listItems(nerdList, nerdReactList[0], listOfItems)
    listOfItems = listItems(cornDogList, cornDogReact, listOfItems)
    listOfItems = listItems(blacklist, blacklistEmoji, listOfItems)
    await interaction.response.send_message(listOfItems)

# /disablebot [channel]
# @tree.command(name = "disablebot", description = "list global triggers activated by the bot")
# async def disablebot(interaction, channelid: int):
#     disabledChannels.append(channelid)
#     # channelName = "<#" + str(discord.Guild.get_channel(channelid)) + ">"
#     await interaction.response.send_message(f"Successfully disabled bot in {channelid}")

# client events
@client.event
async def on_ready():
    await tree.sync()
    print(f'{client.user} is on Discord')

@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    usrMessage = str(message.content)
    channel = str(message.channel.name)
    channelid = str(message.channel.id)
    print(f'{username} has sent a message in {channel} : {usrMessage}')

    # don't read messages sent from bots
    if message.author == client.user:
        return
    
    # don't read messages in disabled channels
    # for i in disabledChannels:
    #     if message.channel.id == i:
    #         return

    # prefix commands
    botPrefix = "nerd."

    sendList = "globaltriggers"

    await reaction(nerdList, nerdReactList[0], "^^ this message has been nerd reacted\n", message)
    await reaction(cornDogList, cornDogReact, "^^ corn dogs!\n", message)
    

    if message.content.lower().startswith(botPrefix):
        # global triggers
        if message.content.lower().endswith(sendList):
            listOfItems = ""
            listOfItems = listItems(nerdList, nerdReactList[0], listOfItems)
            listOfItems = listItems(cornDogList, cornDogReact, listOfItems)
            listOfItems = listItems(blacklist, blacklistEmoji, listOfItems)
            await message.channel.send(listOfItems)
        # help
        elif message.content.lower().endswith("help"):
            await message.channel.send(helpText)
        # invite
        elif message.content.lower().endswith("invite"):
            messageInvite = "Add me to your server using this link\n"+serverInvite
            await message.channel.send(messageInvite)

client.run(token)