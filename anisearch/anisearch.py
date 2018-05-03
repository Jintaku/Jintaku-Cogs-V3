import asyncio
import datetime
import json
import re

import aiohttp
import discord
from discord.ext import commands

numbs = {
    "next": "➡",
    "back": "⬅",
    "exit": "❌"
}

SEARCH_ANIME_MANGA_QUERY = '''
query ($id: Int, $page: Int, $search: String, $type: MediaType) {
    Page (page: $page, perPage: 10) {
        media (id: $id, search: $search, type: $type) {
            id
            idMal
            description(asHtml: false)
            title {
                english
                romaji
            }
            coverImage {
            		medium
            }
            averageScore
            meanScore
            status
            episodes
            chapters
            externalLinks {
                url
                site
            }
            nextAiringEpisode {
                timeUntilAiring
            }
        }
    }
}
'''

SEARCH_CHARACTER_QUERY = '''
query ($id: Int, $page: Int, $search: String) {
  Page(page: $page, perPage: 10) {
    characters(id: $id, search: $search) {
      id
      description (asHtml: true),
      name {
        first
        last
        native
      }
      image {
        large
      }
      media {
        nodes {
          id
          type
          title {
            romaji
            english
            native
            userPreferred
          }
        }
      }
    }
  }
}
'''

SEARCH_USER_QUERY = '''
query ($id: Int, $page: Int, $search: String) {
    Page (page: $page, perPage: 10) {
        users (id: $id, search: $search) {
            id
            name
            siteUrl
            avatar {
                    large
            }
            about (asHtml: true),
            stats {
                watchedTime
                chaptersRead
            }
            favourites {
            manga {
              nodes {
                id
                title {
                  romaji
                  english
                  native
                  userPreferred
                }
              }
            }
            characters {
              nodes {
                id
                name {
                  first
                  last
                  native
                }
              }
            }
            anime {
              nodes {
                id
                title {
                  romaji
                  english
                  native
                  userPreferred
                }
              }
            }
            }
        }
    }
}
'''


