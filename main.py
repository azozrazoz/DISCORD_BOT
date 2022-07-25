# -*- coding: utf-8 -*-
import asyncio

import discord
import youtube_dl
import os
from discord.utils import get
from discord import FFmpegPCMAudio
from os import system
from discord.ext import commands
from config import TOKEN, PREFIX
from pyfiglet import Figlet


server, server_id, name_channel = None, None, None

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

players = {}

# @bot.event
# async def on_message(ctx):
#     if ctx.content == 'exit':
#         bot.close()
#     elif ctx.author != bot.user:
#         await ctx.reply(ctx.content)


# user = await bot.fetch_user(ctx.message.author.id)
# я не знаю зачем, но думаю эта сточка мне потом понадобится


@bot.event
async def on_ready():
    # лучше используйте standard он вроде норм с таким текстом 'B o t  o n l i n e'
    # smisome1 еще вот этот шрифт прикольный
    text = Figlet(font='speed')
    print(text.renderText('Bot online'))


@bot.command(name="test")
async def test(ctx):
    print(ctx)


# просто тестовая функция на то что в ботом все ок
@bot.command(name="foo")
async def foo(ctx, *, arg=None):
    if arg is None:
        await ctx.send('ну хоть что нибудь напиши, просто так не зови :\\')
    else:
        # 0x означает # то есть это HEX color, например 0x070365 = #070365, 0xcfbdf4 = #cfbdf4
        await ctx.send(embed=discord.Embed(description=arg, color=0xcfbdf4))


@bot.command(name="join", pass_context=True)
async def join(ctx):
    channel = ctx.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        await channel.connect()
        print(f"The bot has connected to {channel}\n")

    await ctx.send(f"Joined {channel}")


# @bot.command(name="play", pass_context=True)
# async def play(ctx, *, query):
#     player = Music(bot)
#     await player.play(ctx=ctx, query=query)
#     # async with ctx.typing():
#     #     player = await youtube_audio.YTDLSource.from_url(query, loop=bot.loop, stream=True)
#     #     ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
#     #
#     # await ctx.send(f'Now playing: {player.title}')


@bot.command(name="leave")
async def leave(ctx):
    try:
        channel = ctx.message.author.voice.channel
    except AttributeError:
        await ctx.send(f'{ctx.author.mention} чел тыы сам не гс сидишь')
        return

    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.disconnect()
        await ctx.send(f"Left {channel}")
    else:
        await ctx.send(f"{ctx.author.mention} ты думал я в гс? а нееет")


youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn',
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(executable=filename, **ffmpeg_options), data=data)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command()
    async def play(self, ctx, *, query):
        """Plays a file from the local filesystem"""

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        ctx.voice_client.play(source, after=lambda e: print(f'Player error: {e}') if e else None)

        await ctx.send(f'Now playing: {query}')

    @bot.command(name="play")
    async def yt(self, ctx, *, url):
        """Plays from a url (almost anything youtube_dl supports)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

        await ctx.send(f'Now playing: {player.title}')

    @commands.command()
    async def stream(self, ctx, *, url):
        """Streams from a url (same as yt, but doesn't predownload)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

        await ctx.send(f'Now playing: {player.title}')

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Changed volume to {volume}%")

    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""

        await ctx.voice_client.disconnect()

    @play.before_invoke
    @yt.before_invoke
    @stream.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()


def main():
    bot.run(TOKEN)


if __name__ == '__main__':
    main()
