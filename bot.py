import discord, asyncio, os, re

# This contains all the commands.
# Commands are in the format of:
# "command" : function
command_table = dict()

import modules.util, modules.dice, modules.roles

modules.util.setup_command_table(command_table)

print(command_table)

client = discord.Client()

f = open("{}/{}".format(os.path.dirname(os.path.realpath(__file__)), "token"))
# Discord tokens have no whitespace, remove any that might've slipped in there
bot_token = f.read().rstrip().lstrip()
f.close()

@client.event
async def on_ready():
    print('Successfully logged in as {} (ID {}).'.format(client.user.name, client.user.id))

@client.event
async def on_message(message):
    for command in command_table:
        if re.search("^{}".format(command), message.content):
            await command_table[command](message, client)
    # Dice
    if re.search("^!roll", message.content):
        await modules.dice.roll(message, client)
    if re.search("^!8ball", message.content):
        await modules.dice.magic_eight_ball(message, client)
    # Role Management
    if re.search("^!giverole", message.content):
        await modules.roles.give_role(message, client)
    if re.search("^!removerole", message.content):
        await modules.roles.remove_role(message, client)
    if re.search("^!listroles", message.content):
        await modules.roles.list_roles(message, client)

try:
    # If any background tasks need to run, start them here
    client.run(bot_token)
except KeyboardInterrupt:
    # Properly exit if we get a Ctrl-C
    client.logout()
finally:
    # If anything needs to save, do it here
    print("Done running.")
