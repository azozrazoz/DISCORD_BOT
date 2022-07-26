# -*- coding: utf-8 -*-
import discord
# import youtube_dl as ytdl
# import os
# from discord.utils import get
# from discord import FFmpegPCMAudio
# from os import system
from discord.ext import commands
from config import TOKEN, PREFIX
from music_cog import MusicCog
from help_cog import HelpCog
from additional_cog import IpCog, ManageMsgCog

server, server_id, name_channel = None, None, None

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

bot.remove_command('help')
bot.remove_cog('help')
bot.add_cog(MusicCog(bot))
bot.add_cog(HelpCog(bot))
bot.add_cog(IpCog(bot))
bot.add_cog(ManageMsgCog(bot))


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


@bot.command(name="test")
async def test(ctx):
    await ctx.send(f'дарова {ctx.message.author.name}!')


# просто тестовая функция на то что в ботом все ок
@bot.command(name="foo")
async def foo(ctx, *, arg=None):
    if arg is None:
        await ctx.send('ну хоть что нибудь напиши, просто так не зови :\\')
    else:
        # 0x означает # то есть это HEX color, например 0x070365 = #070365, 0xcfbdf4 = #cfbdf4
        await ctx.send(embed=discord.Embed(description=arg, color=0xcfbdf4))


def main():
    bot.run(TOKEN)


if __name__ == '__main__':
    main()
