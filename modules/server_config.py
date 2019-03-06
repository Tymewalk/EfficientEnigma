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

async def check_if_can_edit(user, client, message):
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

async def set_up_defaults(client, message):
    # Set up the default settings for a server.
    if is_in_server(message):
        # If we're not in a server, every command crashes, as it tries to grab a server ID where there is none.
        global settings
        load_settings()
        changed = False
        if not message.server.id in settings:
            settings[message.server.id] = dict()
            changed = True
        # If only some settings are set, the above check will fail to catch it -
        # this ensures every setting has a value.
        if not "allowed_roles" in settings[message.server.id]:
            settings[message.server.id]["allowed_roles"] = []
            changed = True
        if not "use_logging" in settings[message.server.id]:
            settings[message.server.id]["use_logging"] = False
            changed = True
        if not "log_channel" in settings[message.server.id]:
            settings[message.server.id]["log_channel"] = "modlog"
            changed = True
        if not "use_stars" in settings[message.server.id]:
            settings[message.server.id]["use_stars"] = False
            changed = True
        if not "star_channel" in settings[message.server.id]:
            settings[message.server.id]["star_channel"] = "starboard"
            changed = True
        if not "star_emoji" in settings[message.server.id]:
            settings[message.server.id]["star_emoji"] = "\N{WHITE MEDIUM STAR}"
            changed = True
        if not "star_requirement" in settings[message.server.id]:
            settings[message.server.id]["star_requirement"] = 3
            changed = True
        if not "self_star" in settings[message.server.id]:
            settings[message.server.id]["self_star"] = False
            changed = True
        if not "use_welcome" in settings[message.server.id]:
            settings[message.server.id]["use_welcome"] = False
            changed = True
        if not "welcome_channel" in settings[message.server.id]:
            settings[message.server.id]["welcome_channel"] = "welcome"
            changed = True
        if not "welcome_message" in settings[message.server.id]:
            settings[message.server.id]["welcome_message"] = "<ping> Welcome to our server, <name>!"
            changed = True
        # Prevent issues by only saving settings if we did anything
        if changed:
            save_settings(settings)
    
async def toggle_logs(client, message):
    if is_in_server(message):
        # Toggles logs on and off, simple as that.
        global settings
        is_admin = await check_if_can_edit(message.author, client, message)
        if is_admin:
            load_settings()
            new_settings = server_has_settings(settings, message)
            if re.search("on$", message.content.rstrip()):
                new_settings[message.server.id]["use_logging"] = True
                await client.send_message(message.channel, "{} Logging enabled. Messages will be logged in {}".format(message.author.mention, settings[message.server.id]["log_channel"]))
            elif re.search("off$", message.content.rstrip()):
                new_settings[message.server.id]["use_logging"] = False
                await client.send_message(message.channel, "{} Logging disabled.".format(message.author.mention))
            else:
                await client.send_message(message.channel, "{} Sorry, you need to specify \"on\" or \"off\"!".format(message.author.mention))
            save_settings(new_settings)
        else:
            await client.send_message(message.channel, "{} Sorry, you don't have permission to edit settings.".format(message.author.mention))
    else:
        await client.send_message(message.channel, "{} You need to be in a server to use this command.".format(message.author.mention))

async def set_log_channel(client, message):
    # Set the channel to log edits and deletions in.
    if is_in_server(message):
        global settings
        is_admin = await check_if_can_edit(message.author, client, message)
        if is_admin:
            if re.findall("<#[0-9]+>", message.content):
                # Get the name of the channel - that should be all we need
                log_channel = message.server.get_channel(re.sub("[\<\#\>]", "", re.findall("<#[0-9]+>", message.content)[0])).name
            else:
                await client.send_message(message.channel, "{} Please specify a logging channel by typing `#name_of_channel`.")
                return False
            
            load_settings()
            settings = server_has_settings(settings, message)
            settings[message.server.id]["log_channel"] = log_channel
            save_settings(settings)
            await client.send_message(message.channel, "{} Log channel set to {}".format(message.author.mention, settings[message.server.id]["log_channel"]))
        else:
            await client.send_message(message.channel, "{} Sorry, you don't have permission to edit settings.".format(message.author.mention))
    else:
        await client.send_message(message.channel, "{} You need to be in a server to use this command.".format(message.author.mention))

