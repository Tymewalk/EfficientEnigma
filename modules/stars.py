# stars.py
# Monitors messages for stars and posts them to the assigned starboard channel.
import asyncio, discord, os, json, io, requests

# We create a settings dict because otherwise it complains it hasn't been initialized.
settings = dict()

def load_settings():
    # Load the settings.
    global settings
    f = open("{}/{}".format(os.path.dirname(os.path.realpath(__file__)), "../settings.json"))
    settings = json.load(f)
    f.close()

starred_messages = list()

async def check_for_starring(client, reaction, user):
     # For simplicity
     global starred_messages
     load_settings()
     message = reaction.message
     if settings[str(message.guild.id)]["use_stars"]:
        star_channel = settings[str(message.guild.id)]["star_channel"]
        if not message in starred_messages:
             reactions = 0 
             for reaction in message.reactions:
                if reaction.emoji == settings[str(message.guild.id)]["star_emoji"]:
                    reaction_users = await reaction.users().flatten()
                    # Make sure the author is in before removing them, or the program crashes
                    if not settings[str(message.guild.id)]["self_star"] and message.author in reaction_users:
                        reaction_users.remove(message.author)
                    reactions = len(reaction_users)
             if reactions >= settings[str(message.guild.id)]['star_requirement']:
                 starred_messages.append(message)
                 if message.attachments:
                    filename = message.attachments[0].filename
                    await discord.utils.get(message.guild.channels, name=star_channel, type=discord.ChannelType.text).send( "{}\n{} said in {}:\n{}\n".format(message.created_at.strftime("%Y-%m-%d %H:%M:%S UTC"), message.author.mention, str(message.channel), message.content), file=discord.File(io.BytesIO(requests.get(message.attachments[0].proxy_url).content), filename=filename))
                 else:
                    await discord.utils.get(message.guild.channels, name=star_channel, type=discord.ChannelType.text).send("{}\n{} said in {}:\n{}\n".format(message.created_at.strftime("%Y-%m-%d %H:%M:%S UTC"), message.author.mention, str(message.channel), message.content))

# Now setup
def setup_hooks(hooktable):
    hooktable["reaction_add"].append(check_for_starring)
