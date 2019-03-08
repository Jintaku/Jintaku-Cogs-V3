from redbot.core import commands, checks, Config
from redbot.core.utils.predicates import ReactionPredicate, MessagePredicate
import discord


BaseCog = getattr(commands, "Cog", object)

class Confession(BaseCog):

    def __init__(self):
        self.config = Config.get_conf(self, identifier=665235)
        default_guild = {"confession_room": ""}
        self.config.register_guild(**default_guild)

    @commands.command()
    @checks.admin_or_permissions(manage_guild=True)
    async def confessionset(self, ctx, *, channel: discord.TextChannel):

        rooms = await self.config.guild(ctx.guild).confession_rooms()

        if channel is None:
            return await ctx.send("No channel mentioned.")

        await self.config.guild(ctx.guild).confession_rooms.set(channel.id)
        await ctx.send("The room has been set.")

    @commands.command()
    @checks.admin_or_permissions(manage_guild=True)
    async def confessionunset(self, ctx):

        rooms = await self.config.guild(ctx.guild).confession_rooms()

        await self.config.guild(ctx.guild).confession_rooms.set("")
        await ctx.send("The room has been unset.")

    @commands.command()
    async def confess(self, ctx, *, confession):

        rooms = await self.config.guild(ctx.guild).confession_rooms()

        if rooms == "" or rooms is None:
            return await ctx.send("The room has not been set.")

        for channel in ctx.guild.text_channels:
            if rooms == channel.id:
                confession_room = channel

        try:
            await ctx.message.delete()
        except:
            await ctx.send("I couldn't delete your message, sorry!")
        try:
            await confession_room.send(confession)
        except:
            await ctx.send("I don't have permission to this room or something went wrong")
