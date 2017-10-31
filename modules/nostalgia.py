# nostalgia.py
# Handles the !nostalgia command.
import random, calendar, re, discord.utils, time, requests, io
from datetime import datetime

titles = ["teacher", "scientist", "scholar", "leader", "fighter", "mage", "wizard", "noble", "swordsman", "rifleman", "archer"]
async def nostalgia(message, client):
    searchin = False
    if re.findall("<#[0-9]+>", message.content):
        searchin = message.server.get_channel(re.sub("[\<\#\>]", "", re.findall("<#[0-9]+>", message.content)[0]))
    else:
        searchin = message.channel
    messagelist = list()
    randomtime = datetime.utcfromtimestamp(random.randint(calendar.timegm(searchin.created_at.timetuple()), calendar.timegm(time.gmtime())))
    async for scan in client.logs_from(searchin, limit=3, around=randomtime):
        messagelist.append(scan)
    rand_message = random.choice(messagelist)
    output = rand_message.content
    # Filter user pings
    for m in re.findall("<@[0-9]+>", output):
        userid = re.sub("[\<\@\>]", "", m)
        output = re.sub(m, "\@{}".format(str(message.server.get_member(userid))[:-5]), output)
    # Filter another type of user pings
    for m in re.findall("<@![0-9]+>", output):
        userid = re.sub("[\<\@\!\>]", "", m)
        output = re.sub(m, "\@{}".format(str(message.server.get_member(userid))[:-5]), output)
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

    if rand_message.attachments:
        filename = rand_message.attachments[0]["filename"]
        await client.send_file(message.channel, io.BytesIO(requests.get(rand_message.attachments[0]["proxy_url"]).content), filename=filename, content="The great {} \"{}\" once said:\n\n{}".format(random.choice(titles), rand_message.author.name, output))
    else:
        await client.send_message(message.channel, "The great {} \"{}\" once said:\n\n{}".format(random.choice(titles), rand_message.author.name, output))

# Add the commands to the global command table.
def setup_command_table(table):
    table["!nostalgia"] = nostalgia