# logging.py
# Logs various user activities like message edits and deletions.
import discord.utils, asyncio

log_channel = "(set this)"

async def log_message_edit(client, old, new):
	if not old.content == new.content:
		await client.send_message(discord.utils.get(old.server.channels, name=log_channel, type=discord.ChannelType.text), "User {} edited their message in {}:\nOld: {}\nNew: {}".format(str(old.author), str(old.channel), old.content, new.content))

async def log_message_delete(client, message):
	await client.send_message(discord.utils.get(message.server.channels, name=log_channel, type=discord.ChannelType.text), "User {} deleted their message in {}:\n{}\n".format(str(message.author), str(message.channel), message.content))

# Now setup
def setup_hooks(hooktable):
	hooktable["edit"].append(log_message_edit)
	hooktable["delete"].append(log_message_edit)