class AniSearch:
    """Search for anime, manga, characters and users using Anilist"""

    def __init__(self, bot):
        self.bot = bot
        self.url = 'https://graphql.anilist.co'

    def format_name(self, first_name, last_name):  # Combines first_name and last_name and/or shows either of the two
        if first_name and last_name:
            return first_name + " " + last_name
        elif first_name:
            return first_name
        elif last_name:
            return last_name
        else:
            return 'No name'

    def clean_html(self, description):  # Removes html tags
        if not description:
            return ""
        cleanr = re.compile("<.*?>")
        cleantext = re.sub(cleanr, "", description)
        return cleantext

    def clean_spoilers(self, description):  # Removes spoilers using the html tag given by AniList
        if not description:
            return ""
        cleanr = re.compile("/<span[^>]*>.*</span>/g")
        cleantext = re.sub(cleanr, "", description)
        return cleantext

    def description_parser(self, description):  # Limits text to 400characters and 5 lines and adds "..." at the end
        description = self.clean_spoilers(description)
        description = self.clean_html(description)
        description = "\n".join(description.split("\n")[:5])
        if len(description) > 400:
            return description[:400] + "..."
        else:
            return description

    def list_maximum(self, items):  # Limits to 5 strings than adds "+X more"
        if len(items) > 5:
            return items[:5] + ["+ " + str(len(items) - 5) + " more"]
        else:
            return items

    async def _request(self, query, variables=None):

        if variables is None:
            variables = {}

        request_json = {
            'query': query,
            'variables': variables
        }

        headers = {'content-type': 'application/json'}

        async with aiohttp.ClientSession() as session:
            async with session.post(self.url,
                                    data=json.dumps(request_json),
                                    headers=headers) as response:
                return await response.json()

    async def _search_anime_manga(self, ctx, cmd, entered_title):

        # Outputs MediaStatuses to strings
        MediaStatusToString = {
            # Has completed and is no longer being released
            'FINISHED': 'Finished',
            # Currently releasing
            'RELEASING': 'Releasing',
            # To be released at a later date
            'NOT_YET_RELEASED': 'Not yet released',
            # Ended before the work could be finished
            'CANCELLED': 'Cancelled'
        }

        variables = {
            'search': entered_title,
            'page': 1,
            'type': cmd
        }

        data = (await self._request(SEARCH_ANIME_MANGA_QUERY, variables))['data']['Page']['media']

        print(data)

        if data is not None and len(data) > 0:

            # a list of embeds
            embeds = []

            for anime_manga in data:
                # Sets up various variables for Embed
                link = 'https://anilist.co/{}/{}'.format(cmd.lower(), anime_manga['id'])
                description = anime_manga['description']
                title = anime_manga['title']['english'] or anime_manga['title']['romaji']
                if anime_manga.get('nextAiringEpisode'):
                    seconds = anime_manga['nextAiringEpisode']['timeUntilAiring']
                    time_left = str(datetime.timedelta(seconds=seconds))
                else:
                    time_left = "Never"

                external_links = ""
                for i in range(0, len(anime_manga['externalLinks'])):
                    ext_link = anime_manga['externalLinks'][i]
                    external_links += "[{site_name}]({link}), ".format(site_name=ext_link['site'], link=ext_link['url'])
                    if i + 1 == len(anime_manga['externalLinks']):
                        external_links = external_links[:-2]

                embed = discord.Embed(title=title)
                embed.url = link
                embed.description = self.description_parser(description)
                embed.set_thumbnail(url=anime_manga['coverImage']['medium'])
                embed.add_field(name="Score", value=anime_manga.get('averageScore', 'N/A'))
                if cmd == "ANIME":
                    embed.add_field(name="Episodes", value=anime_manga.get('episodes', 'N/A'))
                    embed.set_footer(text="Status : " + MediaStatusToString[
                        anime_manga['status']] + ", Next episode : " + time_left + ", Powered by Anilist")
                else:
                    embed.add_field(name="Chapters", value=anime_manga.get('chapters', 'N/A'))
                    embed.set_footer(text="Status : " + MediaStatusToString.get(anime_manga.get('status'),
                                                                                'N/A') + ", Powered by Anilist")
                if external_links:
                    embed.add_field(name="Streaming and/or Info sites", value=external_links)
                embed.add_field(name="You can find out more",
                                value="[Anilist]({anilist_url}), [MAL](https://myanimelist.net/{type}/{id_mal}), Kitsu (Soon™)".format(
                                    id_mal=anime_manga['idMal'], anilist_url=link, type=cmd.lower()))
                embeds.append(embed)

            return embeds, data

        else:
            return None

    async def _search_character(self, ctx, entered_title):

        variables = {
            'search': entered_title,
            'page': 1
        }

        data = (await self._request(SEARCH_CHARACTER_QUERY, variables))['data']['Page']['characters']

        if data is not None and len(data) > 0:

            # a list of embeds
            embeds = []

            for character in data:
                # Sets up various variables for Embed
                link = 'https://anilist.co/character/{}'.format(character['id'])
                character_anime = [
                    "[{}]({})".format(anime["title"]["userPreferred"], "https://anilist.co/anime/" + str(anime["id"]))
                    for anime in character["media"]["nodes"] if anime["type"] == "ANIME"]
                character_manga = [
                    "[{}]({})".format(manga["title"]["userPreferred"], "https://anilist.co/manga/" + str(manga["id"]))
                    for manga in character["media"]["nodes"] if manga["type"] == "MANGA"]
                embed = discord.Embed(title=self.format_name(character['name']['first'], character['name']['last']))
                embed.url = link
                embed.description = self.description_parser(character['description'])
                embed.set_thumbnail(url=character['image']['large'])
                if len(character_anime) > 0:
                    embed.add_field(name="Anime", value="\n".join(self.list_maximum(character_anime)))
                if len(character_manga) > 0:
                    embed.add_field(name="Manga", value="\n".join(self.list_maximum(character_manga)))
                embed.set_footer(text="Powered by Anilist")
                embeds.append(embed)

            return embeds, data

        else:
            return None

    async def _search_user(self, ctx, entered_title):

        variables = {
            'search': entered_title,
            'page': 1
        }

        data = (await self._request(SEARCH_USER_QUERY, variables))['data']['Page']['users']

        if data is not None and len(data) > 0:

            # a list of embeds
            embeds = []

            for user in data:
                # Sets up various variables for Embed
                link = 'https://anilist.co/user/{}'.format(user['id'])
                title = "[{}]({})".format(user['name'], link)
                title = user['name']

                embed = discord.Embed(title=title)
                embed.url = link
                embed.description = self.description_parser(user['about'])
                embed.set_thumbnail(url=user['avatar']['large'])
                embed.add_field(name="Watched time",
                                value=datetime.timedelta(minutes=int(user['stats']['watchedTime'])))
                embed.add_field(name="Chapters read", value=user['stats'].get('chaptersRead', 'N/A'))
                if user["favourites"]["anime"]['nodes']:
                    fav_anime = ["[{}]({})".format(anime["title"]["userPreferred"],
                                                   "https://anilist.co/anime/" + str(anime["id"])) for anime in
                                 user["favourites"]["anime"]["nodes"]]
                    embed.add_field(name="Favourite anime", value="\n".join(self.list_maximum(fav_anime)))
                if user["favourites"]["manga"]['nodes']:
                    fav_manga = ["[{}]({})".format(manga["title"]["userPreferred"],
                                                   "https://anilist.co/manga/" + str(manga["id"])) for manga in
                                 user["favourites"]["manga"]["nodes"]]
                    embed.add_field(name="Favourite manga", value="\n".join(self.list_maximum(fav_manga)))
                if user["favourites"]["characters"]['nodes']:
                    fav_ch = ["[{}]({})".format(self.format_name(character["name"]["first"], character["name"]["last"]),
                                                "https://anilist.co/character/" + str(character["id"])) for character in
                              user["favourites"]["characters"]["nodes"]]
                    embed.add_field(name="Favourite characters", value="\n".join(self.list_maximum(fav_ch)))
                embed.set_footer(text="Powered by Anilist")
                embeds.append(embed)

            return embeds, data

        else:
            return None

    @commands.command()
    async def anime(self, ctx, *, entered_title):
        """Searches for anime using Anilist"""

        try:
            cmd = "ANIME"
            embeds, data = await self._search_anime_manga(ctx, cmd, entered_title)

            if embeds is not None:
                await anilist_menu(ctx, embeds, message=None, page=0, timeout=30)
            else:
                await ctx.send('No anime was found or there was an error in the process')

        except TypeError:
            await ctx.send('No anime was found or there was an error in the process')

    @commands.command()
    async def manga(self, ctx, *, entered_title):
        """Searches for manga using Anilist"""

        try:
            cmd = "MANGA"
            embeds, data = await self._search_anime_manga(ctx, cmd, entered_title)

            if embeds is not None:
                await anilist_menu(ctx, embeds, message=None, page=0, timeout=30)
            else:
                await ctx.send('No mangas were found or there was an error in the process')

        except TypeError:
            await ctx.send('No mangas were found or there was an error in the process')

    @commands.command()
    async def character(self, ctx, *, entered_title):
        """Searches for anime using Anilist"""

        try:
            embeds, data = await self._search_character(ctx, entered_title)

            if embeds is not None:
                await anilist_menu(ctx, embeds, message=None, page=0, timeout=30)
            else:
                await ctx.send('No characters were found or there was an error in the process')

        except TypeError:
            await ctx.send('No characters were found or there was an error in the process')

    @commands.command()
    async def user(self, ctx, *, entered_title):
        """Searches users using Anilist"""

        try:
            embeds, data = await self._search_user(ctx, entered_title)

            if embeds is not None:
                await anilist_menu(ctx, embeds, message=None, page=0, timeout=30)
            else:
                await ctx.send('No users were found or there was an error in the process')

        except TypeError:
            await ctx.send('No users were found or there was an error in the process')


