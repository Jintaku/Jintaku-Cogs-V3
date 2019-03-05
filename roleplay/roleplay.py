import discord
from redbot.core import commands, Config
from random import randint

BaseCog = getattr(commands, "Cog", object)


class Roleplay(BaseCog):
    """Interact with people!"""

    def __init__(self):
        self.config = Config.get_conf(self, identifier=842364413)
        default_global = {
            "hugs": [
                "https://img2.gelbooru.com/images/ff/63/ff63a3c4329fda2bf1e9704d4e150fea.gif",
                "https://img2.gelbooru.com/images/2c/e8/2ce81403e0279f1a570711f7472b3abb.gif",
                "https://img2.gelbooru.com/images/e2/05/e205e349535e22c07865913770dcad5f.gif",
                "https://img2.gelbooru.com/images/09/f6/09f63a79f70700abb2593862525ade10.gif",
                "https://safebooru.org//images/1174/5ebeacd87b22a0c5949ecb875667ae75702c2fed.gif",
                "https://safebooru.org//images/848/4828fc43e39f52abd5bac6b299e822ae02786974.gif",
                "https://safebooru.org//images/160/ba09bc95bc05b4f47af22671950e66f085c7ea9e.gif",
                "https://img2.gelbooru.com/images/3f/73/3f73b1c3703d91a9300aebdaab6e26c0.gif",
                "https://img2.gelbooru.com/images/7d/7c/7d7c8ce0c4e561804f16adc7907a78e8.gif",
                "https://img2.gelbooru.com/images/5e/8c/5e8c1a33470c62f6907d0ea5a03ae644.gif",
                "https://img2.gelbooru.com/images/2b/b9/2bb9dc89cf991181bce06279d8d5f0f4.gif",
                "https://cdn.weeb.sh/images/rJaog0FtZ.gif",
                "https://cdn.weeb.sh/images/Hyv6uOQPZ.gif",
            ],
            "kiss": [
                "https://img2.gelbooru.com/images/72/3d/723d7b46a080e459321cb0a46fa4ff84.gif",
                "https://img2.gelbooru.com/images/14/15/141537ae7a372f093e7d6996b16c245b.gif",
                "https://img2.gelbooru.com/images/0d/f6/0df60e366022350bdaf7f49390ac90a9.gif",
                "https://img2.gelbooru.com/images/41/07/41070fe3eff7262f9f607a0a307c9740.gif",
                "https://img2.gelbooru.com/images/1c/67/1c670a0dc8ab6a43eb8b6781d78600ab.gif",
                "https://img2.gelbooru.com/images/63/f5/63f5a9a4cf7a872d6982ae6e518d212e.gif",
                "https://img2.gelbooru.com/images/a1/a8/a1a888b4f4c69e1dc493cbf66a3a855a.gif",
                "https://img2.gelbooru.com/images/ca/67/ca67e314075bab7fde43bfc9686e7fde.gif",
                "https://img2.gelbooru.com/images/28/45/2845a2ad83b4f207d7ccfbb98c3a1be6.gif",
            ],
            "slap": [
                "https://cdn.weeb.sh/images/H16aQJFvb.gif",
                "https://img2.gelbooru.com/images/d2/2c/d22c2eedd00914ce38efb46d797be031.gif",
                "https://safebooru.org//images/192/fb1c45872a172ab384a22b9d9089b861d366564c.gif",
                "https://safebooru.org//images/118/968c5b9f042a5262c8c8628cd52a7a6a557e525d.gif",
                "https://media1.tenor.com/images/d14969a21a96ec46f61770c50fccf24f/tenor.gif?itemid=5509136",
                "https://media1.tenor.com/images/9ea4fb41d066737c0e3f2d626c13f230/tenor.gif?itemid=7355956",
                "https://media1.tenor.com/images/4a6b15b8d111255c77da57c735c79b44/tenor.gif?itemid=10937039",
                "https://media1.tenor.com/images/153b2f1bfd3c595c920ce60f1553c5f7/tenor.gif?itemid=10936993",
                "https://media1.tenor.com/images/4fa82be21ffd18c99a9708ba209d56ad/tenor.gif?itemid=5318916",
                "https://media1.tenor.com/images/1ba1ea1786f0b03912b1c9138dac707c/tenor.gif?itemid=5738394",
            ],
            "pat": [
                "https://cdn.weeb.sh/images/r180y1Yvb.gif",
                "https://img2.gelbooru.com/images/56/b9/56b9297e70fd0312aba34e7ed1608b27.gif",
                "https://img2.gelbooru.com/images/ce/ea/ceea3600c9de0fb5a2452d1e9f2d714b.gif",
                "https://img2.gelbooru.com/images/4e/08/4e0895594994c5eedf5a1991f02bd4dc.gif",
                "https://img2.gelbooru.com/images/c7/41/c741fec81ea5eceb8ebcc7b4dc2bedd5.gif",
                "http://i.imgur.com/10VrpFZ.gif",
                "http://i.imgur.com/x0u35IU.gif",
                "http://i.imgur.com/0gTbTNR.gif",
                "http://i.imgur.com/hlLCiAt.gif",
                "http://i.imgur.com/sAANBDj.gif",
            ],
            "lick": [
                "https://media1.tenor.com/images/c4f68fbbec3c96193386e5fcc5429b89/tenor.gif?itemid=13451325",
                "https://media1.tenor.com/images/ec2ca0bf12d7b1a30fea702b59e5a7fa/tenor.gif?itemid=13417195",
            ],
            "highfive": ["https://media1.tenor.com/images/0ae4995e4eb27e427454526c05b2e3dd/tenor.gif?itemid=12376992"],
            "feed": [
                "https://media1.tenor.com/images/93c4833dbcfd5be9401afbda220066ee/tenor.gif?itemid=11223742",
                "https://media1.tenor.com/images/33cfd292d4ef5e2dc533ff73a102c2e6/tenor.gif?itemid=12165913",
                "https://media1.tenor.com/images/72268391ffde3cd976a456ee2a033f46/tenor.gif?itemid=7589062",
                "https://media1.tenor.com/images/4b48975ec500f8326c5db6b178a91a3a/tenor.gif?itemid=12593977",
                "https://media1.tenor.com/images/187ff5bc3a5628b6906935232898c200/tenor.gif?itemid=9340097",
            ],
        }
        self.config.register_global(**default_global)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def hugs(self, ctx, *, user: discord.Member):
        """Hugs a user!"""

        author = ctx.message.author
        images = await self.config.hugs()
        mn = len(images)
        i = randint(0, mn - 1)

        # Build Embed
        embed = discord.Embed()
        embed.description = f"**{author.mention} hugs {user.mention}**"
        embed.set_image(url=images[i])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def kiss(self, ctx, *, user: discord.Member):
        """Kiss a user!"""

        author = ctx.message.author
        images = await self.config.kiss()
        mn = len(images)
        i = randint(0, mn - 1)

        # Build Embed
        embed = discord.Embed()
        embed.description = f"**{author.mention} kisses {user.mention}**"
        embed.set_image(url=images[i])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def slap(self, ctx, *, user: discord.Member):
        """Slaps a user!"""

        author = ctx.message.author
        images = await self.config.slap()
        mn = len(images)
        i = randint(0, mn - 1)

        # Build Embed
        embed = discord.Embed()
        embed.description = f"**{author.mention} slaps {user.mention}**"
        embed.set_image(url=images[i])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def pat(self, ctx, *, user: discord.Member):
        """Pats a user!"""

        author = ctx.message.author
        images = await self.config.pat()
        mn = len(images)
        i = randint(0, mn - 1)

        # Build Embed
        embed = discord.Embed()
        embed.description = f"**{author.mention} pats {user.mention}**"
        embed.set_image(url=images[i])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def lick(self, ctx, *, user: discord.Member):
        """Licks a user!"""

        author = ctx.message.author
        images = await self.config.lick()
        mn = len(images)
        i = randint(0, mn - 1)

        # Build Embed
        embed = discord.Embed()
        embed.description = f"**{author.mention} licks {user.mention}**"
        embed.set_image(url=images[i])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def highfive(self, ctx, *, user: discord.Member):
        """Highfives a user!"""

        author = ctx.message.author
        images = await self.config.highfive()
        mn = len(images)
        i = randint(0, mn - 1)

        # Build Embed
        embed = discord.Embed()
        embed.description = f"**{author.mention} highfives {user.mention}**"
        embed.set_image(url=images[i])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def feed(self, ctx, *, user: discord.Member):
        """Feeds a user!"""

        author = ctx.message.author
        images = await self.config.feed()
        mn = len(images)
        i = randint(0, mn - 1)

        # Build Embed
        embed = discord.Embed()
        embed.description = f"**{author.mention} feeds {user.mention}**"
        embed.set_image(url=images[i])
        await ctx.send(embed=embed)
