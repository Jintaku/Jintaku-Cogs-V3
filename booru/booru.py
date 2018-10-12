import discord
from redbot.core import Config, checks, commands
import aiohttp
from random import randint
import os
import threading

BaseCog = getattr(commands, "Cog", object)

class booru(BaseCog):
    """Show a picture using image boards (Gelbooru, yandere, konachan)\n\n Usage: -booru [rating: mandatory] [tag: optional]"""

    def __init__(self):
        self.config = Config.get_conf(self, identifier=4894278742742)
        default_global = {
            "filters": [],
            "nsfw": []
        }
        default_guild = {
            "filters": ["rating:s"],
            "nsfw": ["-loli"]
        }
        self.config.register_global(**default_global)
        self.config.register_guild(**default_guild)

    @commands.command()
    async def booru(self, ctx, rating=None, *, tag=None):
        """Shows a image board entry"""

        # Default values
        rating_tag = ["rating:safe"]
        guild_nsfw_filters = []
        guild_filters = []
        nsfw_filters = []

        filters_map = {
            "s": "safe",
            "e": "explicit",
            "q": "questionnable",
            "n": "none",
        }

        accepted_filters = ["s", "e", "q", "n"]

        # Is it a tag?
        if rating not in accepted_filters:
            tag = rating
            rating = "s"

        # Tag splitting and no tag
        if tag is not None:
            tag = tag.split(" ")
        else:
            tag = ["*"]

        # Checks if old format of rating
        if rating in accepted_filters:
            rating = "rating:{}".format(filters_map.get(rating))

        # Adds rating_tag for s, e, q
        if rating in ["rating:safe", "rating:explicit", "rating:questionnable"]:
            rating_tag = ["{}".format(rating)]

        # Adds all rating_tag for n
        if rating == "rating:none":
            rating_tag = ["rating:explicit", "rating:safe", "rating:questionnable"]

        # Adds nsfw filters if rating may contain explicit content
        if rating in ["rating:explicit", "rating:questionnable", "rating:none"]:
            nsfw_filters = await self.config.nsfw()
            if ctx.guild is not None:
                guild_group = self.config.guild(ctx.guild)
                guild_nsfw_filters = await guild_group.nsfw()
                guild_filters = await guild_group.filters()

        # Global filters
        filters = await self.config.filters()

        tags = tag + rating_tag + filters + guild_filters + nsfw_filters + guild_nsfw_filters
        tags = list(set(tags))

        # Debug log
        print(rating_tag)
        print(rating)
        print(tags)

        # Image board fetcher
        yan = threading.Thread(target=await self.fetch_yan(ctx, tags))
        gel = threading.Thread(target=await self.fetch_gel(ctx, tags))
        kon = threading.Thread(target=await self.fetch_kon(ctx, tags))
        yan.start()
        gel.start()
        kon.start()
        yan.join()
        gel.join()
        kon.join()

        # Fuse multiple image board data
        data = self.yan_data + self.gel_data + self.kon_data

        await self.show_booru(ctx, data)

    async def fetch_from_booru(self, urlstr, provider): # Handles provider data and fetcher responses
       content = ""
       async with aiohttp.ClientSession() as session: # Let's try
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
        print(urlstr)
        self.yan_data = await self.fetch_from_booru(urlstr, "Yandere")

    async def fetch_gel(self, ctx, tags): # Gelbooru fetcher
        urlstr = "https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&limit=100&tags=" + "+".join(tags)
        print(urlstr)
        self.gel_data = await self.fetch_from_booru(urlstr, "Gelbooru")

    async def fetch_kon(self, ctx, tags): # Konachan fetcher
        urlstr = "https://konachan.com/post.json?limit=100&tags=" + "+".join(tags)
        print(urlstr)
        self.kon_data = await self.fetch_from_booru(urlstr, "Konachan")

    async def show_booru(self, ctx, data): #Shows various info in embed
       mn = len(data)
       if mn == 0:
          await ctx.send("No results.")
       else:
          # Chooses a random entry from the filtered data
          i = randint(0, mn-1)
          onebooru = data[i]

          # Set variables for owner/author of post
          onebooru_author = onebooru.get('owner') or onebooru.get('author') or onebooru.get('uploader_name') or 'N/A'

          # Set variables for tags
          onebooru_tags = onebooru.get('tags') or onebooru.get('tag_string') or 'N/A'

          # Set variables for score
          onebooru_score = onebooru.get('score') or 'N/A'

          # Set variables for file url
          file_url = onebooru.get('file_url')
          onebooru_url = file_url

          color = {
            "Gelbooru": 3395583,
            "Konachan": 8745592,
            "Yandere": 2236962
          }

          # Build Embed
          embed = discord.Embed()
          embed.color = color[onebooru['provider']]
          embed.title = onebooru['provider'] + " entry by " + onebooru_author
          embed.url = onebooru_url
          embed.set_image(url=onebooru_url)
          embed.add_field(name="Tags", value="```" + onebooru_tags[:300] + "```", inline=False)
          embed.add_field(name="Rating", value=onebooru['rating'])
          embed.add_field(name="Score", value=onebooru_score)
          embed.set_footer(text="If image doesn't appear, it may be a webm or too big, Powered by {}".format(onebooru['provider']))
          await ctx.send(embed=embed)

    @commands.group(autohelp=True)
    async def booruset(self, ctx):
        """Server settings for booru"""
        pass

    # Guild configs
    @booruset.command()
    @checks.admin_or_permissions(manage_guild=True)
    async def filters(self, ctx):
        filters = await self.config.guild(ctx.guild).filters()
        if not filters:
            await ctx.send("There are currently no filters")
        else:
            await ctx.send("Current server filters are: ```{}```".format(",".join(filters)))

    @booruset.command()
    @checks.admin_or_permissions(manage_guild=True)
    async def add(self, ctx, *, filter):
        guild_group = self.config.guild(ctx.guild)
        if len(filter.split(" ")) > 1:
            existing_filters = await guild_group.filters()
            await guild_group.filters.set(existing_filters + filter.split(" "))
        else:
            async with guild_group.filters() as filters:
                filters.append(filter)
        await ctx.send("The filter(s) has been added!")

    @booruset.command()
    @checks.admin_or_permissions(manage_guild=True)
    async def remove(self, ctx, *, filter):
        guild_group = self.config.guild(ctx.guild)
        if len(filter.split(" ")) > 1:
            existing_filters = await guild_group.filters()
            await guild_group.filters.set(list(set(existing_filters) - set(filter.split(" "))))
        else:
            async with guild_group.filters() as filters:
                filters.remove(filter)
        await ctx.send("The filter(s) has been removed!")

    # Global configs
    @booruset.group(autohelp=True, name="global")
    @checks.is_owner()
    async def _global(self, ctx):
        """Global Settings for booru"""
        pass

    @_global.command(name="filters")
    @checks.is_owner()
    async def _global_filters(self, ctx):
        filters = await self.config.filters()
        if not filters:
            await ctx.send("There are currently no filters")
        else:
            await ctx.send("Current global filters are: ```{}```".format(",".join(filters)))

    @_global.command(name="add")
    @checks.is_owner()
    async def _global_add(self, ctx, *, filter):
        if len(filter.split(" ")) > 1:
            existing_filters = await self.config.filters()
            await self.config.filters.set(existing_filters + filter.split(" "))
        else:
            async with self.config.filters() as filters:
                filters.append(filter)
        await ctx.send("The filter(s) has been added!")

    @_global.command(name="remove")
    @checks.is_owner()
    async def _global_remove(self, ctx, *, filter):
        if len(filter.split(" ")) > 1:
            existing_filters = await self.config.filters()
            await self.config.filters.set(list(set(existing_filters) - set(filter.split(" "))))
        else:
            async with self.config.filters() as filters:
                filters.remove(filter)
        await ctx.send("The filter has been removed!")
