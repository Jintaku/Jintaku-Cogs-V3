import discord
from redbot.core import commands
import aiohttp
from numbers import Number
from random import randint

BaseCog = getattr(commands, "Cog", object)

class xkcd(BaseCog):
    """Display XKCD entries"""

    @commands.command(pass_context=True)
    async def xkcd(self, ctx, *, entry_number=None):
        """Post a random xkcd"""

        # Creates random number between 0 and 2002 (number of xkcd comics at time of writing) and queries xkcd
        if entry_number is not None and int(entry_number) > 0 and int(entry_number) < 2002:
            i = int(entry_number)
        else:
            i = randint(0, 2002)
        headers = {'content-type': 'application/json'}
        url = "https://xkcd.com/" + str(i) + "/info.0.json"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                xkcd = await response.json()

        # Build Embed
        print(xkcd)
        embed = discord.Embed()
        embed.title = xkcd['title'] + " (" + xkcd['day'] + "/" + xkcd['month'] + "/" + xkcd['year'] + ")"
        embed.url = "https://xkcd.com/" + str(i)
        embed.description = xkcd['alt']
        embed.set_image(url=xkcd['img'])
        embed.set_footer(text="Powered by xkcd")
        await ctx.send(embed=embed)
