# help.py
# Controls the !help command.

async def help(message, client):
	# TEMPORARY - WILL BE REMOVED SOON
    await client.send_message(message.channel, """Here's a list of what I can do:
!nostalgia - Look at past messages from different channels, and relive the moment.
!8ball - Ask a question, get an answer!
!giverole - Gives you a role.
!roll - Rolls dice. Submit in XdY.
!listroles - Lists all the roles that can be given.
!ping - Simple ping. That's all.
!removerole - Removes a role from you.
!about - Show information about the bot.""")

# Add the commands to the global command table.
def setup_command_table(table):
    table["!help"] = help
