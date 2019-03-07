import discord
from redbot.core import commands, Config
from random import randint

BaseCog = getattr(commands, "Cog", object)


class ConversationGames(BaseCog):
    """Conversation games"""

    def __init__(self):
        self.config = Config.get_conf(self, identifier=763123)
        default_global = {
            "wyr": [
                "...always be 10 minutes late or always be 20 minutes early?",
                "...lose all of your money and valuables or all of the pictures you have ever taken?",
                "...be able to see 10 minutes into your own future or 10 minutes into the future of anyone but yourself?",
                "...be famous when you are alive and forgotten when you die or unknown when you are alive but famous after you die?",
                "...go to jail for 4 years for something you didn’t do or get away with something horrible you did but always live in fear of being caught?",
                "...accidentally be responsible for the death of a child or accidentally be responsible for the deaths of three adults?",
                "...your shirts be always two sizes too big or one size too small?",
                "...live in the wilderness far from civilization or live on the streets of a city as a homeless person?",
                "...the general public think you are a horrible person but your family be very proud of you or your family think you are a horrible person but the general public be very proud of you?",
                "...live your entire life in a virtual reality where all your wishes are granted or in the real world?",
                "...be alone for the rest of your life or always be surrounded by annoying people?",
                "...never use social media sites / apps again or never watch another movie or TV show?",
                "...have an easy job working for someone else or work for yourself but work incredibly hard?",
                "...be the first person to explore a planet or be the inventor of a drug that cures a deadly disease?",
                "...have a horrible short term memory or a horrible long term memory?",
                "...be completely invisible for one day or be able to fly for one day?",
                "...be locked in a room that is constantly dark for a week or a room that is constantly bright for a week?",
                "...be poor but help people or become incredibly rich by hurting people?",
                "...live without the internet or live without AC and heating?",
                "...have a horrible job, but be able to retire comfortably in 10 years or have your dream job, but have to work until the day you die?",
                "...find your true love or a suitcase with five million dollars inside?",
                "...be able to teleport anywhere or be able to read minds?",
                "...die in 20 years with no regrets or die in 50 years with many regrets?",
                "...be feared by all or loved by all?",
                "...be transported permanently 500 years into the future or 500 years into the past?",
                "...never be able to use a touchscreen or never be able to use a keyboard and mouse?",
                "...be able to control fire or water?",
                "...have everything you eat be too salty or not salty enough no matter how much salt you add?",
                "...have hands that kept growing as you got older or feet that kept growing as you got older?",
                "...be unable to use search engines or unable to use social media?",
                "...give up bathing for a month or give up the internet for a month?",
                "...donate your body to science or donate your organs to people who need them?",
                "...go back to age 5 with everything you know now or know now everything your future self will learn?",
                "...relive the same day for 365 days or lose a year of your life?",
                "...have a golden voice or a silver tongue?",
                "...be able to control animals (but not humans) with your mind or control electronics with your mind?",
                "...sell all of your possessions or sell one of your organs?",
                "...lose all of your memories from birth to now or lose your ability to make new long term memories?",
                "...be infamous in history books or be forgotten after your death?",
                "...never have to work again or never have to sleep again (you won’t feel tired or suffer negative health effects)?",
                "...be beautiful / handsome but stupid or intelligent but ugly?",
                "...get one free round trip international plane ticket every year or be able to fly domestic anytime for free?",
                "...be balding but fit or overweight with a full head of hair?",
                "...be able to be free from junk mail or free from email spam for the rest of your life?",
                "...be fluent in all languages and never be able to travel or be able to travel anywhere for a year but never be able to learn a word of a different language?",
                "...have an unlimited international first class ticket or never have to pay for food at restaurants?",
                "...see what was behind every closed door or be able to guess the combination of every safe on the first try?",
                "...live in virtual reality where you are all powerful or live in the real world and be able to go anywhere but not be able to interact with anyone or anything?",
                "...never be able to eat meat or never be able to eat vegetables?",
                "...give up watching TV / movies for a year or give up playing games for a year?",
                "...always be able to see 5 minutes into the future or always be able to see 100 years into the future?",
                "...super sensitive taste or super sensitive hearing?",
                "...be a practicing doctor or a medical researcher?",
                "...be married to a 10 with a bad personality or a 6 with an amazing personality?",
                "...never be able to drink sodas like coke again or only be able to drink sodas and nothing else?",
                "...be a reverse centaur or a reverse mermaid/merman?",
                "...have constantly dry eyes or a constant runny nose?",
                "...be a famous director or a famous actor?",
                "...not be able to open any closed doors (locked or unlocked) or not be able to close any open doors?",
                "...give up all drinks except for water or give up eating anything that was cooked in an oven?",
                "...have to read aloud every word you read or sing everything you say out loud?",
                "...have whatever you are thinking appear above your head for everyone to see or have absolutely everything you do live streamed for anyone to see?",
                "...be put in a maximum security federal prison with the hardest of the hardened criminals for one year or be put in a relatively relaxed prison where wall street types are held for ten years?",
                "...have a clown only you can see that follows you everywhere and just stands silently in a corner watching you without doing or saying anything or have a real life stalker who dresses like the Easter bunny that everyone can see?",
                "...kill one innocent person or five people who committed minor crimes?",
                "...have a completely automated home or a self-driving car?",
                "...work very hard at a rewarding job or hardly have to work at a job that isn’t rewarding?",
                "...be held in high regard by your parents or your friends?",
                "...be an amazing painter or a brilliant mathematician?",
                "...be reincarnated as a fly or just cease to exist after you die?",
                "...be able to go to any theme park in the world for free for the rest of your life or eat for free at any drive through restaurant for the rest of your life?",
                "...be only able to watch the few movies with a rotten tomatoes score of 95-100% or only be able to watch the majority of movies with a rotten tomatoes score of 94% and lower?",
                "...never lose your phone again or never lose your keys again?",
                "...have one real get out of jail free card or a key that opens any door?",
                "...have a criminal justice system that actually works and is fair or an administrative government that is free of corruption?",
                "...have real political power but be relatively poor or be ridiculously rich and have no political power?",
                "...have the power to gently nudge anyone’s decisions or have complete puppet master control of five people?",
                "...have everyone laugh at your jokes but not find anyone else’s jokes funny or have no one laugh at your jokes but you still find other people’s jokes funny?",
                "...be the absolute best at something that no one takes seriously or be well above average but not anywhere near the best at something well respected?",
                "...lose the ability to read or lose the ability to speak?",
                "...live under a sky with no stars at night or live under a sky with no clouds during the day?",
                "...humans go to the moon again or go to mars?",
                "...never get angry or never be envious?",
                "...have free Wi-Fi wherever you go or be able to drink unlimited free coffee at any coffee shop?",
                "...be compelled to high five everyone you meet or be compelled to give wedgies to anyone in a green shirt?",
                "...live in a house with see-through walls in a city or in the same see-though house but in the middle of a forest far from civilization?",
                "...take amazing selfies but all of your other pictures are horrible or take breathtaking photographs of anything but yourself?",
                "...use a push lawn mower with a bar that is far too high or far too low?",
                "...be able to dodge anything no matter how fast it’s moving or be able ask any three questions and have them answered accurately?",
            ],
            "nhie": [
                "...watched the Ghostbusters remake.",
                "...wanted to be one of the Kardashians.",
                "...dressed as the opposite sex.",
                "...watched Spongebob Squarepants.",
                "...cried during a Pixar movie.",
                "...had a crush, or man crush, on Ron Swanson.",
                "...'cleaned up' by piling everything into a closet.",
                "...sung karaoke.",
                "...watched the 'Gangnam Style' music video.",
                "...had a crush on someone from 'Full House'.",
                "...watched an episode of 'Gilmore Girls'.",
                "...pretended to know a stranger.",
                "...worn sleepwear and pretended it was clothing.",
                "...said 'excuse me' when there was no one around.",
                "...scared myself in a mirror.",
                "...missed a high five.",
                "...heard someone else doing it.",
                "...sang in the shower.",
                "...blamed farts on an animal.",
                "...secretly wished I were a wizard at Hogwarts.",
                "...slept in regular clothing.",
                "...had a nightmare about zombies chasing me.",
                "...pretended to laugh at a joke I didn't get.",
                "...been scared of clowns.",
                "...thought a cartoon character was hot.",
                "...faked being sick so I could play video games.",
                "...liked Star Wars more than Star Trek.",
                "...tried out to be an extra in a movie.",
                "...scored over 100 while bowling.",
                "...used an Instant Pot.",
                "...played Candy Crush.",
                "...won a game of Scrabble.",
                "...made a duck face when taking a selfie.",
                "...looked out the car's passenger seat window and imagined it was a scene from a music video.",
                "...actually laughed out loud when typing 'lol'.",
                "...reread an email immediately after sending it.",
                "...daydreamed about being on a talk show and what I'd talk about.",
                "...Googled my own name to see what comes up.",
                "...pretended I was running from zombies while on a run.",
                "...sat in the shower.",
                "...tried something I saw on Pinterest.",
                "...ugly cried for no reason.",
                "...creeped on someone I just met on social media.",
                "...thought about how a loved one could identify me if my face was horribly disfigured in an accident.",
                "...answered someone 'left' or 'right' without thinking, because I have a 50/50 chance of being right.",
                "...been out of the country.",
                "...regifted a gift card.",
                "...traveled out of state by myself.",
                "...flown in a helicopter.",
                "...been on stage in front of a crowd.",
                "...lied in a job interview.",
                "...stalked a crush.",
                "...sung karaoke.",
                "...agreed with something Donald Trump said.",
                "...thought about what type of dog I would be.",
                "...watched children's cartoons I'm too old for.",
                "...lost sunglasses that I was already wearing.",
                "...locked my keys in my car.",
                "...not tipped at a restaurant.",
                "...given money to a homeless person.",
                "...tried to look at the sun.",
                "...bungee-jumped.",
                "...had surgery.",
                "...jumped out of a plane.",
                "...made a wish at a fountain.",
                "...accidentally eaten a bug.",
                "...cut someone in line.",
                "...stayed up all night.",
                "...read a single Harry Potter book.",
                "...been inside of a library.",
                "...lied about my age.",
                "...shot a gun.",
                "...had a cavity.",
                "...been mini golfing.",
                "...seen an elephant in real life.",
                "...been to Disney World.",
                "...bought clothing online.",
                "...had someone draw a caricature of me.",
                "...owned an Xbox.",
                "...spent hours watching funny videos on Youtube.",
                "...seen Titanic.",
                "...met a celebrity.",
                "...thought a movie was better than the book.",
                "...voted.",
                "...owned a watch.",
                "...ridden a skateboard.",
                "...learned how to play a musical instrument.",
                "...seen snow.",
                "...finished a Sudoku puzzle.",
                "...Googled something so I'd know how to spell it.",
                "...cheated on a test.",
                "...cried watching Homeward Bound.",
                "...licked a frozen pole.",
                "...had gum in my hair.",
                "...taken a horrible picture on picture day.",
                "...been a bully.",
                "...wanted to be a superhero.",
                "...been scared of the dark.",
                "...had trouble sleeping after watching a scary movie.",
                "...stayed up all night.",
                "...been to a sleepover.",
                "...had a birthday party.",
                "...cried at school.",
                "...sang on a stage.",
                "...performed in a talent show.",
                "...killed ants with a magnifying glass.",
                "...dropped Mentos into Coke or Pepsi.",
                "...eaten something on a dare.",
                "...used the excuse 'my dog ate my homework'.",
                "...sucked my thumb.",
                "...believed my toys had feelings.",
                "...watched Blue's Clues.",
                "...been terrified of a theme park ride.",
                "...been to a haunted house.",
                "...dressed up as a zombie for Halloween.",
                "...been sent to the principle's office.",
                "...done an Easter Egg Hunt.",
                "...built a fort with blankets.",
                "...fallen off a bike.",
                "...played video games all day.",
                "...stolen money from a sibling's piggy bank.",
                "...wished I had bunk beds.",
                "...played Pokemon.",
                "...been on a family road trip.",
                "...named a stuffed animal.",
                "...used training wheels.",
                "...eaten only candy for dinner.",
                "...stayed in character all day.",
                "...lied about being related to someone on tv.",
                "...written notes on the desk to use during a test.",
                "...tried to sign a permission slip for my parents.",
                "...stolen a friend's story and pretend it happened to me.",
                "...thrown something out of the school bus window.",
                "...lied about staying after school and went somewhere else.",
                "...hopped seats on the school bus.",
                "...accidentally sharted.",
                "...forgotten the punchline of a joke.",
                "...sang a song out loud and messed the lyrics.",
                "...walked in on someone in the bathroom.",
                "...had someone walk in on me in the bathroom.",
                "...sent a text to the wrong person.",
                "...tried to pass a silent fart, but it came out loud instead.",
                "...tripped in public.",
                "...wet the bed after childhood.",
                "...accidentally pooped my pants.",
                "...attempted martial arts moves while by myself.",
                "...drove over a curb.",
                "...mistaken a man for a women or vice versa.",
                "...laughed so hard, I peed my pants.",
                "...picked a wedgie in public.",
                "...called the wrong person, but pretended I meant to call them.",
                "...gone into the wrong restroom.",
                "...been so freaked to be outside at night, that I ran back in.",
                "...lost my swimwear bottoms.",
                "...had diarrhea at a friend's house.",
                "...broken a piece of furniture by sitting on it.",
                "...arrived somewhere late and had everyone staring at me.",
                "...had food stuck in my teeth all day.",
                "...walked around with my zipper down.",
                "...bought a children's toy for myself, as an adult.",
                "...recorded video of myself singing or dancing.",
                "...been caught picking my nose.",
                "...gotten something stuck in my nose.",
                "...greeted someone I thought was someone else.",
            ],
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
                "Do you ever try to solve the problems between your best friend and his/her crush?",
                "Do you ever apply makeup without using the mirror?",
                "Have you ever admired your best friend if he/she get good marks in the examination?",
                "Have you ever tried to sing a tongue twister in a musical way?",
                "Tell me your weirdest habit.",
                "Do you like parties?",
                "Do you have crush on any of your school teachers?",
                "Who is the most annoying person among your friends?",
                "Do you go directly to your home after college in the evening?",
                "How many boyfriends/girlfriends have you had?",
                "Suppose you were a billionaire, how would you spend your time?",
                "If your parents forced you to leave home, where would you go?",
                "If you wanted to start your own business, what it would be?",
                "Have you ever had the crush on someone much younger or older than you? What’s the biggest age difference?",
                "When was the last time you touched yourself?",
                "How many hours do you exercise a day?",
                "Did you ever farted in an elevator and get caught?",
                "What do you think when you are sitting on the commode?",
                "Who is the worst kisser you have ever kissed and why?",
                "What is your favorite villain character?",
                "Have you ever wanted to try BDSM?",
                "Do you like when I act or talk dirty to you?",
                "Do you like having it in the morning or evening?",
                "Have you ever done it with your teacher?",
                "Have you ever flirted with your teacher in the school for good marks and grades?",
                "Have you ever laughed out when doing it and what is the reason?",
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
                "Send love letter through email to your class teacher.",
                "Select one mobile number blindfolded from your contacts and send one breakup message to him/her. Screenshot the response.",
                "Give a deep explanation of one item in front of you.",
                "Paint your fingernails blindfolded with a pencil. Show us the result.",
                "Do a prank call to your mother and tell “I’m expecting a baby soon”. Screenshot the response.",
                "Send me the last message you received from your crush.",
                "Make a voice call to me and sing rhymes.",
                "Make a video call to me and perform belly dance.",
                "Open your gallery, close your eyes, scroll randomly and select one picture and send it to me.",
                "Send a text message to your crush blindfolded.",
                "Put my picture as your mobile wallpaper for three days.",
                "Send a selfie of yours while keeping your finger in your nose.",
                "Call to any random number and do non-stop conversation for 2 minutes.",
                "Send me the message of your first message that sends to me.",
                "Make a video call to me and do 20 situps continuously.",
                "Send next five text messages to your friends using your elbow only.",
                "Wear your dress upside down and send that picture to me.",
                "Send any message using only emojis.",
                "Call someone and say nothing.",
                "Send a message to your crush saying I’ve lost my condoms in your home please find them.",
                "Send five photo from your gallery.",
                "I’ll give you a person's contact information and send a romantic message to that person.",
            ],
        }
        self.config.register_global(**default_global)

    @commands.command(aliases=["wyr"])
    @commands.bot_has_permissions(embed_links=True)
    async def wouldyourather(self, ctx):
        """Would you rather?"""

        strings = await self.config.wyr()
        mn = len(strings)
        i = randint(0, mn - 1)

        # Build Embed
        embed = discord.Embed()
        embed.title = "Would you rather.."
        embed.description = strings[i]
        await ctx.send(embed=embed)

    @commands.command(aliases=["nhie"])
    @commands.bot_has_permissions(embed_links=True)
    async def neverhaveiever(self, ctx):
        """Never have I"""

        strings = await self.config.nhie()
        mn = len(strings)
        i = randint(0, mn - 1)

        # Build Embed
        embed = discord.Embed()
        embed.title = "Never have I ever.."
        embed.description = strings[i]
        await ctx.send(embed=embed)

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
