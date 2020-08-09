# help.py
# Controls the !help command.
import re

# Specify some text up here
pagetext = """Type !help (page number) to see that page's commands.
1 - Generic commands
2 - Roles"""

generictext = """**Generic Commands**
!nostalgia - Look at past messages from different channels, and relive the moment.
!8ball - Ask a question, get an answer!
!roll - Rolls dice. Submit in XdY.
!ping - Simple ping. That's all.
!about - Show information about the bot.
!help - List commands and get help on how to use the bot!"""

roletext = """**Role Commands**
If your server lets you self-assign roles, you'll be able to use these commands.

!listroles - Lists all the roles that can be given.
!giverole (role name) - Gives you a role.
!removerole (role name) - Removes a role from you."""

async def help(client, message):
	# If the length of the message is more than 6 characters, someone specified a page they'd like
    if len(message.content) > 6:
    	page = re.sub("!help ", "", message.content)
    else:
    	# If it isn't, no page is requested
    	page = False
    
    if not page:
    	await message.author.send(pagetext)
    elif page == "1":
    	await message.author.send(generictext)
    elif page == "2":
    	await message.author.send(roletext)
    else:
    	await message.author.send("Sorry, that's not a valid page number! Try !help to see a list of page numbers.")
    
    
    

# Add the commands to the global command table.
def setup_command_table(table):
    table["!help"] = help
