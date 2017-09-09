# nostalgia.py
# Handles the !nostalgia command.
import random, calendar, re, discord.utils
from datetime import datetime
from datetime import *

titles = ["teacher", "scientist", "scholar", "leader", "fighter", "mage", "wizard", "noble", "swordsman", "rifleman", "archer"]
async def nostalgia(message, client):
    messagelist = list()
    randomtime = datetime.utcfromtimestamp(random.randint(calendar.timegm(message.channel.created_at.timetuple()), calendar.timegm(datetime.now().timetuple())))
    async for message in client.logs_from(message.channel, limit=3, around=randomtime):
        messagelist.append(message)
    rand_message = random.choice(messagelist)
    output = rand_message.content
    # Filter user pings
    for m in re.findall("<@[0-9]+>", output):
        userid = re.sub("[\<\@\>]", "", m)
        output = re.sub(m, "{}".format(str(message.server.get_member(userid))[:-5]), output)
    # Filter another type of user pings
    for m in re.findall("<@![0-9]+>", output):
        userid = re.sub("[\<\@\!\>]", "", m)
        output = re.sub(m, "{}".format(str(message.server.get_member(userid))[:-5]), output)
    # Filter role pings
    for m in re.findall("<@&[0-9]+>", output):
        roleid = re.sub("[\<\@\&\>]", "", m)
        output = re.sub(m, "\@{}".format(discord.utils.get(message.server.roles, id=roleid).name), output)
    # Filter everyone pings
    for m in re.findall("@everyone", output):
        output = re.sub(m, "(everyone)", output)
    # Filter here pings
    for m in re.findall("@here", output):
        output = re.sub(m, "(here)", output)
    await client.send_message(message.channel, "The great {} \"{}\" once said:\n\n{}".format(random.choice(titles), rand_message.author.name, output))

# Add the commands to the global command table.
def setup_command_table(table):
    table["!nostalgia"] = nostalgia