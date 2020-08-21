# settings.py
# Allows admins of a server to configure the bot.
import discord, asyncio, json, os, re

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
    if not str(message.guild.id) in in_settings:
        in_settings[str(message.guild.id)] = dict()
    return in_settings

def is_in_server(message):
    # Check if we're in a server.
    return message.guild is not None

async def check_if_can_edit(user, client, message):
    # Does this user have permission to change admin stuff?
    # We need a message so we can properly check if they can.
    found_admin = False
    for r in message.guild.roles:
        for admin_role in settings[str(message.guild.id)]["admin_roles"]:
            if r.name == admin_role:
                found_admin = True


    if not found_admin:
         await message.channel.send("{} It looks like the admin role *doesn't exist* - if you are not able to add one, please tell the server manager to add a role named \"EfficientEnigma Admin\" and assign it to whoever needs it.".format(message.author.mention, admin_role_name))
         return False

    result = False
    for r in settings[str(message.guild.id)]["admin_roles"]:
        if discord.utils.get(message.guild.roles, name=r) in user.roles:
            result = True
    return result

async def set_up_defaults(client, message):
    # Set up the default settings for a server.
    if is_in_server(message):
        # If we're not in a server, every command crashes, as it tries to grab a server ID where there is none.
        global settings
        load_settings()
        changed = False
        if not str(message.guild.id) in settings:
            settings[str(message.guild.id)] = dict()
            changed = True
        # If only some settings are set, the above check will fail to catch it -
        # this ensures every setting has a value.
        if not "allowed_roles" in settings[str(message.guild.id)]:
            settings[str(message.guild.id)]["allowed_roles"] = []
            changed = True
        if not "admin_roles" in settings[str(message.guild.id)]:
            settings[str(message.guild.id)]["admin_roles"] = ["EfficientEnigma Admin"]
            changed = True
        if not "use_logging" in settings[str(message.guild.id)]:
            settings[str(message.guild.id)]["use_logging"] = False
            changed = True
        if not "log_channel" in settings[str(message.guild.id)]:
            settings[str(message.guild.id)]["log_channel"] = "modlog"
            changed = True
        if not "use_stars" in settings[str(message.guild.id)]:
            settings[str(message.guild.id)]["use_stars"] = False
            changed = True
        if not "star_channel" in settings[str(message.guild.id)]:
            settings[str(message.guild.id)]["star_channel"] = "starboard"
            changed = True
        if not "star_emoji" in settings[str(message.guild.id)]:
            settings[str(message.guild.id)]["star_emoji"] = "\N{WHITE MEDIUM STAR}"
            changed = True
        if not "star_requirement" in settings[str(message.guild.id)]:
            settings[str(message.guild.id)]["star_requirement"] = 3
            changed = True
        if not "self_star" in settings[str(message.guild.id)]:
            settings[str(message.guild.id)]["self_star"] = False
            changed = True
        if not "use_welcome" in settings[str(message.guild.id)]:
            settings[str(message.guild.id)]["use_welcome"] = False
            changed = True
        if not "welcome_channel" in settings[str(message.guild.id)]:
            settings[str(message.guild.id)]["welcome_channel"] = "welcome"
            changed = True
        if not "welcome_message" in settings[str(message.guild.id)]:
            settings[str(message.guild.id)]["welcome_message"] = "<ping> Welcome to the server, <name>!"
        if not "use_leave" in settings[str(message.guild.id)]:
            settings[str(message.guild.id)]["use_leave"] = False
            changed = True
        if not "leave_message" in settings[str(message.guild.id)]:
            settings[str(message.guild.id)]["leave_message"] = "<name> has left the server."
            changed = True
        if not "leave_channel" in settings[str(message.guild.id)]:
            settings[str(message.guild.id)]["leave_channel"] = "welcome"
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
                new_settings[str(message.guild.id)]["use_logging"] = True
                await message.channel.send("{} Logging enabled. Messages will be logged in {}".format(message.author.mention, settings[str(message.guild.id)]["log_channel"]))
            elif re.search("off$", message.content.rstrip()):
                new_settings[str(message.guild.id)]["use_logging"] = False
                await message.channel.send("{} Logging disabled.".format(message.author.mention))
            else:
                await message.channel.send("{} Sorry, you need to specify \"on\" or \"off\"!".format(message.author.mention))
            save_settings(new_settings)
        else:
            await message.channel.send("{} Sorry, you don't have permission to edit settings.".format(message.author.mention))
    else:
        await message.channel.send("{} You need to be in a server to use this command.".format(message.author.mention))

