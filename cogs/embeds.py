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
except ImportError as e:
    print("[Import Error] {}".format(e))


class Embeds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

"""
    @commands.command()
    async def events(self, ctx):
        try:
            await ctx.delete()
        except Exception:
            pass

        # Monday
        # Wednesday
        # Friday


        gameNightEmbed = discord.Embed(title="Game Night")
        gameNightEmbed.set_image(url="https://img.morgverd.xyz/discord/gamenight.png")
        gameNightEmbed.add_field(name="When?", value="Game Night is every **Monday** at **8pm**", inline=False)
        gameNightEmbed.add_field(name="Want to join us?", value="Since there is no special roles or anything for this, If you want to join just drop along into the channel when its happening!", inline=False)
        gameNightEmbed.add_field(name="What do we play?", value="No clue. Sometimes it will be Jackbox, Or TTT, or CS, or fucking Scribble.io. Who knows?", inline=False)
        gameNightEmbed.add_field(name="Organiser", value="Since ``Game Night`` is a bit bigger, both <@336521285658083329> and <@325721852058271755> will be in charge.")

        randomNightEmbed = discord.Embed(title="Random Night")
        randomNightEmbed.set_image(url="https://img.morgverd.xyz/discord/randomnight.png")
        randomNightEmbed.add_field(name="When?", value="The Random Night will happen every **Wednesday** at **8pm**", inline=False)
        randomNightEmbed.add_field(name="Want to join us?", value="Same as ``Game Night``, If you want to join us just drop on down. Anyone can join!", inline=False)
        randomNightEmbed.add_field(name="What do we do?", value="Its random. Nobody knows. We could watch a Movie, Play a game, Just talk, Watch Reeve do some dodgy shit on his PC again, The sky is the limit!", inline=False)
        randomNightEmbed.add_field(name="Organiser", value="<@219502433380990976> is organising ``Random Night`` so he will be thinking of shit to keep us entertained basically.")
        
        movieNightEmbed = discord.Embed(title="Movie Night")
        movieNightEmbed.set_image(url="https://img.morgverd.xyz/discord/movienight.png")
        movieNightEmbed.add_field(name="When?", value="We do our Movie Nights every **Friday** at **8pm**", inline=False)
        movieNightEmbed.add_field(name="Want to join us?", value="Good! Since we do our Movie Nights in the ``Movie Night`` channel, You need a special role to be able to join us. If you want to join just PM me and you'll get the role! When you join us, You dont need to join every time. You can just pick and choose what Movie Nights to join and what ones to skip out on.", inline=False)
        movieNightEmbed.add_field(name="What do we watch?", value="We dont know. We choose movies by everyone who is there suggesting a movie name. Then we put all the names in a spinner and choose the movie randomly!", inline=False)
        movieNightEmbed.add_field(name="Organiser", value="<@325721852058271755> is organising ``Movie Nights``, So any issues message him!")
        
        electionNightEmbed = discord.Embed(title="Election")
        electionNightEmbed.set_image(url="https://img.morgverd.xyz/discord/electionnight.png")
        electionNightEmbed.add_field(name="What is it?", value="Well every Saturday starting from **8am** and finishing at **12pm** exactly voting will take place for the new Discord Admin.", inline=False)
        electionNightEmbed.add_field(name="Why should I vote?", value="Two reasons. If you dont vote theres more chance of Reeve becoming the Admin of this server, And secondly the Admin of the server directly affects these nights and what takes place. Whoevers in power will affect you if you use this server at all.", inline=False)
        electionNightEmbed.add_field(name="I want to be admin!", value="Okay, Good. Well PM me any day/time before **6pm** on Saturday to be given your Shiny ``Candidate`` role!")

        await ctx.send(embed=gameNightEmbed)
        await ctx.send(embed=randomNightEmbed)
        await ctx.send(embed=movieNightEmbed)
        await ctx.send(embed=electionNightEmbed)

    @commands.command()
    async def announce(self, ctx):
        announceEmbed = discord.Embed(title="Events Channel")
        announceEmbed.set_image(url="https://img.morgverd.xyz/discord/events.png")
        announceEmbed.add_field(name="Events", value="Lockdown is shit, People are bored and there seems to be less and less to do. So, To hopefully try and make it all a tiny bit easier we are doing some **Weekly Events**! You can find a list of all the weekly events we will be doing over in <#706917132708872264>!", inline=False)
        announceEmbed.add_field(name="Cancellations", value="Sometimes, Shit happens. So if the Organiser of the night cant make it we will try to find someone else to do it. But if we still cant find anyone we may have to cancel it. If we do we will tell everyone in this channel.", inline=False)
        announceEmbed.add_field(name="'I cant make it next week'", value="Dont worry. There is no commitment in joining one of the nights. You can just pick and choose when to turn up!", inline=False)

        await ctx.send(embed=announceEmbed)

"""



def setup(bot):
    bot.add_cog(Embeds(bot))