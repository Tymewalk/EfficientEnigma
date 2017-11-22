# settings.py
# Allows admins of a server to configure the bot.
import discord, asyncio, json, os, re

# This should be hardcoded - that way it's the same across all servers.
# Might change in the future if necessary.
admin_role_name = "EfficientEnigma Admin"

settings = dict()

def load_settings():
    # Load the settings.
    global settings
    f = open("{}/{}".format(os.path.dirname(os.path.realpath(__file__)), "../settings.json"), 'r')
    settings = json.load(f)
    f.close()

def save_settings(in_settings):
    # Save the settings.
    f = open("{}/{}".format(os.path.dirname(os.path.realpath(__file__)), "../settings.json"), 'w')
    json.dump(in_settings, f)
    f.close()

def server_has_settings(in_settings, message):
    # Check if the server has settings - if not, just create a new table for them.
    if not message.server.id in in_settings:
        in_settings[message.server.id] = dict()
    return in_settings

async def check_if_can_edit(user, message, client):
    # Does this user have permission to change admin stuff?
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
    # DEBUG/TEST COMMAND - Checks if a user can edit, and tells them.
    result = await check_if_can_edit(message.author, message, client)
    await client.send_message(message.channel, "{} Have role for editing: {}".format(message.author.mention, result))

async def toggle_logs(message, client):
    # Toggles logs, simple as that.
    global settings
    load_settings()
    settings = server_has_settings(settings, message)
    if not "use_logging" in settings[message.server.id]:
        settings[message.server.id]["use_logging"] = True
        settings[message.server.id]["log_channel"] = "modlog"
    settings[message.server.id]["use_logging"] = not settings[message.server.id]["use_logging"]
    await client.send_message(message.channel, "{} Logging set to {}".format(message.author.mention, settings[message.server.id]["use_logging"]))
    save_settings(settings)

async def set_log_channel(message, client):
    global settings
    if re.findall("<#[0-9]+>", message.content):
        # Get the name of the channel - that should be all we need
        log_channel = message.server.get_channel(re.sub("[\<\#\>]", "", re.findall("<#[0-9]+>", message.content)[0])).name
    else:
        await client.send_message(message.channel, "{} Please specify a logging channel by typing `#name_of_channel`.")
        return False
    
    load_settings()
    settings = server_has_settings(settings, message)
    if not "log_channel" in settings[message.server.id]:
        settings[message.server.id]["use_logging"] = True
    settings[message.server.id]["log_channel"] = log_channel
    await client.send_message(message.channel, "{} Log channel set to {}".format(message.author.mention, settings[message.server.id]["log_channel"]))
    save_settings(settings)

# Add the commands to the global command table.
def setup_command_table(table):
    table["\\$check"] = check_and_return
    table["\\$logtoggle"] = toggle_logs
    table["\\$logchannel"] = set_log_channel