import discord
from redbot.core import commands
import aiohttp
from numbers import Number
from random import randint
from typing import Optional, Union

BaseCog = getattr(commands, "Cog", object)

class XKCD(BaseCog):
    """Display XKCD entries"""

    @commands.command()
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    async def xkcd(self, ctx, entry_number: Optional[Union[int, str]] = None):
        """Post a random xkcd. Accepts "latest" as an entry number."""

        # Creates random number between 0 and the latest xkcd num and queries xkcd
        async with aiohttp.ClientSession() as session:
            xkcd_latest = await self.get_xkcd(session=session)
            xkcd_max = xkcd_latest.get("num")

            if isinstance(entry_number, int):
                if not 0 < entry_number <= xkcd_max:
                    await ctx.send("Not a valid xkcd entry.")
                    return
                num = entry_number
                xkcd = await self.get_xkcd(num, session=session)
            elif entry_number == "latest":
                num = xkcd_max
                xkcd = xkcd_latest
            else:
                num = randint(0, xkcd_max)
                xkcd = await self.get_xkcd(num, session=session)

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
                       session: Optional[aiohttp.ClientSession] = None,
                       headers: Optional[dict] = None) -> dict:
        """Fetches the xkcd metadata for a certain entry. If unspecified, it's the latest."""
        headers = {"Content-Type": "application/json"} if headers is None else headers
        current_session = aiohttp.ClientSession() if session is None else session
        try:
            if entry_number is not None:
                url = "https://xkcd.com/" + str(entry_number) + "/info.0.json"
            else:
                url = "https://xkcd.com/info.0.json"
            async with current_session.get(url, headers=headers) as response:
                    xkcd = await response.json()
                    xkcd = xkcd.copy() # just in case.
            return xkcd
        finally:
            if session is None:
                await current_session.close()
