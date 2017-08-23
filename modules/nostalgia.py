# util.py
# Various utilities, such as !ping.
import random, calendar
from datetime import datetime
from datetime import *

titles = ["teacher", "scientist", "scholar", "leader", "fighter", "mage", "wizard", "noble", "swordsman", "rifleman", "archer"]
async def nostalgia(message, client):
    messagelist = list()
    randomtime = datetime.utcfromtimestamp(random.randint(calendar.timegm(message.channel.created_at.timetuple()), calendar.timegm(datetime.now().timetuple())))
    async for message in client.logs_from(message.channel, limit=3, around=randomtime):
        messagelist.append(message)
    rand_message = random.choice(messagelist)
    await client.send_message(message.channel, "The great {} \"{}\" once said:\n\n{}".format(random.choice(titles), rand_message.author.name, rand_message.content))

# Add the commands to the global command table.
def setup_command_table(table):
    table["!nostalgia"] = nostalgia