async def set_log_channel(client, message):
    # Set the channel to log edits and deletions in.
    if is_in_server(message):
        global settings
        is_admin = await check_if_can_edit(message.author, client, message)
        if is_admin:
            if re.findall("<#[0-9]+>", message.content):
                # Get the name of the channel - that should be all we need
                log_channel = message.guild.get_channel(re.sub("[\<\#\>]", "", re.findall("<#[0-9]+>", message.content)[0])).name
            else:
                await message.channel.send("{} Please specify a logging channel by typing `#name_of_channel`.")
                return False
            
            load_settings()
            settings = server_has_settings(settings, message)
            settings[str(message.guild.id)]["log_channel"] = log_channel
            save_settings(settings)
            await message.channel.send("{} Log channel set to {}".format(message.author.mention, settings[str(message.guild.id)]["log_channel"]))
        else:
            await message.channel.send("{} Sorry, you don't have permission to edit settings.".format(message.author.mention))
    else:
        await message.channel.send("{} You need to be in a server to use this command.".format(message.author.mention))

async def allow_role(client, message):
    if is_in_server(message):
        global settings
        is_admin = await check_if_can_edit(message.author, client, message)
        if is_admin:
            load_settings()
            new_settings = server_has_settings(settings, message)
            if not "allowed_roles" in new_settings[str(message.guild.id)]:
                new_settings[str(message.guild.id)]["allowed_roles"] = []
            if re.match("^\$[^\W]+( |)+$", message.content):
                # Don't do anything if it's all whitespace
                await message.channel.send(":warning: Sorry, you forgot to specify a role.")
                return
            role_name = re.sub("^\$[^\W]+ ", "", message.content)
            role = discord.utils.get(message.guild.roles, name=role_name)
            # Check if the role exists before adding it
            if role:
                if role_name in new_settings[str(message.guild.id)]["allowed_roles"]:
                    await message.channel.send(":warning: The role \"{}\" is already allowed to be self-assigned.".format(role_name))
                else:
                    new_settings[str(message.guild.id)]["allowed_roles"].append(role_name)
                    await message.channel.send(":white_check_mark: The role \"{}\" can now be self-assigned by members.".format(role_name))
                    save_settings(new_settings)
            else:
                await message.channel.send(":no_entry: The role \"{}\" does not exist. Please create it before allowing it to be self-assigned.".format(role_name))  
        else:
            await message.channel.send("{} Sorry, you don't have permission to edit settings.".format(message.author.mention))
    else:
        await message.channel.send("{} You need to be in a server to use this command.".format(message.author.mention))

async def forbid_role(client, message):
    if is_in_server(message):
        global settings
        is_admin = await check_if_can_edit(message.author, client, message)
        if is_admin:
            load_settings()
            new_settings = server_has_settings(settings, message)
            if not "allowed_roles" in settings[str(message.guild.id)]:
                new_settings[str(message.guild.id)]["allowed_roles"] = []
            if re.match("^\\\$[^\W]+( |)+$", message.content):
                # Don't do anything if it's all whitespace
                await message.channel.send(":warning: Sorry, you forgot to specify a role.")
                return
            role_name = re.sub("^\$[^\W]+ ", "", message.content)
            if not role_name in new_settings[str(message.guild.id)]["allowed_roles"]:
                await message.channel.send(":warning: The role \"{}\" is already not allowed to be self-assigned.".format(role_name))
            else:
                new_settings[str(message.guild.id)]["allowed_roles"].remove(role_name)
                await message.channel.send(":white_check_mark: The role \"{}\" can no longer be self-assigned by members.".format(role_name))
                save_settings(new_settings)  
        else:
            await message.channel.send("{} Sorry, you don't have permission to edit settings.".format(message.author.mention))
    else:
        await message.channel.send("{} You need to be in a server to use this command.".format(message.author.mention))
        
