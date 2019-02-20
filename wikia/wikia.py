import discord
from redbot.core import commands
import aiohttp
from redbot.core.utils.predicates import ReactionPredicate, MessagePredicate
from redbot.core.utils.menus import start_adding_reactions

BaseCog = getattr(commands, "Cog", object)

class Wikia(BaseCog):
    """Search wikia"""

    @commands.command(pass_context=True)
    async def wikia(self, ctx, *, subdomain):
        """Search wikia subdomain then bot will ask you which article you want to consult"""

        # the command starts by searching the subdomain the user entered
        subdomains = await self.search_wikiadomains(subdomain)

        # Verify how many subdomains the search returned.
        # if there is more than one domain, the user will be prompted
        # to select which one to use before continuing
        wikia_domain = ""
        if len(subdomains) == 0:
            await ctx.send("No subdomain found. Aborting.")
            return
        elif len(subdomains) == 1:
            wikia_domain = subdomains[0]['domain']
        else:
            data = ["{number} - {title} - ({subdomain})".format(number=i+1, title=subdomains[i]['name'], subdomain=subdomains[i]['domain']) for i in range(0, len(subdomains))]
            msg = await ctx.send("\n".join(["Multiple results found. Pick one:",] + data))
            check = lambda m: m.content.isdigit() and int(m.content) in range(1, len(subdomains) + 1)

            # React Menu
            start_adding_reactions(msg, ReactionPredicate.NUMBER_EMOJIS)
            emojis = ReactionPredicate.NUMBER_EMOJIS
            pred = ReactionPredicate.with_emojis(emojis, msg)
            await ctx.bot.wait_for("reaction_add", check=pred)

            entry = subdomains[int(pred.result)]
            wikia_domain = entry['domain']

        message = await ctx.send(content = "Enter the wikia article for domain " + wikia_domain + ":", delete_after = 10)
        resp = await ctx.bot.wait_for("message", check=MessagePredicate.same_context(ctx))

        await self.wikiasearch(ctx, wikia_domain.split(".")[0], resp.content)

    async def wikiasearch(self, ctx, wikia_domain, wikia_entry):
        """Receives a wikia domain and a searched article.
        Will search articles for the selected domain and prompt the user if more than one is found.
        Selected article will be shown to the user.
        """

        query_string = wikia_entry.replace(' ', '+')
        data = None

        # Queries api to search an article
        headers = {'content-type': 'application/json'}
        async with aiohttp.ClientSession() as session:
            async with session.post("https://" + str(wikia_domain) + ".wikia.com/api/v1/Search/List/?query=" + query_string + "&namespaces=0%2C14&limit=10", headers=headers) as response:
                data = await response.json()

        if not 'items' in data.keys() or len(data['items']) == 0:
           await ctx.send("No results")
        else:
            if len(data['items']) == 1:
               entry = data['items'][0]
               wikia_id = entry['id']
               await self.show_wikia(wikia_id)
            else:
               medias = data['items']
               msg = "**Please choose one by giving its number.**\n"
               for i in range(0, len(medias)):
                   msg += "\n{number} - {title}".format(number=i+1, title=medias[i]['title'])

               message = await ctx.send(msg)

               check = lambda m: m.content.isdigit() and int(m.content) in range(1, len(medias) + 1)
               resp = await ctx.bot.wait_for("message", check=MessagePredicate.same_context(ctx))

               entry = medias[int(resp.content)-1]
               wikia_id = entry['id']
               await self.show_wikia(ctx, wikia_domain, wikia_id)

    async def show_wikia(self, ctx, wikia_domain, wikia_id):
        """Receive the wikia domain and the id of the article to display
        Will build a discord embed and show it in the channel"""

        data = None

        # Queries api to get information about article
        headers = {'content-type': 'application/json'}
        async with aiohttp.ClientSession() as session:
            async with session.get("https://" + str(wikia_domain) + ".wikia.com/api/v1/Articles/Details?abstract=300&ids=" + str(wikia_id), headers=headers) as response:
                data = await response.json()

        print(data)
        selected_wikia = data['items'][str(wikia_id)]

        # Build Embed
        embed = discord.Embed()
        embed.title = selected_wikia['title']
        embed.url = "http://{}.wikia.com{}".format(wikia_domain, selected_wikia['url'])
        if selected_wikia['thumbnail'] is not None:
           embed.set_thumbnail(url=selected_wikia['thumbnail'])
        if selected_wikia['abstract'] != "":
           embed.description = selected_wikia['abstract']
        embed.set_footer(text="Powered by wikia")
        await ctx.send(embed=embed)

    async def search_wikiadomains(self, subdomain_entry):
        """Receive a search query for a subdomain from the user
        Will search subdomains matching the query and return results in an array"""
        query_string = subdomain_entry.replace(' ', '+')

        # Queries api to search wikia subdomains
        headers = {'content-type': 'application/json'}
        async with aiohttp.ClientSession() as session:
            async with session.post("http://www.wikia.com/api/v1/Wikis/ByString/?string=" + query_string + "&limit=10&batch=1&lang=en", headers=headers) as response:
                data = await response.json()
                return data['items']

