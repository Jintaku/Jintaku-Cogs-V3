import discord
from redbot.core import Config, checks, commands
from redbot.core.utils.menus import menu, commands, DEFAULT_CONTROLS
import aiohttp
import contextlib
from random import randint
import asyncio
import logging
from . import boorusources
from aiocache import cached, SimpleMemoryCache

cache = SimpleMemoryCache()

log = logging.getLogger("BooruCore")  # Thanks to Sinbad for the example code for logging
log.setLevel(logging.DEBUG)

console = logging.StreamHandler()

if logging.getLogger("red").isEnabledFor(logging.DEBUG):
    console.setLevel(logging.DEBUG)
else:
    console.setLevel(logging.INFO)
log.addHandler(console)

class BooruCore:

    async def generic_booru(self, ctx, tag):

        tag = await self.filter_tags(ctx, tag)

        # If it returns nothing, something is wrong
        if tag is None:
            return

        # Log tag for debugging purposes
        log.debug(tag)

        # Image boards chosen
        guild_boards = await self.config.guild(ctx.guild).boards()
        channel_boards = await self.config.channel(ctx.channel).boards()

        # If channel setting is default, use guild setting
        if set(channel_boards) == {"dan", "gel", "kon", "yan"}:
            boards = guild_boards
        else:
            boards = channel_boards

        # Clean boards if sfw
        log.debug(boards)
        filtered_boards = []
        if ctx.message.channel.is_nsfw() is False:
            for board in boards:
                if board not in self.nsfw_board_names:
                    filtered_boards.append(board)
            boards = filtered_boards
        log.debug(boards)

        # Remove non-weeb sources
        log.debug(boards)
        filtered_boards = []
        guild_weebmode = await self.config.guild(ctx.guild).weebmode()
        channel_weebmode = await self.config.guild(ctx.channel).weebmode()
        if guild_weebmode == "on" or channel_weebmode == "on":
            for board in boards:
                if board in self.weeb_board_names:
                    filtered_boards.append(board)
            boards = filtered_boards
        log.debug(boards)

        # If no image boards chosen, tell them
        if boards == []:
            await ctx.send("There no image boards, please use [p]booruset guild boards to set them.")
            return

        # Fetch all the stuff!
        async with ctx.typing():
            all_data = await asyncio.gather(*(getattr(self, f"fetch_{board}")(ctx, tag) for board in boards))
        data = [item for board_data in all_data for item in board_data]

        # Filter data without using up requests space
        data = await self.filter_posts(ctx, data)

        # Done sending requests, time to show it
        await self.show_booru(ctx, data)

    async def generic_alias_booru(self, ctx, boards, tag):

        tag = await self.filter_tags(ctx, tag)

        # If it returns nothing, something is wrong
        if tag is None:
            return

        # Log tag for debugging purposes
        log.debug(tag)

        # Clean boards if sfw
        log.debug(boards)
        filtered_boards = []
        if ctx.message.channel.is_nsfw() is False:
            for board in boards:
                if board not in self.nsfw_board_names:
                    filtered_boards.append(board)
            boards = filtered_boards
        log.debug(boards)

        # Remove non-weeb sources
        log.debug(boards)
        filtered_boards = []
        guild_weebmode = await self.config.guild(ctx.guild).weebmode()
        channel_weebmode = await self.config.guild(ctx.channel).weebmode()
        if guild_weebmode == "on" or channel_weebmode == "on":
            for board in boards:
                if board in self.weeb_board_names:
                    filtered_boards.append(board)
            boards = filtered_boards
        log.debug(boards)

        # Fetch all the stuff!
        async with ctx.typing():
            all_data = await asyncio.gather(*(getattr(self, f"fetch_{board}")(ctx, tag) for board in boards))
        data = [item for board_data in all_data if board_data is not None for item in board_data]

        # Filter data without using up requests space
        data = await self.filter_posts(ctx, data)

        # Done sending requests, time to show it
        await self.show_booru(ctx, data)

    async def generic_specific_source(self, ctx, board, tag):
        """Shows a image board entry based on user query from a specific source"""

        tag = await self.filter_tags(ctx, tag)

        if tag is None:
            return

        log.debug(tag)

        # Image board fetcher
        async with ctx.typing():
            data = await getattr(self, f"fetch_{board}")(ctx, tag)

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
        if ctx.channel.is_nsfw() and tag is not None:
            tag.add("rating:none")
        if ctx.channel.is_nsfw() == False and tag is None:
            tag = {"rating:safe", "*"}

        log.debug(tag)

        # Checks common to see if any ratings are there
        ratings = {"rating:safe", "rating:explicit", "rating:questionable", "rating:none", "rating:s", "rating:q", "rating:e"}
        if not ratings & tag:
            tag.add("rating:safe")

        # Checks if none and removes ratings
        if "rating:none" in tag:
            tag.remove("rating:none")

        # Checks if nsfw could be posted in sfw channel
        if not ctx.channel.is_nsfw():

            # Respect onlynsfw setting
            nsfw_booru = await self.config.guild(ctx.guild).onlynsfw()
            if nsfw_booru == "on":
                await ctx.send("You cannot use booru in sfw channels")
                return

            # Checks if explicit or questionable or qe
            if "rating:explicit" in tag or "rating:questionable" in tag or "rating:q" in tag or "rating:e" in tag:
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

        # Set variable because it needs to be set before it can be appended to
        filtered_data = []

        # Filter the content
        for booru in data:
            booru_tags = set(booru["tags"].split())

            # Checks if rating is safe then if filters match with tags
            if booru["rating"] == "s" or booru["rating"] =="safe":
                if filters & booru_tags:
                    continue
            # Checks if rating is explicit or questions then if nsfw fitlers match with tags
            if booru["rating"] in "qe" or booru["rating"] == "questionable" or booru["rating"] == "explicit":
                if nsfw_filters & booru_tags:
                    continue
            # Checks if deleted
            if booru.get("is_deleted"):
                continue
            # Another check for Danbooru because sometimes there's no file_url
            if booru["provider"] == "Danbooru" and "file_url" not in booru:
                continue

            filtered_data.append(booru)

        return filtered_data

    async def fetch_from_nekos(self, urlstr, rating, provider):  # Handles provider data and fetcher responses
        content = ""

        async with self.session.get(urlstr, headers={'User-Agent': "Booru (https://github.com/Jintaku/Jintaku-Cogs-V3)"}) as resp:
            try:
                content = await resp.json(content_type=None)
            except (ValueError, aiohttp.ContentTypeError) as ex:
                log.debug("Pruned by exception, error below:")
                log.debug(ex)
                content = []
        if not content or content == [] or content is None or (type(content) is dict and "success" in content.keys() and content["success"] == False):
            content = []
            return content
        else:
            # Assign stuff to be used by booru_show
            nekos_content = []
            item = {}
            for url in content["data"]["response"]["urls"]:
                item["post_link"] = url
                item["file_url"] = url
                item["provider"] = provider
                item["author"] = "N/A"
                item["rating"] = rating
                item["score"] = "N/A"
                item["tags"] = "N/A"
                nekos_content.append(item)
                item = {}
        return nekos_content

    @cached(ttl=600, cache=SimpleMemoryCache, key="nekos_nsfw_classic")
    async def fetch_nekos_nsfw_classic(self, ctx, tag):  # Nekos nsfw classic fetcher
        life = boorusources.nekos_nsfw_classic
        all_content = []
        for nekos in life:
            urlstr = "https://api.nekos.dev/api/v3/" + nekos + "/?count=20"
            log.debug(urlstr)
            content = await self.fetch_from_nekos(urlstr, "explicit", "Nekos.life")
            all_content.extend(content)
        return all_content

    @cached(ttl=600, cache=SimpleMemoryCache, key="nekos_nsfw_blowjob")
    async def fetch_nekos_nsfw_blowjob(self, ctx, tag):  # Nekos nsfw blowjob fetcher
        life = boorusources.nekos_nsfw_blowjob
        all_content = []
        for nekos in life:
            urlstr = "https://api.nekos.dev/api/v3/" + nekos + "/?count=20"
            log.debug(urlstr)
            content = await self.fetch_from_nekos(urlstr, "explicit", "Nekos.life")
            all_content.extend(content)
        return all_content

    @cached(ttl=600, cache=SimpleMemoryCache, key="nekos_nsfw_boobs")
    async def fetch_nekos_nsfw_boobs(self, ctx, tag):  # Nekos nsfw boobs fetcher
        life = boorusources.nekos_nsfw_boobs
        all_content = []
        for nekos in life:
            urlstr = "https://api.nekos.dev/api/v3/" + nekos + "/?count=20"
            log.debug(urlstr)
            content = await self.fetch_from_nekos(urlstr, "explicit", "Nekos.life")
            all_content.extend(content)
        return all_content

    @cached(ttl=600, cache=SimpleMemoryCache, key="nekos_nsfw_neko")
    async def fetch_nekos_nsfw_neko(self, ctx, tag):  # Nekos nsfw neko fetcher
        life = boorusources.nekos_nsfw_neko
        all_content = []
        for nekos in life:
            urlstr = "https://api.nekos.dev/api/v3/" + nekos + "/?count=20"
            log.debug(urlstr)
            content = await self.fetch_from_nekos(urlstr, "explicit", "Nekos.life")
            all_content.extend(content)
        return all_content

    @cached(ttl=600, cache=SimpleMemoryCache, key="nekos_nsfw_furry")
    async def fetch_nekos_nsfw_furry(self, ctx, tag):  # Nekos nsfw furry fetcher
        life = boorusources.nekos_nsfw_furry
        all_content = []
        for nekos in life:
            urlstr = "https://api.nekos.dev/api/v3/" + nekos + "/?count=20"
            log.debug(urlstr)
            content = await self.fetch_from_nekos(urlstr, "explicit", "Nekos.life")
            all_content.extend(content)
        return all_content

    @cached(ttl=600, cache=SimpleMemoryCache, key="nekos_nsfw_pussy")
    async def fetch_nekos_nsfw_pussy(self, ctx, tag):  # Nekos nsfw pussy fetcher
        life = boorusources.nekos_nsfw_pussy
        all_content = []
        for nekos in life:
            urlstr = "https://api.nekos.dev/api/v3/" + nekos + "/?count=20"
            log.debug(urlstr)
            content = await self.fetch_from_nekos(urlstr, "explicit", "Nekos.life")
            all_content.extend(content)
        return all_content

    @cached(ttl=600, cache=SimpleMemoryCache, key="nekos_nsfw_feet")
    async def fetch_nekos_nsfw_feet(self, ctx, tag):  # Nekos nsfw feet fetcher
        life = boorusources.nekos_nsfw_feet
        all_content = []
        for nekos in life:
            urlstr = "https://api.nekos.dev/api/v3/" + nekos + "/?count=20"
            log.debug(urlstr)
            content = await self.fetch_from_nekos(urlstr, "explicit", "Nekos.life")
            all_content.extend(content)
        return all_content

    @cached(ttl=600, cache=SimpleMemoryCache, key="nekos_nsfw_yuri")
    async def fetch_nekos_nsfw_yuri(self, ctx, tag):  # Nekos nsfw yuri fetcher
        life = boorusources.nekos_nsfw_yuri
        all_content = []
        for nekos in life:
            urlstr = "https://api.nekos.dev/api/v3/" + nekos + "/?count=20"
            log.debug(urlstr)
            content = await self.fetch_from_nekos(urlstr, "explicit", "Nekos.life")
            all_content.extend(content)
        return all_content

    @cached(ttl=600, cache=SimpleMemoryCache, key="nekos_nsfw_anal")
    async def fetch_nekos_nsfw_anal(self, ctx, tag):  # Nekos nsfw anal fetcher
        life = boorusources.nekos_nsfw_anal
        all_content = []
        for nekos in life:
            urlstr = "https://api.nekos.dev/api/v3/" + nekos + "/?count=20"
            log.debug(urlstr)
            content = await self.fetch_from_nekos(urlstr, "explicit", "Nekos.life")
            all_content.extend(content)
        return all_content

    @cached(ttl=600, cache=SimpleMemoryCache, key="nekos_nsfw_solo")
    async def fetch_nekos_nsfw_solo(self, ctx, tag):  # Nekos nsfw solo fetcher
        life = boorusources.nekos_nsfw_solo
        all_content = []
        for nekos in life:
            urlstr = "https://api.nekos.dev/api/v3/" + nekos + "/?count=20"
            log.debug(urlstr)
            content = await self.fetch_from_nekos(urlstr, "explicit", "Nekos.life")
            all_content.extend(content)
        return all_content

    @cached(ttl=600, cache=SimpleMemoryCache, key="nekos_nsfw_cum")
    async def fetch_nekos_nsfw_cum(self, ctx, tag):  # Nekos nsfw cum fetcher
        life = boorusources.nekos_nsfw_cum
        all_content = []
        for nekos in life:
            urlstr = "https://api.nekos.dev/api/v3/" + nekos + "/?count=20"
            log.debug(urlstr)
            content = await self.fetch_from_nekos(urlstr, "explicit", "Nekos.life")
            all_content.extend(content)
        return all_content

    @cached(ttl=600, cache=SimpleMemoryCache, key="nekos_nsfw_spank")
    async def fetch_nekos_nsfw_spank(self, ctx, tag):  # Nekos nsfw spank fetcher
        life = boorusources.nekos_nsfw_spank
        all_content = []
        for nekos in life:
            urlstr = "https://api.nekos.dev/api/v3/" + nekos + "/?count=20"
            log.debug(urlstr)
            content = await self.fetch_from_nekos(urlstr, "explicit", "Nekos.life")
            all_content.extend(content)
        return all_content

    @cached(ttl=600, cache=SimpleMemoryCache, key="nekos_nsfw_cunnilingus")
    async def fetch_nekos_nsfw_cunnilingus(self, ctx, tag):  # Nekos nsfw cunnilingus fetcher
        life = boorusources.nekos_nsfw_cunnilingus
        all_content = []
        for nekos in life:
            urlstr = "https://api.nekos.dev/api/v3/" + nekos + "/?count=20"
            log.debug(urlstr)
            content = await self.fetch_from_nekos(urlstr, "explicit", "Nekos.life")
            all_content.extend(content)
        return all_content

    @cached(ttl=600, cache=SimpleMemoryCache, key="nekos_nsfw_bdsm")
    async def fetch_nekos_nsfw_bdsm(self, ctx, tag):  # Nekos nsfw bdsm fetcher
        life = boorusources.nekos_nsfw_bdsm
        all_content = []
        for nekos in life:
            urlstr = "https://api.nekos.dev/api/v3/" + nekos + "/?count=20"
            log.debug(urlstr)
            content = await self.fetch_from_nekos(urlstr, "explicit", "Nekos.life")
            all_content.extend(content)
        return all_content

    @cached(ttl=600, cache=SimpleMemoryCache, key="nekos_nsfw_piercings")
    async def fetch_nekos_nsfw_piercings(self, ctx, tag):  # Nekos nsfw piercings fetcher
        life = boorusources.nekos_nsfw_piercings
        all_content = []
        for nekos in life:
            urlstr = "https://api.nekos.dev/api/v3/" + nekos + "/?count=20"
            log.debug(urlstr)
            content = await self.fetch_from_nekos(urlstr, "explicit", "Nekos.life")
            all_content.extend(content)
        return all_content

    @cached(ttl=600, cache=SimpleMemoryCache, key="nekos_nsfw_kitsune")
    async def fetch_nekos_nsfw_kitsune(self, ctx, tag):  # Nekos nsfw kitsune fetcher
        life = boorusources.nekos_nsfw_kitsune
        all_content = []
        for nekos in life:
            urlstr = "https://api.nekos.dev/api/v3/" + nekos + "/?count=20"
            log.debug(urlstr)
            content = await self.fetch_from_nekos(urlstr, "explicit", "Nekos.life")
            all_content.extend(content)
        return all_content

    @cached(ttl=600, cache=SimpleMemoryCache, key="nekos_nsfw_holo")
    async def fetch_nekos_nsfw_holo(self, ctx, tag):  # Nekos nsfw holo fetcher
        life = boorusources.nekos_nsfw_holo
        all_content = []
        for nekos in life:
            urlstr = "https://api.nekos.dev/api/v3/" + nekos + "/?count=20"
            log.debug(urlstr)
            content = await self.fetch_from_nekos(urlstr, "explicit", "Nekos.life")
            all_content.extend(content)
        return all_content

    @cached(ttl=600, cache=SimpleMemoryCache, key="nekos_nsfw_femdom")
    async def fetch_nekos_nsfw_femdom(self, ctx, tag):  # Nekos nsfw femdom fetcher
        life = boorusources.nekos_nsfw_femdom
        all_content = []
        for nekos in life:
            urlstr = "https://api.nekos.dev/api/v3/" + nekos + "/?count=20"
            log.debug(urlstr)
            content = await self.fetch_from_nekos(urlstr, "explicit", "Nekos.life")
            all_content.extend(content)
        return all_content

    @cached(ttl=600, cache=SimpleMemoryCache, key="nekos_sfw_neko")
    async def fetch_nekos_sfw_neko(self, ctx, tag):  # Nekos sfw neko fetcher
        life = boorusources.nekos_sfw_neko
        all_content = []
        for nekos in life:
            urlstr = "https://api.nekos.dev/api/v3/" + nekos + "/?count=20"
            log.debug(urlstr)
            content = await self.fetch_from_nekos(urlstr, "safe", "Nekos.life")
            all_content.extend(content)
        return all_content

    @cached(ttl=600, cache=SimpleMemoryCache, key="nekos_sfw_waifu")
    async def fetch_nekos_sfw_waifu(self, ctx, tag):  # Nekos sfw waifu fetcher
        life = boorusources.nekos_sfw_waifu
        all_content = []
        for nekos in life:
            urlstr = "https://api.nekos.dev/api/v3/" + nekos + "/?count=20"
            log.debug(urlstr)
            content = await self.fetch_from_nekos(urlstr, "safe", "Nekos.life")
            all_content.extend(content)
        return all_content

    @cached(ttl=600, cache=SimpleMemoryCache, key="nekos_sfw_kitsune")
    async def fetch_nekos_sfw_kitsune(self, ctx, tag):  # Nekos sfw kitsune fetcher
        life = boorusources.nekos_sfw_kitsune
        all_content = []
        for nekos in life:
            urlstr = "https://api.nekos.dev/api/v3/" + nekos + "/?count=20"
            log.debug(urlstr)
            content = await self.fetch_from_nekos(urlstr, "safe", "Nekos.life")
            all_content.extend(content)
        return all_content

    @cached(ttl=600, cache=SimpleMemoryCache, key="nekos_sfw_smug")
    async def fetch_nekos_sfw_smug(self, ctx, tag):  # Nekos sfw smug fetcher
        life = boorusources.nekos_sfw_smug
        all_content = []
        for nekos in life:
            urlstr = "https://api.nekos.dev/api/v3/" + nekos + "/?count=20"
            log.debug(urlstr)
            content = await self.fetch_from_nekos(urlstr, "safe", "Nekos.life")
            all_content.extend(content)
        return all_content

    @cached(ttl=600, cache=SimpleMemoryCache, key="nekos_sfw_holo")
    async def fetch_nekos_sfw_holo(self, ctx, tag):  # Nekos sfw holo fetcher
        life = boorusources.nekos_sfw_holo
        all_content = []
        for nekos in life:
            urlstr = "https://api.nekos.dev/api/v3/" + nekos + "/?count=20"
            log.debug(urlstr)
            content = await self.fetch_from_nekos(urlstr, "safe", "Nekos.life")
            all_content.extend(content)
        return all_content

    async def fetch_from_o(self, urlstr, rating, provider):  # Handles provider data and fetcher responses
        content = ""

        async with self.session.get(urlstr, headers={'User-Agent': "Booru (https://github.com/Jintaku/Jintaku-Cogs-V3)"}) as resp:
            try:
                content = await resp.json(content_type=None)
            except (ValueError, aiohttp.ContentTypeError) as ex:
                log.debug("Pruned by exception, error below:")
                log.debug(ex)
                content = []
        if not content or content == [] or content is None or (type(content) is dict and "success" in content.keys() and content["success"] == False):
            content = []
            return content
        else:
            # Assign stuff to be used by booru_show
            for item in content:
                if provider == "Oboobs":
                    item["post_link"] = "http://media.oboobs.ru/" + item["preview"]
                    item["file_url"] = "http://media.oboobs.ru/" + item["preview"]
                elif provider == "Obutts":
                    item["post_link"] = "http://media.obutts.ru/" + item["preview"]
                    item["file_url"] = "http://media.obutts.ru/" + item["preview"]
                item["provider"] = provider
                item["author"] = "N/A"
                item["rating"] = rating
                item["score"] = "N/A"
                item["tags"] = "N/A"
        return content

    @cached(ttl=600, cache=SimpleMemoryCache, key="oboobs")
    async def fetch_oboobs(self, ctx, tag):  # oboobs fetcher
        urlstr = boorusources.oboobs
        log.debug(urlstr)
        return await self.fetch_from_o(urlstr, "explicit", "Oboobs")

    @cached(ttl=600, cache=SimpleMemoryCache, key="obutts")
    async def fetch_obutts(self, ctx, tag):  # obutts fetcher
        urlstr = boorusources.obutts
        log.debug(urlstr)
        return await self.fetch_from_o(urlstr, "explicit", "Obutts")

    async def fetch_from_reddit(self, urlstr, rating, provider):  # Handles provider data and fetcher responses
        content = ""

        async with self.session.get(urlstr, headers={'User-Agent': "Booru (https://github.com/Jintaku/Jintaku-Cogs-V3)"}) as resp:
            try:
                content = await resp.json(content_type=None)
            except (ValueError, aiohttp.ContentTypeError) as ex:
                log.debug("Pruned by exception, error below:")
                log.debug(ex)
                content = []
        if not content or content == [] or content is None or (type(content) is dict and "error" in content.keys()):
            content = []
            return content
        else:
            # Clean up to kill bad pictures and crap
            good_content = []
            for item in content["data"]["children"]:
                IMGUR_LINKS = "https://imgur.com/", "https://i.imgur.com/", "http://i.imgur.com/", "http://imgur.com", "https://m.imgur.com"
                GOOD_EXTENSIONS = ".png", ".jpg", ".jpeg", ".gif"
                url = item["data"]["url"]
                if url.startswith(IMGUR_LINKS):
                    if url.endswith(".mp4"):
                        item["file_url"] = url[:-3] + "gif"
                    elif url.endswith(".gifv"):
                        item["file_url"] = url[:-1]
                    elif url.endswith(GOOD_EXTENSIONS):
                        item["file_url"] = url
                    else:
                    	item["file_url"] = url + ".png"
                elif url.startswith("https://gfycat.com/"):
                    url_cut = url[19:]
                    if url_cut.islower():
                        continue
                    item["file_url"] = "https://thumbs.gfycat.com/" + url_cut + "-size_restricted.gif"
                elif url.endswith(GOOD_EXTENSIONS):
                    item["file_url"] = url
                else:
                    continue
                good_content.append(item)
            content = good_content

            # Assign stuff to be used by booru_show
            for item in content:
                item["provider"] = provider
                item["rating"] = rating
                item["post_link"] = "https://reddit.com" + item["data"]["permalink"]
                item["score"] = item["data"]["score"]
                item["tags"] = item["data"]["title"]
                item["author"] = item["data"]["author"]
        return content

    @cached(ttl=3600, cache=SimpleMemoryCache, key="4k")
    async def fetch_4k(self, ctx, tag):  # 4k fetcher
        subreddits = boorusources.fourk
        all_content = []
        for subreddit in subreddits:
            urlstr = "https://reddit.com/r/" + subreddit + "/new.json?limit=100"
            log.debug(urlstr)
            content = await self.fetch_from_reddit(urlstr, "explicit", "Reddit")
            all_content.extend(content)
        return all_content

    @cached(ttl=3600, cache=SimpleMemoryCache, key="ahegao")
    async def fetch_ahegao(self, ctx, tag):  # ahegao fetcher
        subreddits = boorusources.ahegao
        all_content = []
        for subreddit in subreddits:
            urlstr = "https://reddit.com/r/" + subreddit + "/new.json?limit=100"
            log.debug(urlstr)
            content = await self.fetch_from_reddit(urlstr, "explicit", "Reddit")
            all_content.extend(content)
        return all_content

    @cached(ttl=3600, cache=SimpleMemoryCache, key="ass")
    async def fetch_ass(self, ctx, tag):  # ass fetcher
        subreddits = boorusources.ass
        all_content = []
        for subreddit in subreddits:
            urlstr = "https://reddit.com/r/" + subreddit + "/new.json?limit=100"
            log.debug(urlstr)
            content = await self.fetch_from_reddit(urlstr, "explicit", "Reddit")
            all_content.extend(content)
        return all_content

    @cached(ttl=3600, cache=SimpleMemoryCache, key="anal")
    async def fetch_anal(self, ctx, tag):  # anal fetcher
        subreddits = boorusources.anal
        all_content = []
        for subreddit in subreddits:
            urlstr = "https://reddit.com/r/" + subreddit + "/new.json?limit=100"
            log.debug(urlstr)
            content = await self.fetch_from_reddit(urlstr, "explicit", "Reddit")
            all_content.extend(content)
        return all_content

    @cached(ttl=3600, cache=SimpleMemoryCache, key="bdsm")
    async def fetch_bdsm(self, ctx, tag):  # bdsm fetcher
        subreddits = boorusources.bdsm
        all_content = []
        for subreddit in subreddits:
            urlstr = "https://reddit.com/r/" + subreddit + "/new.json?limit=100"
            log.debug(urlstr)
            content = await self.fetch_from_reddit(urlstr, "explicit", "Reddit")
            all_content.extend(content)
        return all_content

    @cached(ttl=3600, cache=SimpleMemoryCache, key="blowjob")
    async def fetch_blowjob(self, ctx, tag):  # blowjob fetcher
        subreddits = boorusources.blowjob
        all_content = []
        for subreddit in subreddits:
            urlstr = "https://reddit.com/r/" + subreddit + "/new.json?limit=100"
            log.debug(urlstr)
            content = await self.fetch_from_reddit(urlstr, "explicit", "Reddit")
            all_content.extend(content)
        return all_content

    @cached(ttl=3600, cache=SimpleMemoryCache, key="boobs")
    async def fetch_boobs(self, ctx, tag):  # boobs fetcher
        subreddits = boorusources.boobs
        all_content = []
        for subreddit in subreddits:
            urlstr = "https://reddit.com/r/" + subreddit + "/new.json?limit=100"
            log.debug(urlstr)
            content = await self.fetch_from_reddit(urlstr, "explicit", "Reddit")
            all_content.extend(content)
        return all_content

    @cached(ttl=3600, cache=SimpleMemoryCache, key="cunnilingus")
    async def fetch_cunnilingus(self, ctx, tag):  # cunnilingus fetcher
        subreddits = boorusources.cunnilingus
        all_content = []
        for subreddit in subreddits:
            urlstr = "https://reddit.com/r/" + subreddit + "/new.json?limit=100"
            log.debug(urlstr)
            content = await self.fetch_from_reddit(urlstr, "explicit", "Reddit")
            all_content.extend(content)
        return all_content

    @cached(ttl=3600, cache=SimpleMemoryCache, key="bottomless")
    async def fetch_bottomless(self, ctx, tag):  # bottomless fetcher
        subreddits = boorusources.bottomless
        all_content = []
        for subreddit in subreddits:
            urlstr = "https://reddit.com/r/" + subreddit + "/new.json?limit=100"
            log.debug(urlstr)
            content = await self.fetch_from_reddit(urlstr, "explicit", "Reddit")
            all_content.extend(content)
        return all_content

    @cached(ttl=3600, cache=SimpleMemoryCache, key="cumshots")
    async def fetch_cumshots(self, ctx, tag):  # cumshots fetcher
        subreddits = boorusources.cumshots
        all_content = []
        for subreddit in subreddits:
            urlstr = "https://reddit.com/r/" + subreddit + "/new.json?limit=100"
            log.debug(urlstr)
            content = await self.fetch_from_reddit(urlstr, "explicit", "Reddit")
            all_content.extend(content)
        return all_content

    @cached(ttl=3600, cache=SimpleMemoryCache, key="deepthroat")
    async def fetch_deepthroat(self, ctx, tag):  # deepthroat fetcher
        subreddits = boorusources.deepthroat
        all_content = []
        for subreddit in subreddits:
            urlstr = "https://reddit.com/r/" + subreddit + "/new.json?limit=100"
            log.debug(urlstr)
            content = await self.fetch_from_reddit(urlstr, "explicit", "Reddit")
            all_content.extend(content)
        return all_content

    @cached(ttl=3600, cache=SimpleMemoryCache, key="dick")
    async def fetch_dick(self, ctx, tag):  # dick fetcher
        subreddits = boorusources.dick
        all_content = []
        for subreddit in subreddits:
            urlstr = "https://reddit.com/r/" + subreddit + "/new.json?limit=100"
            log.debug(urlstr)
            content = await self.fetch_from_reddit(urlstr, "explicit", "Reddit")
            all_content.extend(content)
        return all_content

    @cached(ttl=3600, cache=SimpleMemoryCache, key="doublepenetration")
    async def fetch_double_penetration(self, ctx, tag):  # double penetration fetcher
        subreddits = boorusources.doublepenetration
        all_content = []
        for subreddit in subreddits:
            urlstr = "https://reddit.com/r/" + subreddit + "/new.json?limit=100"
            log.debug(urlstr)
            content = await self.fetch_from_reddit(urlstr, "explicit", "Reddit")
            all_content.extend(content)
        return all_content

    @cached(ttl=3600, cache=SimpleMemoryCache, key="gay")
    async def fetch_gay(self, ctx, tag):  # gay fetcher
        subreddits = boorusources.gay
        all_content = []
        for subreddit in subreddits:
            urlstr = "https://reddit.com/r/" + subreddit + "/new.json?limit=100"
            log.debug(urlstr)
            content = await self.fetch_from_reddit(urlstr, "explicit", "Reddit")
            all_content.extend(content)
        return all_content

    @cached(ttl=3600, cache=SimpleMemoryCache, key="group")
    async def fetch_group(self, ctx, tag):  # group fetcher
        subreddits = boorusources.group
        all_content = []
        for subreddit in subreddits:
            urlstr = "https://reddit.com/r/" + subreddit + "/new.json?limit=100"
            log.debug(urlstr)
            content = await self.fetch_from_reddit(urlstr, "explicit", "Reddit")
            all_content.extend(content)
        return all_content

    @cached(ttl=3600, cache=SimpleMemoryCache, key="hentai")
    async def fetch_hentai(self, ctx, tag):  # hentai fetcher
        subreddits = boorusources.hentai
        all_content = []
        for subreddit in subreddits:
            urlstr = "https://reddit.com/r/" + subreddit + "/new.json?limit=100"
            log.debug(urlstr)
            content = await self.fetch_from_reddit(urlstr, "explicit", "Reddit")
            all_content.extend(content)
        return all_content

    @cached(ttl=3600, cache=SimpleMemoryCache, key="lesbian")
    async def fetch_lesbian(self, ctx, tag):  # lesbian fetcher
        subreddits = boorusources.lesbian
        all_content = []
        for subreddit in subreddits:
            urlstr = "https://reddit.com/r/" + subreddit + "/new.json?limit=100"
            log.debug(urlstr)
            content = await self.fetch_from_reddit(urlstr, "explicit", "Reddit")
            all_content.extend(content)
        return all_content

    @cached(ttl=3600, cache=SimpleMemoryCache, key="milf")
    async def fetch_milf(self, ctx, tag):  # milf fetcher
        subreddits = boorusources.milf
        all_content = []
        for subreddit in subreddits:
            urlstr = "https://reddit.com/r/" + subreddit + "/new.json?limit=100"
            log.debug(urlstr)
            content = await self.fetch_from_reddit(urlstr, "explicit", "Reddit")
            all_content.extend(content)
        return all_content

    @cached(ttl=3600, cache=SimpleMemoryCache, key="public")
    async def fetch_public(self, ctx, tag):  # public fetcher
        subreddits = boorusources.public
        all_content = []
        for subreddit in subreddits:
            urlstr = "https://reddit.com/r/" + subreddit + "/new.json?limit=100"
            log.debug(urlstr)
            content = await self.fetch_from_reddit(urlstr, "explicit", "Reddit")
            all_content.extend(content)
        return all_content

    @cached(ttl=3600, cache=SimpleMemoryCache, key="rule34")
    async def fetch_rule34(self, ctx, tag):  # rule34 fetcher
        subreddits = boorusources.rule34
        all_content = []
        for subreddit in subreddits:
            urlstr = "https://reddit.com/r/" + subreddit + "/new.json?limit=100"
            log.debug(urlstr)
            content = await self.fetch_from_reddit(urlstr, "explicit", "Reddit")
            all_content.extend(content)
        return all_content

    @cached(ttl=3600, cache=SimpleMemoryCache, key="thigh")
    async def fetch_thigh(self, ctx, tag):  # thigh fetcher
        subreddits = boorusources.thigh
        all_content = []
        for subreddit in subreddits:
            urlstr = "https://reddit.com/r/" + subreddit + "/new.json?limit=100"
            log.debug(urlstr)
            content = await self.fetch_from_reddit(urlstr, "explicit", "Reddit")
            all_content.extend(content)
        return all_content

    @cached(ttl=3600, cache=SimpleMemoryCache, key="wild")
    async def fetch_wild(self, ctx, tag):  # wild fetcher
        subreddits = boorusources.wild
        all_content = []
        for subreddit in subreddits:
            urlstr = "https://reddit.com/r/" + subreddit + "/new.json?limit=100"
            log.debug(urlstr)
            content = await self.fetch_from_reddit(urlstr, "explicit", "Reddit")
            all_content.extend(content)
        return all_content

    @cached(ttl=3600, cache=SimpleMemoryCache, key="redhead")
    async def fetch_redhead(self, ctx, tag):  # redhead fetcher
        subreddits = boorusources.redhead
        all_content = []
        for subreddit in subreddits:
            urlstr = "https://reddit.com/r/" + subreddit + "/new.json?limit=100"
            log.debug(urlstr)
            content = await self.fetch_from_reddit(urlstr, "explicit", "Reddit")
            all_content.extend(content)
        return all_content

    async def fetch_from_booru(self, urlstr, provider):  # Handles provider data and fetcher responses
        content = ""

        async with self.session.get(urlstr, headers={'User-Agent': "Booru (https://github.com/Jintaku/Jintaku-Cogs-V3)"}) as resp:
            try:
                content = await resp.json(content_type=None)
                if provider == "e621":
                    content = content["posts"]
                    log.debug(content)
            except (ValueError, aiohttp.ContentTypeError) as ex:
                log.debug("Pruned by exception, error below:")
                log.debug(ex)
                content = []
        if not content or content == [] or content is None or (type(content) is dict and "success" in content.keys() and content["success"] == False):
            content = []
            return content
        else:
            assigned_content = []
            for item in content:
                if item.get("id") is None:
                    continue
                if provider == "Konachan":
                    item["post_link"] = "https://konachan.com/post/show/" + str(item["id"])
                elif provider == "Gelbooru":
                    item["post_link"] = "https://gelbooru.com/index.php?page=post&s=view&id=" + str(item["id"])
                    item["author"] = item["owner"]
                elif provider == "Rule34":
                    item["post_link"] = "https://rule34.xxx/index.php?page=post&s=view&id=" + str(item["id"])
                    item["file_url"] = "https://us.rule34.xxx//images/" + item["directory"] + "/" + item["image"]
                    item["author"] = item["owner"]
                elif provider == "Yandere":
                    item["post_link"] = "https://yande.re/post/show/" + str(item["id"])
                elif provider == "Danbooru":
                    item["post_link"] = "https://danbooru.donmai.us/posts/" + str(item["id"])
                    item["tags"] = item["tag_string"]
                    item["author"] = "Not Available"
                elif provider == "Safebooru":
                    item["post_link"] = "https://safebooru.com/index.php?page=post&s=view&id=" + str(item["id"])
                    item["file_url"] = "https://safebooru.org//images/" + item["directory"] + "/" + item["image"]
                    item["author"] = item["owner"]
                elif provider == "e621":
                    item["post_link"] = "https://e621.net/post/show/" + str(item["id"])
                    item["file_url"] = item["file"]["url"]
                    item["author"] = "Not Available"
                    item["tags"] = " ".join(item["tags"]["general"] + item["tags"]["species"] + item["tags"]["character"] + item["tags"]["copyright"])
                    item["score"] = item["score"]["total"]
                item["provider"] = provider
                assigned_content.append(item)
        return assigned_content

    @cached(ttl=3600, cache=SimpleMemoryCache)
    async def fetch_yan(self, ctx, tags):  # Yande.re fetcher
        urlstr = boorusources.yan + "+".join(tags)
        log.debug(urlstr)
        return await self.fetch_from_booru(urlstr, "Yandere")

    @cached(ttl=3600, cache=SimpleMemoryCache)
    async def fetch_gel(self, ctx, tags):  # Gelbooru fetcher
        urlstr = boorusources.gel + "+".join(tags)
        log.debug(urlstr)
        return await self.fetch_from_booru(urlstr, "Gelbooru")

    @cached(ttl=3600, cache=SimpleMemoryCache)
    async def fetch_safe(self, ctx, tags):  # Safebooru fetcher
        urlstr = boorusources.safe + "+".join(tags)
        log.debug(urlstr)
        return await self.fetch_from_booru(urlstr, "Safebooru")

    @cached(ttl=3600, cache=SimpleMemoryCache)
    async def fetch_kon(self, ctx, tags):  # Konachan fetcher
        urlstr = boorusources.kon + "+".join(tags)
        log.debug(urlstr)
        return await self.fetch_from_booru(urlstr, "Konachan")

    @cached(ttl=3600, cache=SimpleMemoryCache)
    async def fetch_dan(self, ctx, tags):  # Danbooru fetcher
        if len(tags) > 2:
            return []
        urlstr = boorusources.dan + "+".join(tags)
        log.debug(urlstr)
        return await self.fetch_from_booru(urlstr, "Danbooru")

    @cached(ttl=3600, cache=SimpleMemoryCache)
    async def fetch_r34(self, ctx, tags):  # Rule34 fetcher
        urlstr = boorusources.r34 + "+".join(tags)
        log.debug(urlstr)
        return await self.fetch_from_booru(urlstr, "Rule34")

    @cached(ttl=3600, cache=SimpleMemoryCache)
    async def fetch_e621(self, ctx, tags):  # e621 fetcher
        urlstr = boorusources.e621 + "+".join(tags)
        log.debug(urlstr)
        return await self.fetch_from_booru(urlstr, "e621")

    async def show_booru(self, ctx, data):  # Shows various info in embed
        mn = len(data)
        if mn == 0:
            await ctx.send("No results.")
        else:

            i = randint(0, mn - 1)

            # Build Embed
            embeds = []

            # Respect simple setting by guild and channel
            simple_booru_guild = await self.config.guild(ctx.guild).simple()
            if simple_booru_guild == "on":
                return await self.show_simple_booru(ctx, i, data)

            simple_booru_channel = await self.config.guild(ctx.channel).simple()
            if simple_booru_channel == "on":
                return await self.show_simple_booru(ctx, i, data)

            num_pages = len(data)
            for page_num, booru in enumerate(data, 1):

                # Set colour for each board
                color = {"Gelbooru": 3395583, "Danbooru": 3395583, "Konachan": 8745592, "Yandere": 2236962, "Rule34": 339933, "Safebooru": 000000, "e621": 000000, "Reddit": 000000, "Oboobs": 000000, "Obutts": 000000, "Nekos.life": 000000}

                embed = discord.Embed()
                embed.color = color[booru["provider"]]
                embed.title = booru["provider"] + " entry by " + booru["author"]
                embed.url = booru["post_link"]
                embed.set_image(url=booru["file_url"])
                embed.add_field(name="Description / Tags", value="```" + booru["tags"][:300] + "```", inline=False)
                embed.add_field(name="Rating", value=booru["rating"])
                embed.add_field(name="Score", value=booru["score"])
                if booru["provider"] == "Reddit":
                    embed.set_footer(text=f"{page_num}/{num_pages} If image doesn't appear, it may be a webm or too big, Powered by {booru['data']['subreddit_name_prefixed']}")
                else:
                    embed.set_footer(text=f"{page_num}/{num_pages} If image doesn't appear, it may be a webm or too big, Powered by {booru['provider']}")
                embeds.append(embed)
            try:
                await menu(ctx, pages=embeds, controls=DEFAULT_CONTROLS, message=None, page=i, timeout=15)
            except:
                log.debug(data[i])

    async def show_simple_booru(self, ctx, i, data):  # Shows simple embed

            booru = data[i]

            # Set colour for each board
            color = {"Gelbooru": 3395583, "Danbooru": 3395583, "Konachan": 8745592, "Yandere": 2236962, "Rule34": 339933, "Safebooru": 000000, "e621": 000000, "Reddit": 000000, "Oboobs": 000000, "Obutts": 000000}

            embed = discord.Embed()
            embed.color = color[booru["provider"]]
            embed.set_image(url=booru["file_url"])
            try:
                await ctx.send(embed=embed)
            except:
                log.debug(data[i])
