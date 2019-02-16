from .pokemon import Pokemon


def setup(bot):
    n = Pokemon()
    bot.add_cog(n)
