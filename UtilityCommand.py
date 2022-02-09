import discord

from discord import Option

from discord.ext import commands
from discord.ext import pages

from mcstatus import MinecraftServer, MinecraftBedrockServer

class UtilCommand(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    async def server_auto(ctx):
        types = ["Bedrock", "Java"]
        return [typ for typ in types if typ.startswith(ctx.value)]

    @commands.slash_command(name="mcserver", description="Minecraft サーバーの情報を取得します。")
    async def lookupServer(self, ctx,edition : Option(str, "Minecraft のエディションを選択", autocomplete=server_auto), ip : Option(str, "Minecraft サーバーのIPを入力 (例: nekozouneko.ddns.net:25565)")):
        await ctx.defer()
        if (edition == "Bedrock"):
            try:
                server = MinecraftBedrockServer.lookup(ip)

                embed  = discord.Embed(title=f"統合版サーバー \"{ip}\" の情報", description="", color=discord.Color.yellow())

                status = server.status()

                embed.add_field(name="説明", value=f"{status.motd}",inline=False)
                embed.add_field(name="プレイヤー", value=f"{status.players_online} / {status.players_max}")
            except:
                embed = discord.Embed(title="エラー",description="サーバーにアクセスできませんでした。ポート指定/開放またはUDPプロトコル以外で開いている場合があります\nIP指定の例: nekozouneko.ddns.net:19132",color=discord.Color.dark_red())
        elif (edition == "Java"):
            try:
                server = MinecraftServer.lookup(ip)
                status = server.status()

                embed  = discord.Embed(title=f"Java版サーバー \"{ip}\" の情報", description="", color=discord.Color.light_grey())

                embed.add_field(name="説明", value=f"{status.description}",inline=False)
                embed.add_field(name="バージョン", value=f"{status.version.name}")
                embed.add_field(name="プレイヤー", value=f"{status.players.online} / {status.players.max}")

            except:
                embed = discord.Embed(title="エラー",description="サーバーにアクセスできませんでした。ポート指定/開放またはTCPプロトコル以外で開いている場合があります\n`IP指定の例: mc.hypixel.net:25565`",color=discord.Color.dark_red())
        else:
            embed = discord.Embed(title="エラー",description="引数 \"edtion\" で問題が発生しました。",color=discord.Color.dark_red())
        await ctx.respond(embed=embed)
    
def setup(bot : discord.Bot):
    bot.add_cog(UtilCommand(bot))