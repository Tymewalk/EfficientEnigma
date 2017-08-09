# logging.py
# Logs various user activities like message edits and deletions.
import discord.utils, asyncio

log_channel = "(set this)"

async def log_message(client, old, new):
	await client.send_message(discord.utils.get(old.server.channels, name=log_channel, type=discord.ChannelType.text), "User {} edited a message:\nOld: {}\nNew: {}".format(str(old.author), old.content, new.content))