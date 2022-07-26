import discord
from discord.ext import commands

from youtube_dl import YoutubeDL


class MusicCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        # all the music related stuff
        self.is_playing = False
        self.is_paused = False

        # 2d array containing [song, channel]
        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio/best', 'extractaudio': True,
                                                        'audioformat': 'mp3',
                                                        'outtmpl': u'%(id)s.%(ext)s',
                                                        'noplaylist': True,
                                                        'nocheckcertificate': True,
                                                        'postprocessors': [{
                                                            'key': 'FFmpegExtractAudio',
                                                            'preferredcodec': 'mp3',
                                                            'preferredquality': '192',
                                                        }]}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                               'options': '-vn'}

        self.vc = None

    # Changes the player's volume
    @commands.command(name='volume', aliases=['v', 'vol'])
    async def volume(self, ctx, volume: int):
        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        self.vc = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        self.vc.source = discord.PCMVolumeTransformer(self.vc.source, volume=volume)
        await ctx.send(f"Changed volume to {volume}%")

    # searching the item on youtube
    def search_yt(self, item):
        result = ''
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info(str(item), download=False)
                formats = ydl.extract_info(str(item), download=False)['formats']
                for el in formats:
                    if el['format_id'] == '249':
                        result = el['url']
            except Exception:
                print(item)
                return False

        return {'source': result, 'title': info['title']}

    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            # get the first url
            m_url = self.music_queue[0][0]['source']

            # remove the first element as you are currently playing it
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    async def play_music(self, ctx):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']

            # try to connect to voice channel if you are not already connected
            if self.vc is None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()

                # in case we fail to connect
                if self.vc is None:
                    await ctx.send("Could not connect to the voice channel")
                    return
            else:
                await self.vc.move_to(self.music_queue[0][1])

            # remove the first element as you are currently playing it
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    @commands.command(name="play", aliases=["p", "playing"], help="Plays a selected song from youtube")
    async def play(self, ctx, *args):
        query = args[0]
        try:
            voice_channel = ctx.message.author.voice.channel
        except AttributeError:
            await ctx.send(f'{ctx.author.mention} чел тыы, сам не в гс :/')
            return
        if voice_channel is None:
            # you need to be connected so that the bot knows where to go
            await ctx.send("Connect to a voice channel!")
        elif self.is_paused:
            self.vc.resume()
        else:
            song = self.search_yt(query)
            if isinstance(type(song), type(True)):
                await ctx.send(
                    "Не удалось скачать песню.\n"
                    "Неверный формат, попробуйте другое ключевое слово."
                    "Это может быть связано с плейлистом или форматом прямой трансляции.")
            else:
                await ctx.send(f"{ctx.author.mention} песня записана и обработана ✅")
                self.music_queue.append([song, voice_channel])

                if self.is_playing is False:
                    await self.play_music(ctx)

    @commands.command(name="pause", help="Pauses the current song being played")
    async def pause(self, ctx):
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
        elif self.is_paused:
            self.is_paused = False
            self.is_playing = True
            await ctx.send(f"{ctx.author.mention} поехали!")
            self.vc.resume()

    @commands.command(name="resume", aliases=["r"], help="Resumes playing with the discord bot")
    async def resume(self, ctx):
        if self.is_paused:
            self.is_paused = False
            self.is_playing = True
        await ctx.send(f"{ctx.author.mention} поехали!")
        self.vc.resume()

    @commands.command(name="skip", aliases=["s"], help="Skips the current song being played")
    async def skip(self, ctx):
        if self.vc is not None and self.vc:
            await ctx.send(f'{ctx.author.mention} зачееем?')
            self.vc.stop()
            await self.play_music(ctx)

    @commands.command(name="queue", aliases=["q"], help="Displays the current songs in queue")
    async def queue(self, ctx):
        retval = ""
        for i in range(0, len(self.music_queue)):
            # display a max of 5 songs in the current queue
            if i > 4:
                break
            retval += self.music_queue[i][0]['title'] + "\n"

        if retval != "":
            await ctx.send(retval)
        else:
            await ctx.send("No music in queue")

    @commands.command(name="clear", aliases=["c", "bin"], help="Stops the music and clears the queue")
    async def clear(self, ctx):
        if self.vc is not None and self.is_playing:
            self.vc.stop()
        self.music_queue = []
        await ctx.send(f"{ctx.author.mention} бак очищен, можешь залить 92?")

    @commands.command(name="leave", aliases=["disconnect", "l", "d"], help="Kick the bot from VC")
    async def dc(self, ctx):
        try:
            channel = ctx.message.author.voice.channel
        except AttributeError:
            await ctx.send(f'{ctx.author.mention} чел тыы, сам не в гс :/')
            return
        self.vc = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        if self.vc and self.vc.is_connected():
            self.is_playing = False
            self.is_paused = False
            await self.vc.disconnect()
            await ctx.send(f"я пошел, бывайте :3 {str(channel)[1:]}")
        else:
            await ctx.send(f"{ctx.author.mention} ты думал я в гс? а нееет")

    @commands.command(name='join', aliases=['j'])
    async def join(self, ctx):
        try:
            channel = ctx.message.author.voice.channel
        except AttributeError:
            await ctx.send(f'{ctx.author.mention} чел тыы, сам не в гс :/')
            return
        self.vc = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)

        if self.vc and self.vc.is_connected():
            await self.vc.move_to(channel)
        else:
            await channel.connect()
        await ctx.send(f"Залетел на {str(channel)[1:]}")
