import discord
from redbot.core import commands, Config, checks
import aiohttp
import logging
from redbot.core.utils.menus import menu, commands, DEFAULT_CONTROLS
from urllib.parse import urlencode

# Debug stuff
log = logging.getLogger("Booru")  # Thanks to Sinbad for the example code for logging
log.setLevel(logging.DEBUG)

console = logging.StreamHandler()

if logging.getLogger("red").isEnabledFor(logging.DEBUG):
    console.setLevel(logging.DEBUG)
else:
    console.setLevel(logging.INFO)
log.addHandler(console)

BaseCog = getattr(commands, "Cog", object)


class Imdb(BaseCog):
    """Shows movie info"""

    def __init__(self):
        self.config = Config.get_conf(self, identifier=233137652)
        default_global = {"apikey": ""}
        self.config.register_global(**default_global)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def movie(self, ctx, *, title):
        """Search for a movie"""

        # Get API key
        apikey = await self.config.apikey()

        if apikey == "":
            await ctx.send("No omdbkey set, please set one using [p]omdbkey")
            return

        url = "http://www.omdbapi.com/?"+urlencode({
            "apikey": apikey,
            "s": title,
            "plot": "short",
            "type": "movie"
        })
        headers = {"accept": "application/json"}

        # Queries api for a movie
        async with aiohttp.ClientSession() as session:
            async with session.post(url=url, headers=headers) as response:
                data = await response.json()

        # Handle if nothing is found
        if data['Response'] == "False":
            await ctx.send("I couldn't find anything! You probably didn't set your API key properly!")
            return

        results = data['Search']

        # Set variable to be appended to
        embeds = []

        # Loop and ask for more information and build embed
        for game in results:

            # Queries api for a movie information
            url = "http://www.omdbapi.com/?"+urlencode({
                "apikey": apikey,
                "i": game['imdbID'],
                "plot": "full"
            })
            async with aiohttp.ClientSession() as session:
                async with session.post(url=url, headers=headers) as response:
                    data = await response.json()
                    log.debug(data)

            # Build Embed
            embed = discord.Embed()
            embed.title = "{} ({})".format(data['Title'], data['Year'])
            if data['imdbID']:
               embed.url = "http://www.imdb.com/title/{}".format(data['imdbID'])
            if data['Plot']:
               embed.description = data['Plot'][:500]
            if data['Poster'] != "N/A":
               embed.set_thumbnail(url=data['Poster'])
            if data['Runtime']:
               embed.add_field(name="Runtime", value=data.get('Runtime', 'N/A'))
            if data['Genre']:
               embed.add_field(name="Genre", value=data.get('Genre', 'N/A'))
            if data.get("BoxOffice"):
               embed.add_field(name="Box Office", value=data.get('BoxOffice', 'N/A'))
            if data['Metascore']:
               embed.add_field(name="Metascore", value=data.get('Metascore', 'N/A'))
            if data['imdbRating']:
               embed.add_field(name="IMDb", value=data.get('imdbRating', 'N/A'))
            embed.set_footer(text="Powered by omdb")
            embeds.append(embed)

        await menu(ctx, pages=embeds, controls=DEFAULT_CONTROLS, message=None, page=0, timeout=20)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def tv(self, ctx, *, title):
        """Search for a tv show"""

        # Get API key
        apikey = await self.config.apikey()

        if apikey == "":
            await ctx.send("No omdbkey set, please set one using [p]omdbkey")
            return

        url = "http://www.omdbapi.com/?"+urlencode({
            "apikey": apikey,
            "s": title,
            "plot": "short",
            "type": "series"
        })
        headers = {"accept": "application/json"}

        # Queries api for a movie
        async with aiohttp.ClientSession() as session:
            async with session.post(url=url, headers=headers) as response:
                data = await response.json()

        # Handle if nothing is found
        if data['Response'] == "False":
            await ctx.send("I couldn't find anything! You probably didn't set your API key properly!")
            return

        results = data['Search']

        # Set variable to be appended to
        embeds = []

        # Loop and ask for more information and build embed
        for game in results:

            # Queries api for a movie information
            url = "http://www.omdbapi.com/?"+urlencode({
                "apikey": apikey,
                "i": game['imdbID'],
                "plot": "full"
            })
            async with aiohttp.ClientSession() as session:
                async with session.post(url=url, headers=headers) as response:
                    data = await response.json()
                    log.debug(data)

            # Build Embed
            embed = discord.Embed()
            embed.title = "{} ({})".format(data['Title'], data['Year'])
            if data['imdbID']:
               embed.url = "http://www.imdb.com/title/{}".format(data['imdbID'])
            if data['Plot']:
               embed.description = data['Plot'][:500]
            if data['Poster'] != "N/A":
               embed.set_thumbnail(url=data['Poster'])
            if data['Runtime']:
               embed.add_field(name="Runtime", value=data.get('Runtime', 'N/A'))
            if data['Genre']:
               embed.add_field(name="Genre", value=data.get('Genre', 'N/A'))
            if data.get("BoxOffice"):
               embed.add_field(name="Box Office", value=data.get('BoxOffice', 'N/A'))
            if data['Metascore']:
               embed.add_field(name="Metascore", value=data.get('Metascore', 'N/A'))
            if data['imdbRating']:
               embed.add_field(name="IMDb", value=data.get('imdbRating', 'N/A'))
            embed.set_footer(text="Powered by omdb")
            embeds.append(embed)

        await menu(ctx, pages=embeds, controls=DEFAULT_CONTROLS, message=None, page=0, timeout=20)

    @commands.command()
    @checks.is_owner()
    async def omdbkey(self, ctx, *, key):
        """Set a key to use the omdb api"""

        # Load config
        config_boards = await self.config.apikey()

        # Set new config
        await self.config.apikey.set(key)
        await ctx.send("The apikey has been added.")

