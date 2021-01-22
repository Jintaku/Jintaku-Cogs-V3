import discord
from redbot.core import commands, Config
from random import randint
import aiohttp
import logging

log = logging.getLogger("Roleplay")  # Thanks to Sinbad for the example code for logging
log.setLevel(logging.DEBUG)

console = logging.StreamHandler()

if logging.getLogger("red").isEnabledFor(logging.DEBUG):
    console.setLevel(logging.DEBUG)
else:
    console.setLevel(logging.INFO)
log.addHandler(console)

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
                "https://cdn.weeb.sh/images/BJx2l0ttW.gif",
                "https://media.giphy.com/media/iviBUyNqP46Aw/giphy.gif",
                "https://media.giphy.com/media/wnsgren9NtITS/giphy.gif",
                "https://media.giphy.com/media/svXXBgduBsJ1u/giphy.gif",
                "https://media.giphy.com/media/3ZnBrkqoaI2hq/giphy.gif",
                "https://media.giphy.com/media/3o6ZsTopjMRVkJXAWI/giphy.gif",
                "https://media.giphy.com/media/od5H3PmEG5EVq/giphy.gif",
                "https://media.giphy.com/media/vVA8U5NnXpMXK/giphy.gif",
                "https://media.giphy.com/media/aVmEsdMmCTqSs/giphy.gif",
                "https://media.giphy.com/media/ZQN9jsRWp1M76/giphy.gif",
                "https://media.giphy.com/media/DjczAlIcyK1Co/giphy.gif",
                "https://media.giphy.com/media/ba92ty7qnNcXu/giphy.gif",
                "https://media.giphy.com/media/C4gbG94zAjyYE/giphy.gif",
                "https://i.imgur.com/4Y50gzE.gif",
                "https://i.imgur.com/OrpyAfa.gif",
                "https://i.imgur.com/aA8mTuX.gif",
                "https://i.imgur.com/fm9PHyr.gif",
                "https://i.imgur.com/tCuAWNW.gif",
                "https://i.imgur.com/BPMTcq7.gif",
                "https://i.imgur.com/V1fd9oP.gif",
                "https://i.imgur.com/OSDidQJ.gif",
                "https://i.imgur.com/hM1LcZf.gif",
                "https://i.imgur.com/cRfX87T.gif",
                "https://cdn.weeb.sh/images/HyNJIaVCb.gif",
                "https://cdn.weeb.sh/images/ryMqdOXvZ.gif",
                "https://cdn.weeb.sh/images/Hk4qu_XvZ.gif",
                "https://cdn.weeb.sh/images/ByuHsvu8z.gif",
                "https://cdn.weeb.sh/images/Hy4hxRKtW.gif",
                "https://cdn.weeb.sh/images/Sk2gmRZZG.gif",
                "https://cdn.weeb.sh/images/HkfgF_QvW.gif",
                "https://cdn.weeb.sh/images/HJTWcTNCZ.gif",
                "https://cdn.weeb.sh/images/rko9O_mwW.gif",
                "https://cdn.weeb.sh/images/rkx1dJ25z.gif",
                "https://media.giphy.com/media/KMQoRt68bFei4/giphy.gif",
                "https://cdn.weeb.sh/images/BkZngAYtb.gif",
            ],
            "cuddle": [
                "https://cdn.weeb.sh/images/BkTe8U7v-.gif",
                "https://cdn.weeb.sh/images/SykzL87D-.gif",
                "https://cdn.weeb.sh/images/BywGX8caZ.gif",
                "https://cdn.weeb.sh/images/SJceIU7wZ.gif",
                "https://cdn.weeb.sh/images/SJn18IXP-.gif",
                "https://cdn.weeb.sh/images/B1Qb88XvW.gif",
                "https://cdn.weeb.sh/images/r1XEOymib.gif",
                "https://cdn.weeb.sh/images/SJLkLImPb.gif",
                "https://cdn.weeb.sh/images/SyUYOJ7iZ.gif",
                "https://cdn.weeb.sh/images/rkBl8LmDZ.gif",
                "https://cdn.weeb.sh/images/B1S1I87vZ.gif",
                "https://cdn.weeb.sh/images/r1s9RqB7G.gif",
                "https://cdn.weeb.sh/images/Hy5y88mPb.gif",
                "https://cdn.weeb.sh/images/rkA6SU7w-.gif",
                "https://cdn.weeb.sh/images/r1A77CZbz.gif",
                "https://cdn.weeb.sh/images/SJYxIUmD-.gif",
                "https://cdn.weeb.sh/images/H1SfI8XwW.gif",
                "https://cdn.weeb.sh/images/rJCAH8XPb.gif",
                "https://cdn.weeb.sh/images/By03IkXsZ.gif",
                "https://cdn.weeb.sh/images/ryfyLL7D-.gif",
                "https://cdn.weeb.sh/images/BJwpw_XLM.gif",
                "https://cdn.weeb.sh/images/r1VzDkmjW.gif",
                "https://cdn.weeb.sh/images/HkzArUmvZ.gif",
                "https://cdn.weeb.sh/images/r1A77CZbz.gif",
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
                "https://i.imgur.com/WYkVxW2.gif",
                "https://i.imgur.com/xu104Xp.gif",
                "https://i.imgur.com/8jcpBO7.gif",
                "https://i.imgur.com/jmWGYh5.gif",
                "https://i.imgur.com/Sg8Obai.gif",
                "https://i.imgur.com/Pr06rra.gif",
                "https://i.imgur.com/J8xgNpE.gif",
                "https://i.imgur.com/gtIEfcS.gif",
                "https://i.imgur.com/j3zdC5g.gif",
                "https://cdn.weeb.sh/images/r1cB3aOwW.gif",
                "https://cdn.weeb.sh/images/B1MJ2aODb.gif",
                "https://cdn.weeb.sh/images/Hy-oQl91z.gif",
                "https://cdn.weeb.sh/images/rJ6PWohA-.gif",
                "https://cdn.weeb.sh/images/rJrCj6_w-.gif",
                "https://78.media.tumblr.com/7255f36b2c31fac77542e8fe6837b408/tumblr_mokq94dAXR1s05qslo1_500.gif",
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
                "https://i.imgur.com/EO8udG1.gif",
                "https://i.imgur.com/lMmn1wy.gif",
                "https://i.imgur.com/TuSUTg5.gif",
                "https://i.imgur.com/9Ql97mO.gif",
                "https://i.imgur.com/VBGqeIU.gif",
                "https://i.imgur.com/uPZwGFQ.gif",
                "https://i.imgur.com/Su0X9iF.gif",
                "https://i.imgur.com/eNiOIMB.gif",
                "https://i.imgur.com/gsAGyoI.gif",
                "https://cdn.weeb.sh/images/HyPjmytDW.gif",
                "https://cdn.weeb.sh/images/BJ8o71tD-.gif",
                "https://cdn.weeb.sh/images/BJLCX1Kw-.gif",
                "https://cdn.weeb.sh/images/rJvR71KPb.gif",
                "https://cdn.weeb.sh/images/SkZTQkKPZ.gif",
                "https://cdn.weeb.sh/images/Hkw1VkYP-.gif",
                "https://cdn.weeb.sh/images/BkxEo7ytDb.gif",
                "https://cdn.weeb.sh/images/B1fnQyKDW.gif",
                "https://cdn.weeb.sh/images/Bkj-oaV0Z.gif",
                "https://cdn.weeb.sh/images/r1siXJKw-.gif",
                "https://cdn.weeb.sh/images/r1VF-lcyz.gif",
                "https://cdn.weeb.sh/images/BJgsX1Kv-.gif",
                "https://cdn.weeb.sh/images/SkKn-xc1f.gif",
                "https://cdn.weeb.sh/images/Sk9mfCtY-.gif",
                "https://cdn.weeb.sh/images/ry_RQkYDb.gif",
                "https://cdn.weeb.sh/images/HkK2mkYPZ.gif",
                "https://cdn.weeb.sh/images/S1ylxxc1M.gif",
                "https://cdn.weeb.sh/images/SJdXoVguf.gif",
                "https://cdn.weeb.sh/images/ByHUMRNR-.gif",
                "https://cdn.weeb.sh/images/SkdyfWCSf.gif",
                "https://cdn.weeb.sh/images/rknn7Jtv-.gif",
                "https://cdn.weeb.sh/images/rJgTQ1tvb.gif",
                "https://cdn.weeb.sh/images/rkaqm1twZ.gif",
                "https://cdn.weeb.sh/images/ryn_Zg5JG.gif",
                "https://cdn.weeb.sh/images/SJ-CQytvW.gif",
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
                "https://i.imgur.com/10VrpFZ.gif"
                "https://i.imgur.com/x0u35IU.gif",
                "https://i.imgur.com/sAANBDj.gif",
                "https://i.imgur.com/wtxwpm1.gif",
                "https://i.imgur.com/3eR7weH.gif",
                "https://i.imgur.com/cK8Ro3x.gif",
                "https://i.imgur.com/qtHlt3n.gif",
                "https://i.imgur.com/bzzodCZ.gif",
                "https://cdn.weeb.sh/images/r180y1Yvb.gif",
                "https://cdn.weeb.sh/images/Sky1x1YwW.gif",
                "https://cdn.weeb.sh/images/r1Y5L6NCZ.gif",
                "https://cdn.weeb.sh/images/HJGQlJYwb.gif",
                "https://cdn.weeb.sh/images/rkBZkRttW.gif",
                "https://cdn.weeb.sh/images/rJavp1KVM.gif",
                "https://cdn.weeb.sh/images/r1AsJ1twZ.gif",
                "https://cdn.weeb.sh/images/ry1tlj2AW.gif",
                "https://cdn.weeb.sh/images/HyqTkyFvb.gif",
                "https://cdn.weeb.sh/images/H1jnJktPb.gif",
                "https://cdn.weeb.sh/images/ryLKqTVCW.gif",
                "https://cdn.weeb.sh/images/rJJXgJFDW.gif",
                "https://i.imgur.com/grAHcaB.gif",
                "https://cdn.weeb.sh/images/SJS1lyYwW.gif",
                "https://cdn.weeb.sh/images/rkbblkYvb.gif",
                "https://cdn.weeb.sh/images/H1s5hx0Bf.gif",
                "https://cdn.weeb.sh/images/rkSN7g91M.gif",
                "https://cdn.weeb.sh/images/rktsca40-.gif",
                "https://cdn.weeb.sh/images/ryh6x04Rb.gif",
                "https://cdn.weeb.sh/images/rkTC896_f.gif",
                "https://cdn.weeb.sh/images/SJudB96_f.gif",
                "https://cdn.weeb.sh/images/SJudB96_f.gif",
                "https://cdn.weeb.sh/images/r1lVQgcyG.gif",
            ],
            "lick": [
                "https://media1.tenor.com/images/c4f68fbbec3c96193386e5fcc5429b89/tenor.gif?itemid=13451325",
                "https://media1.tenor.com/images/ec2ca0bf12d7b1a30fea702b59e5a7fa/tenor.gif?itemid=13417195",
                "https://cdn.weeb.sh/images/HkEqiExdf.gif",
                "https://media1.tenor.com/images/5f73f2a7b302a3800b3613095f8a5c40/tenor.gif?itemid=10005495",
                "https://media1.tenor.com/images/6b701503b0e5ea725b0b3fdf6824d390/tenor.gif?itemid=12141727",
                "https://media1.tenor.com/images/069076cc8054bb8b114c5a37eec70a1f/tenor.gif?itemid=13248504",
                "https://media1.tenor.com/images/fc0ef2ba03d82af0cbd6c5815c3c83d5/tenor.gif?itemid=12141725",
                "https://media1.tenor.com/images/d702fa41028207c6523b831ec2db9467/tenor.gif?itemid=5990650",
                "https://media1.tenor.com/images/81769ee6622b5396d1489fb4667fd20a/tenor.gif?itemid=14376074",
                "https://media1.tenor.com/images/feeef4685f9307b76c78a22ba0a69f48/tenor.gif?itemid=8413059",
                "https://media1.tenor.com/images/efd46743771a78e493e66b5d26cd2af1/tenor.gif?itemid=14002773",
            ],
            "highfive": [
                "https://media1.tenor.com/images/0ae4995e4eb27e427454526c05b2e3dd/tenor.gif?itemid=12376992",
                "https://media1.tenor.com/images/7b1f06eac73c36721912edcaacddf666/tenor.gif?itemid=10559431",
                "https://media1.tenor.com/images/c3263b8196afc25ddc1d53a4224347cd/tenor.gif?itemid=9443275",
                "https://media1.tenor.com/images/56d6725009312574e4798c732cebc5fe/tenor.gif?itemid=12312526",
                "https://media1.tenor.com/images/e96d2396570a2fadd9c83e284a1ca675/tenor.gif?itemid=5390726",
                "https://media1.tenor.com/images/106c8e64e864230341b59cc892b5a980/tenor.gif?itemid=5682921",
                "https://media1.tenor.com/images/b714d7680f8b49d69b07bc2f1e052e72/tenor.gif?itemid=13400356",
                "https://media1.tenor.com/images/0c23b320822afd5b1ce3faf01c2b9b69/tenor.gif?itemid=14137078",
                "https://media1.tenor.com/images/e2f299d05a7b1832314ec7a331440d4e/tenor.gif?itemid=5374033",
                "https://media1.tenor.com/images/16267f3a34efb42598bd822effaccd11/tenor.gif?itemid=14137081",
                "https://media1.tenor.com/images/9730876547cb3939388cf79b8a641da9/tenor.gif?itemid=8073516",
                "https://media1.tenor.com/images/ce85a2843f52309b85515f56a0a49d06/tenor.gif?itemid=14137077",
            ],
            "feed": [
                "https://media1.tenor.com/images/93c4833dbcfd5be9401afbda220066ee/tenor.gif?itemid=11223742",
                "https://media1.tenor.com/images/33cfd292d4ef5e2dc533ff73a102c2e6/tenor.gif?itemid=12165913",
                "https://media1.tenor.com/images/72268391ffde3cd976a456ee2a033f46/tenor.gif?itemid=7589062",
                "https://media1.tenor.com/images/4b48975ec500f8326c5db6b178a91a3a/tenor.gif?itemid=12593977",
                "https://media1.tenor.com/images/187ff5bc3a5628b6906935232898c200/tenor.gif?itemid=9340097",
                "https://media1.tenor.com/images/15e7d9e1eb0aad2852fabda1210aee95/tenor.gif?itemid=12005286",
                "https://media1.tenor.com/images/d08d0825019c321f21293c35df8ed6a9/tenor.gif?itemid=9032297",
                "https://media1.tenor.com/images/571da4da1ad526afe744423f7581a452/tenor.gif?itemid=11658244",
                "https://media1.tenor.com/images/6bde17caa5743a22686e5f7b6e3e23b4/tenor.gif?itemid=13726430",
                "https://media1.tenor.com/images/fd3616d34ade61e1ac5cd0975c25a917/tenor.gif?itemid=13653906",
                "https://imgur.com/v7jsPrv",
            ],
            "tickle": [
                "https://img2.gelbooru.com/images/c4/41/c441cf1fce1fe51420796f6bd0e420e1.gif",
                "https://img2.gelbooru.com/images/00/a8/00a8b5ad3ceb7b063ed8a4a59f7c8bdf.gif",
                "https://img2.gelbooru.com/images/51/63/516318277e9438626c12d0543eb5808b.gif",
                "https://img2.gelbooru.com/images/0c/e4/0ce45bee2e1aaed9f1e650438f1e2867.gif",
                "https://img2.gelbooru.com/images/11/74/1174ccbee672bd3f1129f5dc36964926.gif",
                "https://media1.tenor.com/images/02f62186ccb7fa8a2667f3216cfd7e13/tenor.gif?itemid=13269751",
                "https://media1.tenor.com/images/d38554c6e23b86c81f8d4a3764b38912/tenor.gif?itemid=11379131",
                "https://media1.tenor.com/images/05a64a05e5501be2b1a5a734998ad2b2/tenor.gif?itemid=11379130",
            ],
            "poke": [
                "https://img2.gelbooru.com/images/07/86/078690a58e0b816e8e00cc58e090b499.gif",
                "https://img2.gelbooru.com/images/b7/89/b789369db69022afde47a1ed62598ec6.gif",
                "https://img2.gelbooru.com/images/49/ec/49ecc543b7b0b680ad0c27c29e942a21.gif",
                "https://img2.gelbooru.com/images/91/ef/91ef340231f6d537836e23c8ab90a255.gif",
                "https://img2.gelbooru.com/images/62/d9/62d9a16a640bfcd25dd6159e53fc50d2.gif",
                "https://img2.gelbooru.com/images/1d/8b/1d8b77bf65858101a82d195deaa39252.gif",
                "https://img2.gelbooru.com/images/c0/22/c022dc318c7f014d7bac6c2300b9f7a2.gif",
                "https://media1.tenor.com/images/3b2bfd09965bd77f2a8cb9ba59cedbe4/tenor.gif?itemid=5607667",
                "https://media1.tenor.com/images/514efe749cb611eb382713596e3427d8/tenor.gif?itemid=13054528",
                "https://media1.tenor.com/images/8795ff617de989265907eed8029a99a3/tenor.gif?itemid=14629871",
                "https://media1.tenor.com/images/1e0ea8b241a7db2b9c03775133138733/tenor.gif?itemid=10064326",
                "https://media1.tenor.com/images/90f68d48795c51222c60afc7239c930c/tenor.gif?itemid=8701034",
                "https://media1.tenor.com/images/01b264dc057eff2d0ee6869e9ed514c1/tenor.gif?itemid=14346763",
                "https://media1.tenor.com/images/f8a48a25f47d5d12342705c7c87368bb/tenor.gif?itemid=14134415",
                "https://media.tenor.com/images/6b5c1554a6ee9d48ab0392603bab8a8e/tenor.gif",
            ],
            "smug": [
                "https://cdn.nekos.life/v3/sfw/gif/smug/smug_027.gif",
                "https://cdn.nekos.life/v3/sfw/gif/smug/smug_057.gif",
                "https://i.kym-cdn.com/photos/images/original/001/087/562/93c.gif",
                "https://i.kym-cdn.com/photos/images/newsfeed/001/161/167/eda.gif",
                "https://media1.tenor.com/images/d9b3127da3f9419cbb28f9f7c00860d8/tenor.gif?itemid=9588226",
                "https://media1.tenor.com/images/0097fa7f957477f9edc5ff147bb9a5ad/tenor.gif?itemid=12390496",

            ],
        }
        self.config.register_global(**default_global)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def hugs(self, ctx, *, user: discord.Member):
        """Hugs a user!"""

        author = ctx.message.author
        images = await self.config.hugs()

        nekos = await self.fetch_nekos_life(ctx, "hug")
        images.extend(nekos)

        mn = len(images)
        i = randint(0, mn - 1)

        # Build Embed
        embed = discord.Embed()
        embed.description = f"**{author.mention} hugs {user.mention}**"
        embed.set_footer(text="Made with the help of nekos.life")
        embed.set_image(url=images[i])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def cuddle(self, ctx, *, user: discord.Member):
        """Cuddles a user!"""

        author = ctx.message.author
        images = await self.config.cuddle()

        nekos = await self.fetch_nekos_life(ctx, "cuddle")
        images.extend(nekos)

        mn = len(images)
        i = randint(0, mn - 1)

        # Build Embed
        embed = discord.Embed()
        embed.description = f"**{author.mention} cuddles {user.mention}**"
        embed.set_footer(text="Made with the help of nekos.life")
        embed.set_image(url=images[i])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def kiss(self, ctx, *, user: discord.Member):
        """Kiss a user!"""

        author = ctx.message.author
        images = await self.config.kiss()

        nekos = await self.fetch_nekos_life(ctx, "kiss")
        images.extend(nekos)

        mn = len(images)
        i = randint(0, mn - 1)

        # Build Embed
        embed = discord.Embed()
        embed.description = f"**{author.mention} kisses {user.mention}**"
        embed.set_footer(text="Made with the help of nekos.life")
        embed.set_image(url=images[i])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def slap(self, ctx, *, user: discord.Member):
        """Slaps a user!"""

        author = ctx.message.author
        images = await self.config.slap()

        nekos = await self.fetch_nekos_life(ctx, "slap")
        images.extend(nekos)

        mn = len(images)
        i = randint(0, mn - 1)

        # Build Embed
        embed = discord.Embed()
        embed.description = f"**{author.mention} slaps {user.mention}**"
        embed.set_footer(text="Made with the help of nekos.life")
        embed.set_image(url=images[i])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def pat(self, ctx, *, user: discord.Member):
        """Pats a user!"""

        author = ctx.message.author
        images = await self.config.pat()

        nekos = await self.fetch_nekos_life(ctx, "pat")
        images.extend(nekos)

        mn = len(images)
        i = randint(0, mn - 1)

        # Build Embed
        embed = discord.Embed()
        embed.description = f"**{author.mention} pats {user.mention}**"
        embed.set_footer(text="Made with the help of nekos.life")
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
        embed.set_footer(text="Made with the help of nekos.life")
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
        embed.set_footer(text="Made with the help of nekos.life")
        embed.set_image(url=images[i])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def feed(self, ctx, *, user: discord.Member):
        """Feeds a user!"""

        author = ctx.message.author
        images = await self.config.feed()

        nekos = await self.fetch_nekos_life(ctx, "feed")
        images.extend(nekos)

        mn = len(images)
        i = randint(0, mn - 1)

        # Build Embed
        embed = discord.Embed()
        embed.description = f"**{author.mention} feeds {user.mention}**"
        embed.set_footer(text="Made with the help of nekos.life")
        embed.set_image(url=images[i])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def tickle(self, ctx, *, user: discord.Member):
        """Tickles a user!"""

        author = ctx.message.author
        images = await self.config.tickle()

        nekos = await self.fetch_nekos_life(ctx, "tickle")
        images.extend(nekos)

        mn = len(images)
        i = randint(0, mn - 1)

        # Build Embed
        embed = discord.Embed()
        embed.description = f"**{author.mention} tickles {user.mention}**"
        embed.set_footer(text="Made with the help of nekos.life")
        embed.set_image(url=images[i])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def poke(self, ctx, *, user: discord.Member):
        """Pokes a user!"""

        author = ctx.message.author
        images = await self.config.poke()

        nekos = await self.fetch_nekos_life(ctx, "poke")
        images.extend(nekos)

        mn = len(images)
        i = randint(0, mn - 1)

        # Build Embed
        embed = discord.Embed()
        embed.description = f"**{author.mention} pokes {user.mention}**"
        embed.set_footer(text="Made with the help of nekos.life")
        embed.set_image(url=images[i])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def smug(self, ctx):
        """Be smug towards someone!"""

        author = ctx.message.author
        images = await self.config.smug()

        smug = await self.fetch_nekos_life(ctx, "smug")
        images.extend(smug)

        mn = len(images)
        i = randint(0, mn - 1)

        # Build Embed
        embed = discord.Embed()
        embed.description = f"**{author.mention} is smug**"
        embed.set_footer(text="Made with the help of nekos.life")
        embed.set_image(url=images[i])
        await ctx.send(embed=embed)

    async def fetch_nekos_life(self, ctx, rp_action):

        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.nekos.dev/api/v3/images/sfw/gif/{rp_action}/?count=20") as resp:
                try:
                    content = await resp.json(content_type=None)
                except (ValueError, aiohttp.ContentTypeError) as ex:
                    log.debug("Pruned by exception, error below:")
                    log.debug(ex)
                    return []

        if content["data"]["status"]["code"] == 200:
            return content["data"]["response"]["urls"]

