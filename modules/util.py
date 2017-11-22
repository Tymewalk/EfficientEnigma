# util.py
# Various utilities, such as !ping.
async def ping(message, client):
    await client.send_message(message.channel, "{} :ping_pong: Pong!".format(message.author.mention))

# Add the commands to the global command table.
def setup_command_table(table):
    table["!ping - Literally just ping."] = ping
