from .dmannouncer import Dmannouncer


def setup(bot):
    n = Dmannouncer()
    bot.add_cog(n)
