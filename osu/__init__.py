from .osu import Osu


def setup(bot):
    n = Osu()
    bot.add_cog(n)
