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


class Booru(BaseCog, BooruCore, Booruset, Boorualias):
    """Show images from various sources"""

    def __init__(self):
        # Reusable stuff
        self.board_names = ["dan", "gel", "kon", "yan", "r34", "safe", "e621", "4k", "ahegao", "ass", "anal", "bdsm", "blowjob", "boobs", "cunnilingus", "bottomless", "cumshots", "deepthroat", "dick", "double_penetration", "gay", "group", "hentai", "lesbian", "milf", "public", "rule34", "thigh", "trap", "wild", "redhead", "oboobs", "obutts", "nekos_nsfw_classic", "nekos_nsfw_blowjob", "nekos_nsfw_boobs", "nekos_nsfw_neko", "nekos_nsfw_furry", "nekos_nsfw_pussy", "nekos_nsfw_feet", "nekos_nsfw_yuri", "nekos_nsfw_anal", "nekos_nsfw_solo", "nekos_nsfw_cum", "nekos_nsfw_spank", "nekos_nsfw_cunnilingus", "nekos_nsfw_bdsm", "nekos_nsfw_piercings", "nekos_nsfw_trap", "nekos_nsfw_kitsune", "nekos_nsfw_holo", "nekos_nsfw_femdom", "nekos_sfw_neko", "nekos_sfw_waifu", "nekos_sfw_kitsune", "nekos_sfw_smug", "nekos_sfw_holo"]
        self.nsfw_board_names = ["4k", "ahegao", "ass", "anal", "bdsm", "blowjob", "boobs", "cunnilingus", "bottomless", "cumshots", "deepthroat", "dick", "double_penetration", "gay", "group", "hentai", "lesbian", "milf", "public", "rule34", "thigh", "trap", "wild", "redhead", "oboobs", "obutts", "nekos_nsfw_classic", "nekos_nsfw_blowjob", "nekos_nsfw_boobs", "nekos_nsfw_neko", "nekos_nsfw_furry", "nekos_nsfw_pussy", "nekos_nsfw_feet", "nekos_nsfw_yuri", "nekos_nsfw_anal", "nekos_nsfw_solo", "nekos_nsfw_cum", "nekos_nsfw_spank", "nekos_nsfw_cunnilingus", "nekos_nsfw_bdsm", "nekos_nsfw_piercings", "nekos_nsfw_trap", "nekos_nsfw_kitsune", "nekos_nsfw_holo", "nekos_nsfw_femdom"]
        self.weeb_board_names = ["dan", "gel", "kon", "yan", "r34", "safe", "e621", "hentai", "nekos_nsfw_classic", "nekos_nsfw_blowjob", "nekos_nsfw_boobs", "nekos_nsfw_neko", "nekos_nsfw_furry", "nekos_nsfw_pussy", "nekos_nsfw_feet", "nekos_nsfw_yuri", "nekos_nsfw_anal", "nekos_nsfw_solo", "nekos_nsfw_cum", "nekos_nsfw_spank", "nekos_nsfw_cunnilingus", "nekos_nsfw_bdsm", "nekos_nsfw_piercings", "nekos_nsfw_trap", "nekos_nsfw_kitsune", "nekos_nsfw_holo", "nekos_nsfw_femdom", "nekos_sfw_neko", "nekos_sfw_waifu", "nekos_sfw_kitsune", "nekos_sfw_smug", "nekos_sfw_holo"]
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
        """Shows images based on user input and settings"""

        await self.generic_booru(ctx, tag)

    @commands.group()
    async def boorus(self, ctx):
        """Query the boorus"""
        pass

    @boorus.group(autohelp=False)
    @commands.guild_only()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def yan(self, ctx, *, tag=None):
        """Shows images using tags from yande.re"""

        board = "yan"
        await self.generic_specific_source(ctx, board, tag)

    @boorus.group(autohelp=False)
    @commands.guild_only()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def gel(self, ctx, *, tag=None):
        """Shows images using tags from gelbooru"""

        board = "gel"
        await self.generic_specific_source(ctx, board, tag)

    @boorus.group(autohelp=False)
    @commands.guild_only()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def kon(self, ctx, *, tag=None):
        """Shows images using tags from konachan"""

        board = "kon"
        await self.generic_specific_source(ctx, board, tag)

    @boorus.group(autohelp=False)
    @commands.guild_only()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def dan(self, ctx, *, tag=None):
        """Shows images using tags from Danbooru"""

        board = "dan"
        await self.generic_specific_source(ctx, board, tag)

    @boorus.group(autohelp=False)
    @commands.guild_only()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def r34(self, ctx, *, tag=None):
        """Shows images using tags from Rule34"""

        board = "r34"
        await self.generic_specific_source(ctx, board, tag)

    @boorus.group(autohelp=False)
    @commands.guild_only()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def safe(self, ctx, *, tag=None):
        """Shows images using tags from Safebooru"""

        board = "safe"
        await self.generic_specific_source(ctx, board, tag)

    @boorus.group(autohelp=False)
    @commands.guild_only()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def e621(self, ctx, *, tag=None):
        """Shows images using tags from Safebooru"""

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
        """Images from 4k subreddits"""

        board = "4k"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @reddits.group(name="ahegao", autohelp=False)
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _ahegao(self, ctx):
        """Images from ahegao subreddits"""

        board = "ahegao"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @reddits.group(name="ass", autohelp=False)
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _ass(self, ctx):
        """Images from ass subreddits"""

        board = "ass"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @reddits.group(name="anal", autohelp=False)
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _anal(self, ctx):
        """Images from anal subreddits"""

        board = "anal"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @reddits.group(name="bdsm", autohelp=False)
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _bdsm(self, ctx):
        """Images from bdsm subreddits"""

        board = "bdsm"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @reddits.group(name="blowjob", autohelp=False)
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _blowjob(self, ctx):
        """Images from blowjob subreddits"""

        board = "blowjob"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @reddits.group(name="cunnilingus", autohelp=False)
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _cunnilingus(self, ctx):
        """Images from cunnilingus subreddits"""

        board = "cunnilingus"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @reddits.group(name="bottomless", autohelp=False)
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _bottomless(self, ctx):
        """Images from bottomless subreddits"""

        board = "bottomless"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @reddits.group(name="cumshots", autohelp=False)
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _cumshots(self, ctx):
        """Images from cumshots subreddits"""

        board = "cumshots"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @reddits.group(name="deepthroat", autohelp=False)
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _deepthroat(self, ctx):
        """Images from deepthroat subreddits"""

        board = "deepthroat"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @reddits.group(name="dick", autohelp=False)
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _dick(self, ctx):
        """Images from dick subreddits"""

        board = "dick"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @reddits.group(name="doublepenetration", autohelp=False)
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _doublepenetration(self, ctx):
        """Images from double penetration subreddits"""

        board = "double_penetration"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @reddits.group(name="gay", autohelp=False)
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _gay(self, ctx):
        """Images from gay subreddits"""

        board = "gay"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @reddits.group(name="group", autohelp=False)
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _group(self, ctx):
        """Images from group subreddits"""

        board = "group"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @reddits.group(name="hentai", autohelp=False)
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _hentai(self, ctx):
        """Images from hentai subreddits"""

        board = "hentai"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @reddits.group(name="lesbian", autohelp=False)
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _lesbian(self, ctx):
        """Images from lesbian subreddits"""

        board = "lesbian"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @reddits.group(name="milf", autohelp=False)
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _milf(self, ctx):
        """Images from milf subreddits"""

        board = "milf"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @reddits.group(name="public", autohelp=False)
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _public(self, ctx):
        """Images from public subreddits"""

        board = "public"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @reddits.group(name="rule34", autohelp=False)
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _rule34(self, ctx):
        """Images from rule34 subreddits"""

        board = "rule34"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @reddits.group(name="thigh", autohelp=False)
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _thigh(self, ctx):
        """Images from thigh subreddits"""

        board = "thigh"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @reddits.group(name="wild", autohelp=False)
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _wild(self, ctx):
        """Images from wild subreddits"""

        board = "wild"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @reddits.group(name="boobs", autohelp=False)
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _boobs(self, ctx):
        """Images from boobs subreddits"""

        board = "boobs"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @reddits.group(name="redhead", autohelp=False)
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _redhead(self, ctx):
        """Images from redhead subreddits"""

        board = "redhead"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @commands.group()
    async def others(self, ctx):
        """Query Other sources!"""
        pass

    @others.group(name="oboobs", autohelp=False)
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _oboobs(self, ctx):
        """Images from oboobs"""

        board = "oboobs"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @others.group(name="obutts", autohelp=False)
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _obutts(self, ctx):
        """Images from obutts"""

        board = "obutts"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @commands.group()
    async def nekos(self, ctx):
        """Query sources from nekos.life!"""
        pass

    @nekos.group()
    async def nsfw(self, ctx):
        """Query nsfw sources from nekos.life!"""
        pass

    @nsfw.group(name="classic", autohelp=False)
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _nekos_nsfw_classic(self, ctx):
        """Images from classic endpoints"""

        board = "nekos_nsfw_classic"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @nsfw.group(name="blowjob", autohelp=False)
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _nekos_nsfw_blowjob(self, ctx):
        """Images from blowjob endpoints"""

        board = "nekos_nsfw_blowjob"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @nsfw.group(name="boobs", autohelp=False)
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _nekos_nsfw_boobs(self, ctx):
        """Images from boobs endpoints"""

        board = "nekos_nsfw_boobs"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @nsfw.group(name="neko", autohelp=False)
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _nekos_nsfw_neko(self, ctx):
        """Images from nekos endpoints"""

        board = "nekos_nsfw_neko"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @nsfw.group(name="furry", autohelp=False)
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _nekos_nsfw_furry(self, ctx):
        """Images from furry endpoints"""

        board = "nekos_nsfw_furry"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @nsfw.group(name="feet", autohelp=False)
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _nekos_nsfw_feet(self, ctx):
        """Images from feet endpoints"""

        board = "nekos_nsfw_feet"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @nsfw.group(name="yuri", autohelp=False)
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _nekos_nsfw_yuri(self, ctx):
        """Images from yuri endpoints"""

        board = "nekos_nsfw_yuri"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @nsfw.group(name="anal", autohelp=False)
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _nekos_nsfw_anal(self, ctx):
        """Images from anal endpoints"""

        board = "nekos_nsfw_anal"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @nsfw.group(name="solo", autohelp=False)
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _nekos_nsfw_solo(self, ctx):
        """Images from solo endpoints"""

        board = "nekos_nsfw_solo"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @nsfw.group(name="cum", autohelp=False)
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _nekos_nsfw_cum(self, ctx):
        """Images from cum endpoints"""

        board = "nekos_nsfw_cum"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @nsfw.group(name="spank", autohelp=False)
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _nekos_nsfw_spank(self, ctx):
        """Images from spank endpoints"""

        board = "nekos_nsfw_spank"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @nsfw.group(name="cunnilingus", autohelp=False)
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _nekos_nsfw_cunnilingus(self, ctx):
        """Images from cunnilingus endpoints"""

        board = "nekos_nsfw_cunnilingus"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @nsfw.group(name="bdsm", autohelp=False)
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _nekos_nsfw_bdsm(self, ctx):
        """Images from bdsm endpoints"""

        board = "nekos_nsfw_bdsm"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @nsfw.group(name="piercings", autohelp=False)
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _nekos_nsfw_piercings(self, ctx):
        """Images from piercings endpoints"""

        board = "nekos_nsfw_piercings"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @nsfw.group(name="kitsune", autohelp=False)
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _nekos_nsfw_kitsune(self, ctx):
        """Images from kitsune endpoints"""

        board = "nekos_nsfw_kitsune"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @nsfw.group(name="holo", autohelp=False)
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _nekos_nsfw_holo(self, ctx):
        """Images from holo endpoints"""

        board = "nekos_nsfw_holo"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @nsfw.group(name="femdom", autohelp=False)
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _nekos_nsfw_femdom(self, ctx):
        """Images from femdom endpoints"""

        board = "nekos_nsfw_femdom"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @nekos.group()
    async def sfw(self, ctx):
        """Query sfw sources from nekos.life!"""
        pass

    @sfw.group(name="neko", autohelp=False)
    @commands.guild_only()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _nekos_sfw_neko(self, ctx):
        """Images from neko endpoints"""

        board = "nekos_sfw_neko"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @sfw.group(name="waifu", autohelp=False)
    @commands.guild_only()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _nekos_sfw_waifu(self, ctx):
        """Images from waifu endpoints"""

        board = "nekos_sfw_waifu"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @sfw.group(name="kitsune", autohelp=False)
    @commands.guild_only()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _nekos_sfw_kitsune(self, ctx):
        """Images from kitsune endpoints"""

        board = "nekos_sfw_kitsune"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @sfw.group(name="smug", autohelp=False)
    @commands.guild_only()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _nekos_sfw_smug(self, ctx):
        """Images from smug endpoints"""

        board = "nekos_sfw_smug"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    @sfw.group(name="holo", autohelp=False)
    @commands.guild_only()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _nekos_sfw_holo(self, ctx):
        """Images from holo endpoints"""

        board = "nekos_sfw_holo"
        tag = None
        await self.generic_specific_source(ctx, board, tag)

    def __unload(self):
        # Aiohttp closing plz work
        self.session.detach()

