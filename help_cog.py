from discord.ext import commands
from pyfiglet import Figlet


class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.help_message = """
```c++
Основные команды:
#help - (то что ты сейчас видишь) показывает набор команд
#play or #p [url on youtube link] - воспроизводит шедевры
#queue or #q - выводит список текущей музыки
#clear - очищащет текущий список 
#skip - это делает Шамиль когда играет в доту
#leave - и это тоже
#join - просто подключает бота к каналу
#pause - останавливает музыку
#resume - отпускает паузу

Доп. команды:
#foo - может выводить ваше сообщение в виде вложения
#test - проверка
```
"""
        self.text_channel_list = []

    # some debug info so that we know the bot has started
    @commands.Cog.listener()
    async def on_ready(self):
        # лучше используйте standard он вроде норм с таким текстом 'B o t  o n l i n e'
        # smisome1 еще вот этот шрифт прикольный
        text = Figlet(font='speed')
        print(text.renderText('Bot online'))

    @commands.command(name="help", help="Displays all the available commands")
    async def get_help(self, ctx):
        await ctx.send(self.help_message)

    async def send_to_all(self, msg):
        for text_channel in self.text_channel_list:
            await text_channel.send(msg)