async def allow_admin_role(client, message):
    if is_in_server(message):
        global settings
        is_admin = await check_if_can_edit(message.author, client, message)
        if is_admin:
            load_settings()
            new_settings = server_has_settings(settings, message)
            if not "admin_roles" in new_settings[str(message.guild.id)]:
                new_settings[str(message.guild.id)]["admin_roles"] = []
            if re.match("^\$[^\W]+( |)+$", message.content):
                # Don't do anything if it's all whitespace
                await message.channel.send(":warning: Sorry, you forgot to specify a role.")
                return
            role_name = re.sub("^\$[^\W]+ ", "", message.content)
            role = discord.utils.get(message.guild.roles, name=role_name)
            # Check if the role exists before adding it
            if role:
                if role_name in new_settings[str(message.guild.id)]["admin_roles"]:
                    await message.channel.send(":warning: The role \"{}\" is already an EfficientEnigma admin.".format(role_name))
                else:
                    new_settings[str(message.guild.id)]["admin_roles"].append(role_name)
                    await message.channel.send(":white_check_mark: The role \"{}\" can now edit EfficientEnigma's settings.".format(role_name))
                    save_settings(new_settings)
            else:
                await message.channel.send(":no_entry: The role \"{}\" does not exist. Please create it before allowing it to be an admin.".format(role_name))  
        else:
            await message.channel.send("{} Sorry, you don't have permission to edit settings.".format(message.author.mention))
    else:
        await message.channel.send("{} You need to be in a server to use this command.".format(message.author.mention))

async def forbid_admin_role(client, message):
    if is_in_server(message):
        global settings
        is_admin = await check_if_can_edit(message.author, client, message)
        if is_admin:
            load_settings()
            new_settings = server_has_settings(settings, message)
            if not "admin_roles" in settings[str(message.guild.id)]:
                new_settings[str(message.guild.id)]["admin_roles"] = []
            if re.match("^\\\$[^\W]+( |)+$", message.content):
                # Don't do anything if it's all whitespace
                await message.channel.send(":warning: Sorry, you forgot to specify a role.")
                return
            role_name = re.sub("^\$[^\W]+ ", "", message.content)
            # Don't allow people to accidentally lock themselves out - EE Admin should always be allowed
            if role_name == "EfficientEnigma Admin":
                await message.channel.send(":no_entry: The role \"EfficientEnigma Admin\" can not be removed. This is to prevent the admin list from being empty, locking up the bot. Sorry!")
                return
            if not role_name in new_settings[str(message.guild.id)]["admin_roles"]:
                await message.channel.send(":warning: The role \"{}\" is already not an EfficientEnigma admin".format(role_name))
            else:
                new_settings[str(message.guild.id)]["admin_roles"].remove(role_name)
                await message.channel.send(":white_check_mark: The role \"{}\" can no longer edit EfficientEnigma's settings.".format(role_name))
                save_settings(new_settings)  
        else:
            await message.channel.send("{} Sorry, you don't have permission to edit settings.".format(message.author.mention))
    else:
        await message.channel.send("{} You need to be in a server to use this command.".format(message.author.mention))

async def toggle_starboard(client, message):
    if is_in_server(message):
        # Toggles the starboard on and off, simple as that.
        global settings
        is_admin = await check_if_can_edit(message.author, client, message)
        if is_admin:
            load_settings()
            new_settings = server_has_settings(settings, message)
            if re.search("on$", message.content.rstrip()):
                new_settings[str(message.guild.id)]["use_stars"] = True
                await message.channel.send("{} Starboard enabled. Messages that receive {} star(s) will be put in in {}.".format(message.author.mention, settings[str(message.guild.id)]["star_requirement"], settings[str(message.guild.id)]["star_channel"]))
            elif re.search("off$", message.content.rstrip()):
                new_settings[str(message.guild.id)]["use_stars"] = False
                await message.channel.send("{} Starboard disabled.".format(message.author.mention))
            else:
                await message.channel.send("{} Sorry, you need to specify \"on\" or \"off\"!".format(message.author.mention))
            save_settings(new_settings)
        else:
            await message.channel.send("{} Sorry, you don't have permission to edit settings.".format(message.author.mention))
    else:
        await message.channel.send("{} You need to be in a server to use this command.".format(message.author.mention))

