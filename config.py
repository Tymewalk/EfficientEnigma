import json, os

settings = dict()

token = input("Enter your bot's token: ")
settings["token"] = token

use_logging = ""

while not (use_logging == "y" or use_logging == "n"):
    use_logging = input("Would you like to log message edits and deletions? [yn] ").lower()[0]

if use_logging == "y":
    settings["use_logging"] = True
    log_channel = input("What channel would you like them to be logged in? ")
    settings["log_channel"] = log_channel
else:
    settings["use_logging"] = False

f = open("{}/{}".format(os.path.dirname(os.path.realpath(__file__)), "settings.json"), 'w')
json.dump(settings, f)
f.close()
