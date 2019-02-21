import discord
from redbot.core import Config, checks, commands
from redbot.core.utils.menus import menu, commands, DEFAULT_CONTROLS
import aiohttp
import contextlib
from random import randint
import os
import asyncio
import logging

log = logging.getLogger("Booru")  # Thanks to Sinbad for the example code for logging
log.setLevel(logging.DEBUG)

console = logging.StreamHandler()

if logging.getLogger("red").isEnabledFor(logging.DEBUG):
    console.setLevel(logging.DEBUG)
else:
    console.setLevel(logging.INFO)
log.addHandler(console)

BaseCog = getattr(commands, "Cog", object)


class Booru(BaseCog):
    """Show a picture using image boards (Gelbooru, yandere, konachan)"""

    def __init__(self):
        self.config = Config.get_conf(self, identifier=4894278742742)
        default_global = {"filters": [], "nsfw_filters": []}
        default_guild = {"filters": [], "nsfw_filters": ["loli", "shota"], "boards": ["dan", "gel", "kon", "yan"]}
        self.config.register_global(**default_global)
        self.config.register_guild(**default_guild)

    @commands.command()
    async def booru(self, ctx, *, tag=None):
        """Shows a image board entry based on user query"""

        tag = await self.filter_tags(ctx, tag)

        if tag is None:
            return

        log.debug(tag)

        # Image board fetcher
        boards = await self.config.guild(ctx.guild).boards()
        if boards == []:
            await ctx.send("There no image boards, please use [p]booruset guild boards to set them.")
            return

        all_data = await asyncio.gather(*(getattr(self, f'fetch_{board}')(ctx, tag) for board in boards))
        data = [item for board_data in all_data for item in board_data]

        # Filter data without using up requests space
        data = await self.filter_posts(ctx, data)

        # Done sending requests, time to show it
        await self.show_booru(ctx, data)

    @commands.command()
    async def yan(self, ctx, *, tag=None):
        """Shows a image board entry based on user query from yande.re"""

        tag = await self.filter_tags(ctx, tag)

        if tag is None:
            return

        log.debug(tag)

        # Image board fetcher
        data = await self.fetch_yan(ctx, tag)

        # Filter data without using up requests space
        data = await self.filter_posts(ctx, data)

        # Done sending requests, time to show it
        await self.show_booru(ctx, data)

    @commands.command()
    async def gel(self, ctx, *, tag=None):
        """Shows a image board entry based on user query from gelbooru"""

        tag = await self.filter_tags(ctx, tag)

        if tag is None:
            return

        log.debug(tag)

        # Image board fetcher
        data = await self.fetch_gel(ctx, tag)

        # Filter data without using up requests space
        data = await self.filter_posts(ctx, data)

        # Done sending requests, time to show it
        await self.show_booru(ctx, data)

    @commands.command()
    async def kon(self, ctx, *, tag=None):
        """Shows a image board entry based on user query from konachan"""

        tag = await self.filter_tags(ctx, tag)

        if tag is None:
            return

        log.debug(tag)

        # Image board fetcher
        data = await self.fetch_kon(ctx, tag)

        # Filter data without using up requests space
        data = await self.filter_posts(ctx, data)

        # Done sending requests, time to show it
        await self.show_booru(ctx, data)

    @commands.command()
    async def dan(self, ctx, *, tag=None):
        """Shows a image board entry based on user query from Danbooru"""

        tag = await self.filter_tags(ctx, tag)

        if tag is None:
            return

        log.debug(tag)

        # Image board fetcher
        data = await self.fetch_dan(ctx, tag)

        # Filter data without using up requests space
        data = await self.filter_posts(ctx, data)

        # Done sending requests, time to show it
        await self.show_booru(ctx, data)

    @commands.command()
    async def r34(self, ctx, *, tag=None):
        """Shows a image board entry based on user query from Rule34"""

        tag = await self.filter_tags(ctx, tag)

        if tag is None:
            return

        log.debug(tag)

        # Image board fetcher
        data = await self.fetch_r34(ctx, tag)
        print (data)

        # Filter data without using up requests space
        data = await self.filter_posts(ctx, data)

        # Done sending requests, time to show it
        await self.show_booru(ctx, data)

    async def filter_tags(self, ctx, tag):
        # Checks if there is a tag and defaults depending on channel
        if tag is not None:
            tag = set(tag.split(" "))
        if ctx.channel.is_nsfw() and tag is None:
            tag = {"rating:none", "*"}
        if ctx.channel.is_nsfw() == False and tag is None:
            tag = {"rating:safe", "*"}

        log.debug(tag)

        # Checks common to see if any ratings are there
        ratings = {"rating:safe", "rating:explicit", "rating:questionable", "rating:none"}
        if not ratings & tag:
            tag.add("rating:safe")

        # Checks if none and removes ratings
        if "rating:none" in tag:
            tag.remove("rating:none")

        # Checks if nsfw could be posted in sfw channel
        if not ctx.channel.is_nsfw():
            if "rating:explicit" in tag or "rating:questionable" in tag or not ratings & tag:
                await ctx.send("You cannot post nsfw content in sfw channels")
                return

        # Checks if more than 6 tag and tells user you can't do that
        if len(tag) > 6:
            await ctx.send("You cannot search for more than 6 tags at once")
            return

        log.debug(tag)

        return tag

    async def filter_posts(self, ctx, data):
        # Global filters
        global_filters = set(await self.config.filters())
        global_nsfw_filters = set(await self.config.nsfw_filters())

        # Guild filters
        guild_group = self.config.guild(ctx.guild)
        guild_nsfw_filters = set(await guild_group.nsfw_filters())
        guild_filters = set(await guild_group.filters())

        # Fuse both global and guild for cleaner use
        filters = global_filters | guild_filters
        nsfw_filters = global_nsfw_filters | guild_nsfw_filters

        # Set variable because
        filtered_data = []

        # Filter the content
        for booru in data:
            booru_tags_string = booru.get("tags") or booru.get("tag_string") or "N/A"
            booru_tags = set(booru_tags_string.split())

            if booru["rating"] in "sqe":
                if filters & booru_tags or (booru["rating"] != "s" and nsfw_filters & booru_tags):
                    continue
            if booru.get("is_deleted"):
                continue

            filtered_data.append(booru)

        return filtered_data

    async def fetch_from_booru(self, urlstr, provider):  # Handles provider data and fetcher responses
        content = ""
        async with aiohttp.ClientSession() as session:
            async with session.get(urlstr) as url:
                try:
                    content = await url.json(content_type=None)
                except (ValueError, aiohttp.ContentTypeError):
                    content = []
        if not content or content == [] or content is None or (type(content) is dict and "success" in content.keys() and content["success"] == False):
            content = []
            return content
        else:
            for item in content:
                item["provider"] = provider
        return content

    async def fetch_yan(self, ctx, tags):  # Yande.re fetcher
        urlstr = "https://yande.re/post.json?limit=100&tags=" + "+".join(tags)
        log.debug(urlstr)
        return await self.fetch_from_booru(urlstr, "Yandere")

    async def fetch_gel(self, ctx, tags):  # Gelbooru fetcher
        urlstr = "https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&limit=100&tags=" + "+".join(tags)
        log.debug(urlstr)
        return await self.fetch_from_booru(urlstr, "Gelbooru")

    async def fetch_kon(self, ctx, tags):  # Konachan fetcher
        urlstr = "https://konachan.com/post.json?limit=100&tags=" + "+".join(tags)
        log.debug(urlstr)
        return await self.fetch_from_booru(urlstr, "Konachan")

    async def fetch_dan(self, ctx, tags):  # Danbooru fetcher
        if len(tags) > 2:
            return []
        urlstr = "https://danbooru.donmai.us/posts.json?limit=100&tags=" + "+".join(tags)
        log.debug(urlstr)
        return await self.fetch_from_booru(urlstr, "Danbooru")

    async def fetch_r34(self, ctx, tags):  # Rule34 fetcher
        urlstr = "https://rule34.xxx/index.php?page=dapi&s=post&q=index&json=1&limit=100&tags=" + "+".join(tags)
        log.debug(urlstr)
        return await self.fetch_from_booru(urlstr, "Rule34")

    async def show_booru(self, ctx, data):  # Shows various info in embed
        mn = len(data)
        if mn == 0:
            await ctx.send("No results.")
        else:

            i = randint(0, mn - 1)

            # Build Embed
            embeds = []

            num_pages = len(data)
            for page_num, booru in enumerate(data, 1):
                # Set variables for owner/author of post
                booru_author = booru.get("owner") or booru.get("author") or booru.get("uploader_name") or "N/A"

                # Set variables for tags
                booru_tags = booru.get("tags") or booru.get("tag_string") or "N/A"

                # Set variables for score
                booru_score = booru.get("score") or "N/A"

                # Set variables for file url
                file_url = booru.get("file_url") or "https://us.rule34.xxx//images/" + booru.get("directory") + "/" + booru.get("image")
                booru_url = file_url

                # Set variable for post link
                if booru["provider"] == "Konachan":
                    booru_post = "https://konachan.com/post/show/" + str(booru.get("id"))
                if booru["provider"] == "Gelbooru":
                    booru_post = "https://gelbooru.com/index.php?page=post&s=view&id=" + str(booru.get("id"))
                if booru["provider"] == "Rule34":
                    booru_post = "https://rule34.xxx/index.php?page=post&s=view&id=" + str(booru.get("id"))
                if booru["provider"] == "Yandere":
                    booru_post = "https://yande.re/post/show/" + str(booru.get("id"))
                if booru["provider"] == "Danbooru":
                    booru_post = "https://danbooru.donmai.us/posts/" + str(booru.get("id"))

                # Set colour for each board
                color = {"Gelbooru": 3395583, "Danbooru": 3395583, "Konachan": 8745592, "Yandere": 2236962, "Rule34": 339933}

                embed = discord.Embed()
                embed.color = color[booru["provider"]]
                embed.title = booru["provider"] + " entry by " + booru_author
                embed.url = booru_post
                embed.set_image(url=booru_url)
                embed.add_field(name="Tags", value="```" + booru_tags[:300] + "```", inline=False)
                embed.add_field(name="Rating", value=booru["rating"])
                embed.add_field(name="Score", value=booru_score)
                embed.set_footer(text=f"{page_num}/{num_pages} If image doesn't appear, it may be a webm or too big, Powered by {booru['provider']}")
                embeds.append(embed)

            await menu(ctx, pages=embeds, controls=DEFAULT_CONTROLS, message=None, page=i, timeout=15)

    # TODO : Use Reaction menus now that I know how with self
    @commands.group()
    @checks.admin_or_permissions()
    async def booruset(self, ctx):
        """Settings for booru \n\n
        These filter whatever you add *out* of the search results, it does not add anything.
        This is because the filters are applied locally instead of in the API to avoid reaching the
        maximum amount of tags given by these APIs."""
        pass

    # Guild configs
    @booruset.group(name="guild")
    @checks.admin_or_permissions(manage_guild=True)
    async def _guild(self, ctx):
        """Guild Settings for booru"""
        pass

    @_guild.group(name="all")
    @checks.admin_or_permissions(manage_guild=True)
    async def _guild_allfilters(self, ctx):
        """Commands pertaining to all filters which apply on the guild"""
        pass

    @_guild_allfilters.command(name="show")
    @checks.admin_or_permissions(manage_guild=True)
    async def _guild_allfilters_show(self, ctx):
        """Filters that apply to all guild queries"""
        filters = await self.config.guild(ctx.guild).filters()
        await self.generic_show(ctx, filters)

    @_guild_allfilters.command(name="add")
    @checks.admin_or_permissions(manage_guild=True)
    async def _guild_allfilters_add(self, ctx, *, filter):
        """Add guild filters"""

        # Load config
        config_filters = await self.config.guild(ctx.guild).filters()

        origin = ["all"]
        await self.generic_add(ctx, origin, config_filters, filter)

    @_guild_allfilters.command(name="remove")
    @checks.admin_or_permissions(manage_guild=True)
    async def _guild_allfilters_remove(self, ctx, *, filter):
        """Remove guild filters"""

        # Load config
        config_filters = await self.config.guild(ctx.guild).filters()

        origin = ["all"]
        await self.generic_remove(ctx, origin, config_filters, filter)

    @_guild.group(name="nsfw")
    @checks.admin_or_permissions(manage_guild=True)
    async def _guild_nsfwfilters(self, ctx):
        """Commands pertaining to guild NSFW filters which apply on the guild"""
        pass

    @_guild_nsfwfilters.command(name="show")
    @checks.admin_or_permissions(manage_guild=True)
    async def _guild_nsfwfilters_show(self, ctx):
        """Show global nsfw filters"""

        filters = await self.config.guild(ctx.guild).nsfw_filters()
        await self.generic_show(ctx, filters)

    @_guild_nsfwfilters.command(name="add")
    @checks.admin_or_permissions(manage_guild=True)
    async def _guild_nsfwfilters_add(self, ctx, *, filter):
        """Add guild nsfw filters"""

        # Load config
        config_filters = await self.config.guild(ctx.guild).nsfw_filters()

        origin = ["nsfw"]
        await self.generic_add(ctx, origin, config_filters, filter)

    @_guild_nsfwfilters.command(name="remove")
    @checks.admin_or_permissions(manage_guild=True)
    async def _guild_nsfwfilters_remove(self, ctx, *, filter):
        """Remove guild nsfw filters"""

        # Load config
        config_filters = await self.config.guild(ctx.guild).nsfw_filters()

        origin = ["nsfw"]
        await self.generic_remove(ctx, origin, config_filters, filter)

    # Global configs
    @booruset.group(name="global")
    @checks.is_owner()
    async def _global(self, ctx):
        """Global Settings for booru"""
        pass

    @_global.group(name="all")
    @checks.is_owner()
    async def _global_allfilters(self, ctx):
        """Commands pertaining to all filters which apply globally"""
        pass

    @_global_allfilters.command(name="show")
    @checks.is_owner()
    async def _global_allfilters_show(self, ctx):
        """Show current global filters which apply to all queries"""
        filters = await self.config.filters()
        await self.generic_show(ctx, filters)

    @_global_allfilters.command(name="add")
    @checks.is_owner()
    async def _global_allfilters_add(self, ctx, *, filter):
        """Add global filters"""

        # Load config
        config_filters = await self.config.filters()

        origin = ["global", "all"]
        await self.generic_add(ctx, origin, config_filters, filter)

    @_global_allfilters.command(name="remove")
    @checks.is_owner()
    async def _global_allfilters_remove(self, ctx, *, filter):
        """Remove global nsfw filters"""

        # Load config
        config_filters = await self.config.filters()

        origin = ["global", "all"]
        await self.generic_remove(ctx, origin, config_filters, filter)

    @_global.group(name="nsfw")
    @checks.is_owner()
    async def _global_nsfwfilters(self, ctx):
        """Commands pertaining to NSFW filters which apply globally"""
        pass

    @_global_nsfwfilters.command(name="show")
    @checks.is_owner()
    async def _global_nsfwfilters_show(self, ctx):
        """Show global nsfw filters"""
        filters = await self.config.nsfw_filters()
        await self.generic_show(ctx, filters)

    @_global_nsfwfilters.command(name="add")
    @checks.is_owner()
    async def _global_nsfwfilters_add(self, ctx, *, filter):
        """Add global nsfw filters"""

        # Load config
        config_filters = await self.config.nsfw_filters()

        origin = ["global", "nsfw"]
        await self.generic_add(ctx, origin, config_filters, filter)

    @_global_nsfwfilters.command(name="remove")
    @checks.is_owner()
    async def _global_nsfwfilters_remove(self, ctx, *, filter):
        """Remove global nsfw filters"""

        # Load config
        config_filters = await self.config.nsfw_filters()

        origin = ["global", "nsfw"]
        await self.generic_remove(ctx, origin, config_filters, filter)

    async def generic_show(self, ctx, filters):
        if not filters:
            await ctx.send("There are currently no filters")
        else:
            await ctx.send(f"Current filters are: ```{','.join(filters)}```")

    async def generic_add(self, ctx, origin, config_filters, filter):

        filter = set(filter.split(" "))

        config_filters = set(config_filters)
        config_filters.update(filter)

        # Check variables to see where they come from and do the right thing
        if "all" in origin:
            await self.config.guild(ctx.guild).filters.set(list(config_filters))
        if "nsfw" in origin:
            await self.config.guild(ctx.guild).nsfw_filters.set(list(config_filters))
        if "all" in origin and "global" in origin:
            await self.config.filters.set(list(config_filters))
        if "nsfw" in origin and "global" in origin:
            await self.config.nsfw_filters.set(list(config_filters))
        await ctx.send("The filters have been added!")

    async def generic_remove(self, ctx, origin, config_filters, filter):

        filter = set(filter.split(" "))

        config_filters = set(config_filters)

        # Check variables to see where they come from and do the right thing
        if "all" in origin:
            await self.config.guild(ctx.guild).filters.set(list(set(config_filters) - set(filter)))
        if "nsfw" in origin:
            await self.config.guild(ctx.guild).nsfw_filters.set(list(set(config_filters) - set(filter)))
        if "all" in origin and "global" in origin:
            await self.config.filters.set(list(set(config_filters) - set(filter)))
        if "nsfw" in origin and "global" in origin:
            await self.config.nsfw_filters.set(list(set(config_filters) - set(filter)))
        await ctx.send("The filters have been removed!")

    @_guild.group(name="boards")
    @checks.admin_or_permissions(manage_guild=True)
    async def _guild_boards(self, ctx):
        """Commands pertaining to which boards are shown in booru"""
        pass

    @_guild_boards.command(name="show")
    @checks.admin_or_permissions(manage_guild=True)
    async def _guild_boards_show(self, ctx):
        """Show booru boards"""
        boards = await self.config.guild(ctx.guild).boards()
        if not boards:
            await ctx.send("There are currently no boards shown in booru")
        else:
            await ctx.send(f"Current boards shown in booru are: ```{','.join(boards)}```")

    @_guild_boards.command(name="add")
    @checks.is_owner()
    async def _global_boards_add(self, ctx, *, boards):
        """Add image boards to booru"""

        # Load config
        config_boards = await self.config.guild(ctx.guild).boards()

        # Filter input
        boards = await self.boards_filter(boards)
        if boards is None:
            await ctx.send("Reminder that the board names that can be used are dan, gel, kon, yan and r34. Please try again")
            return

        # Fuse input and config
        config_boards = set(config_boards)
        config_boards.update(boards)

        # Set new config
        await self.config.guild(ctx.guild).boards.set(list(config_boards))
        await ctx.send("The boards have been added.")

    @_guild_boards.command(name="remove")
    @checks.is_owner()
    async def _global_boards_remove(self, ctx, *, boards):
        """Remove image boards to booru"""

        # Load config
        config_boards = await self.config.guild(ctx.guild).boards()

        # Filter input
        boards = await self.boards_filter(boards)
        if boards is None:
            await ctx.send("Reminder that the board names that can be used are dan, gel, kon, yan. Please try again")
            return

        # Set new config
        config_boards = set(config_boards)
        await self.config.guild(ctx.guild).boards.set(list(set(config_boards) - set(boards)))
        await ctx.send("The boards have been removed.")

    async def boards_filter(self, boards):

        boards = set(boards.split(" "))

        # Set variable to see which are good
        correct_board_names = ["dan", "gel", "kon", "yan", "r34"]

        # Check if good
        if boards & set(correct_board_names):
            return boards
        else:
            return
