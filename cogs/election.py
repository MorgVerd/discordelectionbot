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

class Cmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.testMode = True
        self.testIDs = [325721852058271755, 212327858708676609, 338819690275012608]
        self.version = "1.5"

    async def getMessageEmbed(self, candidateUser):
        filePath = "/root/bots/govbot/data/messages/" + str(candidateUser.id) + ".txt"
        if not os.path.isfile(filePath):
            messageEmbed = discord.Embed(title="Oops")
            messageEmbed.add_field(name="Not Set", value="You have not got an election message set, to set one please use ``?setmessage``", inline=False)
        else:
            messageEmbed = discord.Embed(title=(str(candidateUser.name) + "'s Message"), description=(open(filePath, "r").read()))
            messageEmbed.set_thumbnail(url=candidateUser.avatar_url)


        return (os.path.isfile(filePath), messageEmbed)

    @commands.command()
    async def openvoting(self, ctx):
        try:
            await ctx.message.delete()
        except Exception:
            pass
        adminCheck, reason = (await self.bot.hasRole(self, ctx.message.author, "674620226494791720"))
        if not adminCheck:
            # Not admin
            return

        members = []; candidates = []
        for member in ctx.guild.members:
            if not member.bot:
                verifiedCheck, reason = (await self.bot.hasRole(self, member, "699286702467842058")) # Make sure user is verified
                if verifiedCheck:
                    members.append(member)
                    roleCheck, reason = (await self.bot.hasRole(self, member, "706535937462632479")) # Are they a candidate
                    if roleCheck:
                        # User is a candidate
                        candidates.append(member)


        candidateString = ""; candidateStartString = ""; exampleString = ""
        embedsToSend = []
        exampleString += "This is an example of how the Candidates will be layed out. To vote, You must use the first name (Username) not the Nickname.\n```\n"
        exampleString += "   - Username\n"
        exampleString += "      - Nickname\n"
        exampleString += "``` \n"
        for candidate in candidates:
            candidateString += "```\n"
            candidateString += "  - " + candidate.name + "\n"
            candidateString += "     - " + candidate.nick + "\n"
            candidateString += "\n``` "
            exists, embed = (await self.getMessageEmbed(candidate))
            if exists:
                embedsToSend.append(embed)
        if len(embedsToSend) > 0:
            candidateStartString = "Above, you will see some candidates messages and their reasons for why you should vote for them. Give them a read first!\n\n"


        thanksCreditsEmbed = discord.Embed(title="Thanks / Credits")
        thanksCreditsEmbed.set_footer(text="Bot version " + str(self.version), icon_url="https://img.morgverd.xyz/discord/jakesolutionfund.png")
        thanksCreditsEmbed.add_field(name="Special Thanks / Credits", value="**Morgan** = Programmer\n\nThanks to Cameron for extensive and annoying testing.\nThanks to Flynn for suggestions.", inline=False)


        electionCategory = None

        textChannelNames = []; textChannels = []
        for c in ctx.guild.channels:
            if str(c.type).lower() == "text":
                textChannelNames.append(str(c.name).upper())
                textChannels.append(c)
            if str(c.type).lower() == "category":
                if str(c.id) == "699292065225375874":
                    electionCategory = c

        self.bot.electionCategory = electionCategory
        verifiedRole = None
        for role in ctx.guild.roles:
            if (str(role.id) == "699286702467842058"):
                verifiedRole = role

        electionChannels = []
        for member in members:
            allowed = False
            if self.testMode:
                if member.id in self.testIDs:
                    allowed = True
            else:
                allowed = True

            if allowed:

                importantInfoString = ""
                importantInfoString += "UID:  " + str(member.id) + "\n"
                importantInfoString += "TIME: " + str(int(time.time())) + "\n"


                votingEmbed = discord.Embed(title="Your vote counts!")
                votingEmbed.set_image(url="https://img.morgverd.xyz/discord/electionnight.png")
                votingEmbed.add_field(name=("Hello " + member.name), value="Its election day, So its time to vote for who should be our new discord administrator! You only have one vote and once you've voted you cant change your vote, So vote wisely. Please read the entirety of this channel before you vote.", inline=False)
                votingEmbed.add_field(name="Example", value=exampleString, inline=False)
                votingEmbed.add_field(name="Candidates", value=candidateStartString + candidateString + "\n", inline=False)
                votingEmbed.add_field(name="Important Info", value="If there is an issue with your voting, you will be asked to provide the following infomation to a developer.\n```\n" + importantInfoString + "\n```\n", inline=False)
                votingEmbed.add_field(name="How to vote", value="To vote just send ``?vote username``. For example if you wanted to vote for ``morgverd`` you would simply send ``?vote morgverd`` in this channel. You can see a list of people you may vote for above. You should vote for the candidates username instead of their nickname.", inline=False)

                filePath = "/root/bots/govbot/data/votes/" + str(member.id) + ".txt"
                if not os.path.isfile(filePath):

                    channelName = ("ROOM-" + str(member.id))

                    if not channelName in textChannelNames:

                        createdChannel = await ctx.guild.create_text_channel(name=channelName, category=electionCategory, reason="Election room")
                        await createdChannel.set_permissions(ctx.guild.default_role, view_channel=False)
                        await createdChannel.set_permissions(verifiedRole, view_channel=False)
                        await createdChannel.set_permissions(member, view_channel=True)
                        electionChannels.append(createdChannel)

                        await createdChannel.send("<@" + str(member.id) + ">")
                        await createdChannel.send(embed=thanksCreditsEmbed)
                        for embed in embedsToSend:
                            await createdChannel.send(embed=embed)
                        await createdChannel.send(embed=votingEmbed)

                else:
                    print(member.name + " has already voted, Not making their channel")

        self.bot.votingActive = True
        self.bot.cachedMembers = members
        self.bot.electionChannels = electionChannels

    @commands.command()
    async def previewmessage(self, ctx):
        try:
            await ctx.message.delete()
        except Exception:
            pass
        candidateCheck, reason = (await self.bot.hasRole(self, ctx.message.author, "706535937462632479"))
        if not candidateCheck:
            # Not candidate
            return

        exists, embed = (await self.getMessageEmbed(ctx.message.author))
        await ctx.send(embed=embed, delete_after=20)
        return


    @commands.command()
    async def setmessage(self, ctx, *, message : str = "UNDEFINED"):
        try:
            await ctx.message.delete()
        except Exception:
            pass
        candidateCheck, reason = (await self.bot.hasRole(self, ctx.message.author, "706535937462632479"))
        if not candidateCheck:
            # Not candidate
            return

        if message == "UNDEFINED":
            await ctx.send(":warning: Incorrect usage, Please use ``?setmessage your message would go here, You can make it fairly long! Upto 200 characters! Woo!``", delete_after=20)
            return

        overwrite = False
        filePath = "/root/bots/govbot/data/messages/" + str(ctx.message.author.id) + ".txt"
        if os.path.isfile(filePath): overwrite = True
        with open(filePath, "w") as file:
            file.write(message)

        if overwrite:
            await ctx.send(":white_check_mark: You have successfully overwritten your message. You can use ``?previewmessage`` to see what your new message looks like!", delete_after=20)
        else:
            await ctx.send(":white_check_mark: You have successfully set your message. You can use ``?previewmessage`` to see what your message now looks like!", delete_after=20)
        return



    @commands.command()
    async def vote(self, ctx, *, candidatename : str = "UNDEFINED"):
        try:
            await ctx.message.delete()
        except Exception:
            pass

        filePath = "/root/bots/govbot/data/votes/" + str(ctx.message.author.id) + ".txt"

        if not self.bot.votingActive: return

        print((ctx.message.channel.name).upper())
        print(("ROOM-" + str(ctx.message.channel.id)))

        if not ((ctx.message.channel.name).upper() == ("ROOM-" + str(ctx.message.author.id))):
            # User is NOT in PMs
            await ctx.send(":warning: Please only use this in your election channel!", delete_after=20)
            return

        if candidatename == "UNDEFINED":
            # Ran raw command
            await ctx.send(":warning: Incorrect usage! Please read the help message carefully!")
            return

        if os.path.isfile(filePath):
            # Already voted
            await ctx.send(":warning: You've already voted! You may not vote again. Contact an Administrator if you require assistance.")
            return

        candidates = []
        for member in self.bot.cachedMembers:
            if not member.bot:
                candidateCheck, reason = (await self.bot.hasRole(self, member, "706535937462632479"))
                if candidateCheck:
                    candidates.append(member)

        candidateExists = False; selectedCandidate = None
        for candidate in candidates:
            if (((candidate.name).upper()) == (candidatename.upper())):
                # Name is valid
                candidateExists = True
                selectedCandidate = candidate
                break

        if not candidateExists:
            # Candidate doesnt exist
            await ctx.send(":warning: Candidate doesn't exist, Did you misspell their name?", delete_after=10)
            return


        # If they are here, The candidate exists, and everything is good.

        # PROCESS VOTE HERE

        file = open(filePath, "w")
        file.write(str(selectedCandidate.id))
        file.close()

        await ctx.send(":smile: Your vote has been counted and saved! Thankyou.")
        await ctx.message.channel.delete()
        return


    @commands.command()
    async def closevoting(self, ctx):
        try:
            await ctx.message.delete()
        except Exception:
            pass
        adminCheck, reason = (await self.bot.hasRole(self, ctx.message.author, "674620226494791720"))
        if not adminCheck:
            # Not admin
            return
        self.bot.votingActive = False
        # Close any active voting channels
        for m in ctx.guild.members:
            for c in ctx.guild.channels:
                if ((str(c.type) == "text") and (str(c.name).lower() == ("room-" + str(m.id)))):
                    await c.delete()
        
        os.chdir("/root/bots/govbot/data/votes")
        unsortedvotes = {}
        for filename in glob.glob("*.txt"):
            with open(filename, "r") as file:
                uid = str(file.read().replace("\n", ""))
                if uid in unsortedvotes:
                    unsortedvotes[uid] += 1
                else:
                    unsortedvotes[uid] = 1

        votes = (dict(sorted(unsortedvotes.items(), key=operator.itemgetter(1),reverse=True))) # Sort the votes

        state = ""
        if len(votes) > 1:
            # If the votes are more than one
            votes1 = list(votes.items())[0][1]
            votes2 = list(votes.items())[1][1]
            if votes1 == votes2:
                state = "TIE"
            else:
                state = "WIN"

        else:
            # Everyone voted for one person, or none
            if (len(votes)) == 0:
                state = "LOSS"
            else:
                state = "WIN"

        closingElectionEmbed = discord.Embed(title="Election Results")
        closingElectionEmbed.set_image(url="https://img.morgverd.xyz/discord/electionnight.png")
        tieWinner = False
        tieWinnerUsr = None

        if state == "TIE":
            closingElectionEmbed.add_field(name="Tie", value="There has been a tie between two or more candidates. In this eventuality I will now randomly pick a winner...", inline=False)
            # Fuck okay, Do this legit
            userone = self.bot.get_user(int(list(votes.items())[0][0]))
            usertwo = self.bot.get_user(int(list(votes.items())[1][0]))
            isuserone = bool(int(random.randint(0, 1))) # Get random true or false
            tieWinner = True # For the win state
            if isuserone:
                tieWinnerUsr = userone
            else:
                tieWinnerUsr = usertwo
            state = "WIN" # Now declare a win state

        if state == "WIN":
            if not tieWinner:
                winner = self.bot.get_user(int(list(votes.items())[0][0]))
            else:
                winner = tieWinnerUsr
            closingElectionEmbed.add_field(name="Winner", value="The winner of this weeks election is... <@" + str(winner.id) + ">! They will shortly recive their new shiny role and their power! Good job to them, and thanks to everyone for voting.", inline=False)
            closingElectionEmbed.add_field(name=("Note to " + str(winner.name)), value="To recive your actual powers, Please contact Morgan so that you can be given the guidelines and rules of your term.", inline=False)

        if state == "LOSS":
            closingElectionEmbed.add_field(name="Loss", value="Nobody bothered to vote. For this reason the current Admin will remain in power for an additional term.")

        # Get announcement channel
        for c in ctx.guild.channels:
            if str(c.id) == "699292114189811722":
                announcementChannel = c

        await announcementChannel.send(embed=closingElectionEmbed)
        # delete votes?
        for filename in glob.glob("*.txt"):
            os.remove("/root/bots/govbot/data/votes/" + filename)
            print("Removed: " + filename + ".txt")

        return # Done




def setup(bot):
    bot.add_cog(Cmds(bot))
