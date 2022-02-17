#
# MIT License
#
# Copyright (c) 2022 Nekozouneko Team Lab
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import discord
from discord import ActivityType
from discord.ext import commands
from discord.ext import pages

import asyncio

import random, datetime, locale, aioconsole

class EventHandler(commands.Cog):

    def __init__(self, bot : discord.Bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_ready(self):
        print("Authorized token.")
        print(f"============================== NKZNK ==============================")
        print(f" Discord API: Pycord {discord.__version__}")
        print('\nMIT License\n\nCopyright (c) 2022 Nekozouneko Team Lab\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.')
        print("\nTHIS BOT BY NEKOZOUNEKO TEAM")
        print(f"==========================================================================")       
        task = asyncio.create_task(self.presences())
        consoleTask = asyncio.create_task(self.console())
        await self.bot.change_presence(activity=discord.Activity(name="NKZNK v2022.02.10",type=ActivityType.playing), status=discord.Status.online)

    async def presences(self):
        locale.setlocale(locale.LC_TIME, "ja_JP")
        print(datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y年%m月%d日（%a）'))
        while True:
            today = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
            l = ["/help でヘルプを表示","ver.2022.02.17 Unstable","/help to Help",f"現在{len(self.bot.guilds)}個のサーバーで利用されています!", f"本日は、{today.strftime('%Y年%m月%d日（%a）')}です。", "Pythonで動いています"]
            await asyncio.sleep(10)
            await self.bot.change_presence(activity=discord.Activity(name=l[random.randrange(6)],type=ActivityType.playing), status=discord.Status.online)

    async def console(self):
        input_command = await aioconsole.ainput("CONSOLE > ")
        while True:
            if (input_command == "exit" or input_command == "stop"):
                await self.bot.close()
                break
            elif (input_command == "version"):
                print("NKZNK v.2022.02.17 beta release.")
                print("Repository: https://github.com/TEAMNekozouneko/NKZNK")
            elif (input_command == "reload" or input_command == "rl"):
                print("Reloading All Cogs...")
                self.bot.reload_extension("Cog.ChannelCommand")
                self.bot.reload_extension("Cog.GuildCommand")
                self.bot.reload_extension("Cog.HelpCommand")
                self.bot.reload_extension("Cog.UserCommand")
                self.bot.reload_extension("Cog.UtilityCommand")
                self.bot.reload_extension("Cog.VoiceCommand")
                self.bot.reload_extension("Cog.WikiCommand")
                print("Reloaded")
            elif (input_command == "invite"):
                print(f"Link: https://discord.com/oauth2/authorize?client_id={self.bot.user.id}&permissions=2199023255551&scope=bot%20applications.commands")
            elif (input_command == "help" or input_command == "?"):
                print("NKZNK Console Help\n")
                print("help - show this")
                print("version - about this bot")
                print("invite - show invite link")
                print("reload - reload cogs")
            else:
                print(f"ERR: Command \"{input_command}\" is not found. Type \"help\" for help.")
            input_command = await aioconsole.ainput("CONSOLE > ")

def setup(bot):
    bot.add_cog(EventHandler(bot))