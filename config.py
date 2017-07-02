token = input("Enter your bot's token: ")
f = open("{}/{}".format(os.path.dirname(os.path.realpath(__file__)), "token"), 'w')
f.write(token)
f.close()
