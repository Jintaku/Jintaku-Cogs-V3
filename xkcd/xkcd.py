import discord
from redbot.core import commands
from redbot.core.bot import Red
import aiohttp
from random import randint
from typing import Optional, Union

BaseCog = getattr(commands, "Cog", object)

class XKCD(BaseCog):
    """Display XKCD entries"""

    def __init__(self, bot: Red):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    def cog_unload(self):
        self.bot.loop.create_task(self.session.close())

    @commands.command()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def xkcd(self, ctx, entry_number: Optional[Union[int, str]] = None):
        """Post a random xkcd. Accepts "latest" as an entry number."""

        xkcd_latest = await self.get_xkcd()
        xkcd_max = xkcd_latest.get("num")

        if isinstance(entry_number, int):
            if not 0 < entry_number <= xkcd_max:
                await ctx.send("Not a valid xkcd entry.")
                return
            num = entry_number
            xkcd = await self.get_xkcd(num)
        elif entry_number == "latest":
            num = xkcd_max
            xkcd = xkcd_latest
        else:
            num = randint(0, xkcd_max)
            xkcd = await self.get_xkcd(num)

        # Build Embed
        embed = discord.Embed()
        embed.title = (xkcd["title"] + " (" + xkcd["year"]
                                            + "/" + xkcd["month"].zfill(2)
                                            + "/" + xkcd["day"].zfill(2) + ")")
        embed.url = "https://xkcd.com/" + str(num) + "/"
        embed.description = xkcd["alt"]
        embed.set_image(url=xkcd["img"])
        embed.set_footer(text="Powered by xkcd")
        await ctx.send(embed=embed)

    async def get_xkcd(self, entry_number: Optional[Union[int, str]] = None,
                       headers: Optional[dict] = None) -> dict:
        """Fetches the xkcd metadata for a certain entry.
        If unspecified, it's the latest."""

        headers = {"Content-Type": "application/json"} if headers is None else headers

        if entry_number is not None:
            url = "https://xkcd.com/" + str(entry_number) + "/info.0.json"
        else:
            url = "https://xkcd.com/info.0.json"
        async with self.session.get(url, headers=headers) as response:
                xkcd = await response.json()
                xkcd = xkcd.copy() # just in case.
        return xkcd
