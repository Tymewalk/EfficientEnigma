# dice.py
# For various commands using random numbers or items.
import random

eight_ball_phrases = [
    # Positive
    "Yes", "It is certain", "Of course", ":100:", "Definitely",
    # Neutral
    "Maybe", "Perhaps", "I'm not sure", "Reply hazy, ask again", "Who knows?",
    # Negative
    "No", "Of course not", "Never", "Absolutely not", "Not a chance"
    ]

async def magic_eight_ball(client, message):
    # Magic 8 Ball - ask a question, get an answer.
    await message.channel.send("{} {}".format(message.author.mention, random.choice(eight_ball_phrases)))

async def roll(client, message):
    # Roll dice.
    args = message.content.split(sep=' ')
    # Ignore args[0] - it's !roll
    dice_args = args[1].split(sep='d')
    # There should only be two parts - XdY
    if not len(dice_args) == 2:
        await message.channel.send("{} Sorry, that's not a valid roll. Valid rolls are in the form XdY.".format(message.author.mention))
        return
    # Try making them ints, if we can't they're not numbers and we shouldn't be rolling them
    try:
        amount = int(dice_args[0])
        die_size = int(dice_args[1])
    except ValueError:
        await message.channel.send("{} Sorry, I can't roll something that's not a number!".format(message.author.mention))
        return
    finally:
        pass

    if amount < 1 or die_size < 1:
        await message.channel.send("{} Sorry, I can't roll nothing.".format(message.author.mention))
        return

    if amount > 250 or die_size > 1000:
        await message.channel.send("{} Sorry, that roll is too big! Please limit your rolls to 250d1000.".format(message.author.mention))
        return

    roll_message = "{} Rolling {}d{} gives:\n".format(message.author.mention, amount, die_size)

    for i in range(amount):
        roll_message += str(random.randint(1, die_size))
        if not i + 1 == amount:
            roll_message += ", "
    await message.channel.send(roll_message)

# Add the commands to the global command table.
def setup_command_table(table):
    table["!8ball"] = magic_eight_ball
    table["!roll"] = roll