from .xkcd import XKCD


def setup(bot):
    n = XKCD()
    bot.add_cog(n)
