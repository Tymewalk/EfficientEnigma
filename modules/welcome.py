# welcome.py
# Handles the welcome message for the server.
import discord, asyncio, re

settings = dict()

def format_welcome_message(member, message):
	message = re.sub("<ping>", member.mention, message)
	message = re.sub("<name>", member.name, message)
	return message

async def announce_welcome(client, member):
	load_settings()
	server = member.server
	welcome_channel = settings[server.id]["welcome_channel"]
	await client.send_message(discord.utils.get(server.channels, name=welcome_channel, type=discord.ChannelType.text), format_welcome_message(member, settings[server.id]["welcome_message"]))

def setup_hooks(hooktable):
    hooktable["member_join"].append(announce_welcome)