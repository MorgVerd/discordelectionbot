import os
try:
    import discord
    import asyncio
    from discord.ext.commands import Bot
    from discord.ext import commands
    import os, random
    import urllib.request
    import datetime
    import os.path
    import time
    import glob
    import operator
except ImportError as e:
    print("[Import Error] {}".format(e))

class UsrManagementSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def safe_reactdelete(self, reaction, usr):
        try:
            await reaction.remove(usr)
        except Exception:
            pass
        return

    def genericCheck(self, react, userObject):
        return True

    async def handleReact(self, messageObject, reacts, acceptedUser, timeout=60):
        bot = self.bot
        if messageObject is None: return (False, "")
        for react in reacts:
            await messageObject.add_reaction(react)
        while True:
            try:
                reaction, userObject = await self.bot.wait_for("reaction_Add", timeout=timeout, check=self.genericCheck) # Could use lambda but for the sake of changeability, Keep as genericCheck
                if reaction:
                    if userObject.id == acceptedUser.id:
                        if (str(reaction.emoji) in reacts):
                            return (True, reaction)
                        else:
                            await self.safe_reactdelete(reaction, userObject)
                    else:
                        if not userObject.id == self.bot.user.id:
                            await self.safe_reactdelete(reaction, userObject)
            except asyncio.TimeoutError:
                return (False, "")


    @commands.command(aliases=["lb", "liveunban", "lu"], pass_context=True)
    async def liveban(self, ctx, *, target: discord.Member = None):
        try:
            await ctx.message.delete()
        except Exception:
            pass
        check, reason = (await self.bot.isGov(self, ctx.message.author))
        if not check:
            await ctx.send("You do not have permission to use this command. Only the Government and Root users may use this!", delete_after=20)
            return

        target = target or ctx.author
        goLiveRole = discord.utils.get(ctx.guild.roles, id=698296284569927720)
        embedMessage = None; string = ""; img = ""

        while True:

            check, reason = (await self.bot.hasRole(self, target, '698296284569927720'))
            if check:
                string = "are **NOT**"
                img = "green"
            else:
                string = "**ARE**"
                img = "red"

            embedObject = discord.Embed(title="Live Unban/Ban")
            embedObject.set_thumbnail(url=f"https://img.morgverd.xyz/discord/status_{img}.png")
            embedObject.add_field(name=str(target.name), value=(f"{target.name} {string} banned from going live in any channel."), inline=True)
            embedObject.add_field(name="Help", value="Click 🟢 to unban / allow them to Go Live, alternatively click 🔴 to ban / disallow them from going Live. You can also click 🛑 to exit this message.", inline=False)
            embedObject.add_field(name="Warning", value="Due to how Discord handles permissions, Those with ``Root`` permissions will override this ban when going live.", inline=False)
            
            if embedMessage is None:
                embedMessage = await ctx.send(embed=embedObject)
            else:
                await embedMessage.edit(embed=embedObject)

            success, reaction = await self.handleReact(embedMessage, ["🟢", "🔴", "🛑"], ctx.message.author, timeout=30) # Green and Red emoji
            if not success:
                await ctx.send(":warning: You took too long!", delete_after=20)
                break
            else:
                await self.safe_reactdelete(reaction, ctx.message.author)
                if str(reaction.emoji) == "🛑":
                    break
                if str(reaction.emoji) == "🟢":
                    # Unban
                    await target.add_roles(goLiveRole, reason=("Unbanned by " + str(ctx.message.author)))                
                if str(reaction.emoji) == "🔴":
                    # Ban
                    await target.remove_roles(goLiveRole, reason=("Banned by " + str(ctx.message.author)))
        try:
            await embedMessage.delete()
        except Exception:
            pass



    @commands.command(aliases=["m", "um", "unmute"], pass_context=True)
    async def mute(self, ctx, *, target: discord.Member = None):
        try:
            await ctx.message.delete()
        except Exception:
            pass
        check, reason = (await self.bot.isGov(self, ctx.message.author))
        if not check:
            await ctx.send("You do not have permission to use this command. Only the Government and Root users may use this!", delete_after=20)
            return

        check, reason = (await self.bot.isGov(self, target))
        if check:
            await ctx.send("You may not mute a user with Government status or ``Root`` permissions.", delete_after=20)
            return


        target = target or ctx.author
        mutedRole = discord.utils.get(ctx.guild.roles, id=699287554184184004)
        embedMessage = None; string = ""; img = ""

        while True:

            check, reason = (await self.bot.hasRole(self, target, '699287554184184004'))
            if not check:
                string = "are **NOT**"
                img = "green"
            else:
                string = "**ARE**"
                img = "red"

            embedObject = discord.Embed(title="Live Unban/Ban")
            embedObject.set_thumbnail(url=f"https://img.morgverd.xyz/discord/status_{img}.png")
            embedObject.add_field(name=str(target.name), value=(f"{target.name} {string} muted from chat."), inline=True)
            embedObject.add_field(name="Help", value="Click 🟢 to unban / allow them to message in chat, alternatively click 🔴 to ban / disallow them from messaging. You can also click 🛑 to exit this message.", inline=False)
            embedObject.add_field(name="Warning", value="Due to how Discord handles permissions, Those with ``Root`` permissions will override this ban when going live.", inline=False)
            
            if embedMessage is None:
                embedMessage = await ctx.send(embed=embedObject)
            else:
                await embedMessage.edit(embed=embedObject)

            success, reaction = await self.handleReact(embedMessage, ["🟢", "🔴", "🛑"], ctx.message.author, timeout=30) # Green and Red emoji
            if not success:
                await ctx.send(":warning: You took too long!", delete_after=20)
                break
            else:
                await self.safe_reactdelete(reaction, ctx.message.author)
                if str(reaction.emoji) == "🛑":
                    break
                if str(reaction.emoji) == "🔴":
                    # Ban
                    await target.add_roles(mutedRole, reason=("Muted by " + str(ctx.message.author)))                
                if str(reaction.emoji) == "🟢":
                    # Unmute
                    await target.remove_roles(mutedRole, reason=("Unmuted by " + str(ctx.message.author)))
        try:
            await embedMessage.delete()
        except Exception:
            pass


    @commands.command(pass_context=True)
    async def verify(self, ctx, target: discord.Member = None):
        try:
            await ctx.message.delete()
        except Exception:
            pass
        if (not str(ctx.message.channel.id) == "699286875843723328"): return # Only in unverified talk
        check, reason = (await self.bot.isGov(self, ctx.message.author))
        if not check:
            await ctx.send("You do not have permission to use this command. Only the Government and Root users may use this!", delete_after=20)
            return
        verificationCheck, reason = (await self.bot.hasRole(self, target, "699286702467842058"))
        if verificationCheck:
            await ctx.send("This user is already verified!", delete_after=20)
            return
        
        verifiedRole = discord.utils.get(ctx.guild.roles, id=699286702467842058); await target.add_roles(verifiedRole, reason=("User verified by " + str(ctx.message.author.name)))
        canGoLiveRole = discord.utils.get(ctx.guild.roles, id=698296284569927720); await target.add_roles(canGoLiveRole, reason=("User verified by " + str(ctx.message.author.name)))
        canChangeNicknameRole = discord.utils.get(ctx.guild.roles, id=701563649747189850); await target.add_roles(canChangeNicknameRole, reason=("User verified by " + str(ctx.message.author.name)))

        generalChannel = discord.utils.get(ctx.guild.channels, id=699287508688699392)
        await generalChannel.send(f"Welcome <@{str(target.id)}>")
        return


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
            await ctx.send(embed=(await self.bot.generate_error(self, err)), delete_after=20)
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
    bot.add_cog(UsrManagementSystem(bot))