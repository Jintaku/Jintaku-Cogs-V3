from .anisearch import AniSearch


def setup(bot):
    n = AniSearch(bot)
    bot.add_cog(n)
