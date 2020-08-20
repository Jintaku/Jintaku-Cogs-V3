import discord
from redbot.core import commands, Config, checks
import aiohttp
import asyncio
import async_lru
from redbot.core.utils.menus import menu, commands, DEFAULT_CONTROLS

BaseCog = getattr(commands, "Cog", object)


@async_lru.alru_cache(maxsize=32)
async def cached_json_request(url, *, headers=(), **kw):
    kw["headers"] = dict(headers)

    async with aiohttp.ClientSession() as session:
        async with session.post(url, **kw) as response:
            return await response.json()


class Gamesearch(BaseCog):
    """Search IGDB for games"""

    def __init__(self):
        self.config = Config.get_conf(self, identifier=7535876897)
        default_global = {"apikey": ""}
        self.config.register_global(**default_global)

    async def get_game_embed(self, headers, game_data):

        # Set data query and send it to get game data
        if game_data.get('cover'):
            cover_query = f"fields url; where id = {game_data['cover']};".encode()

            async with aiohttp.ClientSession() as session:
                async with session.post("https://api-v3.igdb.com/covers", data=cover_query, headers=headers) as response:
                    cover_data = await response.json()
        else:
            cover_data = []

        # Try to query platforms with cache
        if game_data.get('platforms'):
            platforms_data = await asyncio.gather(
                *(cached_json_request("https://api-v3.igdb.com/platforms", data=f"fields name; where id = {platform};".encode(), headers=tuple(headers.items())) for platform in game_data["platforms"])
            )
        else:
            platforms_data = []

        # Build and return embed
        embed = discord.Embed(title=game_data["name"], url=game_data["url"])
        if platforms_data != []:
            embed.add_field(name="Platforms", value=", ".join(platform_data[0]["name"] for platform_data in platforms_data))
        if "summary" in game_data:
            embed.description = game_data["summary"][:1024] + "..."
        if cover_data != []:
            embed.set_thumbnail(url="https:" + cover_data[0]["url"])
        return embed

    @commands.command()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def game(self, ctx, *, game):
        """Search IGDB.com for games"""

        apikey = await self.config.apikey()

        # Tell user if their apikey isn't set
        if apikey is None or apikey == "":
            await ctx.send("You need to set an api key to use the IGDB api, please use [p]igdbkey")
            return

        headers = {"accept": "application/json", "user-key": apikey}

        # Format and create data
        escaped_game = game.replace("\\", "\\\\").replace('"', '\\"')
        game_query = f"""fields cover, name, platforms, summary, url; search "{escaped_game}";""".encode()

        # Queries api for a game
        async with aiohttp.ClientSession() as session:
            async with session.post(f"https://api-v3.igdb.com/games/", data=game_query, headers=headers) as response:
                games_data = await response.json()
                if games_data == []:
                    await ctx.send("No results.")
                    return

        # Get more information such as cover and platforms and build embed
        embeds = await asyncio.gather(*(self.get_game_embed(headers, game_data) for game_data in games_data))

        # Show embed, success.
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