async def set_starboard_channel(client, message):
    # Set the channel to log edits and deletions in.
    if is_in_server(message):
        global settings
        is_admin = await check_if_can_edit(message.author, client, message)
        if is_admin:
            if re.findall("<#[0-9]+>", message.content):
                # Get the name of the channel - that should be all we need
                star_channel = message.guild.get_channel(re.sub("[\<\#\>]", "", re.findall("<#[0-9]+>", message.content)[0])).name
            else:
                await message.channel.send("{} Please specify a starboard channel by typing `#name_of_channel`.".format(message.author.mention))
                return False
            
            load_settings()
            settings = server_has_settings(settings, message)
            settings[str(message.guild.id)]["star_channel"] = star_channel
            save_settings(settings)
            await message.channel.send("{} Starboard channel set to {}".format(message.author.mention, settings[str(message.guild.id)]["star_channel"]))
        else:
            await message.channel.send("{} Sorry, you don't have permission to edit settings.".format(message.author.mention))
    else:
        await message.channel.send("{} You need to be in a server to use this command.".format(message.author.mention))

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
            settings[str(message.guild.id)]["star_emoji"] = star_emoji
            save_settings(settings)
            await message.channel.send("{} Starboard emoji set to {}".format(message.author.mention, settings[str(message.guild.id)]["star_emoji"]))
        else:
            await message.channel.send("{} Sorry, you don't have permission to edit settings.".format(message.author.mention))
    else:
        await message.channel.send("{} You need to be in a server to use this command.".format(message.author.mention))

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
                await message.channel.send("{} Sorry, that's not an integer!".format(message.author.mention))
            finally:
                if star_count >= 1:
                    load_settings()
                    settings = server_has_settings(settings, message)
                    settings[str(message.guild.id)]["star_requirement"] = star_count
                    save_settings(settings)
                    await message.channel.send("{} Star requirement set to {}".format(message.author.mention, settings[str(message.guild.id)]["star_requirement"]))
                else:
                   await message.channel.send("{} The number of stars required needs to be at least 1.".format(message.author.mention)) 
        else:
            await message.channel.send("{} Sorry, you don't have permission to edit settings.".format(message.author.mention))
    else:
        await message.channel.send("{} You need to be in a server to use this command.".format(message.author.mention))

async def toggle_self_star(client, message):
    if is_in_server(message):
        # Toggles self-starring.
        global settings
        is_admin = await check_if_can_edit(message.author, client, message)
        if is_admin:
            load_settings()
            new_settings = server_has_settings(settings, message)
            if re.search("on$", message.content.rstrip()):
                new_settings[str(message.guild.id)]["self_star"] = True
                await message.channel.send("{} Self-starring enabled. Users can now star their own posts.".format(message.author.mention))
            elif re.search("off$", message.content.rstrip()):
                new_settings[str(message.guild.id)]["self_star"] = False
                await message.channel.send("{} Self-starring disabled. Users can still star their own posts, but it will not count toward the star requirement.".format(message.author.mention))
            else:
                await message.channel.send("{} Sorry, you need to specify \"on\" or \"off\"!".format(message.author.mention))
            save_settings(new_settings)
        else:
            await message.channel.send("{} Sorry, you don't have permission to edit settings.".format(message.author.mention))
    else:
        await message.channel.send("{} You need to be in a server to use this command.".format(message.author.mention))

async def toggle_welcome(client, message):
    if is_in_server(message):
        # Turns the welcome message on or off.
        global settings
        is_admin = await check_if_can_edit(message.author, client, message)
        if is_admin:
            load_settings()
            new_settings = server_has_settings(settings, message)
            if re.search("on$", message.content.rstrip()):
                new_settings[str(message.guild.id)]["use_welcome"] = True
                await message.channel.send("{} Welcome message enabled. Welcome message is currently set to `{}`.".format(message.author.mention, settings[str(message.guild.id)]["welcome_message"]))
            elif re.search("off$", message.content.rstrip()):
                new_settings[str(message.guild.id)]["use_welcome"] = False
                await message.channel.send("{} Welcome message disabled.".format(message.author.mention))
            else:
                await message.channel.send("{} Sorry, you need to specify \"on\" or \"off\"!".format(message.author.mention))
            save_settings(new_settings)
        else:
            await message.channel.send("{} Sorry, you don't have permission to edit settings.".format(message.author.mention))
    else:
        await message.channel.send("{} You need to be in a server to use this command.".format(message.author.mention))

