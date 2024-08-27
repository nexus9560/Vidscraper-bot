# This file is the main body of the bot, the idea is that the bot will sit in permitted channels waiting for a message with a [youtube] video to be posted, when someone does post...
# ... the youtube video the bot will grab the message, download, downscale and convert, take the original message and reply with an embed of the converted video.
# By default, all the channels in a server will be disabled for the bot, whatever channels the configurator wants the bot to lurk in ***must*** be enabled by the configurator.
# Further, by default, the bot will auto ignore any channels with the following labels:
#       >Staff
#       >Mod
#       >Admin
#       >NSFW

import discord
import Video_Downloader as VDL

class BotCore(discord.client):

    global token

    async def start(tkn = None):
        token =str(tkn)

