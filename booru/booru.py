import discord
from redbot.core import Config, checks, commands
from redbot.core.utils.menus import menu, commands, DEFAULT_CONTROLS
import aiohttp
import contextlib
from random import randint
import asyncio
import logging

from .boorucore import BooruCore
from .booruset import Booruset
from .boorualias import Boorualias

log = logging.getLogger("Booru")  # Thanks to Sinbad for the example code for logging
log.setLevel(logging.DEBUG)

console = logging.StreamHandler()

if logging.getLogger("red").isEnabledFor(logging.DEBUG):
    console.setLevel(logging.DEBUG)
else:
    console.setLevel(logging.INFO)
log.addHandler(console)

BaseCog = getattr(commands, "Cog", object)


class Booru(BaseCog, BooruCore, Booruset, Boorualias):
    """Show a picture using image boards (Gelbooru, yandere, konachan)"""

    def __init__(self):
        # Reusable stuff
        self.board_names = ["dan", "gel", "kon", "yan", "r34", "safe", "e621", "4k", "ahegao", "ass", "anal", "bdsm", "blowjob", "boobs", "cunnilingus", "bottomless", "cumshots", "deepthroat", "dick", "double_penetration", "gay", "group", "hentai", "lesbian", "milf", "public", "rule34", "thigh", "trap", "wild", "redhead"]
        self.nsfw_board_names = ["4k", "ahegao", "ass", "anal", "bdsm", "blowjob", "boobs", "cunnilingus", "bottomless", "cumshots", "deepthroat", "dick", "double_penetration", "gay", "group", "hentai", "lesbian", "milf", "public", "rule34", "thigh", "trap", "wild", "redhead"]
        self.weeb_board_names = ["dan", "gel", "kon", "yan", "r34", "safe", "e621", "hentai"]
        self.session = aiohttp.ClientSession()

        # Config stuff
        self.config = Config.get_conf(self, identifier=4894278742742)
        default_global = {"filters": [], "nsfw_filters": []}
        default_guild = {"filters": [], "nsfw_filters": ["loli", "shota"], "boards": ["dan", "gel", "kon", "yan"], "simple": "off", "weebmode": "off", "onlynsfw": "off"}
        default_channel = {"boards": ["dan", "gel", "kon", "yan"], "simple": "off", "weebmode": "off"}
        self.config.register_global(**default_global)
        self.config.register_guild(**default_guild)
        self.config.register_channel(**default_channel)

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def booru(self, ctx, *, tag=None):
        """Shows a image board entry based on user query"""

        await self.generic_booru(ctx, tag)

    @commands.group()
    async def boorus(self, ctx):
        """Query sources for all the boorus!"""
        pass

    @boorus.group()
    @commands.guild_only()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def yan(self, ctx, *, tag=None):
        """Shows a image board entry based on user query from yande.re"""

        board = "yan"
        await self.generic_specific_source(ctx, board, tag)

    @boorus.group()
    @commands.guild_only()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def gel(self, ctx, *, tag=None):
        """Shows a image board entry based on user query from gelbooru"""

        board = "gel"
        await self.generic_specific_source(ctx, board, tag)

    @boorus.group()
    @commands.guild_only()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def kon(self, ctx, *, tag=None):
        """Shows a image board entry based on user query from konachan"""

        board = "kon"
        await self.generic_specific_source(ctx, board, tag)

    @boorus.group()
    @commands.guild_only()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def dan(self, ctx, *, tag=None):
        """Shows a image board entry based on user query from Danbooru"""

        board = "dan"
        await self.generic_specific_source(ctx, board, tag)

    @boorus.group()
    @commands.guild_only()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def r34(self, ctx, *, tag=None):
        """Shows a image board entry based on user query from Rule34"""

        board = "r34"
        await self.generic_specific_source(ctx, board, tag)

    @boorus.group()
    @commands.guild_only()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def safe(self, ctx, *, tag=None):
        """Shows a image board entry based on user query from Safebooru"""

        board = "safe"
        await self.generic_specific_source(ctx, board, tag)

    @boorus.group()
    @commands.guild_only()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def e621(self, ctx, *, tag=None):
        """Shows a image board entry based on user query from Safebooru"""

        board = "e621"
        await self.generic_specific_source(ctx, board, tag)

    @commands.group()
    async def reddits(self, ctx):
        """Query sources for all the subreddits!"""
        pass

    @reddits.group(name="4k", autohelp=False)
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _4k(self, ctx):
        """Shows a image board entry based on user query from 4k subreddits"""

        board = "4k"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @reddits.group(name="ahegao", autohelp=False)
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _ahegao(self, ctx):
        """Shows a image board entry based on user query from ahegao subreddits"""

        board = "ahegao"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @reddits.group(name="ass", autohelp=False)
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _ass(self, ctx):
        """Shows a image board entry based on user query from ass subreddits"""

        board = "ass"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @reddits.group(name="anal", autohelp=False)
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _anal(self, ctx):
        """Shows a image board entry based on user query from anal subreddits"""

        board = "anal"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @reddits.group(name="bdsm", autohelp=False)
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _bdsm(self, ctx):
        """Shows a image board entry based on user query from bdsm subreddits"""

        board = "bdsm"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @reddits.group(name="blowjob", autohelp=False)
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _blowjob(self, ctx):
        """Shows a image board entry based on user query from blowjob subreddits"""

        board = "blowjob"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @reddits.group(name="cunnilingus", autohelp=False)
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _cunnilingus(self, ctx):
        """Shows a image board entry based on user query from cunnilingus subreddits"""

        board = "cunnilingus"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @reddits.group(name="bottomless", autohelp=False)
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _bottomless(self, ctx):
        """Shows a image board entry based on user query from bottomless subreddits"""

        board = "bottomless"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @reddits.group(name="cumshots", autohelp=False)
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _cumshots(self, ctx):
        """Shows a image board entry based on user query from cumshots subreddits"""

        board = "cumshots"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @reddits.group(name="deepthroat", autohelp=False)
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _deepthroat(self, ctx):
        """Shows a image board entry based on user query from deepthroat subreddits"""

        board = "deepthroat"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @reddits.group(name="dick", autohelp=False)
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _dick(self, ctx):
        """Shows a image board entry based on user query from dick subreddits"""

        board = "dick"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @reddits.group(name="doublepenetration", autohelp=False)
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _doublepenetration(self, ctx):
        """Shows a image board entry based on user query from double penetration subreddits"""

        board = "double_penetration"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @reddits.group(name="gay", autohelp=False)
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _gay(self, ctx):
        """Shows a image board entry based on user query from gay subreddits"""

        board = "gay"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @reddits.group(name="group", autohelp=False)
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _group(self, ctx):
        """Shows a image board entry based on user query from group subreddits"""

        board = "group"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @reddits.group(name="hentai", autohelp=False)
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _hentai(self, ctx):
        """Shows a image board entry based on user query from hentai subreddits"""

        board = "hentai"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @reddits.group(name="lesbian", autohelp=False)
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _lesbian(self, ctx):
        """Shows a image board entry based on user query from lesbian subreddits"""

        board = "lesbian"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @reddits.group(name="milf", autohelp=False)
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _milf(self, ctx):
        """Shows a image board entry based on user query from milf subreddits"""

        board = "milf"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @reddits.group(name="public", autohelp=False)
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _public(self, ctx):
        """Shows a image board entry based on user query from public subreddits"""

        board = "public"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @reddits.group(name="rule34", autohelp=False)
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _rule34(self, ctx):
        """Shows a image board entry based on user query from rule34 subreddits"""

        board = "rule34"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @reddits.group(name="thigh", autohelp=False)
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _thigh(self, ctx):
        """Shows a image board entry based on user query from thigh subreddits"""

        board = "thigh"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @reddits.group(name="trap", autohelp=False)
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _trap(self, ctx):
        """Shows a image board entry based on user query from trap subreddits"""

        board = "trap"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @reddits.group(name="wild", autohelp=False)
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _wild(self, ctx):
        """Shows a image board entry based on user query from wild subreddits"""

        board = "wild"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @reddits.group(name="boobs", autohelp=False)
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _boobs(self, ctx):
        """Shows a image board entry based on user query from boobs subreddits"""

        board = "boobs"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @reddits.group(name="redhead", autohelp=False)
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _redhead(self, ctx):
        """Shows a image board entry based on user query from redhead subreddits"""

        board = "redhead"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    def __unload(self):
        fut = asyncio.ensure_future(self.session.close())
        yield from fut.__await__
        self.session.close()
