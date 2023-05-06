from .gamesearch import Gamesearch


async def setup(bot):
    n = Gamesearch()
    await bot.add_cog(n)
