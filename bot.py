import discord, asyncio, os, re, json

# Load the settings
f = open("{}/{}".format(os.path.dirname(os.path.realpath(__file__)), "settings.json"))
settings = json.load(f)
f.close()

# This contains all the commands.
# Commands are in the format of:
# "command" : function
command_table = dict()
# Set up hooks. These get called every time something happens.
hook_table = dict()
hook_table["edit"] = list()
hook_table["delete"] = list()
hook_table["message"] = list()

import modules.util, modules.dice, modules.roles, modules.nostalgia, modules.server_config, modules.logging

modules.util.setup_command_table(command_table)
modules.dice.setup_command_table(command_table)
modules.roles.setup_command_table(command_table)
modules.nostalgia.setup_command_table(command_table)
modules.server_config.setup_command_table(command_table)

modules.logging.setup_hooks(hook_table)
modules.server_config.setup_hooks(hook_table)

client = discord.Client()


bot_token = settings["token"].lstrip().rstrip()

help_command = str()
# Loop through, list all the commands
for command in command_table:
    help_command += "{}\n".format(command)

@client.event
async def on_ready():
    print('Successfully logged in as {} (ID {}).'.format(client.user.name, client.user.id))
    await client.change_presence(game=discord.Game(name="Try !help"))

@client.event
async def on_message(message):
    # Check everything against our command table.
    # The modules specify what commands they run - so we just loop through and check

    # Run through all the hooks, these get called every message:
    for hook in hook_table["message"]:
        await hook(client, message)
    
    for command in command_table:
        if re.search("^{}".format(command), message.content):
            await command_table[command](message, client)
    # The exception is !help - this one gets generated automatically
    if re.search("^!help", message.content):
        await client.send_message(message.channel, "{} {}".format(message.author.mention, help_command))

@client.event
async def on_message_edit(old, new):
    for hook in hook_table["edit"]:
        await hook(client, old, new)
    
@client.event
async def on_message_delete(message):
    for hook in hook_table["delete"]:
        await hook(client, message)

try:
    # If any background tasks need to run, start them here
    client.run(bot_token)
except KeyboardInterrupt:
    # Properly exit if we get a Ctrl-C
    client.logout()
finally:
    # If anything needs to save, do it here
    print("Done running.")