async def set_welcome_channel(client, message):
    # Set the channel to send welcome messages in.
    if is_in_server(message):
        global settings
        is_admin = await check_if_can_edit(message.author, client, message)
        if is_admin:
            if re.findall("<#[0-9]+>", message.content):
                # Get the name of the channel - that should be all we need
                welcome_channel = message.guild.get_channel(re.sub("[\<\#\>]", "", re.findall("<#[0-9]+>", message.content)[0])).name
            else:
                await message.channel.send("{} Please specify a welcome channel by typing `#name_of_channel`.".format(message.author.mention))
                return False
            
            load_settings()
            settings = server_has_settings(settings, message)
            settings[str(message.guild.id)]["welcome_channel"] = welcome_channel
            save_settings(settings)
            await message.channel.send("{} Welcome channel set to {}".format(message.author.mention, settings[str(message.guild.id)]["welcome_channel"]))
        else:
            await message.channel.send("{} Sorry, you don't have permission to edit settings.".format(message.author.mention))
    else:
        await message.channel.send("{} You need to be in a server to use this command.".format(message.author.mention))

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
            settings[str(message.guild.id)]["welcome_message"] = welcome_message
            save_settings(settings)
            await message.channel.send("{} Welcome message set to `{}`".format(message.author.mention, settings[str(message.guild.id)]["welcome_message"]))
        else:
            await message.channel.send("{} Sorry, you don't have permission to edit settings.".format(message.author.mention))
    else:
        await message.channel.send("{} You need to be in a server to use this command.".format(message.author.mention))

async def toggle_leave(client, message):
    if is_in_server(message):
        # Turns the leaving message on or off.
        global settings
        is_admin = await check_if_can_edit(message.author, client, message)
        if is_admin:
            load_settings()
            new_settings = server_has_settings(settings, message)
            if re.search("on$", message.content.rstrip()):
                new_settings[str(message.guild.id)]["use_leave"] = True
                await message.channel.send("{} Leaving message enabled. Leaving message is currently set to `{}`.".format(message.author.mention, settings[str(message.guild.id)]["leave_message"]))
            elif re.search("off$", message.content.rstrip()):
                new_settings[str(message.guild.id)]["use_leave"] = False
                await message.channel.send("{} Leaving message disabled.".format(message.author.mention))
            else:
                await message.channel.send("{} Sorry, you need to specify \"on\" or \"off\"!".format(message.author.mention))
            save_settings(new_settings)
        else:
            await message.channel.send("{} Sorry, you don't have permission to edit settings.".format(message.author.mention))
    else:
        await message.channel.send("{} You need to be in a server to use this command.".format(message.author.mention))

async def set_leave_channel(client, message):
    # Set the channel to send leave messages in.
    if is_in_server(message):
        global settings
        is_admin = await check_if_can_edit(message.author, client, message)
        if is_admin:
            if re.findall("<#[0-9]+>", message.content):
                # Get the name of the channel - that should be all we need
                leave_channel = message.guild.get_channel(re.sub("[\<\#\>]", "", re.findall("<#[0-9]+>", message.content)[0])).name
            else:
                await message.channel.send("{} Please specify a leave channel by typing `#name_of_channel`.".format(message.author.mention))
                return False
            
            load_settings()
            settings = server_has_settings(settings, message)
            settings[str(message.guild.id)]["leave_channel"] = leave_channel
            save_settings(settings)
            await message.channel.send("{} Leaving message channel set to {}".format(message.author.mention, settings[str(message.guild.id)]["leave_channel"]))
        else:
            await message.channel.send("{} Sorry, you don't have permission to edit settings.".format(message.author.mention))
    else:
        await message.channel.send("{} You need to be in a server to use this command.".format(message.author.mention))

