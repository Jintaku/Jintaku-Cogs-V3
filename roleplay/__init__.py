from .roleplay import Roleplay


def setup(bot):
    n = Roleplay()
    bot.add_cog(n)
