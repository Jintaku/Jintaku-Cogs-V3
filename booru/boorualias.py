import discord
from redbot.core import Config, checks, commands
from redbot.core.utils.menus import menu, commands, DEFAULT_CONTROLS
import asyncio
import logging

from .boorucore import BooruCore

class Boorualias:
    """Show a picture using image boards (Gelbooru, yandere, konachan)"""

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def neko(self, ctx, *, tag=""):
        """Shows a neko image board entry based on user query"""

        tag_default = " neko"
        tag += tag_default
        boards = ["dan", "gel", "kon", "yan", "safe"]

        await self.generic_alias_booru(ctx, boards, tag)

    @commands.command(name="4k")
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def _4_k(self, ctx, *, tag=""):
        """Shows a 4k image board entry based on user query"""

        tag_default = " 4k"
        tag += tag_default
        boards = ["dan", "gel", "kon", "yan", "safe", "4k"]

        await self.generic_alias_booru(ctx, boards, tag)

    @commands.command()
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def ahegao(self, ctx, *, tag=""):
        """Shows a ahegao image board entry based on user query"""

        tag_default = " ahegao"
        tag += tag_default
        boards = ["dan", "gel", "kon", "yan", "safe", "ahegao"]

        await self.generic_alias_booru(ctx, boards, tag)

    @commands.command()
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def anal(self, ctx, *, tag=""):
        """Shows a anal image board entry based on user query"""

        tag_default = " anal"
        tag += tag_default
        boards = ["dan", "gel", "kon", "yan", "safe", "anal"]

        await self.generic_alias_booru(ctx, boards, tag)

    @commands.command()
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def ass(self, ctx, *, tag=""):
        """Shows a ass image board entry based on user query"""

        tag_default = " ass"
        tag += tag_default
        boards = ["dan", "gel", "kon", "yan", "safe", "ass"]

        await self.generic_alias_booru(ctx, boards, tag)

    @commands.command()
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def bdsm(self, ctx, *, tag=""):
        """Shows a bdsm image board entry based on user query"""

        tag_default = " bdsm"
        tag += tag_default
        boards = ["dan", "gel", "kon", "yan", "safe", "bdsm"]

        await self.generic_alias_booru(ctx, boards, tag)

    @commands.command()
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def boobs(self, ctx, *, tag=""):
        """Shows a boobs image board entry based on user query"""

        tag_default = " boobs"
        tag += tag_default
        boards = ["dan", "gel", "kon", "yan", "safe", "boobs"]

        await self.generic_alias_booru(ctx, boards, tag)

    @commands.command()
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def bottomless(self, ctx, *, tag=""):
        """Shows a boobs image board entry based on user query"""

        tag_default = " bottomless"
        tag += tag_default
        boards = ["dan", "gel", "kon", "yan", "safe", "bottomless"]

        await self.generic_alias_booru(ctx, boards, tag)

    @commands.command()
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def blowjob(self, ctx, *, tag=""):
        """Shows a boobs image board entry based on user query"""

        tag_default = " blowjob"
        tag += tag_default
        boards = ["dan", "gel", "kon", "yan", "safe", "blowjob"]

        await self.generic_alias_booru(ctx, boards, tag)

    @commands.command()
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def cumon(self, ctx, *, tag=""):
        """Shows a boobs image board entry based on user query"""

        tag_default = " cum_on_*"
        tag += tag_default
        boards = ["dan", "gel", "kon", "yan", "safe", "cumshots"]

        await self.generic_alias_booru(ctx, boards, tag)

    @commands.command()
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def cunni(self, ctx, *, tag=""):
        """Shows a cunnilingus image board entry based on user query"""

        tag_default = " cunnilingus"
        tag += tag_default
        boards = ["dan", "gel", "kon", "yan", "safe", "cunnilingus"]

        await self.generic_alias_booru(ctx, boards, tag)

    @commands.command()
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def deepthroat(self, ctx, *, tag=""):
        """Shows a deepthroat image board entry based on user query"""

        tag_default = " deepthroat"
        tag += tag_default
        boards = ["dan", "gel", "kon", "yan", "safe", "deepthroat"]

        await self.generic_alias_booru(ctx, boards, tag)

    @commands.command()
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def dick(self, ctx, *, tag=""):
        """Shows a dick image board entry based on user query"""

        tag_default = " dick"
        tag += tag_default
        boards = ["dan", "gel", "kon", "yan", "safe", "dick"]

        await self.generic_alias_booru(ctx, boards, tag)

    @commands.command()
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def doublepenetration(self, ctx, *, tag=""):
        """Shows a doublepenetration image board entry based on user query"""

        tag_default = " double_penetration"
        tag += tag_default
        boards = ["dan", "gel", "kon", "yan", "safe", "double_penetration"]

        await self.generic_alias_booru(ctx, boards, tag)

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def yaoi(self, ctx, *, tag=""):
        """Shows a yaoi image board entry based on user query"""

        tag_default = " yaoi"
        tag += tag_default
        boards = ["dan", "gel", "kon", "yan", "safe", "gay"]

        await self.generic_alias_booru(ctx, boards, tag)

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def lesbian(self, ctx, *, tag=""):
        """Shows a lesbian image board entry based on user query"""

        tag_default = " lesbian yuri"
        tag += tag_default
        boards = ["dan", "gel", "kon", "yan", "safe", "lesbian"]

        await self.generic_alias_booru(ctx, boards, tag)

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def milf(self, ctx, *, tag=""):
        """Shows a milf image board entry based on user query"""

        tag_default = " milf"
        tag += tag_default
        boards = ["dan", "gel", "kon", "yan", "safe", "milf"]

        await self.generic_alias_booru(ctx, boards, tag)

    @commands.command()
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def oral(self, ctx, *, tag=""):
        """Shows a oral image board entry based on user query"""

        tag_default = " oral"
        tag += tag_default
        boards = ["dan", "gel", "kon", "yan", "cunnilingus", "blowjob", "deepthroat"]

        await self.generic_alias_booru(ctx, boards, tag)

    @commands.command()
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def public(self, ctx, *, tag=""):
        """Shows a public sex image board entry based on user query"""

        tag_default = " public"
        tag += tag_default
        boards = ["dan", "gel", "kon", "yan", "safe", "public"]

        await self.generic_alias_booru(ctx, boards, tag)

    @commands.command()
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def pussy(self, ctx, *, tag=""):
        """Shows a pussy image board entry based on user query"""

        tag_default = " pussy"
        tag += tag_default
        boards = ["dan", "gel", "kon", "yan", "safe", "pussy", "cunnilingus"]

        await self.generic_alias_booru(ctx, boards, tag)

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def thigh(self, ctx, *, tag=""):
        """Shows a thigh image board entry based on user query"""

        tag_default = " thigh"
        tag += tag_default
        boards = ["dan", "gel", "kon", "yan", "safe", "thigh"]

        await self.generic_alias_booru(ctx, boards, tag)

    @commands.command()
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def trap(self, ctx, *, tag=""):
        """Shows a trap image board entry based on user query"""

        tag_default = " trap"
        tag += tag_default
        boards = ["dan", "gel", "kon", "yan", "safe", "trap"]

        await self.generic_alias_booru(ctx, boards, tag)

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def red(self, ctx, *, tag=""):
        """Shows a redhead image board entry based on user query"""

        tag_default = " red_hair"
        tag += tag_default
        boards = ["dan", "gel", "kon", "yan", "safe"]

        await self.generic_alias_booru(ctx, boards, tag)

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def collar(self, ctx, *, tag=""):
        """Shows a image of someone with a collar board entry based on user query"""

        tag_default = " collar"
        tag += tag_default
        boards = ["dan", "gel", "kon", "yan", "safe"]

        await self.generic_alias_booru(ctx, boards, tag)

    @commands.command()
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def group(self, ctx, *, tag=""):
        """Shows a group sex image board entry based on user query"""

        tag_default = " group_sex gangbang"
        tag += tag_default
        boards = ["dan", "gel", "kon", "yan", "safe", "group"]

        await self.generic_alias_booru(ctx, boards, tag)

    @commands.command()
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def wild(self, ctx, *, tag=""):
        """Shows a futanari image board entry based on user query"""

        tag_default = " wild"
        tag += tag_default
        boards = ["dan", "gel", "kon", "yan", "safe", "wild"]

        await self.generic_alias_booru(ctx, boards, tag)