async def anilist_menu(ctx, anime_list: list,
                       message: discord.Message = None,
                       page=0, timeout: int = 30):
    """menu control logic for this taken from
       https://github.com/Lunar-Dust/Dusty-Cogs/blob/master/menu/menu.py"""
    emb = anime_list[page]
    if not message:
        message = await ctx.send(embed=emb)
        await message.add_reaction("⬅")
        await message.add_reaction("❌")
        await message.add_reaction("➡")
    else:
        await message.edit(embed=emb)

    def react_check(r, u):
        return u == ctx.author and str(r.emoji) in ["➡", "⬅", "❌"]

    try:
        react, user = await ctx.bot.wait_for(
            "reaction_add", check=react_check, timeout=timeout
        )
    except asyncio.TimeoutError:
        try:
            await message.clear_reactions()
        except discord.Forbidden:
            await message.remove_reaction("⬅", ctx.guild.me)
            await message.remove_reaction("❌", ctx.guild.me)
            await message.remove_reaction("➡", ctx.guild.me)
        return None
    reacts = {v: k for k, v in numbs.items()}
    react = reacts[react.emoji]
    if react == "next":
        perms = message.channel.permissions_for(ctx.guild.me)
        if perms.manage_messages:
            try:
                await message.remove_reaction("➡", ctx.author)
            except discord.NotFound:
                pass
        if page == len(anime_list) - 1:
            next_page = 0  # first item
        else:
            next_page = page + 1
        return await anilist_menu(ctx, anime_list, message=message, page=next_page, timeout=timeout)
    elif react == "back":
        perms = message.channel.permissions_for(ctx.guild.me)
        if perms.manage_messages:
            try:
                await message.remove_reaction("⬅", ctx.author)
            except discord.NotFound:
                pass
        if page == 0:
            next_page = len(anime_list) - 1  # last item
        else:
            next_page = page - 1
        return await anilist_menu(ctx, anime_list, message=message, page=next_page, timeout=timeout)
    else:
        try:
            await message.clear_reactions()
        except discord.Forbidden:
            await message.remove_reaction("⬅", ctx.guild.me)
            await message.remove_reaction("❌", ctx.guild.me)
            await message.remove_reaction("➡", ctx.guild.me)
        return None
