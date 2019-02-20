from .wikia import Wikia


def setup(bot):
    n = Wikia()
    bot.add_cog(n)
