# logging.py
# Logs various user activities like message edits and deletions.
import discord.utils, asyncio, os, json

# Load the settings
f = open("{}/{}".format(os.path.dirname(os.path.realpath(__file__)), "../settings.json"))
settings = json.load(f)
f.close()

log_channel = settings["log_channel"]

async def log_message_edit(client, old, new):
    if not old.content == new.content:
        await client.send_message(discord.utils.get(old.server.channels, name=log_channel, type=discord.ChannelType.text), "{}\nUser {} edited their message in {}:\nOld: {}\nNew: {}".format(new.edited_timestamp.strftime("%Y-%m-%d %H:%M:%S UTC"), str(old.author), str(old.channel), old.content, new.content))

async def log_message_delete(client, message):
    await client.send_message(discord.utils.get(message.server.channels, name=log_channel, type=discord.ChannelType.text), "{}\nUser {} deleted their message in {}:\n{}\n".format(message.timestamp.strftime("%Y-%m-%d %H:%M:%S UTC"), str(message.author), str(message.channel), message.content))

# Now setup
def setup_hooks(hooktable):
    hooktable["edit"].append(log_message_edit)
    hooktable["delete"].append(log_message_delete)