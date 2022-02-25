import discord

from discord import ApplicationContext, Bot, Option

from discord.ext import commands

import wikipediaapi

class WikiCommand(commands.Cog):

    def __init__(self, bot : Bot):
        self.bot = bot
        self._last_member = None

    @commands.slash_command(name="wikipedia", description="公式Wikipediaから内容を引用します（サードパーティはサポートしていません）")
    async def getContent(self, ctx: ApplicationContext, page : Option(str, "ページ名を入力"), locale : Option(str, "言語コードを入力", required=False)):
        await ctx.defer()
        if (locale is None):
            locale = "ja"

        wikiapi = wikipediaapi.Wikipedia(locale)

        pg = wikiapi.page(page)
        if (pg.exists()):
            embed = discord.Embed(title=pg.title, description=f"{pg.summary}\n[もっと見る]({pg.fullurl})",url=pg.fullurl, color=discord.Color.from_rgb(255, 255, 255))
            embed.set_footer(text="出典: フリー百科事典『ウィキペディア（Wikipedia）』", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Wikipedia-logo-v2.svg/100px-Wikipedia-logo-v2.svg.png")
            await ctx.respond(embed=embed)
        else:
            await ctx.respond("そのようなページは存在していません")
        
def setup(bot : Bot):
    bot.add_cog(WikiCommand(bot))