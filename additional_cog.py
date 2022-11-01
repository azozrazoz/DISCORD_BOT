from discord.ext import commands
import socket
import random
import requests


class ManageMsgCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="rmmsg")
    async def del_msg(self, ctx, count):
        try:
            amount = int(count) + 1
            if amount < 1:
                await ctx.send('Как я тебе это сделаю? :\\')
            else:
                await ctx.channel.purge(limit=amount)
                print(f'Was deleted {count} messages!')
        except Exception as ex:
            await ctx.send(f'Как я тебе это сделаю? :\\ {ex}')


class IpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.url = 'www.youtube.com'
        self.ip = '127.0.0.1'

    def get_info_by_ip(self):
        try:
            response = requests.get(url=f'http://ip-api.com/json/{self.ip}').json()

            data = f"[Int provider]: {response.get('isp')}\n" \
                   f"[Org]: {response.get('org')}\n" \
                   f"[County]: {response.get('country')}\n" \
                   f"[Region Name]: {response.get('regionName')}\n" \
                   f"[City]: {response.get('city')}\n" \
                   f"[ZIP]: {response.get('zip')}\n" \
                   f"[Lat]: {response.get('lat')}\n" \
                   f"[Lon]: {response.get('lon')}\n" \
                   f"[Mobile]: {response.get('mobile')}\n" \
                   f"[Hosting]: {response.get('hosting')}"

            return data

        except requests.exceptions.ConnectionError:
            print('[!] Please check your connection!')
            return '[!] Please check your connection!'

    def get_ip_by_host(self):
        try:
            self.ip = socket.gethostbyname(self.url)
            return f'[Hostname]: {self.url}\n[IP address]: {self.ip}'
        except socket.gaierror as error:
            return f'Invalid Hostname - {error}\nMay be try example: youtube.com'

    # не знаю зачем, но это прикольный скрипт
    @commands.command(name="curl")
    async def get_ip(self, ctx, *, args=None):
        if args is None:
            await ctx.send('Сюда нужно обязательный url или domain :\\')
        else:
            self.url = args
            await ctx.send(self.get_ip_by_host() + "\n" + self.get_info_by_ip())

    @commands.command(name="pip")
    async def get_ip(self, ctx, *, args=None):
        if args is None:
            await ctx.send('Сюда нужно обязательный ip address :\\')
        else:
            self.ip = args
            await ctx.send(self.get_info_by_ip())


class GetRandomCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="rnd")
    async def get_random(self, ctx, *args):
        try:
            await ctx.send(f"Ваше число: {random.randint(int(args[0]), int(args[1]))}")
        except (ValueError, TypeError, IndexError):
            await ctx.send("Введи нормальный диапазон плз :<")
