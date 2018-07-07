# nostalgia.py
# Handles the !nostalgia command.
import random, calendar, re, discord.utils, time, requests, io
from datetime import datetime

async def nostalgia(message, client):
    # Pulls up a random message.
    searchin = False
    cansearch = True
    # If the user specified a channel, use it, otherwise just default to the current one.
    if re.findall("<#[0-9]+>", message.content):
        searchin = message.server.get_channel(re.sub("[\<\#\>]", "", re.findall("<#[0-9]+>", message.content)[0]))
    else:
        searchin = message.channel
    # Check if the user can read the channel - if this wasn't here, anyone with the ID could read the channel!
    if searchin.permissions_for(message.author).read_messages == False:
        await client.send_message(message.channel, "You don't have permission to see messages from that channel!")
        cansearch = False
    if cansearch:
        messagelist = list()
        # discord.py doesn't like you taking huge numbers of messages, so instead, we pick a random time.
        randomtime = datetime.utcfromtimestamp(random.randint(calendar.timegm(searchin.created_at.timetuple()), calendar.timegm(time.gmtime())))
        # discord.py also doesn't like taking just one, so we take 3 and make it even.
        async for scan in client.logs_from(searchin, limit=3, around=randomtime):
            messagelist.append(scan)
        # Then we just pick one anyways.
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
        # Grab any attachments if the message has them - so we don't get lots of blank messages that actually had files.
        if rand_message.attachments:
            filename = rand_message.attachments[0]["filename"]
            await client.send_file(message.channel, io.BytesIO(requests.get(rand_message.attachments[0]["proxy_url"]).content), filename=filename, content="At {}, {} said:\n\n{}".format(rand_message.timestamp.strftime("%Y-%m-%d %H:%M:%S UTC"), rand_message.author.name, output))
        else:
            await client.send_message(message.channel, "At {}, {} said:\n\n{}".format(rand_message.timestamp.strftime("%Y-%m-%d %H:%M:%S UTC"), rand_message.author.name, output))

# Add the commands to the global command table.
def setup_command_table(table):
    table["!nostalgia"] = nostalgia
