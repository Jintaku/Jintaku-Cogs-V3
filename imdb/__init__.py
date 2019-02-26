from .imdb import Imdb


def setup(bot):
    n = Imdb()
    bot.add_cog(n)
