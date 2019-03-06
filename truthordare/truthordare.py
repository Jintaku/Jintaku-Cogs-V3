import discord
from redbot.core import commands, Config
from random import randint

BaseCog = getattr(commands, "Cog", object)


class Truthordare(BaseCog):
    """Truth or dare people!"""

    def __init__(self):
        self.config = Config.get_conf(self, identifier=842364413)
        default_global = {
            "truths": [
                "What was the last thing you searched for on your phone?",
                "If you had to choose between going naked or having your thoughts appear in thought bubbles above your head for everyone to read, which would you choose?",
                "After you've dropped a piece of food, what's the longest time you've left it on the ground and then ate it?",
                "Have you ever played Cards Against Humanity with your parents?",
                "What's the first thing you would do if you woke up one day as the opposite sex?",
                "Have you ever peed in the pool?",
                "Who do you think is the worst dressed person here?",
                "True or false? You have a crush on {name}.",
                "Of the people here, who do you want to trade lives with?",
                "Did you have an imaginary friend growing up?",
                "Do you cover your eyes during a scary parts of a movie?",
                "Have you ever practiced kissing in a mirror?",
                "Did your parents ever give you the “birds and the bees” talk?",
                "What is your guilty pleasure?",
                "What is your worst habit?",
                "Have you ever walked into a wall?",
                "What was your most embarrassing moment in public?",
                "Do you ever talk to yourself in the mirror?",
                "You’re in a public restroom and just went #2, then you realized your stall has no toilet paper. What do you do?",
                "What would be in your web history that you’d be embarrassed if someone saw?",
                "Do you sleep with a stuffed animal?",
                "Do you drool in your sleep?",
                "Do you talk in your sleep?",
                "Who is your secret crush?",
                "Who do you like the least here and why?",
                "What is your go-to song for the shower?",
                "Who is the sexiest person in this room?",
                "How would you rate your looks on a scale of 1 to 10?",
                "Would you rather have sex with {name} in secret or not have sex with that person but everyone thinks you did?",
                "What don't you like about me?",
                "What color underwear are you wearing right now?",
                "If you were rescuing people from a burning building and you had to leave one person behind from here, who would it be?",
            ],
            "dares": [
                "Set your crush's profile picture as your profile picture.",
                "Flirt with {name} poorly in text and send screenshots of it to you.",
                "Send a screenshot of your search history of last 2 days.",
                "Send the most recent photo of your gallery.",
                "Send your ugliest selfie.",
                "Text flirt and then send “I love you” to a someone already in a relationship (not married) and screenshot his/her reaction",
                "Send a romantic message to someone of your own gender and screenshot their response",
                "Send a video of you dancing.",
                "Call me and sing a song for me.",
                "Send a voice message saying that you love me in 3 romantic ways.",
                "Send me a pic of you wearing the least clothes on you.",
                "Be my one day boyfriend or girlfriend.",
                "Write your and my name in your status for 1 day.",
                "Propose to me in the most sensual way possible.",
            ],
        }
        self.config.register_global(**default_global)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def truth(self, ctx, *, user: discord.Member):
        """Ask a truth question to users!"""

        # Set author
        author = ctx.message.author

        # Get and pick random string
        strings = await self.config.truths()
        mn = len(strings)
        rs = randint(0, mn - 1)

        # Get and pick random user
        mn2 = len(ctx.guild.members)
        rp = randint(0, mn2 - 1)
        name = ctx.guild.members[rp].mention

        # Build Embed
        embed = discord.Embed()
        embed.title = f"{author.name} asked {user.name}"
        embed.description = strings[rs].format(name=name)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def dare(self, ctx, *, user: discord.Member):
        """Dare someone!"""

        # Set author
        author = ctx.message.author

        # Get and pick random string
        strings = await self.config.dares()
        mn = len(strings)
        rs = randint(0, mn - 1)

        # Get and pick random user
        mn2 = len(ctx.guild.members)
        rp = randint(0, mn2 - 1)
        name = ctx.guild.members[rp].mention

        # Build Embed
        embed = discord.Embed()
        embed.title = f"{author.name} dared {user.name}"
        embed.description = strings[rs].format(name=name)
        await ctx.send(embed=embed)

