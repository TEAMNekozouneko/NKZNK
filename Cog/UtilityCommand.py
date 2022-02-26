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

from discord import ApplicationContext, ButtonStyle, Option

from discord.ext import commands

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
    
    @commands.slash_command(name="invite",description="ボットの招待リンクを取得")
    async def inviteBot(self, ctx, id : Option(str, "BotのIDを入力",required=False)):
        if (id is None):
            inviteLink=f"https://discord.com/oauth2/authorize?client_id={self.bot.user.id}&permissions=2199023255551&scope=bot%20applications.commands"
            v = discord.ui.Button(
                style=discord.ButtonStyle.link,
                label="全権限",
                url=inviteLink
            )

            i = discord.ui.Button(
                style=discord.ButtonStyle.link,
                label="管理者権限",
                url=f"https://discord.com/oauth2/authorize?client_id={self.bot.user.id}&permissions=8&scope=bot%20applications.commands"
            )

            w = discord.ui.Button(
                style=discord.ButtonStyle.link,
                label="権限なし",
                url=f"https://discord.com/oauth2/authorize?client_id={self.bot.user.id}&permissions=0&scope=bot%20applications.commands"
            )

            e = discord.Embed(
                title="ボットを招待する。",
                description="ボットの招待リンクを生成しました",
                url=inviteLink,
                color=discord.Color.purple()
            )

            iew = discord.ui.View()

            iew.add_item(v)
            iew.add_item(i)
            iew.add_item(w)

            await ctx.respond(embed=e, view=iew)
        else:
            id = int(id)
            inviteLink=f"https://discord.com/oauth2/authorize?client_id={id}&permissions=2199023255551&scope=bot%20applications.commands"
            v = discord.ui.Button(
                style=discord.ButtonStyle.link,
                label="全権限",
                url=inviteLink
            )

            i = discord.ui.Button(
                style=discord.ButtonStyle.link,
                label="管理者権限",
                url=f"https://discord.com/oauth2/authorize?client_id={id}&permissions=8&scope=bot%20applications.commands"
            )

            w = discord.ui.Button(
                style=discord.ButtonStyle.link,
                label="権限なし",
                url=f"https://discord.com/oauth2/authorize?client_id={id}&permissions=0&scope=bot%20applications.commands"
            )

            e = discord.Embed(
                title="ボットを招待する。",
                description=f"ボットの招待リンクを生成しました（ID:{id}）",
                url=inviteLink,
                color=discord.Color.purple()
            )

            iew = discord.ui.View()

            iew.add_item(v)
            iew.add_item(i)
            iew.add_item(w)

            await ctx.respond(embed=e, view=iew)

    @commands.slash_command(name="ebdimage", description="埋め込みに画像を追加します。")
    async def EmbedonImage(self, ctx : ApplicationContext, url : Option(str, "埋め込みに追加する画像を入力"), dlbutton: Option(bool, "ダウンロードボタンを表示するか", required=False)):
        embed = discord.Embed(color=discord.Color.from_rgb(47, 49, 54))
        embed.set_image(url=url)
        if (dlbutton is None or dlbutton):
            download_button = discord.ui.Button(
                style=ButtonStyle.url,
                url=url,
                label="ダウンロード",
                emoji="⬇"
            )
            vie = discord.ui.View()
            vie.add_item(download_button)
            await ctx.respond(view=vie, embed=embed)

        else:
            await ctx.respond(embed=embed)
    
def setup(bot : discord.Bot):
    bot.add_cog(UtilCommand(bot))