async def allow_role(client, message):
    if is_in_server(message):
        global settings
        is_admin = await check_if_can_edit(message.author, client, message)
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
            role = discord.utils.get(message.server.roles, name=role_name)
            # Check if the role exists before adding it
            if role:
                if role_name in new_settings[message.server.id]["allowed_roles"]:
                    await client.send_message(message.channel, ":warning: The role \"{}\" is already allowed to be self-assigned.".format(role_name))
                else:
                    new_settings[message.server.id]["allowed_roles"].append(role_name)
                    await client.send_message(message.channel, ":white_check_mark: The role \"{}\" can now be self-assigned by members.".format(role_name))
                    save_settings(new_settings)
            else:
                await client.send_message(message.channel, ":no_entry: The role \"{}\" does not exist. Please create it before allowing it to be self-assigned.".format(role_name))  
        else:
            await client.send_message(message.channel, "{} Sorry, you don't have permission to edit settings.".format(message.author.mention))
    else:
        await client.send_message(message.channel, "{} You need to be in a server to use this command.".format(message.author.mention))

async def forbid_role(client, message):
    if is_in_server(message):
        global settings
        is_admin = await check_if_can_edit(message.author, client, message)
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

async def toggle_starboard(client, message):
    if is_in_server(message):
        # Toggles the starboard on and off, simple as that.
        global settings
        is_admin = await check_if_can_edit(message.author, client, message)
        if is_admin:
            load_settings()
            new_settings = server_has_settings(settings, message)
            if re.search("on$", message.content.rstrip()):
                new_settings[message.server.id]["use_stars"] = True
                await client.send_message(message.channel, "{} Starboard enabled. Messages that receive {} star(s) will be put in in {}.".format(message.author.mention, settings[message.server.id]["star_requirement"], settings[message.server.id]["star_channel"]))
            elif re.search("off$", message.content.rstrip()):
                new_settings[message.server.id]["use_stars"] = False
                await client.send_message(message.channel, "{} Starboard disabled.".format(message.author.mention))
            else:
                await client.send_message(message.channel, "{} Sorry, you need to specify \"on\" or \"off\"!".format(message.author.mention))
            save_settings(new_settings)
        else:
            await client.send_message(message.channel, "{} Sorry, you don't have permission to edit settings.".format(message.author.mention))
    else:
        await client.send_message(message.channel, "{} You need to be in a server to use this command.".format(message.author.mention))

async def set_starboard_channel(client, message):
    # Set the channel to log edits and deletions in.
    if is_in_server(message):
        global settings
        is_admin = await check_if_can_edit(message.author, client, message)
        if is_admin:
            if re.findall("<#[0-9]+>", message.content):
                # Get the name of the channel - that should be all we need
                star_channel = message.server.get_channel(re.sub("[\<\#\>]", "", re.findall("<#[0-9]+>", message.content)[0])).name
            else:
                await client.send_message(message.channel, "{} Please specify a starboard channel by typing `#name_of_channel`.".format(message.author.mention))
                return False
            
            load_settings()
            settings = server_has_settings(settings, message)
            settings[message.server.id]["star_channel"] = star_channel
            save_settings(settings)
            await client.send_message(message.channel, "{} Starboard channel set to {}".format(message.author.mention, settings[message.server.id]["star_channel"]))
        else:
            await client.send_message(message.channel, "{} Sorry, you don't have permission to edit settings.".format(message.author.mention))
    else:
        await client.send_message(message.channel, "{} You need to be in a server to use this command.".format(message.author.mention))

