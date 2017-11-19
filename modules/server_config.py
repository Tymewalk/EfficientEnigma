# settings.py
# Allows admins of a server to configure the bot.
import discord, asyncio

async def check_if_can_edit(user, message, client):
    result = discord.utils.get(message.server.roles, name="EfficientEnigma Admin") in user_roles
    return result

async def check_and_return(message, client):
    result = await check_if_can_edit(message.author, message, client)
    await client.send_message(message.channel, "{} Have role for editing: {}".format(message.author.mention, result))

# Add the commands to the global command table.
def setup_command_table(table):
    table["\\$check"] = check_and_return