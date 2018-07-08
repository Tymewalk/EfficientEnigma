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

def is_in_server(message):
    # Check if we're in a server.
    return message.server is not None

async def check_if_can_edit(user, message, client):
    # Does this user have permission to change admin stuff?
    # We need a message so we can properly check if they can.
    found_admin = False
    for r in message.server.roles:
        if r.name == admin_role_name:
            found_admin = True

    if not found_admin:
         await client.send_message(message.channel, "{} It looks like the admin role *doesn't exist* - if you are not able to add one, please tell the server manager to add a role named \"{}\" and assign it to whoever needs it.".format(message.author.mention, admin_role_name))
         return False

    result = discord.utils.get(message.server.roles, name=admin_role_name) in user.roles
    return result
    
async def toggle_logs(message, client):
    if is_in_server(message):
        # Toggles logs on and off, simple as that.
        global settings
        is_admin = await check_if_can_edit(message.author, message, client)
        if is_admin:
            load_settings()
            settings = server_has_settings(settings, message)
            if not "use_logging" in settings[message.server.id]:
                settings[message.server.id]["use_logging"] = True
                settings[message.server.id]["log_channel"] = "modlog"
            if re.search("on$", message.content.rstrip()):
                settings[message.server.id]["use_logging"] = True
                await client.send_message(message.channel, "{} Logging enabled. Messages will be logged in {}".format(message.author.mention, settings[message.server.id]["log_channel"]))
            elif re.search("off$", message.content.rstrip()):
                settings[message.server.id]["use_logging"] = False
                await client.send_message(message.channel, "{} Logging disabled.".format(message.author.mention))
            else:
                await client.send_message(message.channel, "{} Sorry, you need to specify \"on\" or \"off\"!".format(message.author.mention))
            
            save_settings(settings)
        else:
            await client.send_message(message.channel, "{} Sorry, you don't have permission to edit settings.".format(message.author.mention))
    else:
        await client.send_message(message.channel, "{} You need to be in a server to use this command.".format(message.author.mention))

async def set_log_channel(message, client):
    # Set the channel to log edits and deletions in.
    if is_in_server(message):
        global settings
        is_admin = await check_if_can_edit(message.author, message, client)
        if is_admin:
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
            save_settings(settings)
            await client.send_message(message.channel, "{} Log channel set to {}".format(message.author.mention, settings[message.server.id]["log_channel"]))
        else:
            await client.send_message(message.channel, "{} Sorry, you don't have permission to edit settings.".format(message.author.mention))
    else:
        await client.send_message(message.channel, "{} You need to be in a server to use this command.".format(message.author.mention))

async def allow_role(message, client):
    if is_in_server(message):
        global settings
        is_admin = await check_if_can_edit(message.author, message, client)
        if is_admin:
            load_settings()
            new_settings = server_has_settings(settings, message)
            if not "allowed_roles" in new_settings[message.server.id]:
                new_settings[message.server.id]["allowed_roles"] = []
            if re.match("^\$[^\W]+( |)+$", message.content):
                # Don't do anything if it's all whitespace
                await client.send_message(message.channel, ":warning: Sorry, you forgot to specify a role.")
                return
            role_name = re.sub("^\$[^\W]+ ", "", message.content)
            if role_name in new_settings[message.server.id]["allowed_roles"]:
                await client.send_message(message.channel, ":warning: The role \"{}\" is already allowed to be self-assigned.".format(role_name))
            else:
                new_settings[message.server.id]["allowed_roles"].append(role_name)
                await client.send_message(message.channel, ":white_check_mark: The role \"{}\" can now be self-assigned by members.".format(role_name))
                save_settings(new_settings)
                
        else:
            await client.send_message(message.channel, "{} Sorry, you don't have permission to edit settings.".format(message.author.mention))
    else:
        await client.send_message(message.channel, "{} You need to be in a server to use this command.".format(message.author.mention))

