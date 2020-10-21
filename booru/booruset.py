import discord
from redbot.core import Config, checks, commands
from redbot.core.utils.menus import menu, commands, DEFAULT_CONTROLS
import aiohttp
import contextlib

class Booruset:

    # TODO : Use Red internals
    @commands.group()
    @checks.admin_or_permissions()
    async def booruset(self, ctx):
        """Settings for booru \n\n
        These filter whatever you add *out* of the search results, it does not add anything.
        This is because the filters are applied locally instead of in the API to avoid reaching the
        maximum amount of tags given by these APIs."""
        pass

    # Guild configs
    @booruset.group(name="guild")
    @checks.admin_or_permissions(manage_guild=True)
    async def _guild(self, ctx):
        """Guild Settings for booru"""
        pass

    @_guild.group(name="all")
    @checks.admin_or_permissions(manage_guild=True)
    async def _guild_allfilters(self, ctx):
        """Commands pertaining to all filters which apply on the guild"""
        pass

    @_guild_allfilters.command(name="show")
    @checks.admin_or_permissions(manage_guild=True)
    async def _guild_allfilters_show(self, ctx):
        """Filters that apply to all guild queries"""
        filters = await self.config.guild(ctx.guild).filters()
        await self.generic_show(ctx, filters)

    @_guild.group(name="simple", autohelp=False)
    @checks.admin_or_permissions(manage_guild=True)
    async def _guild_simple(self, ctx):
        """Give out only a picture with no reactions or other information, as simple as can be!"""

        toggle_status = await self.config.guild(ctx.guild).simple()

        if toggle_status == "on":
            await self.config.guild(ctx.guild).simple.set("off")
            await ctx.send("Simple booru now off! Get all the fancy menus!")
        if toggle_status == "off":
            await self.config.guild(ctx.guild).simple.set("on")
            await ctx.send("Simple booru now on, plain and simple!")

    @_guild.group(name="weebmode", autohelp=False)
    @checks.admin_or_permissions(manage_guild=True)
    async def _guild_weebmode(self, ctx):
        """Give out only weeb-related sources!"""

        toggle_status = await self.config.guild(ctx.guild).weebmode()

        if toggle_status == "on":
            await self.config.guild(ctx.guild).weebmode.set("off")
            await ctx.send("Weebmode now off! Get that IRL!")
        if toggle_status == "off":
            await self.config.guild(ctx.guild).weebmode.set("on")
            await ctx.send("Weebmode now on, all the anime!")

    @_guild.group(name="onlynsfw", autohelp=False)
    @checks.admin_or_permissions(manage_guild=True)
    async def _guild_onlynsfw(self, ctx):
        """Only post in nsfw channels"""

        toggle_status = await self.config.guild(ctx.guild).onlynsfw()

        if toggle_status == "on":
            await self.config.guild(ctx.guild).onlynsfw.set("off")
            await ctx.send("You can use booru as normal!")
        if toggle_status == "off":
            await self.config.guild(ctx.guild).onlynsfw.set("on")
            await ctx.send("You can only use it in nsfw channels!")

    @_guild_allfilters.command(name="add")
    @checks.admin_or_permissions(manage_guild=True)
    async def _guild_allfilters_add(self, ctx, *, filter):
        """Add guild filters"""

        # Load config
        config_filters = await self.config.guild(ctx.guild).filters()

        origin = ["all"]
        await self.generic_add(ctx, origin, config_filters, filter)

    @_guild_allfilters.command(name="remove")
    @checks.admin_or_permissions(manage_guild=True)
    async def _guild_allfilters_remove(self, ctx, *, filter):
        """Remove guild filters"""

        # Load config
        config_filters = await self.config.guild(ctx.guild).filters()

        origin = ["all"]
        await self.generic_remove(ctx, origin, config_filters, filter)

    @_guild.group(name="nsfw")
    @checks.admin_or_permissions(manage_guild=True)
    async def _guild_nsfwfilters(self, ctx):
        """Commands pertaining to guild NSFW filters which apply on the guild"""
        pass

    @_guild_nsfwfilters.command(name="show")
    @checks.admin_or_permissions(manage_guild=True)
    async def _guild_nsfwfilters_show(self, ctx):
        """Show global nsfw filters"""

        filters = await self.config.guild(ctx.guild).nsfw_filters()
        await self.generic_show(ctx, filters)

    @_guild_nsfwfilters.command(name="add")
    @checks.admin_or_permissions(manage_guild=True)
    async def _guild_nsfwfilters_add(self, ctx, *, filter):
        """Add guild nsfw filters"""

        # Load config
        config_filters = await self.config.guild(ctx.guild).nsfw_filters()

        origin = ["nsfw"]
        await self.generic_add(ctx, origin, config_filters, filter)

    @_guild_nsfwfilters.command(name="remove")
    @checks.admin_or_permissions(manage_guild=True)
    async def _guild_nsfwfilters_remove(self, ctx, *, filter):
        """Remove guild nsfw filters"""

        # Load config
        config_filters = await self.config.guild(ctx.guild).nsfw_filters()

        origin = ["nsfw"]
        await self.generic_remove(ctx, origin, config_filters, filter)

    # Global configs
    @booruset.group(name="global")
    @checks.is_owner()
    async def _global(self, ctx):
        """Global Settings for booru"""
        pass

    @_global.group(name="all")
    @checks.is_owner()
    async def _global_allfilters(self, ctx):
        """Commands pertaining to all filters which apply globally"""
        pass

    @_global_allfilters.command(name="show")
    @checks.is_owner()
    async def _global_allfilters_show(self, ctx):
        """Show current global filters which apply to all queries"""
        filters = await self.config.filters()
        await self.generic_show(ctx, filters)

    @_global_allfilters.command(name="add")
    @checks.is_owner()
    async def _global_allfilters_add(self, ctx, *, filter):
        """Add global filters"""

        # Load config
        config_filters = await self.config.filters()

        origin = ["global", "all"]
        await self.generic_add(ctx, origin, config_filters, filter)

    @_global_allfilters.command(name="remove")
    @checks.is_owner()
    async def _global_allfilters_remove(self, ctx, *, filter):
        """Remove global nsfw filters"""

        # Load config
        config_filters = await self.config.filters()

        origin = ["global", "all"]
        await self.generic_remove(ctx, origin, config_filters, filter)

    @_global.group(name="nsfw")
    @checks.is_owner()
    async def _global_nsfwfilters(self, ctx):
        """Commands pertaining to NSFW filters which apply globally"""
        pass

    @_global_nsfwfilters.command(name="show")
    @checks.is_owner()
    async def _global_nsfwfilters_show(self, ctx):
        """Show global nsfw filters"""
        filters = await self.config.nsfw_filters()
        await self.generic_show(ctx, filters)

    @_global_nsfwfilters.command(name="add")
    @checks.is_owner()
    async def _global_nsfwfilters_add(self, ctx, *, filter):
        """Add global nsfw filters"""

        # Load config
        config_filters = await self.config.nsfw_filters()

        origin = ["global", "nsfw"]
        await self.generic_add(ctx, origin, config_filters, filter)

    @_global_nsfwfilters.command(name="remove")
    @checks.is_owner()
    async def _global_nsfwfilters_remove(self, ctx, *, filter):
        """Remove global nsfw filters"""

        # Load config
        config_filters = await self.config.nsfw_filters()

        origin = ["global", "nsfw"]
        await self.generic_remove(ctx, origin, config_filters, filter)

    async def generic_show(self, ctx, filters):
        if not filters:
            await ctx.send("There are currently no filters")
        else:
            await ctx.send(f"Current filters are: ```{','.join(filters)}```")

    async def generic_add(self, ctx, origin, config_filters, filter):

        filter = set(filter.split(" "))

        config_filters = set(config_filters)
        config_filters.update(filter)

        # Check variables to see where they come from and do the right thing
        if "all" in origin:
            await self.config.guild(ctx.guild).filters.set(list(config_filters))
        if "nsfw" in origin:
            await self.config.guild(ctx.guild).nsfw_filters.set(list(config_filters))
        if "all" in origin and "global" in origin:
            await self.config.filters.set(list(config_filters))
        if "nsfw" in origin and "global" in origin:
            await self.config.nsfw_filters.set(list(config_filters))
        await ctx.send("The filters have been added!")

    async def generic_remove(self, ctx, origin, config_filters, filter):

        filter = set(filter.split(" "))

        config_filters = set(config_filters)

        # Check variables to see where they come from and do the right thing
        if "all" in origin:
            await self.config.guild(ctx.guild).filters.set(list(set(config_filters) - set(filter)))
        if "nsfw" in origin:
            await self.config.guild(ctx.guild).nsfw_filters.set(list(set(config_filters) - set(filter)))
        if "all" in origin and "global" in origin:
            await self.config.filters.set(list(set(config_filters) - set(filter)))
        if "nsfw" in origin and "global" in origin:
            await self.config.nsfw_filters.set(list(set(config_filters) - set(filter)))
        await ctx.send("The filters have been removed!")

    @_guild.group(name="boards")
    @checks.admin_or_permissions(manage_guild=True)
    async def _guild_boards(self, ctx):
        """Commands pertaining to which boards are shown in booru"""
        pass

    @_guild_boards.command(name="show")
    @checks.admin_or_permissions(manage_guild=True)
    async def _guild_boards_show(self, ctx):
        """Show booru boards"""
        boards = await self.config.guild(ctx.guild).boards()
        if not boards:
            await ctx.send("There are currently no boards shown in booru")
        else:
            await ctx.send(f"Current boards shown in booru are: ```{','.join(boards)}```")

    @_guild_boards.command(name="add")
    @checks.admin_or_permissions(manage_guild=True)
    async def _guild_boards_add(self, ctx, *, boards):
        """Add image boards to booru"""

        # Load config
        config_boards = await self.config.guild(ctx.guild).boards()

        # Filter input
        boards = await self.boards_filter(boards)
        if boards is None:
            board_names_string = ""
            for board in self.board_names:
                board_names_string += f" {board},"
            await ctx.send(f"Reminder that the board names that can be used are {board_names_string}. Please try again")
            return
        else:
            for board in boards:
                if board not in self.board_names:
                    board_names_string = ""
                    for board in self.board_names:
                        board_names_string += f" {board},"
                    await ctx.send(f"Reminder that the board names that can be used are {board_names_string}. Please try again")
                    return

        # Fuse input and config
        config_boards = set(config_boards)
        config_boards.update(boards)

        # Set new config
        await self.config.guild(ctx.guild).boards.set(list(config_boards))
        await ctx.send("The boards have been added.")

    @_guild_boards.command(name="remove")
    @checks.admin_or_permissions(manage_guild=True)
    async def _guild_boards_remove(self, ctx, *, boards):
        """Remove image boards to booru"""

        # Load config
        config_boards = await self.config.guild(ctx.guild).boards()

        # Filter input
        boards = await self.boards_filter(boards)
        if boards is None:
            board_names_string = ""
            for board in self.board_names:
                board_names_string += f" {board},"
            await ctx.send(f"Reminder that the board names that can be used are {board_names_string}. Please try again")
            return
        else:
            for board in boards:
                if board not in self.board_names:
                    for board in self.board_names:
                        board_names_string += f" {board},"
                    await ctx.send(f"Reminder that the board names that can be used are {board_names_string}. Please try again")

        # Set new config
        config_boards = set(config_boards)
        await self.config.guild(ctx.guild).boards.set(list(set(config_boards) - set(boards)))
        await ctx.send("The boards have been removed.")

    async def boards_filter(self, boards):

        boards = set(boards.split(" "))

        # Check if good
        if boards & set(self.board_names):
            return boards
        else:
            return

    # Channel configs
    @booruset.group(name="channel")
    @checks.admin_or_permissions(manage_guild=True)
    async def _channel(self, ctx):
        """Channel Settings for booru"""
        pass

    @_channel.group(name="boards")
    @checks.admin_or_permissions(manage_guild=True)
    async def _channel_boards(self, ctx):
        """Commands pertaining to which boards are shown in booru"""
        pass

    @_channel.group(name="simple", autohelp=False)
    @checks.admin_or_permissions(manage_guild=True)
    async def _channel_simple(self, ctx):
        """Give out only a picture with no reactions or other information, as simple as can be!"""

        toggle_status = await self.config.guild(ctx.channel).simple()

        if toggle_status == "on":
            await self.config.guild(ctx.channel).simple.set("off")
            await ctx.send("Simple booru now off! Get all the fancy menus!")
        if toggle_status == "off":
            await self.config.guild(ctx.channel).simple.set("on")
            await ctx.send("Simple booru now on, plain and simple!")

    @_channel.group(name="weebmode", autohelp=False)
    @checks.admin_or_permissions(manage_guild=True)
    async def _channel_weebmode(self, ctx):
        """Give out only weeb-related sources!"""

        toggle_status = await self.config.guild(ctx.channel).weebmode()

        if toggle_status == "on":
            await self.config.guild(ctx.channel).weebmode.set("off")
            await ctx.send("Weebmode now off! Get that IRL!")
        if toggle_status == "off":
            await self.config.guild(ctx.channel).weebmode.set("on")
            await ctx.send("Weebmode now on, all the anime!")

    @_channel_boards.command(name="show")
    @checks.admin_or_permissions(manage_guild=True)
    async def _channel_boards_show(self, ctx):
        """Show booru boards"""
        boards = await self.config.channel(ctx.channel).boards()
        if not boards:
            await ctx.send("There are currently no boards shown in booru")
        else:
            await ctx.send(f"Current boards shown in booru are: ```{','.join(boards)}```")

    @_channel_boards.command(name="add")
    @checks.admin_or_permissions(manage_guild=True)
    async def _channel_boards_add(self, ctx, *, boards):
        """Add image boards to booru"""

        # Load config
        config_boards = await self.config.channel(ctx.channel).boards()

        # Filter input
        boards = await self.boards_filter(boards)
        if boards is None:
            board_names_string = ""
            for board in self.board_names:
                board_names_string += f" {board},"
            await ctx.send(f"Reminder that the board names that can be used are {board_names_string}. Please try again")
            return
        else:
            for board in boards:
                if board not in self.board_names:
                    for board in self.board_names:
                        board_names_string += f" {board},"
                    await ctx.send(f"Reminder that the board names that can be used are {board_names_string}. Please try again")

        # Fuse input and config
        config_boards = set(config_boards)
        config_boards.update(boards)

        # Set new config
        await self.config.channel(ctx.channel).boards.set(list(config_boards))
        await ctx.send("The boards have been added.")

    @_channel_boards.command(name="remove")
    @checks.admin_or_permissions(manage_guild=True)
    async def _channel_boards_remove(self, ctx, *, boards):
        """Remove image boards to booru"""

        # Load config
        config_boards = await self.config.channel(ctx.channel).boards()

        # Filter input
        boards = await self.boards_filter(boards)
        if boards is None:
            board_names_string = ""
            for board in self.board_names:
                board_names_string += f" {board},"
            await ctx.send(f"Reminder that the board names that can be used are {board_names_string}. Please try again")
            return
        else:
            for board in boards:
                if board not in self.board_names:
                    for board in self.board_names:
                        board_names_string += f" {board},"
                    await ctx.send(f"Reminder that the board names that can be used are {board_names_string}. Please try again")

        # Set new config
        config_boards = set(config_boards)
        await self.config.channel(ctx.channel).boards.set(list(set(config_boards) - set(boards)))
        await ctx.send("The boards have been removed.")     
