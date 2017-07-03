# dice.py
# For various commands using random numbers or items.
import random

async def roll(message, client):
    args = message.content.split(sep=' ')
    # Ignore args[0] - it's !roll
    dice_args = args[1].split(sep='d')
    # There should only be two parts - XdY
    if not len(dice_args) == 2:
        await client.send_message(message.channel, "{} Sorry, that's not a valid roll. Valid rolls are in the form XdY.",format(message.author.mention))
        return
    # Try making them ints, if we can't they're not numbers
    try:
        amount = int(dice_args[0])
        die_size = int(dice_args[1])
    except ValueError:
        await client.send_message(message.channel, "{} Sorry, I can't roll something that's not a number!".format(message.author.mention))
        return
    finally:
        pass

    if amount < 1 or die_size < 1:
        await client.send_message(message.channel, "{} Sorry, I can't roll nothing.".format(message.author.mention))
        return

    roll_message = "{} Rolling {}d{} gives:\n".format(message.author.mention, amount, die_size)

    for i in range(amount):
        roll_message += str(random.randint(1, die_size))
        if not i + 1 == amount:
            roll_message += ", "
    await client.send_message(message.channel, roll_message)
