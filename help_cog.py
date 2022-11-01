import json
import os
import discord
from discord.ext import commands
from pyfiglet import Figlet


class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.JSON_FILE = str(os.path.dirname(os.path.realpath(__file__))) + '\\data.json'
        self.data = self.get_data_from_json_file()

        with open("help_desc.txt", "r", encoding='utf-8') as file_help:
            self.help_message = file_help.read()

        self.text_channel_list = []

    @commands.command(name="help", help="Displays all the available commands")
    async def get_help(self, ctx):
        await ctx.send(self.help_message)

    async def send_to_all(self, msg):
        for text_channel in self.text_channel_list:
            await text_channel.send(msg)

    @commands.Cog.listener()
    async def on_ready(self):
        """ Runs once the bot has established a connection with Discord """
        # print(self.get_data_from_json_file())
        print(f'{self.bot.user.name} has connected to Discord')

        # check if bot has connected to guilds
        if len(self.bot.guilds) > 0:
            print('connected to the following guilds:')

            # list guilds
            for guild in self.bot.guilds:
                # display guild name, id and member count
                print(f'* {guild.name} #{guild.id}, member count: {len(guild.members)}')
                # update the member count
                await self.update_member_bot_count_channel_name(guild)

        # лучше используйте standard он вроде норм с таким текстом 'B o t  o n l i n e'
        # smisome1 еще вот этот шрифт прикольный
        text = Figlet(font='speed')
        print(text.renderText('Bot online'))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """ gets triggered when a new member joins a guild """
        print(f"* {member} joined {member.guild}")
        await self.update_member_bot_count_channel_name(member.guild)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """ gets triggered when a new member leaves or gets removed from a guild """
        print(f"* {member} left {member.guild}")
        await self.update_member_bot_count_channel_name(member.guild)

    @commands.command(name="update")
    async def on_update_cmd(self, ctx):
        """ triggers manual update of member count channel """
        print(f"* {ctx.author} issued update")
        await self.update_member_bot_count_channel_name(ctx.guild)

    async def update_member_bot_count_channel_name(self, guild):
        """ updates the name of the member count channel """
        member_count_channel_id = self.get_guild_member_count_channel_id(guild)
        member_count_suffix = self.get_guild_member_count_suffix(guild)

        bot_count_channel_id = self.get_guild_bot_count_channel_id(guild)
        bot_count_suffix = self.get_guild_bot_count_suffix(guild)

        if member_count_channel_id is not None and member_count_suffix is not None:
            member_count_channel = discord.utils.get(guild.channels, id=member_count_channel_id)
            new_name = f"{member_count_suffix}: {HelpCog.get_guild_count(guild)[0]}"
            await member_count_channel.edit(name=new_name)

        if bot_count_channel_id is not None and bot_count_suffix is not None:
            bot_count_channel = discord.utils.get(guild.channels, id=bot_count_channel_id)
            new_name = f"{bot_count_suffix}: {HelpCog.get_guild_count(guild)[1]}"
            await bot_count_channel.edit(name=new_name)

        else:
            print(f"* could not update member count channel for {guild}, id not found in {self.JSON_FILE}")

    @staticmethod
    def get_guild_count(guild):
        count_members = 0
        count_bots = 0
        for member in guild.members:
            if not member.bot:
                count_members += 1
            else:
                count_bots += 1
        return [count_members, count_bots]

    def get_data_from_json_file(self):
        with open(self.JSON_FILE, encoding='utf-8') as json_file:
            return json.load(json_file)

    def get_guild_bot_count_channel_id(self, guild):
        for data_guild in self.data['guilds']:
            if int(data_guild['id']) == guild.id:
                return data_guild['channel_id_bots']

            return None

    def get_guild_member_count_channel_id(self, guild):
        for data_guild in self.data['guilds']:
            if int(data_guild['id']) == guild.id:
                return data_guild['channel_id_members']

            return None

    def get_guild_member_count_suffix(self, guild):
        for data_guild in self.data['guilds']:
            if int(data_guild['id']) == guild.id:
                return data_guild['suffix_members']

            return None

    def get_guild_bot_count_suffix(self, guild):
        for data_guild in self.data['guilds']:
            if int(data_guild['id']) == guild.id:
                return data_guild['suffix_bots']

            return None
