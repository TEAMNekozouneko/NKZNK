from discord.ext import commands
from discord import ActivityType, Game, Option
from discord.ext import pages
import discord

class helpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_ready(self):
        print("started")
        await self.bot.change_presence(activity=discord.Activity(name="/help でヘルプを表示 | NKZNK Rewrited v-1.0",type=ActivityType.playing))
        
    
    @commands.slash_command(name="help",description="このBotについて色々知ることができます。")
    async def helpCommand(self, ctx, commands : Option(str,"詳しく知るコマンドを選ぶ",required=False)):
        await ctx.defer()
        if (commands is None):
            helpPage = [
                discord.Embed(title="NKZNK - システム情報",description="API: Pycord (Python 3.10.1 64 bit)",color=discord.Color.blue(),url="https://discord.gg/ErDmtEpaqe"),
                discord.Embed(title="NKZNK - 試験版",description="ページ2",color=discord.Color.blue(),url="https://discord.gg/ErDmtEpaqe"),
                discord.Embed(title="NKZNK - 試験版",description="ページ3",color=discord.Color.blue(),url="https://discord.gg/ErDmtEpaqe"),
            ]

            helpPage[0].set_footer(text=f'{str(ctx.author)} ({ctx.author.id})',icon_url=ctx.author.avatar.url)
            helpPage[1].set_footer(text=f'{str(ctx.author)} ({ctx.author.id})',icon_url=ctx.author.avatar.url)
            helpPage[2].set_footer(text=f'{str(ctx.author)} ({ctx.author.id})',icon_url=ctx.author.avatar.url)
        
            helpPage[0].add_field(name="クレジット",value="Pycord: https://github.com/Pycord-Development/pycord")

            pageManager = pages.Paginator(pages=helpPage)
            await pageManager.respond(ctx.interaction,ephemeral=True)
        else:
            await ctx.respond("未実装です。",ephemeral=True)

def setup(bot):
    return bot.add_cog(helpCommand(bot))
