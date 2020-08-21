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
    return message.guild is not None

async def log_message_edit(client, old, new):
    # Log message edits.
    if is_in_server(old):
        # No sense in logging DMs
        load_settings()
        if settings[str(old.guild.id)]["use_logging"] == True:
            log_channel = settings[str(old.guild.id)]["log_channel"]
            if not old.content == new.content:
                await discord.utils.get(old.guild.channels, name=log_channel, type=discord.ChannelType.text).send("{}\nUser {} (ID {}) edited their message in {}:\nOld: {}\nNew: {}".format(new.edited_at.strftime("%Y-%m-%d %H:%M:%S UTC"), str(old.author), old.author.id, str(old.channel), old.content, new.content))

async def log_message_delete(client, message):
    # Log message deletions.
    if is_in_server(message):
        load_settings()
        if settings[str(message.guild.id)]["use_logging"] == True:
            log_channel = settings[str(message.guild.id)]["log_channel"]
            if message.channel.name is not settings[str(message.guild.id)]["log_channel"]:
                if message.attachments:
                    filename = message.attachments[0].filename
                    await discord.utils.get(message.guild.channels, name=log_channel, type=discord.ChannelType.text).send("{}\nMessage by {} (ID {}) was deleted in {}:\n{}\n".format(message.created_at.strftime("%Y-%m-%d %H:%M:%S UTC"), str(message.author), message.author.id, str(message.channel), message.content), file=discord.File(io.BytesIO(requests.get(message.attachments[0].proxy_url).content), filename=filename))
                else:
                    await discord.utils.get(message.guild.channels, name=log_channel, type=discord.ChannelType.text).send("{}\nMessage by {} (ID {}) was deleted in {}:\n{}\n".format(message.created_at.strftime("%Y-%m-%d %H:%M:%S UTC"), str(message.author), message.author.id, str(message.channel), message.content))

# Now setup
def setup_hooks(hooktable):
    hooktable["edit"].append(log_message_edit)
    hooktable["delete"].append(log_message_delete)