from .confession import Confession


def setup(bot):
    n = Confession()
    bot.add_cog(n)
