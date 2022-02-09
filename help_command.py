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

from discord.ext import commands
from discord import ActivityType, Game, Option
from discord.ext import pages

import platform

class helpCommand(commands.Cog):
    def __init__(self, bot : discord.Bot):
        self.bot = bot
        self._last_member = None
        
    async def commands_auto(ctx) -> list[str]:
        command = ["disconnect","join","joins","mcserver","play","server","speak","stop","user"]
        return [c for c in command if c.startswith(ctx.value)]
    
    @commands.slash_command(name="help",description="このBotについて色々知ることができます。")
    async def helpCommand(self, ctx, commands : Option(str,"詳しく知るコマンドを選ぶ", autocomplete=commands_auto, required=False)):
        await ctx.defer()
        if (commands is None):
            helpPage = [
                discord.Embed(title="NKZNK - システム情報",description=f"**Python**: {platform.python_version()}\n**Pycord**: {discord.__version__}",color=discord.Color.blue(),url="https://discord.gg/ErDmtEpaqe"),
                discord.Embed(title="NKZNK - クレジット",description="各モジュール、ソフトウェアのクレジットです。",color=discord.Color.blue(),url="https://discord.gg/ErDmtEpaqe"),
                discord.Embed(title="NKZNK - 協力",description="開発協力していただいた以下の方々にお礼申し上げます。",color=discord.Color.blue(),url="https://discord.gg/ErDmtEpaqe"),
            ]
        
            helpPage[0].add_field(name="ライセンス",value='このBotはMITライセンスの上オープンソースで提供されています。\n[ライセンス情報](https://github.com/TEAMNekozouneko/NKZNK/blob/main/LICENSE)')
            helpPage[0].set_thumbnail(url=self.bot.user.avatar.url)

            helpPage[1].add_field(name="Python", value="Copyright (c) 2001-2022 Python Software Foundation.\nAll Rights Reserved.")
            helpPage[1].add_field(name="Pycord", value=f"{discord.__copyright__}")
            helpPage[1].add_field(name="mcstatus", value=f"https://github.com/Dinnerbone/mcstatus")

            helpPage[2].add_field(name="Nekozouneko TEAM", value="||~~Nekozouneko (考案／サーバー)~~||\nTaitaitatata (開発)")
            helpPage[2].add_field(name="Special Thanks", value="モジュールを開発していただいた皆様")

            pageManager = pages.Paginator(pages=helpPage)
            await pageManager.respond(ctx.interaction)
        else:
            await ctx.respond("未実装です。",ephemeral=True)

def setup(bot):
    return bot.add_cog(helpCommand(bot))