async def set_leave_message(client, message):
    # Set the number of reactions necessary before starring.
    if is_in_server(message):
        global settings
        is_admin = await check_if_can_edit(message.author, client, message)
        if is_admin:
            # First one removes the command's name, second filters any whitespace Discord adds to the end.
            leave_message = re.sub("^\$\S+ ", "", re.sub("\s+$", "",  message.content))
            load_settings()
            settings = server_has_settings(settings, message)
            settings[str(message.guild.id)]["leave_message"] = leave_message
            save_settings(settings)
            await message.channel.send("{} Leaving message set to `{}`".format(message.author.mention, settings[str(message.guild.id)]["leave_message"]))
        else:
            await message.channel.send("{} Sorry, you don't have permission to edit settings.".format(message.author.mention))
    else:
        await message.channel.send("{} You need to be in a server to use this command.".format(message.author.mention))

async def show_settings(client, message):
    if is_in_server(message):
        global settings
        is_admin = await check_if_can_edit(message.author, client, message)
        if is_admin:
            load_settings()
            settings = server_has_settings(settings, message)
            settings_display = "**Settings for {}**\n".format(message.guild.name)
            # Assemble the settings output
            allowed_roles = settings[str(message.guild.id)]["allowed_roles"]
            role_list = ""
            for role in allowed_roles:
                role_list += "{}, ".format(role)
            role_list = role_list[:-2]
            if role_list == "":
                role_list = "None"
            settings_display += "Roles Allowed: {}\n".format(role_list)
            admin_roles = settings[str(message.guild.id)]["admin_roles"]
            role_list = ""
            for role in admin_roles:
                role_list += "{}, ".format(role)
            role_list = role_list[:-2]
            if role_list == "":
                role_list = "None"
            settings_display += "Roles That Can Edit Settings: {}\n".format(role_list)
            if settings[str(message.guild.id)]["use_stars"]:
                settings_display += "Starboard: Enabled\nStarboard Requirement: {}\nStarboard Emoji: {}\nStarboard Channel: {}\nSelf-starring allowed: {}\n".format(settings[str(message.guild.id)]["star_requirement"], settings[str(message.guild.id)]["star_emoji"], settings[str(message.guild.id)]["star_channel"], settings[str(message.guild.id)]["self_star"])
            else:
                settings_display += "Starboard: Disabled\n"
            if settings[str(message.guild.id)]["use_welcome"]:
                settings_display += "Welcome Message: Enabled\nMessage: `{}`\nWelcome Channel: {}\n".format(settings[str(message.guild.id)]["welcome_message"], settings[str(message.guild.id)]["welcome_channel"])
            else:
                settings_display += "Welcome Message: Disabled\n"
            if settings[str(message.guild.id)]["use_leave"]:
                settings_display += "Leaving Message: Enabled\nMessage: `{}`\nLeaving Channel: {}\n".format(settings[str(message.guild.id)]["leaving_message"], settings[str(message.guild.id)]["leaving_channel"])
            else:
                settings_display += "Leaving Message: Disabled\n"
            if settings[str(message.guild.id)]["use_logging"]:
                settings_display += "Logging: Enabled\nLog Channel: {}".format(settings[str(message.guild.id)]["log_channel"])
            else:
                settings_display += "Logging: Disabled\n"
            await message.channel.send(settings_display)
        else:
            await message.channel.send("{} Sorry, you don't have permission to edit settings.".format(message.author.mention))
    else:
        await message.channel.send("{} You need to be in a server to use this command.".format(message.author.mention))

# Add the commands to the global command table.
def setup_command_table(table):
    table["\\$logtoggle"] = toggle_logs
    table["\\$logchannel"] = set_log_channel
    table["\\$allowrole"] = allow_role
    table["\\$forbidrole"] = forbid_role
    table["\\$allowadminrole"] = allow_admin_role
    table["\\$forbidadminrole"] = forbid_admin_role
    table["\\$startoggle"] = toggle_starboard
    table["\\$starchannel"] = set_starboard_channel
    table["\\$staremoji"] = set_starboard_emoji
    table["\\$starreq"] = set_starboard_requirement
    table["\\$selfstar"] = toggle_self_star
    table["\\$welcometoggle"] = toggle_welcome
    table["\\$welcomechannel"] = set_welcome_channel
    table["\\$welcomemessage"] = set_welcome_message
    table["\\$leavetoggle"] = toggle_leave
    table["\\$leavechannel"] = set_leave_channel
    table["\\$leavemessage"] = set_leave_message
    table["\\$settings"] = show_settings

    # TODO: Work out how to add help commands for these properly

def setup_hooks(hooktable):
    hooktable["message"].append(set_up_defaults)
