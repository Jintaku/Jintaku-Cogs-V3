from .booru import booru


def setup(bot):
    n = booru()
    bot.add_cog(n)
