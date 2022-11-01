import discord
from discord.ext import commands


class TestCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="test")
    async def test(self, ctx):
        await ctx.send(f'Дарова {ctx.message.author.name}!')

    # просто тестовая функция на то что в ботом все ок
    @commands.command(name="foo")
    async def foo(self, ctx, *, arg=None):
        if arg is None:
            await ctx.send('Ну хоть что нибудь напиши, просто так не зови :\\')
        else:
            # 0x означает # то есть это HEX color, например 0x070365 = #070365, 0xcfbdf4 = #cfbdf4
            await ctx.send(embed=discord.Embed(description=arg, color=0xcfbdf4))

    @commands.command(name="resetprx")
    async def _reset_prx(self, ctx, *, arg=None):
        if arg is None:
            await ctx.send('ну хоть что нибудь напиши, просто так не зови :\\')
        else:
            self.bot.command_prefix = arg
            await ctx.send(f'Та даам, вот теперь префикс такой: {self.bot.command_prefix}')
