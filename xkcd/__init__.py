from .xkcd import xkcd


def setup(bot):
    n = xkcd()
    bot.add_cog(n)
