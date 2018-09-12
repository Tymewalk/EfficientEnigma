# about.py
# Commands that show information about the bot.

async def about(client, message):
    await client.send_message(message.channel, "{} I'm EfficientEnigma, a Discord bot created by Tymewalk!\nFollow my development here: https://github.com/Tymewalk/EfficientEnigma\nYou can also report issues on the GitHub page, and see a useful list of commands, too!".format(message.author.mention))

# Add the commands to the global command table.
def setup_command_table(table):
    table["!about"] = about