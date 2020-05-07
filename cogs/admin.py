import discord, asyncio
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
import urllib, random
import os

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(pass_context=True)
    async def cut(self, ctx, limit: int = 1):
        try:
            await ctx.message.delete()
        except Exception:
            pass
        permCheck, reason = (await self.bot.hasRole(self, ctx.message.author, "674620226494791720"))
        if permCheck:
            await ctx.channel.purge(limit=limit)
            await ctx.send('``{}`` messages were cleared by {}'.format(limit, ctx.author.mention), delete_after=20)
        else:
            await ctx.send(embed=(await self.bot.generate_error(self, err)))
        return
        
    @commands.command(pass_context=True)
    async def echo(self, ctx, *, message):
        try:
            await ctx.message.delete()
        except Exception:
            pass
        permCheck, reason = (await self.bot.hasRole(self, ctx.message.author, "674620226494791720"))
        if permCheck:
            await ctx.send(message)
        else:
            return
        return

def setup(bot):
    bot.add_cog(Admin(bot))