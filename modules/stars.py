# stars.py
# Monitors messages for stars and posts them to the assigned starboard channel.
import asyncio, discord, os, json

# We create a settings dict because otherwise it complains it hasn't been initialized.
settings = dict()

def load_settings():
    # Load the settings.
    global settings
    f = open("{}/{}".format(os.path.dirname(os.path.realpath(__file__)), "../settings.json"))
    settings = json.load(f)
    f.close()

speed = 1

async def check_for_starring(client, reaction, user):
     # For simplicity
     load_settings()
     message = reaction.message
     star_channel = settings[message.server.id]["star_channel"]
     if settings[message.server.id]["use_stars"]:
         reactions = 0 
         for e in message.reactions:
            if e.emoji == settings[message.server.id]["star_emoji"]:
                reactions = e.count
         if reactions >= settings[message.server.id]['star_requirement']:
             if message.attachments:
                filename = message.attachments[0]["filename"]
                await client.send_file(discord.utils.get(message.server.channels, name=star_channel, type=discord.ChannelType.text), io.BytesIO(requests.get(message.attachments[0]["proxy_url"]).content), filename=filename, content="{}\n{} said in {}:\n{}\n".format(message.timestamp.strftime("%Y-%m-%d %H:%M:%S UTC"), message.author.mention, str(message.channel), message.content))
             else:
                await client.send_message(discord.utils.get(message.server.channels, name=star_channel, type=discord.ChannelType.text), "{}\n{} said in {}:\n{}\n".format(message.timestamp.strftime("%Y-%m-%d %H:%M:%S UTC"), message.author.mention, str(message.channel), message.content))

# Now setup
def setup_hooks(hooktable):
    hooktable["reaction_add"].append(check_for_starring)