async def set_starboard_emoji(client, message):
    # Set the channel to log stars in.
    if is_in_server(message):
        global settings
        is_admin = await check_if_can_edit(message.author, client, message)
        if is_admin:
            # First one removes the command's name, second filters any whitespace Discord adds to the end.
            star_emoji = re.sub("^\$\S+ ", "", re.sub("\s+$", "",  message.content))
            star_emoji = star_emoji[0] # Only one character
            load_settings()
            settings = server_has_settings(settings, message)
            settings[message.server.id]["star_emoji"] = star_emoji
            save_settings(settings)
            await client.send_message(message.channel, "{} Starboard emoji set to {}".format(message.author.mention, settings[message.server.id]["star_emoji"]))
        else:
            await client.send_message(message.channel, "{} Sorry, you don't have permission to edit settings.".format(message.author.mention))
    else:
        await client.send_message(message.channel, "{} You need to be in a server to use this command.".format(message.author.mention))

async def set_starboard_requirement(client, message):
    # Set the number of reactions necessary before starring.
    if is_in_server(message):
        global settings
        is_admin = await check_if_can_edit(message.author, client, message)
        if is_admin:
            # First one removes the command's name, second filters any whitespace Discord adds to the end.
            star_count = 0
            try:
                star_count = int(re.sub("^\$\S+ ", "", re.sub("\s+$", "",  message.content)))
            except:
                await client.send_message(message.channel, "{} Sorry, that's not an integer!".format(message.author.mention))
            finally:
                if star_count >= 1:
                    load_settings()
                    settings = server_has_settings(settings, message)
                    settings[message.server.id]["star_requirement"] = star_count
                    save_settings(settings)
                    await client.send_message(message.channel, "{} Star requirement set to {}".format(message.author.mention, settings[message.server.id]["star_requirement"]))
                else:
                   await client.send_message(message.channel, "{} The number of stars required needs to be at least 1.".format(message.author.mention)) 
        else:
            await client.send_message(message.channel, "{} Sorry, you don't have permission to edit settings.".format(message.author.mention))
    else:
        await client.send_message(message.channel, "{} You need to be in a server to use this command.".format(message.author.mention))

async def toggle_self_star(client, message):
    if is_in_server(message):
        # Toggles self-starring.
        global settings
        is_admin = await check_if_can_edit(message.author, client, message)
        if is_admin:
            load_settings()
            new_settings = server_has_settings(settings, message)
            if re.search("on$", message.content.rstrip()):
                new_settings[message.server.id]["self_star"] = True
                await client.send_message(message.channel, "{} Self-starring enabled. Users can now star their own posts.".format(message.author.mention))
            elif re.search("off$", message.content.rstrip()):
                new_settings[message.server.id]["self_star"] = False
                await client.send_message(message.channel, "{} Self-starring disabled. Users can still star their own posts, but it will not count toward the star requirement.".format(message.author.mention))
            else:
                await client.send_message(message.channel, "{} Sorry, you need to specify \"on\" or \"off\"!".format(message.author.mention))
            save_settings(new_settings)
        else:
            await client.send_message(message.channel, "{} Sorry, you don't have permission to edit settings.".format(message.author.mention))
    else:
        await client.send_message(message.channel, "{} You need to be in a server to use this command.".format(message.author.mention))

async def toggle_welcome(client, message):
    if is_in_server(message):
        # Turns the welcome message on or off.
        global settings
        is_admin = await check_if_can_edit(message.author, client, message)
        if is_admin:
            load_settings()
            new_settings = server_has_settings(settings, message)
            if re.search("on$", message.content.rstrip()):
                new_settings[message.server.id]["use_welcome"] = True
                await client.send_message(message.channel, "{} Welcome message enabled. Welcome message is currently set to `{}`.".format(message.author.mention, settings[message.server.id]["welcome_message"]))
            elif re.search("off$", message.content.rstrip()):
                new_settings[message.server.id]["use_welcome"] = False
                await client.send_message(message.channel, "{} Welcome message disabled.".format(message.author.mention))
            else:
                await client.send_message(message.channel, "{} Sorry, you need to specify \"on\" or \"off\"!".format(message.author.mention))
            save_settings(new_settings)
        else:
            await client.send_message(message.channel, "{} Sorry, you don't have permission to edit settings.".format(message.author.mention))
    else:
        await client.send_message(message.channel, "{} You need to be in a server to use this command.".format(message.author.mention))

