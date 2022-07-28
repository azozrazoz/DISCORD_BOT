# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
from config import TOKEN, PREFIX
from my_music_cog import MusicCog
from help_cog import HelpCog
from additional_cog import IpCog, ManageMsgCog
from test_cog import TestCog

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
bot.add_cog(TestCog(bot))


def main():
    bot.run(TOKEN)


if __name__ == '__main__':
    main()
