import discord
import youtube_dl
import os
from discord.utils import get
from discord import FFmpegPCMAudio
from os import system
from discord.ext import commands
from config import TOKEN, PREFIX

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# @bot.event
# async def on_message(ctx):
#     if ctx.content == 'exit':
#         bot.close()
#     elif ctx.author != bot.user:
#         await ctx.reply(ctx.content)


@bot.command(name="test")
async def foo(ctx, *arg):
    result = ''
    for el in arg:
        result += el + ' '

    # 0x означает # то есть это HEX color, например 0x070365 = #070365, 0xcfbdf4 = #cfbdf4
    await ctx.send(embed=discord.Embed(description=result, color=0xcfbdf4))


@bot.command(name="play")
async def play(ctx):
    members = ctx.guild.members
    result = ''
    for el in members:
        result += str(el.id) + '\n'
    await ctx.send(result)


@bot.command(name="leave")
async def leave(ctx):
    try:
        channel = ctx.message.author.voice.channel
    except AttributeError:
        # user = await bot.fetch_user(ctx.message.author.id)
        await ctx.send(f'{ctx.author.mention} чел тыы сам не гс сидишь')
        return

    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.disconnect()
        await ctx.send(f"Left {channel}")
    else:
        await ctx.send(f"{ctx.author.mention} ты думал я в гс? а нееет")

if __name__ == '__main__':
    bot.run(TOKEN)