async def set_welcome_channel(client, message):
    # Set the channel to send welcome messages in.
    if is_in_server(message):
        global settings
        is_admin = await check_if_can_edit(message.author, client, message)
        if is_admin:
            if re.findall("<#[0-9]+>", message.content):
                # Get the name of the channel - that should be all we need
                welcome_channel = message.server.get_channel(re.sub("[\<\#\>]", "", re.findall("<#[0-9]+>", message.content)[0])).name
            else:
                await client.send_message(message.channel, "{} Please specify a welcome channel by typing `#name_of_channel`.".format(message.author.mention))
                return False
            
            load_settings()
            settings = server_has_settings(settings, message)
            settings[message.server.id]["welcome_channel"] = welcome_channel
            save_settings(settings)
            await client.send_message(message.channel, "{} Welcome channel set to {}".format(message.author.mention, settings[message.server.id]["welcome_channel"]))
        else:
            await client.send_message(message.channel, "{} Sorry, you don't have permission to edit settings.".format(message.author.mention))
    else:
        await client.send_message(message.channel, "{} You need to be in a server to use this command.".format(message.author.mention))

async def set_welcome_message(client, message):
    # Set the number of reactions necessary before starring.
    if is_in_server(message):
        global settings
        is_admin = await check_if_can_edit(message.author, client, message)
        if is_admin:
            # First one removes the command's name, second filters any whitespace Discord adds to the end.
            welcome_message = re.sub("^\$\S+ ", "", re.sub("\s+$", "",  message.content))
            load_settings()
            settings = server_has_settings(settings, message)
            settings[message.server.id]["welcome_message"] = welcome_message
            save_settings(settings)
            await client.send_message(message.channel, "{} Welcome message set to `{}`".format(message.author.mention, settings[message.server.id]["welcome_message"]))
        else:
            await client.send_message(message.channel, "{} Sorry, you don't have permission to edit settings.".format(message.author.mention))
    else:
        await client.send_message(message.channel, "{} You need to be in a server to use this command.".format(message.author.mention))

async def show_settings(client, message):
    if is_in_server(message):
        global settings
        is_admin = await check_if_can_edit(message.author, client, message)
        if is_admin:
            load_settings()
            settings = server_has_settings(settings, message)
            settings_display = "**Settings for {}**\n".format(message.server.name)
            # Assemble the settings output
            allowed_roles = settings[message.server.id]["allowed_roles"]
            role_list = ""
            for role in allowed_roles:
                role_list += "{}, ".format(role)
            role_list = role_list[:-2]
            if role_list == "":
                role_list = "None"
            settings_display += "Roles Allowed: {}\n".format(role_list)
            if settings[message.server.id]["use_stars"]:
                settings_display += "Starboard: Enabled\nStarboard Requirement: {}\nStarboard Emoji: {}\nStarboard Channel: {}\nSelf-starring allowed: {}\n".format(settings[message.server.id]["star_requirement"], settings[message.server.id]["star_emoji"], settings[message.server.id]["star_channel"], settings[message.server.id]["self_star"])
            else:
                settings_display += "Starboard: Disabled\n"
            if settings[message.server.id]["use_welcome"]:
                settings_display += "Welcome Message: Enabled\nMessage: `{}`\nWelcome Channel: {}\n".format(settings[message.server.id]["welcome_message"], settings[message.server.id]["welcome_channel"])
            else:
                settings_display += "Welcome Message: Disabled\n"
            if settings[message.server.id]["use_logging"]:
                settings_display += "Logging: Enabled\nLog Channel: {}".format(settings[message.server.id]["log_channel"])
            else:
                settings_display += "Logging: Disabled\n"
            await client.send_message(message.channel, settings_display)
        else:
            await client.send_message(message.channel, "{} Sorry, you don't have permission to edit settings.".format(message.author.mention))
    else:
        await client.send_message(message.channel, "{} You need to be in a server to use this command.".format(message.author.mention))

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
    table["\\$selfstar"] = toggle_self_star
    table["\\$welcometoggle"] = toggle_welcome
    table["\\$welcomechannel"] = set_welcome_channel
    table["\\$welcomemessage"] = set_welcome_message
    table["\\$settings"] = show_settings

    # TODO: Work out how to add help commands for these properly

def setup_hooks(hooktable):
    hooktable["message"].append(set_up_defaults)
