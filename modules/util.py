# util.py
# Various utilities, such as !ping.
import aiohttp, time

async def ping(client, message):
    aiosession = aiohttp.ClientSession(loop=client.loop)
    start = time.time()
    async with aiosession.get('https://discordapp.com'):
        duration = time.time() - start
    duration = round(duration * 1000)
    await message.channel.send("{} :ping_pong: Pong! (**{}ms**)".format(message.author.mention, duration))
    aiosession.close()

# Add the commands to the global command table.
def setup_command_table(table):
    table["!ping"] = ping