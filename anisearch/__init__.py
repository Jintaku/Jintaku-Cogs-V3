from .anisearch import AniSearch


async def setup(bot):
    n = AniSearch()
    await bot.add_cog(n)
