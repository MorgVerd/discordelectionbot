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

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Ready!')
        print('Logged in as ---->', self.bot.user)
        print('ID:', self.bot.user.id)
        return

    async def giveUserGovRole(self, role, member):
        govRoleCheck, reason = (await self.bot.hasRole(self, member, "708026215264419963"))
        if not govRoleCheck:
            await member.add_roles(role)
        return

    async def takeUserGovRole(self, role, member):
        govRoleCheck, reason = (await self.bot.hasRole(self, member, "708026215264419963"))
        if govRoleCheck:
            await member.remove_roles(role)
        return

    @commands.Cog.listener()
    async def on_member_update(self, memberBefore, memberAfter):

        if self.bot.cachedGovRole is None:
            self.bot.cachedGovRole = discord.utils.get(memberAfter.guild.roles, id=708026215264419963)

        wasUserAlreadyGov, reason = (await self.bot.isGov(self, memberBefore, excludeRoot=True))
        if not wasUserAlreadyGov:
            # User was not apart of the government originally
            userIsNowGov, reason = (await self.bot.isGov(self, memberBefore, excludeRoot=True))
            if userIsNowGov:
                # User was not orignally apart of the government, They are now
                await self.giveUserGovRole(self.bot.cachedGovRole, memberAfter)
                return

            else:
                # User was not apart of the government, and they still are not
                await self.takeUserGovRole(self.bot.cachedGovRole, memberAfter)
                return
        else:
            # User was apart of the government
            isUserStillGov, reason = (await self.bot.isGov(self, memberAfter, excludeRoot=True))
            if isUserStillGov:
                # User is still apart of the government
                await self.giveUserGovRole(self.bot.cachedGovRole, memberAfter)
                return

            else:
                # User was originally government, They are no longer
                # Remove their government role if they still have it
                await self.takeUserGovRole(self.bot.cachedGovRole, memberAfter)
                return

def setup(bot):
    bot.add_cog(Events(bot))