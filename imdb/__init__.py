from .imdb import Imdb


async def setup(bot):
    n = Imdb()
    await bot.add_cog(n)
