from .gamesearch import Gamesearch


def setup(bot):
    n = Gamesearch()
    bot.add_cog(n)
