# logging.py
# Logs various user activities like message edits and deletions.
import discord.utils

log_channel = "(set this)"

async def on_message_edit(old, new):
	await client.send_message(discord.utils.get(old.server, name=log_channel, type=discord.ChannelType.text), "User {} edited a message:\nOld: {}\nNew: {}".format(str(message.author), old.content, new.content))