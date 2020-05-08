
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

    async def permissions_isgov(self, user, excludeRoot = False):
        root = 674620226494791720 # 674620226494791720
        idBank = [706267350458040363, 700362039461150773] # Elected Admin Powers, Council Powers
        govRoleIDs = []
        if excludeRoot:
            govRoleIDs = idBank
        else:
            govRoleIDs.append(root)
            for ID in idBank:
                govRoleIDs.append(ID)

        for govRoleID in govRoleIDs:
            check, reason = (await self.bot.hasRole(self, user, str(govRoleID)))
            if check:
                return (True, "User has role")
        return (False, "You are missing the needed role to do this.")

