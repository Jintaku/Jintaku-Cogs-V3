import discord
from redbot.core import commands, Config, checks
import aiohttp
import asyncio
from redbot.core.utils.menus import menu, commands, DEFAULT_CONTROLS
from redbot.core.utils.predicates import ReactionPredicate, MessagePredicate

BaseCog = getattr(commands, "Cog", object)


class Imdb(BaseCog):
    """Shows movie info"""

    def __init__(self):
        self.config = Config.get_conf(self, identifier=233137652)
        default_global = {"apikey": ""}
        self.config.register_global(**default_global)

    @commands.command()
    async def movie(self, ctx, title):
        """Search a movie"""

        titlesearch = title.replace(' ', '_')
        apikey = await self.config.apikey()

        headers = {"accept": "application/json"}

        # Queries api for a game
        async with aiohttp.ClientSession() as session:
            async with session.post("http://www.omdbapi.com/?apikey=" + apikey + "&s=" + titlesearch + "&plot=short", headers=headers) as response:
                data = await response.json()

        # Handle response based on query result and user input
        if data['Response'] == "False":
            await ctx.send("I couldn't find anything!")
        if data['Response'] == "True":
            if data['totalResults'] == "1":
                await self.show_movie(data['Search'][0]['imdbID'])
            if data['totalResults'] != "1":
                medias = data['Search']
                msg = "**Please choose one by giving its number.**\n"
                for i in range(0, len(medias)):
                    msg += "\n{number} - {title} - {year}".format(number=i+1, title=medias[i]['Title'], year=medias[i]['Year'])

                message = await ctx.send(msg)

                check = lambda m: m.content.isdigit() and int(m.content) in range(1, len(medias) + 1)
                resp = await ctx.bot.wait_for("message", check=MessagePredicate.same_context(ctx))

                entry = medias[int(resp.content)-1]
                await self.show_movie(ctx, entry['imdbID'])

    async def show_movie(self, ctx, imdbID):
        """Show a movie"""

        apikey = await self.config.apikey()

        headers = {"accept": "application/json"}

        # Queries api for a game
        async with aiohttp.ClientSession() as session:
            async with session.post(f"http://www.omdbapi.com/?apikey={apikey}&i={imdbID}&plot=full", headers=headers) as response:
                data = await response.json()

        # Build Embed
        embed = discord.Embed()
        embed.title = "{} {}".format(data['Title'], data['Year'])
        if data['imdbID']:
           embed.url = "http://www.imdb.com/title/{}".format(data['imdbID'])
        if data['Plot']:
           embed.description = data['Plot']
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
        embed.set_footer(text="Powered by omdb")
        await ctx.send(embed=embed)

    @commands.command()
    @checks.is_owner()
    async def omdbkey(self, ctx, *, key):
        """Set a key to use the omdb api"""

        # Load config
        config_boards = await self.config.apikey()

        # Set new config
        await self.config.apikey.set(key)
        await ctx.send("The apikey has been added.")

