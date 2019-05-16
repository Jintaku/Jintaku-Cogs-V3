from .ball import ball


def setup(bot):
    n = ball()
    bot.add_cog(n)
