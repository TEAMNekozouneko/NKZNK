from discord.ext import commands
from discord import ActivityType, Game, Option
from discord.ext import pages
import discord
import sys
import platform

class helpCommand(commands.Cog):
    def __init__(self, bot : discord.Bot):
        self.bot = bot
        self._last_member = None
    
    @commands.slash_command(name="help",description="このBotについて色々知ることができます。")
    async def helpCommand(self, ctx, commands : Option(str,"詳しく知るコマンドを選ぶ",required=False)):
        await ctx.defer()
        if (commands is None):
            helpPage = [
                discord.Embed(title="NKZNK - システム情報",description=f"**Python**: {platform.python_version()}\n**Pycord**: {discord.__version__}",color=discord.Color.blue(),url="https://discord.gg/ErDmtEpaqe"),
                discord.Embed(title="NKZNK - ",description="ページ2",color=discord.Color.blue(),url="https://discord.gg/ErDmtEpaqe"),
                discord.Embed(title="NKZNK - 試験版",description="ページ3",color=discord.Color.blue(),url="https://discord.gg/ErDmtEpaqe"),
            ]
        
            helpPage[0].add_field(name="ライセンス",value='このBotはMITライセンスの上オープンソースで提供されています。\n[ライセンス情報](https://github.com/TEAMNekozouneko/NKZNK/blob/main/LICENSE)')
            helpPage[0].set_thumbnail(url=self.bot.user.avatar.url)

            pageManager = pages.Paginator(pages=helpPage)
            await pageManager.respond(ctx.interaction,ephemeral=True)
        else:
            await ctx.respond("未実装です。",ephemeral=True)

def setup(bot):
    return bot.add_cog(helpCommand(bot))