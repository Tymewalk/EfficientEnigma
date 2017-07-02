# util.py
# Various utilities, such as !ping.
import discord, asyncio

async def ping(message, client):
    await client.send_message(message.channel, "{} :ping_pong: Pong!".format(message.author.mention))
