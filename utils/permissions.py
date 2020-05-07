
import asyncio, aiohttp, discord, async_timeout, pytz, time
import os, sys, linecache, async_timeout, inspect, traceback
import re, math, random, uuid, time
from datetime import datetime
import os.path


class Permissions():
    def __init__(self, bot, cursor):
        self.bot = bot
        self.session = aiohttp.ClientSession()
        self.tz = pytz.timezone('UTC')

    async def permissions_hasrole(self, user, roleid):
        bot = self.bot
        for role in user.roles:
            if (roleid == str(role.id)): return (True, "User has role")
        return (False, "You are missing the needed role to do this.")


def setup(bot):
    bot.add_cog(Permissions(bot))