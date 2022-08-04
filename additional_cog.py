from discord.ext import commands
import socket
import random


class ManageMsgCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="rmmsg")
    async def del_msg(self, ctx, count):
        try:
            amount = int(count) + 1
            if amount < 1:
                await ctx.send('как я тебе это сделаю? :\\')
            else:
                await ctx.channel.purge(limit=amount)
                print(f'Was deleted {count} messages!')
        except Exception as ex:
            await ctx.send(f'как я тебе это сделаю? :\\ {ex}')


class IpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.url = 'www.youtube.com'

    def get_ip_by_host(self):
        try:
            return f'Hostname: {self.url}\nIP address: {socket.gethostbyname(self.url)}'
        except socket.gaierror as error:
            return f'Invalid Hostname - {error}\nMay be try example: youtube.com'

    # не знаю зачем, но это прикольный скрипт
    @commands.command(name="curl")
    async def get_ip(self, ctx, *, args=None):
        if args is None:
            await ctx.send('сюда нужно обязательный url или domain :\\')
        else:
            self.url = args
            await ctx.send(self.get_ip_by_host())


class GetRandomCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="rnd")
    async def get_random(self, ctx, *args):
        try:
            await ctx.send(f"Ваше число: {random.randint(int(args[0]), int(args[1]))}")
        except (ValueError, TypeError, IndexError):
            await ctx.send("Введи нормальный диапазон плз :<")
