import json, os

settings = dict()

token = input("Enter your bot's token: ")
settings["token"] = token

f = open("{}/{}".format(os.path.dirname(os.path.realpath(__file__)), "settings.json"), 'w')
json.dump(settings, f)
f.close()
