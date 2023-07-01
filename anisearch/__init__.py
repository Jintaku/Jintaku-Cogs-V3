from .anisearch import AniSearch

async def setup(bot):
    await bot.add_cog(AniSearch())