async def forbid_role(message, client):
    if is_in_server(message):
        global settings
        is_admin = await check_if_can_edit(message.author, message, client)
        if is_admin:
            load_settings()
            new_settings = server_has_settings(settings, message)
            if not "allowed_roles" in settings[message.server.id]:
                new_settings[message.server.id]["allowed_roles"] = []
            if re.match("^\\\$[^\W]+( |)+$", message.content):
                # Don't do anything if it's all whitespace
                await client.send_message(message.channel, ":warning: Sorry, you forgot to specify a role.")
                return
            role_name = re.sub("^\$[^\W]+ ", "", message.content)
            if not role_name in new_settings[message.server.id]["allowed_roles"]:
                await client.send_message(message.channel, ":warning: The role \"{}\" is already not allowed to be self-assigned.".format(role_name))
            else:
                new_settings[message.server.id]["allowed_roles"].remove(role_name)
                await client.send_message(message.channel, ":white_check_mark: The role \"{}\" can no longer be self-assigned by members.".format(role_name))
                save_settings(new_settings)  
        else:
            await client.send_message(message.channel, "{} Sorry, you don't have permission to edit settings.".format(message.author.mention))
    else:
        await client.send_message(message.channel, "{} You need to be in a server to use this command.".format(message.author.mention))

async def toggle_starboard(message, client):
    if is_in_server(message):
        # Toggles logs on and off, simple as that.
        global settings
        is_admin = await check_if_can_edit(message.author, message, client)
        if is_admin:
            load_settings()
            settings = server_has_settings(settings, message)
            if not "use_stars" in settings[message.server.id]:
                settings[message.server.id]["use_stars"] = False
                settings[message.server.id]["star_channel"] = "starboard"
                settings[message.server.id]["star_emoji"] = "\N{WHITE MEDIUM STAR}"
                settings[message.server.id]["star_requirement"] = 3
            if re.search("on$", message.content.rstrip()):
                settings[message.server.id]["use_stars"] = True
                await client.send_message(message.channel, "{} Starboard enabled. Messages that receive {} star(s) will be put in in {}.".format(message.author.mention, settings[message.server.id]["star_requirement"], settings[message.server.id]["star_channel"]))
            elif re.search("off$", message.content.rstrip()):
                settings[message.server.id]["use_stars"] = False
                await client.send_message(message.channel, "{} Starboard disabled.".format(message.author.mention))
            else:
                await client.send_message(message.channel, "{} Sorry, you need to specify \"on\" or \"off\"!".format(message.author.mention))
            save_settings(settings)
        else:
            await client.send_message(message.channel, "{} Sorry, you don't have permission to edit settings.".format(message.author.mention))
    else:
        await client.send_message(message.channel, "{} You need to be in a server to use this command.".format(message.author.mention))

async def set_starboard_channel(message, client):
    # Set the channel to log edits and deletions in.
    if is_in_server(message):
        global settings
        is_admin = await check_if_can_edit(message.author, message, client)
        if is_admin:
            if re.findall("<#[0-9]+>", message.content):
                # Get the name of the channel - that should be all we need
                star_channel = message.server.get_channel(re.sub("[\<\#\>]", "", re.findall("<#[0-9]+>", message.content)[0])).name
            else:
                await client.send_message(message.channel, "{} Please specify a starboard channel by typing `#name_of_channel`.".format(message.author.mention))
                return False
            
            load_settings()
            settings = server_has_settings(settings, message)
            if not "star_channel" in settings[message.server.id]:
                settings[message.server.id]["use_stars"] = False
                settings[message.server.id]["star_emoji"] = "\N{WHITE MEDIUM STAR}"
                settings[message.server.id]["star_requirement"] = 3
            settings[message.server.id]["star_channel"] = star_channel
            save_settings(settings)
            await client.send_message(message.channel, "{} Starboard channel set to {}".format(message.author.mention, settings[message.server.id]["star_channel"]))
        else:
            await client.send_message(message.channel, "{} Sorry, you don't have permission to edit settings.".format(message.author.mention))
    else:
        await client.send_message(message.channel, "{} You need to be in a server to use this command.".format(message.author.mention))

