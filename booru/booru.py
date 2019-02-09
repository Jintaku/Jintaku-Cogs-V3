import discord
from redbot.core import Config, checks, commands
from redbot.core.utils.menus import menu, commands, DEFAULT_CONTROLS
import aiohttp
import contextlib
from random import randint
import os
import threading
import logging

log = logging.getLogger("Booru") # Thanks to Sinbad for the example code for logging
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
        default_global = {
            "filters": [],
            "nsfw_filters": []
        }
        default_guild = {
            "filters": [],
            "nsfw_filters": ["-loli", "-shota"]
        }
        self.config.register_global(**default_global, force_registration=True)
        self.config.register_guild(**default_guild, force_registration=True)

    @commands.command()
    async def booru(self, ctx, *, tag=None):
        """Shows a image board entry based on user query"""

        # Global filters
        global_filters = await self.config.filters()
        global_nsfw_filters = await self.config.nsfw_filters()

        # Guild filters
        guild_group = self.config.guild(ctx.guild)
        guild_nsfw_filters = await guild_group.nsfw_filters()
        guild_filters = await guild_group.filters()

        # Checks if there is a tag and defaults depending on channel
        if tag is not None:
            tag = set(tag.split())
        if ctx.channel.is_nsfw() and tag is None:
            tag = {'rating:none', '*'}
        if ctx.channel.is_nsfw() == False and tag is None:
            tag = {'rating:safe', '*'}

        log.debug(tag)

        # Checks common to see if any ratings are there
        ratings = {'rating:safe', 'rating:explicit', 'rating:questionable'}
        if not ratings & tag:
            tag.add('rating:safe')

        # Checks if none and applies ratings
        if 'rating:none' in tag:
            tag.remove('rating:none')
            tag.update(ratings)

        # Applies filters which always apply
        if global_filters is not None:
            tag.update(global_filters)
        if guild_filters is not None:
            tag.update(guild_filters)

        # Checks if nsfw and adds nsfw filters
        if 'rating:explicit' in tag or 'rating:questionable' in tag:
            if global_nsfw_filters is not None:
                tag.update(global_nsfw_filters)
            if guild_nsfw_filters is not None:
                tag.update(guild_nsfw_filters)

        # Checks if nsfw could be posted in sfw channel
        if not ctx.channel.is_nsfw():
            if 'rating:explicit' in tag or 'rating:questionable' in tag:
                await ctx.send("You cannot post nsfw content in sfw channels")
                return

        log.debug(tag)

        # Image board fetcher
        yan = threading.Thread(target=await self.fetch_yan(ctx, tag))
        gel = threading.Thread(target=await self.fetch_gel(ctx, tag))
        kon = threading.Thread(target=await self.fetch_kon(ctx, tag))
        yan.start()
        gel.start()
        kon.start()
        yan.join()
        gel.join()
        kon.join()

        # Fuse multiple image board data
        data = self.yan_data + self.gel_data + self.kon_data

        # Done sending requests, time to show it
        await self.show_booru(ctx, data)

    async def fetch_from_booru(self, urlstr, provider): # Handles provider data and fetcher responses
       content = ""
       async with aiohttp.ClientSession() as session:
           async with session.get(urlstr) as url:
               try:
                   content = await url.json()
               except ValueError:
                   content = None
       if not content or (type(content) is dict and 'success' in content.keys() and content['success'] == False):
           return []
       else:
         for item in content:
             item['provider'] = provider
       return content

    async def fetch_yan(self, ctx, tags): # Yande.re fetcher
        urlstr = "https://yande.re/post.json?limit=100&tags=" + "+".join(tags)
        log.debug(urlstr)
        self.yan_data = await self.fetch_from_booru(urlstr, "Yandere")

    async def fetch_gel(self, ctx, tags): # Gelbooru fetcher
        urlstr = "https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&limit=100&tags=" + "+".join(tags)
        log.debug(urlstr)
        self.gel_data = await self.fetch_from_booru(urlstr, "Gelbooru")

    async def fetch_kon(self, ctx, tags): # Konachan fetcher
        urlstr = "https://konachan.com/post.json?limit=100&tags=" + "+".join(tags)
        log.debug(urlstr)
        self.kon_data = await self.fetch_from_booru(urlstr, "Konachan")

    async def show_booru(self, ctx, data): #Shows various info in embed
       mn = len(data)
       if mn == 0:
          await ctx.send("No results.")
       else:

          i = randint(0, mn-1)

          # Build Embed
          embeds = []

          for booru in data:
              # Set variables for owner/author of post
              booru_author = booru.get('owner') or booru.get('author') or booru.get('uploader_name') or 'N/A'

              # Set variables for tags
              booru_tags = booru.get('tags') or booru.get('tag_string') or 'N/A'

              # Set variables for score
              booru_score = booru.get('score') or 'N/A'

              # Set variables for file url
              file_url = booru.get('file_url')
              booru_url = file_url

              # Set variable for post link
              if booru['provider'] == "Konachan":
                  booru_post = "https://konachan.com/post/show/" + str(booru.get('id'))
              if booru['provider'] == "Gelbooru":
                  booru_post = "https://gelbooru.com/index.php?page=post&s=view&id=" + str(booru.get('id'))
              if booru['provider'] == "Yandere":
                  booru_post = "https://yande.re/post/show/" + str(booru.get('id'))

              color = {
                "Gelbooru": 3395583,
                "Konachan": 8745592,
                "Yandere": 2236962
              }

              embed = discord.Embed()
              embed.color = color[booru['provider']]
              embed.title = booru['provider'] + " entry by " + booru_author
              embed.url = booru_post
              embed.set_image(url=booru_url)
              embed.add_field(name="Tags", value="```" + booru_tags[:300] + "```", inline=False)
              embed.add_field(name="Rating", value=booru['rating'])
              embed.add_field(name="Score", value=booru_score)
              embed.set_footer(text="If image doesn't appear, it may be a webm or too big, Powered by {}".format(booru['provider']))
              embeds.append(embed)

          await menu(ctx, pages=embeds, controls=DEFAULT_CONTROLS, message=None, page=i, timeout=15)

    @commands.group()
    async def booruset(self, ctx):
        """Settings for booru"""
        pass

    # Guild configs
    @booruset.group(name="guild")
    @checks.admin_or_permissions()
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

        origin = ['all']
        await self.generic_add(ctx, origin, config_filters, filter)

    @_guild_allfilters.command(name="remove")
    @checks.admin_or_permissions(manage_guild=True)
    async def _guild_allfilters_remove(self, ctx, *, filter):
        """Remove guild filters"""

        # Load config
        config_filters = await self.config.guild(ctx.guild).filters()

        origin = ['all']
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

        origin = ['nsfw']
        await self.generic_add(ctx, origin, config_filters, filter)

    @_guild_nsfwfilters.command(name="remove")
    @checks.admin_or_permissions(manage_guild=True)
    async def _guild_nsfwfilters_remove(self, ctx, *, filter):
        """Remove guild nsfw filters"""

        # Load config
        config_filters = await self.config.guild(ctx.guild).nsfw_filters()

        origin = ['nsfw']
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

        origin = ['global', 'all']
        await self.generic_add(ctx, origin, config_filters, filter)

    @_global_allfilters.command(name="remove")
    @checks.is_owner()
    async def _global_allfilters_remove(self, ctx, *, filter):
        """Remove global nsfw filters"""

        # Load config
        config_filters = await self.config.filters()

        origin = ['global', 'all']
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

        origin = ['global', 'nsfw']
        await self.generic_add(ctx, origin, config_filters, filter)

    @_global_nsfwfilters.command(name="remove")
    @checks.is_owner()
    async def _global_nsfwfilters_remove(self, ctx, *, filter):
        """Remove global nsfw filters"""

        # Load config
        config_filters = await self.config.nsfw_filters()

        origin = ['global', 'nsfw']
        await self.generic_remove(ctx, origin, config_filters, filter)

    async def generic_show(self, ctx, filters):
        if not filters:
            await ctx.send("There are currently no filters")
        else:
            await ctx.send("Current filters are: ```{}```".format(",".join(filters)))

    async def generic_add(self, ctx, origin, config_filters, filter):

        filter = set(filter.split(" "))

        config_filters = set(config_filters)
        config_filters.update(filter)

        if 'all' in origin:
            await self.config.guild(ctx.guild).filters.set(list(config_filters))
        if 'nsfw' in origin:
            await self.config.guild(ctx.guild).nsfw_filters.set(list(config_filters))
        if 'all' in origin and 'global' in origin:
            await self.config.filters.set(list(config_filters))
        if 'nsfw' in origin and 'global' in origin:
            await self.config.nsfw_filters.set(list(config_filters))
        await ctx.send("The filters have been added!")

    async def generic_remove(self, ctx, origin, config_filters, filter):

        filter = set(filter.split(" "))

        config_filters = set(config_filters)

        if 'all' in origin:
            await self.config.guild(ctx.guild).filters.set(list(set(config_filters) - set(filter)))
        if 'nsfw' in origin:
            await self.config.guild(ctx.guild).nsfw_filters.set(list(set(config_filters) - set(filter)))
        if 'all' in origin and 'global' in origin:
            await self.config.filters.set(list(set(config_filters) - set(filter)))
        if 'nsfw' in origin and 'global' in origin:
            await self.config.nsfw_filters.set(list(set(config_filters) - set(filter)))
        await ctx.send("The filters have been removed!")
