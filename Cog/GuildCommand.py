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

from discord import Option

from discord.ext import pages
from discord.ext import commands

import datetime

from math import floor

class GuildCommands(commands.Cog):

    def __init__(self, bot : discord.Bot):
        self.bot = bot
        self._last_member = None

    @commands.slash_command(name="server", description="サーバーを取得します。")
    async def guildinfo(self, ctx, id : Option(str, "取得するサーバーIDを入力（このBotが参加していないサーバーは取得不可能です。）",required=False)):
        await ctx.defer()
        if (id is None):
            guildInfo = ctx.guild 
            embeds = [
                discord.Embed(title=f"{guildInfo.name} の基本情報", description=f"**ID:** {guildInfo.id}",color=discord.Color.green()),
                discord.Embed(title=f"{guildInfo.name} のチャンネル情報", description=f"**ID:** {guildInfo.id}",color=discord.Color.green()),
                discord.Embed(title=f"{guildInfo.name} の詳細情報", description=f"**ID:** {guildInfo.id}",color=discord.Color.green()),
            ]

            # === Embeds[0] の設定 ===

            e1 = embeds[0]

            # 説明があるかチェックしてから説明を挿入

            if (guildInfo.description is None):
                e1.add_field(name="説明", value="説明は存在していません",inline=False)
            else:
                e1.add_field(name="説明", value=guildInfo.description, inline=False)

            e1.add_field(name="所有者", value=f"<@!{guildInfo.owner_id}>")

            e1.add_field(name="サーバーブースト", value=f"Lv. {guildInfo.premium_tier} ({guildInfo.premium_subscription_count} ブースト済み)")

            e1.add_field(name="作成日",value=f"<t:{floor(datetime.datetime.fromtimestamp(guildInfo.created_at.timestamp(), datetime.timezone(datetime.timedelta(hours=9))).timestamp())}>")
            
            # チャンネル設定

            e2 = embeds[1]

            e2.add_field(name="チャンネル数", value=f"テキスト: `{len(guildInfo.text_channels)}` ボイス: `{len(guildInfo.voice_channels)}` ステージ: `{len(guildInfo.stage_channels)}` スレッド: `{len(guildInfo.threads)}`",inline=False)

            if (not guildInfo.afk_channel is None):
                e2.add_field(name="AFK 設定", value=f"{guildInfo.afk_channel.mention}\n`{guildInfo.afk_timeout / 60}` 分")

            if (not guildInfo.rules_channel is None):
                e2.add_field(name="ルールチャンネル", value=f"{guildInfo.rules_channel.mention}")

            if (not guildInfo.system_channel is None):
                e2.add_field(name="システムチャンネル", value=f"{guildInfo.system_channel.mention}")

            # ==== Embeds[2] の設定 ====

            e3 = embeds[2]

            e3.add_field(name="メンバー数", value=f"メンバー: `{guildInfo.member_count}` 人")

            e3.add_field(name="アップロード上限", value=f"{floor(guildInfo.filesize_limit /1000 /1000)} MB")

            role_mentioned = []
            for role in guildInfo.roles:
                role_mentioned = role_mentioned + [role.mention]

            amention = ", ".join(role_mentioned)

            e3.add_field(name="ロール", value=amention, inline=False)

            e3.add_field(name="絵文字上限", value=f"{len(guildInfo.emojis)} / {guildInfo.emoji_limit}")

            e3.add_field(name="ステッカー上限", value=f"{len(guildInfo.stickers)} / {guildInfo.sticker_limit}")
            
            # アイコンがないサーバーのことも考えない場合はスキップさせる

            if (not guildInfo.icon is None):
                e1.set_thumbnail(url=guildInfo.icon.url)
                e2.set_thumbnail(url=guildInfo.icon.url)
                e3.set_thumbnail(url=guildInfo.icon.url)
                embeds = embeds + [discord.Embed(title=f"{guildInfo.name} のサーバーアイコン", description=f"{guildInfo.icon.url}")]
                embeds[3].set_image(url=guildInfo.icon.url)

            if (not guildInfo.splash is None):
                embeds = embeds + [discord.Embed(title=f"{guildInfo.name} のサーバースプラッシュ画面", description=f"{guildInfo.splash.url}")]
                embeds[4].set_image(url=guildInfo.splash.url)

            if (not guildInfo.banner is None):
                embeds = embeds + [discord.Embed(title=f"{guildInfo.name} のサーバーバナー", description=f"{guildInfo.banner.url}")]
                embeds[5].set_image(url=guildInfo.banner.url)
            
            pageMan = pages.Paginator(embeds)
            await pageMan.respond(ctx.interaction)
        else:
            try:
                intid = int(id)
            except:
                embed = discord.Embed(title="エラー",description="サーバーの取得に失敗しました。", color=discord.Color.dark_red())
                await ctx.respond(embed=embed)
                return
            if (not self.bot.get_guild(intid) is None):
                guildInfo = self.bot.get_guild(intid)
                embeds = [
                    discord.Embed(title=f"{guildInfo.name} の基本情報", description=f"**ID:** {guildInfo.id}",color=discord.Color.green()),
                    discord.Embed(title=f"{guildInfo.name} の詳細情報", description=f"**ID:** {guildInfo.id}",color=discord.Color.green()),
                ]

                # === Embeds[0] の設定 ===

                e1 = embeds[0]

                # 説明があるかチェックしてから説明を挿入

                if (guildInfo.description is None):
                    e1.add_field(name="説明", value="説明は存在していません",inline=False)
                else:
                    e1.add_field(name="説明", value=guildInfo.description, inline=False)

                e1.add_field(name="所有者", value=f"<@!{guildInfo.owner_id}>")

                e1.add_field(name="サーバーブースト", value=f"Lv. {guildInfo.premium_tier} ({guildInfo.premium_subscription_count} ブースト済み)")

                e1.add_field(name="作成日",value=f"<t:{floor(datetime.datetime.fromtimestamp(guildInfo.created_at.timestamp(), datetime.timezone(datetime.timedelta(hours=9))).timestamp())}>")
                
                # ==== Embeds[1] の設定 ====

                e3 = embeds[1]

                e3.add_field(name="メンバー数", value=f"メンバー: `{guildInfo.member_count}` 人")
                e3.add_field(name="アップロード上限", value=f"{floor(guildInfo.filesize_limit /1000 /1000)} MB")

                e3.add_field(name="絵文字上限", value=f"{len(guildInfo.emojis)} / {guildInfo.emoji_limit}")

                e3.add_field(name="ステッカー上限", value=f"{len(guildInfo.stickers)} / {guildInfo.sticker_limit}")

                # アイコンがないサーバーのことも考えない場合はスキップさせる
                
                if (not guildInfo.icon is None):
                    e1.set_thumbnail(url=guildInfo.icon.url)
                    e3.set_thumbnail(url=guildInfo.icon.url)
                    embeds = embeds + [discord.Embed(title=f"{guildInfo.name} のサーバーアイコン", description=f"{guildInfo.icon.url}")]
                    embeds[2].set_image(url=guildInfo.icon.url)

                if (not guildInfo.splash is None):
                    embeds = embeds + [discord.Embed(title=f"{guildInfo.name} のサーバースプラッシュ画面", description=f"{guildInfo.splash.url}")]
                    embeds[3].set_image(url=guildInfo.splash.url)

                if (not guildInfo.banner is None):
                    embeds = embeds + [discord.Embed(title=f"{guildInfo.name} のサーバーバナー", description=f"{guildInfo.banner.url}")]
                    embeds[4].set_image(url=guildInfo.banner.url)

                pageMan = pages.Paginator(embeds)
                await pageMan.respond(ctx.interaction)
            else:
                embed = discord.Embed(title="エラー",description="サーバーの取得に失敗しました。", color=discord.Color.dark_red())
                await ctx.respond(embed=embed)

def setup(bot : discord.Bot):
    bot.add_cog(GuildCommands(bot))