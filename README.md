# EfficientEnigma
*A Discord bot that works well, for no reason at all.*

## Setup and Installation
Step 1: Clone the repository:

    cd /path/to/where/you/want/the/files/
    git clone https://github.com/Tymewalk/EfficientEnigma/
    cd EfficientEnigma
    
Step 2: Install dependencies:

    pip3 install -r requirements.txt
    
Step 3: Set up the bot:

    python3.5 config.py

You will be prompted for your bot's token.

Step 4: Run the bot:

    python3.5 bot.py

## Configuration
Anyone with a role titled "EfficientEnigma Admin" may use the bot's internal configuration commands to set up the bot for their server.

## List of Admin commands

$settings - Display the current server's settings.

$logtoggle (on/off) - Turns message edit/deletion logging on and off. Default: off

$logchannel #(channel) - Sets the channel that edit/deletion messages will be logged in. Default: modlog

$allowrole (role name) - Allows users to assign a role to themselves.

$forbidrole (role name) - Forbids users from assigning a role to themselves.

$allowadminrole (role name) - Allows users with this role to edit EfficientEnigma's settings. By default, the role "EfficientEnigma Admin" will always be allowed to edit settings. This can not be changed - otherwise, users could lock themselves out of the bot.

$forbidadminrole (role name) - Forbids users with this role from editing EfficientEnigma's settings, if they were previously able to. (NOTE: If a user has another admin role, they will still be able to edit settings!)

$startoggle (on/off) - Turns the starboard on and off. Default: off

$starchannel #(channel) - Sets the channel starred messages will be placed in. Default: starboard

$staremoji (emoji) - Sets the emoji users react with to star messages. Default: :star:

$starreq (number) - Sets how many stars a message must get to be sent to the starboard. Default: 3

$selfstar (on/off) - Sets whether or not users may star their own posts to get them on the starboard. Default: off

$welcometoggle (on/off) - Turns the welcome message on and off. Default: off

$welcomemessage (message) - Sets the messsage to be sent. `<name>` replaces it with the user's name, whereas `<ping>` pings the user. Default: `<ping> Welcome to our server, <name>!`

$welcomechannel #(channel) - Set the channel that welcome messages get sent in. Default: welcome

$leavetoggle (on/off) - Turns the message when a member leaves on and off. Default: off

$leavemessage (message) - Sets the messsage to be sent. `<name>` replaces it with the user's name, whereas `<ping>` pings the user. Default: `What a shame, <name> just left the server...`

$leavechannel #(channel) - Set the channel that leaving messages get sent in. Default: welcome