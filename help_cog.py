from discord.ext import commands
from pyfiglet import Figlet


class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open("Help_desc.txt", "r", encoding='utf-8') as file_help:
            self.help_message = file_help.read()
        self.text_channel_list = []

    # some debug info so that we know the bot has started
    @commands.Cog.listener()
    async def on_ready(self):
        # лучше используйте standard он вроде норм с таким текстом 'B o t  o n l i n e'
        # smisome1 еще вот этот шрифт прикольный
        text = Figlet(font='speed')
        print(text.renderText('Bot online'))

    @commands.command(name="help", help="Displays all the available commands")
    async def get_help(self, ctx):
        await ctx.send(self.help_message)

    async def send_to_all(self, msg):
        for text_channel in self.text_channel_list:
            await text_channel.send(msg)
