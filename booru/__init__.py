from .booru import Booru


def setup(bot):
    n = Booru()
    bot.add_cog(n)
