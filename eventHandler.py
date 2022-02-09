import discord
from discord import ActivityType
from discord.ext import commands
from discord.ext import pages

class eventhandler(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"============================== NKZNK ==============================")
        print(f" Discord API: Pycord {discord.__version__}")
        print('\nMIT License\n\nCopyright (c) 2022 Nekozouneko Team Lab\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.')
        print("\nTHIS BOT BY NEKOZOUNEKO TEAM")
        print(f"==========================================================================")
        
        await self.bot.change_presence(activity=discord.Activity(name="/help でヘルプを表示 | NKZNK Rewrited v-1.0",details="Unknown",type=ActivityType.playing))


def setup(bot):
    bot.add_cog(eventhandler(bot))