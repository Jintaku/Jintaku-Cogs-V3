from redbot.core import commands, checks, Config
from redbot.core.utils.predicates import ReactionPredicate, MessagePredicate
from redbot.core.utils.menus import DEFAULT_CONTROLS, menu
import contextlib
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
        """Set a confession room"""

        rooms = await self.config.guild(ctx.guild).confession_rooms()

        if channel is None:
            return await ctx.send("No channel mentioned.")

        await self.config.guild(ctx.guild).confession_rooms.set(channel.id)
        await ctx.send("The room has been set.")

    @commands.command()
    @checks.admin_or_permissions(manage_guild=True)
    async def confessionunset(self, ctx):
        """Unset a confession room"""

        rooms = await self.config.guild(ctx.guild).confession_rooms()

        await self.config.guild(ctx.guild).confession_rooms.set("")
        await ctx.send("The room has been unset.")

    @commands.command()
    async def confess(self, ctx, *, confession):
        """Confess your dirty sins

        It'll ask you which guild to confess in if you have more than one with a confession
        """

        async def select_guild(ctx: commands.Context, pages: list, controls: dict, message: discord.Message, page: int, timeout: float, emoji: str):
            # Clean up
            with contextlib.suppress(discord.NotFound):
                await message.delete()
            # Send it off to this function so it sends to initiate search after selecting subdomain
            await self.selected_guild(ctx, user_guilds, confession, page)
            return None

        if bool(ctx.guild):
            await ctx.send("You should do this in DMs!")
            try :
                await ctx.message.delete()
            except:
                pass
            return

        all_guilds = ctx.bot.guilds
        user_guilds = []
        for guild in all_guilds:
            if guild.get_member(ctx.message.author.id):
                room = await self.config.guild(guild).confession_rooms()
                if room is not None:
                    user_guilds.append(guild)

        if len(user_guilds) == 0:
            await ctx.author.send("No server with a confession room, ask your server owners to set it up!")
        if len(user_guilds) == 1:
            await self.send_confession(ctx, user_guilds[0], confession)
        else:
            SELECT_DOMAIN = {"\N{WHITE HEAVY CHECK MARK}": select_guild}

            # Create dict for controls used by menu
            SELECT_CONTROLS = {}
            SELECT_CONTROLS.update(DEFAULT_CONTROLS)
            SELECT_CONTROLS.update(SELECT_DOMAIN)

            embeds = []
            for guild in user_guilds:
                embed = discord.Embed()
                embed.title = "Where do you want to confess?"
                embed.description = guild.name
                embeds.append(embed)

            await menu(ctx, pages=embeds, controls=SELECT_CONTROLS, message=None, page=0, timeout=20)

    async def selected_guild(self, ctx, user_guilds, confession, page):

        confession_guild = user_guilds[page]
        await self.send_confession(ctx, confession_guild, confession)

    async def send_confession(self, ctx, confession_guild, confession):

        rooms = await self.config.guild(confession_guild).confession_rooms()

        for channel in confession_guild.text_channels:
            if rooms == channel.id:
                confession_room = channel

        if not confession_room:
            return await ctx.author.send("The confession room does not appear to exist.")

        try:
            await ctx.bot.send_filtered(destination=confession_room, content=confession)
        except discord.errors.Forbidden:
            return await ctx.author.send("I don't have permission to send messages to this room or something went wrong.")
            

        await ctx.author.send("Your confession has been sent, you are forgiven now.")
