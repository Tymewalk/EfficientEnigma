import discord, asyncio, os, re
import modules.util

client = discord.Client()

f = open("{}/{}".format(os.path.dirname(os.path.realpath(__file__)), "token"))
# Discord tokens have no whitespace, remove any that might've slipped in there
bot_token = f.read().rstrip().lstrip()
f.close()

@client.event
async def on_ready():
    print('Successfully logged in as {} (ID {}).'.format(client.user.name, client.user.id))

@client.event
async def on_message(message):
    if re.search("^!ping", message.content):
        await modules.util.ping(message, client)

try:
    # If any background tasks need to run, start them here
    client.run(bot_token)
except KeyboardInterrupt:
    # Properly exit if we get a Ctrl-C
    client.logout()
finally:
    # If anything needs to save, do it here
    print("Done running.")
