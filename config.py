import json, os


token = input("Enter your bot's token: ")

# Check if there are already settings - if not, just initialize them
if os.path.isfile("{}/{}".format(os.path.dirname(os.path.realpath(__file__)), "settings.json")):
	f = open("{}/{}".format(os.path.dirname(os.path.realpath(__file__)), "settings.json"), 'r')
	settings = json.load(f)
	f.close()
else:
	settings = dict()

settings["token"] = token
f = open("{}/{}".format(os.path.dirname(os.path.realpath(__file__)), "settings.json"), 'w')
json.dump(settings, f)
f.close()
