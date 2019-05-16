from .8ball import 8ball


def setup(bot):
    n = 8ball()
    bot.add_cog(n)
