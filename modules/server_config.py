# settings.py
# Allows admins of a server to configure the bot.
import discord, asyncio

admin_role_name = "EfficientEnigma Admin"

async def check_if_can_edit(user, message, client):
    found_admin = False
    for r in message.server.roles:
        if r.name == admin_role_name:
            found_admin = True

    if not found_admin:
         await client.send_message(message.channel, "{} It looks like the admin role *doesn't exist* - if you are not able to add one, please tell the server manager to add a role named \"{}\" and assign it to whoever needs it.".format(message.author.mention, admin_role_name))
         return False

    result = discord.utils.get(message.server.roles, name=admin_role_name) in user.roles
    return result

async def check_and_return(message, client):
    result = await check_if_can_edit(message.author, message, client)
    await client.send_message(message.channel, "{} Have role for editing: {}".format(message.author.mention, result))

# Add the commands to the global command table.
def setup_command_table(table):
    table["\\$check"] = check_and_return