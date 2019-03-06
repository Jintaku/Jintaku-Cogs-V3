from .truthordare import Truthordare


def setup(bot):
    n = Truthordare()
    bot.add_cog(n)
