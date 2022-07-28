import discord
from discord.ext import commands


class TestCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="test")
    async def test(self, ctx):
        await ctx.send(f'дарова {ctx.message.author.name}!')

    # просто тестовая функция на то что в ботом все ок
    @commands.command(name="foo")
    async def foo(self, ctx, *, arg=None):
        if arg is None:
            await ctx.send('ну хоть что нибудь напиши, просто так не зови :\\')
        else:
            # 0x означает # то есть это HEX color, например 0x070365 = #070365, 0xcfbdf4 = #cfbdf4
            await ctx.send(embed=discord.Embed(description=arg, color=0xcfbdf4))

# вот это то что ниже не включайте оно пока не работает)

# @bot.event
# async def on_message(ctx):
#     bla_bla = False
#     if ctx.content == 'exit':
#         bla_bla = False
#     elif ctx.content == 'start':
#         bla_bla = True
#     if bla_bla is True:
#         await ctx.reply(ctx.content)
#         bla_bla = False


# user = await bot.fetch_user(ctx.message.author.id)
# я не знаю зачем, но думаю эта сточка мне потом понадобится
