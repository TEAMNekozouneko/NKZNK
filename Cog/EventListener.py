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

from Cog.Util.config_sys import reset_bot_cfg

import aioconsole, asyncio, datetime, random, locale, platform, json

class EventHandler(commands.Cog):

    def __init__(self, bot : discord.Bot):
        self.bot = bot
        self._last_member = None

        self.ConfigFile = open("config.json", "r")
        self.ConfigDict = json.load(self.ConfigFile)

        self.bot_name = self.ConfigDict["settings"]["name"]
        self.bot_ver = self.ConfigDict["settings"]["version"]

    @commands.Cog.listener()
    async def on_ready(self):
        print("Authorized token.")
        print(f"================================= NKZNK =================================")
        print(f"Discord API: Pycord {discord.__version__}")
        print('\nMIT License\n\nCopyright (c) 2022 Nekozouneko Team Lab\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.')
        print("\nTHIS BOT BY NEKOZOUNEKO TEAM")
        print(f"==========================================================================")       
        task = asyncio.create_task(self.presences())
        if (self.ConfigDict["settings"]["enable_console"]):
            consoleTask = asyncio.create_task(self.console())
        await self.bot.change_presence(activity=discord.Activity(name=f"{self.bot_name} v{self.bot_ver}",type=ActivityType.playing), status=discord.Status.online)

    async def presences(self):
        if (self.ConfigDict["settings"]["unix"]):
            locale.setlocale(locale.LC_TIME, "ja_JP.UTF-8")
        else:
            locale.setlocale(locale.LC_TIME, "ja-JP")

        while True:
            today = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))

            l = ["/help to Help.", "/help ???????????????????????????", "???????????????????????????????????????????????????", f"{len(self.bot.guilds)}??????????????????????????????????????????????????????!", f"{self.bot_name} Version {self.bot_ver}", "(c) 2022 TEAM Nekozouneko",f"????????????{today.strftime('%Y/%m/%d %H:%M')}"]
            
            await asyncio.sleep(10)
            await self.bot.change_presence(activity=discord.Activity(name=random.choice(l),type=ActivityType.playing), status=discord.Status.online)

    async def console(self):
        print(f"{platform.system()} {platform.release()} ({platform.architecture()[0]}) / {platform.python_implementation()} {platform.python_version()}")
        print(f"\n{self.bot_name} [Version {self.bot_ver}]")
        print("Copyright (C) 2021-2022 TEAM Nekozouneko\n")
        input_command = await aioconsole.ainput("NKZNK@CONSOLE > ")
        while True:
            if (input_command == "exit" or input_command == "stop"):
                await self.bot.close()
                break
            elif (input_command == "version"):
                print(f"{self.bot_name} v.{self.bot_ver} release.")
                print("Repository: https://github.com/TEAMNekozouneko/NKZNK")
            elif (input_command == "reload" or input_command == "rl"):
                print("Reloading All Exts...")
                l = []
                for extname in self.bot.extensions.keys():
                    l = l + [str(extname)]
                
                l.remove("Cog.EventListener")

                for ex in l:
                    print(f"Reloading {ex}")
                    self.bot.reload_extension(ex)
                print("Reloaded")
            elif (input_command == "invite"):
                print(f"Link: https://discord.com/oauth2/authorize?client_id={self.bot.user.id}&permissions=2199023255551&scope=bot%20applications.commands")
            elif (input_command == "help" or input_command == "?"):
                print("NKZNK Console Help\n")
                print("cogs    - Cog and exetensions list")
                print("help    - show this")
                print("invite  - show invite link")
                print("info    - bot information")
                print("reload  - reload cogs")
                print("reset   - reset config.json")
                print("stop    - stop bot")
                print("version - about this bot")
            elif (input_command == "cogs" or input_command == "exts" or input_command == "extensions"):
                print(f"Cogs ({len(self.bot.cogs.keys())}):")
                print(", ".join(self.bot.cogs.keys()) + "\n")

                print(f"Extensions ({len(self.bot.extensions.keys())})")
                print(", ".join(self.bot.extensions.keys()))
            elif (input_command == "info"):
                print(f"===== BOT INFOMATION =====\n")
                print(f"NAME / ID: {str(self.bot.user)} ({self.bot.user.id})")
                print(f"AVATAR URL: {self.bot.user.avatar.url}")
                print(f"2FA VERIFYED: {self.bot.user.mfa_enabled}")
                print(f"\n===== SERVER INFOMATION =====\n")
                print(f"SERVERS: {len(self.bot.guilds)} SERVERS JOINED")
                print(f"VOICE / STAGES: {len(self.bot.voice_clients)} CONNECTED")
                print(f"EMOJIS: {len(self.bot.emojis)}")
                print(f"STICKERS: {len(self.bot.stickers)}")
            elif (input_command == "reset"):
                print("\"reset confirm\" to reset config.json")
            elif (input_command == "reset confirm"):
                print("reseting config.json...")
                reset_bot_cfg()
                await self.bot.close()
                break
            else:
                print(f"ERR: Command \"{input_command}\" is not found. Type \"help\" for help.")
            input_command = await aioconsole.ainput("NKZNK@CONSOLE > ")

def setup(bot : discord.Bot):
    bot.add_cog(EventHandler(bot))