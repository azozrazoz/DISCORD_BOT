# import discord
# import asyncio
from unicodedata import name
from discord.ext import commands
from config import TOKEN, PREFIX


bot = commands.Bot(command_prefix=PREFIX)

# @bot.event
# async def on_message(ctx):
#     if ctx.content == 'exit':
#         bot.close()
#     elif ctx.author != bot.user:
#         await ctx.reply(ctx.content)


@bot.command(name="test")
async def foo(ctx, arg):
    await ctx.send(arg)


@bot.command(name="play")
async def play(ctx, url):
    await ctx.send(url)

# test commit

bot.run(TOKEN)
