import aiohttp, time

# util.py
# Various utilities, such as !ping.
async def ping(message, client):
    start = time.time()
    async with aiosession.get('https://discordapp.com'):
        duration = time.time() - start
    duration = round(duration * 1000)
    await client.send_message(message.channel, "{} :ping_pong: Pong! (**{}ms**)".format(message.author.mention, duration))

# Add the commands to the global command table.
def setup_command_table(table, helptable):
    table["!ping"] = ping

    helptable["!ping"] = "Simple ping. That's all."
