import asyncio
import os
import discord
from discord.ext import commands

PREFIX = '%'

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)


async def load_cogs():
    bot.remove_command('help')
    await bot.remove_cog('help')
    for file in os.listdir('cogs'):
        if file.endswith('.py'):
            await bot.load_extension(f"cogs.{file[:-3]}")


async def main():
    await load_cogs()
    with open("config.txt", 'r', encoding='utf-8') as f:
        await bot.start(f.readline())


if __name__ == '__main__':
    asyncio.run(main())