async def set_starboard_emoji(message, client):
    # Set the channel to log stars in.
    if is_in_server(message):
        global settings
        is_admin = await check_if_can_edit(message.author, message, client)
        if is_admin:
            # First one removes the command's name, second filters any whitespace Discord adds to the end.
            star_emoji = re.sub("^\$\S+ ", "", re.sub("\s+$", "",  message.content))
            star_emoji = star_emoji[0] # Only one character
            load_settings()
            settings = server_has_settings(settings, message)
            if not "star_emoji" in settings[message.server.id]:
                settings[message.server.id]["use_stars"] = False
                settings[message.server.id]["star_channel"] = "starboard"
                settings[message.server.id]["star_requirement"] = 3
            settings[message.server.id]["star_emoji"] = star_emoji
            save_settings(settings)
            await client.send_message(message.channel, "{} Starboard emoji set to {}".format(message.author.mention, settings[message.server.id]["star_emoji"]))
        else:
            await client.send_message(message.channel, "{} Sorry, you don't have permission to edit settings.".format(message.author.mention))
    else:
        await client.send_message(message.channel, "{} You need to be in a server to use this command.".format(message.author.mention))

async def set_starboard_requirement(message, client):
    # Set the number of reactions necessary before starring.
    if is_in_server(message):
        global settings
        is_admin = await check_if_can_edit(message.author, message, client)
        if is_admin:
            # First one removes the command's name, second filters any whitespace Discord adds to the end.
            try:
                star_count = int(re.sub("^\$\S+ ", "", re.sub("\s+$", "",  message.content)))
            except:
                await client.send_message(message.channel, "{} Sorry, that's not an integer!".format(message.author.mention))
            finally:
                if star_count >= 1:
                    load_settings()
                    settings = server_has_settings(settings, message)
                    if not "star_emoji" in settings[message.server.id]:
                        settings[message.server.id]["use_stars"] = False
                        settings[message.server.id]["star_channel"] = "starboard"
                        settings[message.server.id]["star_emoji"] = "\N{WHITE MEDIUM STAR}"
                    settings[message.server.id]["star_requirement"] = star_count
                    save_settings(settings)
                    await client.send_message(message.channel, "{} Star requirement set to {}".format(message.author.mention, settings[message.server.id]["star_requirement"]))
                else:
                   await client.send_message(message.channel, "{} The number of stars required needs to be at least 1.".format(message.author.mention)) 
        else:
            await client.send_message(message.channel, "{} Sorry, you don't have permission to edit settings.".format(message.author.mention))
    else:
        await client.send_message(message.channel, "{} You need to be in a server to use this command.".format(message.author.mention))

async def set_up_defaults(client, message):
    if is_in_server(message):
        # If we're not in a server, every command crashes, as it tries to grab a server ID where there is none.
        global settings
        load_settings()
        if not message.server.id in settings:
            print("Had to set up default settings for server {}".format(message.server.id))
            settings[message.server.id] = dict()
            settings[message.server.id]["allowed_roles"] = []
            settings[message.server.id]["use_logging"] = True
            settings[message.server.id]["log_channel"] = "modlog"
            settings[message.server.id]["use_stars"] = False
            settings[message.server.id]["star_channel"] = "starboard"
            settings[message.server.id]["star_emoji"] = "\N{WHITE MEDIUM STAR}"
            settings[message.server.id]["star_requirement"] = 3
            save_settings(settings)

# Add the commands to the global command table.
def setup_command_table(table):
    table["\\$logtoggle"] = toggle_logs
    table["\\$logchannel"] = set_log_channel
    table["\\$allowrole"] = allow_role
    table["\\$forbidrole"] = forbid_role
    table["\\$startoggle"] = toggle_starboard
    table["\\$starchannel"] = set_starboard_channel
    table["\\$staremoji"] = set_starboard_emoji
    table["\\$starreq"] = set_starboard_requirement

    # TODO: Work out how to add help commands for these properly

def setup_hooks(hooktable):
    hooktable["message"].append(set_up_defaults)