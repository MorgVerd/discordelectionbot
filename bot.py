import os
try:
    import discord
    import asyncio
    from discord.ext.commands import Bot
    from discord.ext import commands
    import os, random
    import urllib.request
    import datetime
except ImportError as e:
    print("[Import Error] {}".format(e))

# Government Bot
class config:
    botOwners = ["325721852058271755"]
    speakerUserID = "325721852058271755"
    electionChannelID = "699299380586348665"
    votedAdminID = "706265884926148678"
    councilRoleID = "699290566587842571"

from utils.permissions import Permissions
bot = commands.Bot(command_prefix="?")
bot.votingActive = False
bot.cachedMembers = []
bot.electionCategory = None
bot.electionChannels = []
bot.hasRole = Permissions.permissions_hasrole

try:
    bot.remove_command("help")
except Exception as e: 
    print("[Help Command] ".format(e))

@bot.event
async def on_ready():
    print('Logged in as '+bot.user.name+' (ID:'+str(bot.user.id)+')')




if __name__ == "__main__":
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')
            print(f"[LAUNCHER][INFO] Loaded Cog : {filename[:-3]}")


bot.run(open("token.txt", "r").read().replace("\n", ""))
