# bot.py
# Houses the main code that the modules run off of.
import discord, asyncio, os, re, json

# Load the settings - we need this for the token
f = open("{}/{}".format(os.path.dirname(os.path.realpath(__file__)), "settings.json"))
settings = json.load(f)
f.close()

# This contains all the commands.
# Commands are in the format of ("command" : function) in the table.
command_table = dict()
# Set up hooks. These get called every time something happens.
hook_table = dict()
hook_table["edit"] = list()
hook_table["delete"] = list()
hook_table["message"] = list()
hook_table["reaction_add"] = list()
hook_table["reaction_remove"] = list()
# This is the help table - it controls all the help descriptions.
help_table = dict()

import modules.util, modules.dice, modules.roles, modules.nostalgia, modules.server_config, modules.messagelog, modules.stars

# Set up command tables
# Most of them also get a help table passed in, to set up the help descriptions
modules.util.setup_command_table(command_table, help_table)
modules.dice.setup_command_table(command_table, help_table)
modules.roles.setup_command_table(command_table, help_table)
modules.nostalgia.setup_command_table(command_table, help_table)
modules.server_config.setup_command_table(command_table)

# Set up hook tables
modules.messagelog.setup_hooks(hook_table)
modules.server_config.setup_hooks(hook_table)
modules.stars.setup_hooks(hook_table)

client = discord.Client()

bot_token = settings["token"].lstrip().rstrip()

help_command = str()
# Loop through, list all the commands
for command in help_table:
    help_command += "{} - {}\n".format(command, help_table[command])

@client.event
async def on_ready():
    print('Successfully logged in as {} (ID {}).'.format(client.user.name, client.user.id))
    await client.change_presence(game=discord.Game(name="Try !help"))

@client.event
async def on_message(message):
    if message.author.bot and not message.author == client.user: #make sure it doesn't respond to other bots
        return
    # Run through all the hooks, these get called every message:
    for hook in hook_table["message"]:
        await hook(client, message)

    # Check everything against our command table.
    # The modules specify what commands they run - so we just loop through and check    
    for command in command_table:
        if re.search("^{}".format(command), message.content):
            await command_table[command](message, client)

    # The exception is !help - this one gets generated automatically above
    if re.search("^!help", message.content):
        await client.send_message(message.channel, "{} {}".format(message.author.mention, help_command))

@client.event
async def on_message_edit(old, new):
    # Since this doesn't have one message just pick the old one for checking
    if old.author.bot and not old.author == client.user: #make sure it doesn't respond to other bots
        return
    # Run through anything that needs to be done on message edits.
    for hook in hook_table["edit"]:
        await hook(client, old, new)
    
@client.event
async def on_message_delete(message):
    if message.author.bot and not message.author == client.user: #make sure it doesn't respond to other bots
        return
    # Run through anything that needs to be done on message deletions.
    for hook in hook_table["delete"]:
        await hook(client, message)

@client.event
async def on_reaction_add(reaction, user):
    # Run through anything that needs to be done on reactions being added.
    for hook in hook_table["reaction_add"]:
        await hook(client, reaction, user)

@client.event
async def on_reaction_remove(reaction, user):
    # Run through anything that needs to be done on reactions being deleted.
    for hook in hook_table["reaction_remove"]:
        await hook(client, reaction, user)

try:
    # If any background tasks need to run, start them here.
    client.run(bot_token)
except KeyboardInterrupt:
    # Properly exit if we get a Ctrl-C
    # Also apparently works if the code crashes for some reason.
    client.logout()
finally:
    # If anything needs to save, do it here
    # Saving settings doesn't need to be done because anything modifying them automatically saves.
    print("EfficientEnigma is done running.")
