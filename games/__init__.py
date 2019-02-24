from .games import Games


def setup(bot):
    n = Games()
    bot.add_cog(n)
