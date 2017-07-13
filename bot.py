import discord, asyncio, os, re

# This contains all the commands.
# Commands are in the format of:
# "command" : function
command_table = dict()

import modules.util, modules.dice, modules.roles

modules.util.setup_command_table(command_table)
modules.dice.setup_command_table(command_table)
modules.roles.setup_command_table(command_table)

client = discord.Client()

f = open("{}/{}".format(os.path.dirname(os.path.realpath(__file__)), "token"))
# Discord tokens have no whitespace, remove any that might've slipped in there
bot_token = f.read().rstrip().lstrip()
f.close()

help_command = str()
# Loop through, list all the commands
for command in command_table:
    help_command += "{}, ".format(command)

# Remove the final ", "
help_command = help_command[:-2]

@client.event
async def on_ready():
    print('Successfully logged in as {} (ID {}).'.format(client.user.name, client.user.id))

@client.event
async def on_message(message):
    # Check everything against our command table.
    # The modules specify what commands they run - so we just loop through and check
    for command in command_table:
        if re.search("^{}".format(command), message.content):
            await command_table[command](message, client)
    # The exception is !help - this one gets generated automatically
    if re.search("^!help", message.content):
        await client.send_message(message.channel, "{} {}".format(message.author.mention, help_command))

try:
    # If any background tasks need to run, start them here
    client.run(bot_token)
except KeyboardInterrupt:
    # Properly exit if we get a Ctrl-C
    client.logout()
finally:
    # If anything needs to save, do it here
    print("Done running.")
