import discord
from redbot.core import commands, Config, checks
import aiohttp
from redbot.core.utils.menus import menu, commands, DEFAULT_CONTROLS

BaseCog = getattr(commands, "Cog", object)


class Games(BaseCog):
    """Search wikia"""

    def __init__(self):
        self.config = Config.get_conf(self, identifier=7535876897)
        default_global = {"apikey": ""}
        self.config.register_global(**default_global)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def games(self, ctx, game):
        """Search IGDB.com for games"""

        apikey = await self.config.apikey()

        if apikey is None or apikey == "":
            await ctx.send("You need to set an api key to use the IGDB api, please use [p]igdbkey")
            return

        # Queries api to search an article
        headers = {"content-type": "application/json", "user-key": apikey}

        async with aiohttp.ClientSession() as session:
            async with session.post(f"https://api-v3.igdb.com/games/?search={game}&fields=*&filter[version_parent][not_exists]=1", headers=headers) as response:
                data = await response.json()

        embeds = []

        for games in data:

            # TODO : Make thumbnails work
            # async with aiohttp.ClientSession() as session:
            #    async with session.post("https://api-v3.igdb.com/games/" + str(games['id']) + "?fields=cover", headers=headers) as response:
            #        data = await response.text()

            # print(data)

            embed = discord.Embed()
            embed.title = games["name"]
            if games.get("summary"):
                embed.description = games["summary"][:1024] + "..."
            # embed.set_thumbnail(url="https:" + data["url"])
            embed.url = games["url"]
            embeds.append(embed)

        await menu(ctx, pages=embeds, controls=DEFAULT_CONTROLS, message=None, page=0, timeout=15)

    @commands.command()
    @checks.is_owner()
    async def igdbkey(self, ctx, *, key):
        """Set a key to use the IGDB api"""

        # Load config
        config_boards = await self.config.apikey()

        # Set new config
        await self.config.apikey.set(key)
        await ctx.send("The apikey has been added.")
