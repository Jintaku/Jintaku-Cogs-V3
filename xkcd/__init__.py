from .xkcd import XKCD
from redbot.core.bot import Red

def setup(bot: Red):
    n = XKCD(bot)
    bot.add_cog(n)
