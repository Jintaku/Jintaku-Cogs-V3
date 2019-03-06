import discord
from redbot.core import commands, checks, Config

BaseCog = getattr(commands, "Cog", object)


class Dmannouncer(BaseCog):
    """Send messages to server owners"""

    def __init__(self):
        self.config = Config.get_conf(self, identifier=233137652)
        default_user = {"toggle": "1"}
        self.config.register_user(**default_user)

    @commands.command()
    @checks.is_owner()
    async def dmannounce(self, ctx, *, message):
        """Send messages to server owners \n
        THIS WILL NOTIFY THE OWNERS OF ALL YOUR SERVERS, USE WITH CAUTION"""

        guilds = ctx.bot.guilds


        server_owners = []

        for guild in guilds:
            server_owner = guild.owner

            toggle_status = await self.config.user(server_owner).toggle()

            if toggle_status == "1":
                continue

            server_owners.append(server_owner)

        for owner in set(server_owners):

            embed = discord.Embed()
            embed.title = f"Announcement sent by {ctx.author}"
            embed.description = message
            embed.set_footer(text="Use [p]dmannouncements toggle to turn off announcements")
            await owner.send(embed=embed)

        await ctx.send("DM'ed successfully!")

    @commands.command()
    @checks.is_owner()
    async def dmannouncements(self, ctx):

        toggle_status = await self.config.user(ctx.author).toggle()

        if toggle_status == "0":
            await self.config.user(ctx.author).toggle.set("1")
            await ctx.send("Announcements now off")
        if toggle_status == "1":
            await self.config.user(ctx.author).toggle.set("0")
            await ctx.send("Announcements back on!")

    async def on_guild_join(self, guild):

        server_owner = guild.owner

        embed = discord.Embed()
        embed.title = "News announcements"
        embed.description = "If you wish to receive new features, maintenance and such announcements, please use [p]dmannouncements to turn this on!"
        await server_owner.send(embed=embed)
