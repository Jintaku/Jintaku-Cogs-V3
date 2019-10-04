import discord
from redbot.core import Config, checks, commands
import aiohttp
from redbot.core.utils.predicates import ReactionPredicate, MessagePredicate
from redbot.core.utils.menus import menu, commands, DEFAULT_CONTROLS, start_adding_reactions
import contextlib

BaseCog = getattr(commands, "Cog", object)


class Wikia(BaseCog):
    """Search wikia"""

    def __init__(self):
        self.config = Config.get_conf(self, identifier=4894278742742)
        default_channel = {"url": ""}
        self.config.register_channel(**default_channel)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def wikia(self, ctx, *, query):
        """Search wikia subdomain then bot will ask you which article you want to consult unless using a default wiki"""

        if await self.config.channel(ctx.channel).url() != "":
            domain = await self.config.channel(ctx.channel).url()
            await self.search_article(ctx, query, domain)
            return

        subdomain = await self.search_subdomain(ctx, query)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def wikias(self, ctx, *, query):
        """Search wikia subdomain then bot will ask you which article you want to consult ignoring default wiki"""

        subdomain = await self.search_subdomain(ctx, query)

    async def search_subdomain(self, ctx, subdomain):

        subdomain = subdomain.replace(" ", "+")

        # Queries api to search wikia subdomains
        headers = {"content-type": "application/json"}

        async with aiohttp.ClientSession() as session:
            async with session.post("http://www.wikia.com/api/v1/Wikis/ByString?expand=1&limit=25&batch=1&includeDomain=true&string=" + subdomain, headers=headers) as response:
                data = await response.json()

        # Function which selects domain using reaction
        async def select_domain(ctx: commands.Context, pages: list, controls: dict, message: discord.Message, page: int, timeout: float, emoji: str):
            # Clean up
            with contextlib.suppress(discord.NotFound):
                await message.delete()
            # Send it off to this function so it sends to initiate search after selecting subdomain
            await self.selected_domain(ctx, data, page)
            return None

        SELECT_DOMAIN = {"\N{WHITE HEAVY CHECK MARK}": select_domain}

        # Create dict for controls used by menu
        SELECT_CONTROLS = {}
        SELECT_CONTROLS.update(DEFAULT_CONTROLS)
        SELECT_CONTROLS.update(SELECT_DOMAIN)

        # Set empty list to be appended to later
        embeds = []

        # Checks if there is actually subdomains
        if data["total"] == 0:
            await ctx.send("There is no such subdomain")
            return

        # Loop through subdomains to show them in menu
        for subdomains in data["items"]:
            embed = discord.Embed(color = await ctx.embed_color())
            embed.title = subdomains["name"] + f" ({subdomains['url']})"
            embed.url = subdomains["url"]
            embed.set_thumbnail(url=subdomains["image"])
            embed.description = subdomains["desc"]
            embed.add_field(name="Language", value=subdomains.get("language", "N/A"))
            embed.add_field(name="Number of articles", value=subdomains["stats"].get("articles", "N/A"))
            embed.set_footer(text="Powered by Wikia/Fandom.com")
            embeds.append(embed)

        await menu(ctx, pages=embeds, controls=SELECT_CONTROLS, message=None, page=0, timeout=60)

    async def selected_domain(self, ctx, data, page):

        # Sets variable for selected domain
        selected_domain = data["items"][page]

        # Initiate searching of article part
        article = await self.enter_article(ctx, selected_domain)
        await self.search_article(ctx, article, selected_domain)

    async def enter_article(self, ctx, selected_domain):

        message = await ctx.send(content="Enter the wikia article for " + selected_domain["name"] + ":", delete_after=10)
        response = await ctx.bot.wait_for("message", check=MessagePredicate.same_context(ctx))

        response = str(response.content).replace(" ", "+")

        return response

    async def search_article(self, ctx, article, domain):

        if type(domain) is str:
            domain = domain
        else:
            domain = domain["url"]

        # Queries api to search an article
        headers = {"content-type": "application/json"}

        async with aiohttp.ClientSession() as session:
            async with session.post(str(domain) + "/api/v1/Search/List?limit=10&batch=1&query=" + article, headers=headers) as response:
                data = await response.json()

        embeds = []

        # Checks if there is actually articles
        if data.get("exception"):
            await ctx.send("There is no such articles")
            return

        # Loops and queries api because Wikia doesn't give enough information with the List api, this is the slowest part sadly
        for articles in data["items"]:

            # Queries api for more information
            async with aiohttp.ClientSession() as session:
                async with session.post(domain + "/api/v1/Articles/Details?abstract=300&ids=" + str(articles["id"]), headers=headers) as response:
                    article_data = await response.json()

            # Sets variable for better use in embed
            article_id = str(articles["id"])
            article = article_data["items"][article_id]

            embed = discord.Embed(color = await ctx.embed_color())
            embed.title = article["title"]
            embed.url = articles["url"]
            if article["thumbnail"]:
                embed.set_thumbnail(url=article["thumbnail"])
            embed.description = article["abstract"]
            embed.set_footer(text="Powered by Wikia/Fandom.com")
            embeds.append(embed)

        await menu(ctx, pages=embeds, controls=DEFAULT_CONTROLS, message=None, page=0, timeout=15)

    @commands.command()
    @checks.admin_or_permissions(manage_guild=True)
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def wikiaset(self, ctx, *, url):
        """Set default wiki domain"""

        # Set new config
        await self.config.channel(ctx.channel).url.set(url)
        await ctx.send("The default wiki has been changed.")

    @commands.command()
    @checks.admin_or_permissions(manage_guild=True)
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def wikiaunset(self, ctx):
        """Remove default wiki domain"""

        # Set new config
        await self.config.channel(ctx.channel).url.set("")
        await ctx.send("The default wiki has been changed.")
