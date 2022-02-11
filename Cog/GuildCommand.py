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

from discord import ApplicationContext, Option, TextChannel, SlashCommandGroup

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
                
                # ==== Embeds[1] の設定====

                e2 = embeds[1]

                e2.add_field(name="チャンネル数", value=f"テキスト: `{len(guildInfo.text_channels)}` ボイス: `{len(guildInfo.voice_channels)}` ステージ: `{len(guildInfo.stage_channels)}` スレッド: `{len(guildInfo.threads)}`", inline=False)

                if (not guildInfo.afk_channel is None):
                    e2.add_field(name="AFK 設定", value=f"{guildInfo.afk_channel.mention} | `{guildInfo.afk_timeout}` 秒")

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
                embed = discord.Embed(title="エラー",description="サーバーの取得に失敗しました。", color=discord.Color.dark_red())
                await ctx.respond(embed=embed)

    channelGroup = SlashCommandGroup("channel","チャンネル関係のコマンドです。")

    TextChannelGroup = channelGroup.create_subgroup("text", "テキストチャンネルのコマンドです。")

    @TextChannelGroup.command(name="lock",description="@everyoneからの送信をできなくします。(再実行で解除)")
    async def lock(self, ctx : ApplicationContext, channel : Option(TextChannel,"ロックするチャンネルを選択"), reason : Option(str, "理由を入力", required=False)):
        if (ctx.author.guild_permissions.manage_channels or ctx.author.guild_permissions.manage_guild):
            if (channel.permissions_for(channel.guild.default_role).send_messages):
                await channel.set_permissions(channel.guild.default_role, send_messages=False)
                if (reason is None):
                    reason = "なし"
                embed = discord.Embed(title="🔒 このチャンネルをロックしました。",description="理由: {0}".format(reason),color=discord.Color.blue())
                await ctx.respond(embed=embed)
            else:
                await channel.set_permissions(channel.guild.default_role, send_messages=True)
                if (reason is None):
                    reason = "なし"
                embed = discord.Embed(title="🔓 このチャンネルのロックを解除しました。",description="理由: {0}".format(reason),color=discord.Color.blue())
                await ctx.respond(embed=embed)
        else:
            embed = discord.Embed(title="権限はありません。",description="権限 `サーバーを管理` または `チャンネルの管理`が必要です。",color=discord.Color.dark_red())
            await ctx.respond(embed=embed)

    @TextChannelGroup.command(name="info",description="テキストチャンネルの情報を取得します。")
    async def tinfo(self, ctx : ApplicationContext, channel : Option(TextChannel, "テキストチャンネルの情報を取得します")):
        embed = discord.Embed(title=f":speech_balloon: {channel.name} の情報", description="**ID**: {0}".format(channel.id),color=discord.Color.light_grey(),url=f"https://discord.com/channels/{channel.guild.id}/{channel.id}")
        
        if (not channel.topic is None):
            embed.add_field(name="説明", value=channel.topic, inline=False)
        else:
            embed.add_field(name="説明", value="なし", inline=False)

        if (not channel.category is None):
            embed.add_field(name="カテゴリ名", value=f"{str(channel.category)}")

        if (channel.nsfw):
            embed.add_field(name=":underage: NSFWであるか", value="はい")
        else:
            embed.add_field(name=":underage: NSFWであるか", value="いいえ")

        embed.add_field(name="メッセージ遅延", value=f"{channel.slowmode_delay}秒")
        await ctx.respond(embed=embed)

    @TextChannelGroup.command(name="slowmode",description="遅延する時間を設定します。")
    async def setSlow(self, ctx : ApplicationContext, channel : TextChannel, slow : Option(int, "遅延時間を入力"),reason : Option(str, "理由を設定します。", required=False)):
        if (ctx.author.guild_permissions.manage_channels or ctx.author.guild_permissions.manage_guild):
            if (reason is None):
                reason = f"{str(ctx.author)}によって実行されました。"

            if (slow < 0):
                embed = discord.Embed(title="エラーが発生しました。",description="負の数ではない数字を入力してください。",color=discord.Color.dark_red())
                await ctx.respond(embed=embed)
                return

            embed = discord.Embed(title=f"{channel.name}の遅延を設定しました。",description=f"{channel.slowmode_delay}秒 -> {slow}秒に",color=discord.Color.green())
            await channel.edit(slowmode_delay=slow, reason=reason)
            await ctx.respond(embed=embed)
        else:
            embed = discord.Embed(title="エラーが発生しました。",description="権限 `サーバーを管理` または `チャンネルの管理`が必要です。",color=discord.Color.dark_red())
            await ctx.respond(embed=embed)
            return

def setup(bot : discord.Bot):
    bot.add_cog(GuildCommands(bot))