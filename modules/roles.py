# roles.py
# Role management, such as assigning and removing roles.
import discord.utils, re

# TODO: Set up config for role list
allowed_roles = []

async def give_role(message, client):
    role_list = ""
    for role in allowed_roles:
        role_list += "{}, ".format(role)
    role_list = role_list[:-2]
    if re.match("^\![^\W]+( |)+", message.content):
        # Don't do anything if it's all whitespace
        await client.send_message(message.channel, ":warning: Sorry, you forgot to specify a role. Available roles are:\n{}".format(role_list))
        return
    role_name = re.sub("^\![^\W]+ ", "", message.content)
    print("User wants {}".format(role_name))
    if not role_name in allowed_roles:
        await client.send_message(message.channel, ":warning: Sorry, that's not an available role. Available roles are:\n{}".format(role_list))
    else:
        role = discord.utils.get(message.server.roles, name=role_name)
        if role:
            if not role in message.author.roles:
                try:
                    await client.add_roles(message.author, role)
                    await client.send_message(message.channel, ":white_check_mark: Successfully added role {0}".format(role.name))
                except discord.Forbidden as e:
                    await client.send_message(message.channel, ":no_entry: I don't have permission to add that role, even though it's in the allowed roles list.\nPlease notify the bot admin.")
            else:
                    await client.send_message(message.channel, ":warning: You already have that role.")
        else:
            await client.send_message(message.channel, ":no_entry: That role is in the allowed roles list, but does not actually exist.\nPlease notify the bot admin.")

async def list_roles(message, client):
    roleList = ""
    for role in allowed_roles:
        roleList += "{}, ".format(i)
    roleList = roleList[:-2]
    await client.send_message(message.channel, "You can assign yourself any of the following:\n{}".format(roleList))

async def remove_role(message, client):
    role_list = ""
    for role in allowed_roles:
        role_list += "{}, ".format(role)
    role_list = role_list[:-2]
    if re.match("^\![^\W]+( |)+", message.content):
        # Don't do anything if it's all whitespace
        await client.send_message(message.channel, ":warning: Sorry, you forgot to specify a role. Available roles are:\n{}".format(role_list))
        return
    role_name = re.sub("^\![^\W]+ ", "", message.content)
    print("User wants {}".format(role_name))
    if not role_name in allowed_roles:
        await client.send_message(message.channel, ":warning: Sorry, that's not an available role. Available roles are:\n{}".format(role_list))
    else:
        role = discord.utils.get(message.server.roles, name=role_name)
        if role:
            if role in message.author.roles:
                try:
                    await client.remove_roles(message.author, role)
                    await client.send_message(message.channel, ":white_check_mark: Successfully removed role {0}".format(role.name))
                except discord.Forbidden as e:
                    await client.send_message(message.channel, ":no_entry: I don't have permission to remove that role, even though it's in the allowed roles list.\nPlease notify the bot admin.")
            else:
                    await client.send_message(message.channel, ":warning: You don't have that role.")
        else:
            await client.send_message(message.channel, ":no_entry: That role is in the allowed roles list, but does not actually exist.\nPlease notify the bot admin.")

# Add the commands to the global command table.
def setup_command_table(table):
    table["!giverole (role) - give yourself a role."] = give_role
    table["!removerole (role) - removes one of your roles."] = remove_role
    table["!listroles - lists all the roles you can give yourself."] = list_roles
