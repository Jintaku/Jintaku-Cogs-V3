from redbot.core import commands, checks, Config
from redbot.core.utils.predicates import ReactionPredicate, MessagePredicate
from redbot.core.utils.menus import DEFAULT_CONTROLS, menu
import contextlib
import discord


BaseCog = getattr(commands, "Cog", object)


class Confession(commands.Cog):
            def __init__(self):
                self.config = Config.get_conf(self, identifier=665235, force_registration=True)
                default_guild = {"confession_room": None, "tracker_room": None}
                self.config.register_guild(**default_guild)
                self.confessioncount = {}
         
            @commands.group()
            @checks.admin_or_permissions(manage_guild=True)
            @commands.guild_only()
            async def confessionset(self, ctx):
                """ Manage confession rooms """
                pass
         
            @confessionset.command(name="confess")
            async def confessionset_confess(self, ctx, *, channel: discord.TextChannel = None):
                """Set a confession room
               Leave empty to unset the room.
               **Make sure bot is able to embed messages in confession room.**
               """
         
                room = await self.config.guild(ctx.guild).confession_room()
                room = ctx.guild.get_channel(room)
         
                if not channel:
                    if room:
                        await ctx.send(f"Unset confession channel {room.mention} ?")
                        pred = MessagePredicate.yes_or_no(ctx)
                        await ctx.bot.wait_for("message", check=pred)
                        if pred.result:
                            await self.config.guild(ctx.guild).confession_room.clear()
                            await ctx.tick()
                        else:
                            await ctx.send("Cancelled.")
                        return
                    else:
                        await ctx.send("No confession room defined.")
                        return
         
                await self.config.guild(ctx.guild).confession_room.set(channel.id)
                await ctx.tick()
         
         
            @commands.command()
            @commands.cooldown(rate=1, per=90, type=commands.BucketType.user)
            async def confess(self, ctx, *, confession: str):
                """Confess your dirty sins
               Make sure to use in DMs
               It'll ask you which guild to confess in if you have more than one with a confession
               """
         
                async def select_guild(
                    ctx: commands.Context,
                    pages: list,
                    controls: dict,
                    message: discord.Message,
                    page: int,
                    timeout: float,
                    emoji: str,
                ):
                    # Clean up
                    with contextlib.suppress(discord.NotFound):
                        await message.delete()
                    # Send it off to this function so it sends to initiate search after selecting subdomain
                    await self.selected_guild(ctx, user_guilds, confession, page)
                    return None
         
                if bool(ctx.guild):
                    msg = await ctx.send("You should do this in DMs!")
                    try:
                        await ctx.message.delete()
                        await asyncio.sleep(10)
                        await msg.delete()
                    except:
                        pass
                    return
         
                all_guilds = ctx.bot.guilds
                user_guilds = []
                for guild in all_guilds:
                    if guild.get_member(ctx.message.author.id):
                        room = await self.config.guild(guild).confession_room()
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
           
            """
           This keeps track of the amount of confessions per server.
           param serv_id: str:     The server ID to confess in, as a string because numerical keys imply indexes.
         
           return: int:            The number of the confession in the server, easy for if you wanna add it in the embed
           """
            def _count_confession(serv_id: str) -> int:
                # Not 100% sure this works as intended. It SHOULD return None when getting a key that isn't there.
                cur_count = self.confessioncount.get(serv_id)
                self.confessioncount[serv_id] = cur_count+1 if cur_count is not None else 1
                return cur_count
         
            async def send_confession(self, ctx, confession_guild: discord.Guild, confession: str):
         
                confession_room = await self.config.guild(confession_guild).confession_room()
                confession_room = confession_guild.get_channel(confession_room)
         
                if not confession_room:
                    await ctx.author.send("The confession room does not appear to exist.")
                    return
         
                try:
                    # Get the number of the sin
                    count = self._count_confession(str(confession_guild.id))
                    # Changed this to an f-string so the count can be formatted in
                    embed = discord.Embed(title=f"I have forgiven another sin (#{count})", colour=0xf47fff)
                    embed.set_footer(text="type ,confess in my DMs to confess")
                    embed.add_field(name="**Confession**", value=confession)
         
                    await ctx.bot.send_filtered(destination=confession_room, embed=embed)
                except discord.errors.Forbidden:
                    await ctx.author.send(
                        "I don't have permission to send messages to this room, embed messages or something went wrong."
                    )
                    return
         
         
                await ctx.author.send("Your confession has been sent, you are forgiven now.")

