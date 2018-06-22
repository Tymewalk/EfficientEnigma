# logging.py
# Logs various user activities like message edits and deletions.
import discord.utils, asyncio, os, json, requests, io

# We create a settings dict because otherwise it complains it hasn't been initialized.
settings = dict()

def load_settings():
    # Load the settings.
    global settings
    f = open("{}/{}".format(os.path.dirname(os.path.realpath(__file__)), "../settings.json"))
    settings = json.load(f)
    f.close()

def is_in_server(message):
    # Check if we're in a server.
    return message.server is not None

async def log_message_edit(client, old, new):
    # Log message edits.
    if is_in_server(old):
        # No sense in logging DMs
        load_settings()
        if settings[old.server.id]["use_logging"] == True:
            log_channel = settings[old.server.id]["log_channel"]
            if not old.content == new.content:
                await client.send_message(discord.utils.get(old.server.channels, name=log_channel, type=discord.ChannelType.text), "{}\nUser {} (ID {}) edited their message in {}:\nOld: {}\nNew: {}".format(new.edited_timestamp.strftime("%Y-%m-%d %H:%M:%S UTC"), str(old.author), old.author.id, str(old.channel), old.content, new.content))

async def log_message_delete(client, message):
    # Log message deletions.
    if is_in_server(message):
        load_settings()
        if settings[message.server.id]["use_logging"] == True:
            log_channel = settings[message.server.id]["log_channel"]
            if message.channel.name is not settings[message.server.id]["log_channel"]:
                if message.attachments:
                    filename = message.attachments[0]["filename"]
                    await client.send_file(discord.utils.get(message.server.channels, name=log_channel, type=discord.ChannelType.text), io.BytesIO(requests.get(message.attachments[0]["proxy_url"]).content), filename=filename, content="{}\nMessage by {} (ID {}) was deleted in {}:\n{}\n".format(message.timestamp.strftime("%Y-%m-%d %H:%M:%S UTC"), str(message.author), message.author.id, str(message.channel), message.content))
                else:
                    await client.send_message(discord.utils.get(message.server.channels, name=log_channel, type=discord.ChannelType.text), "{}\nMessage by {} (ID {}) was deleted in {}:\n{}\n".format(message.timestamp.strftime("%Y-%m-%d %H:%M:%S UTC"), str(message.author), message.author.id, str(message.channel), message.content))

# Now setup
def setup_hooks(hooktable):
    hooktable["edit"].append(log_message_edit)
    hooktable["delete"].append(log_message_delete)