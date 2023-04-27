from .conversationgames import ConversationGames


async def setup(bot):
    n = ConversationGames()
    await bot.add_cog(n)
