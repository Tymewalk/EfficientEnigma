# EfficientEnigma
*A Discord bot that works well, for no reason at all.*

## Setup and Installation
Step 1: Clone the repository:

    cd /path/to/where/you/want/the/files/
    git clone https://github.com/Tymewalk/EfficientEnigma/
    cd EfficientEnigma
    
Step 2: Install dependencies:

    pip3 install discord-py asyncio aiohttp
    
Step 3: Set up the bot:

    python3.5 config.py

You will be prompted for your bot's token.

Step 4: Run the bot:

    python3.5 bot.py

## Configuration
Anyone with a role titled "EfficientEnigma Admin" may use the bot's internal configuration commands to set up the bot for their server.

## List of Admin commands

$logtoggle (on/off) - Turns message edit/deletion logging on and off. Default: off
$logchannel #(channel) - Sets the channel that edit/deletion messages will be logged in. Default: modlog
$allowrole (role name) - Allows users to assign a role to themselves.
$forbidrole (role name) - Forbids users from assigning a role to themselves.
$startoggle (on/off) - Turns the starboard on and off. Default: off
$starchannel #(channel) - Sets the channel starred messages will be placed in. Default: starboard
$staremoji (emoji) - Sets the emoji users react with to star messages. Default: :star:
$starreq (number) - Sets how many stars a message must get to be sent to the starboard. Default: 3