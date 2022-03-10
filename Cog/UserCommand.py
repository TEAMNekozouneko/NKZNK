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

from discord import ApplicationContext, Option, SlashCommandGroup

from discord.ext import commands
from discord.ext import pages

import datetime

from math import floor

from Cog.Util.messages import msgFormat

class userCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    UserCommandGroup = SlashCommandGroup("user", "ユーザーに関するコマンドです。")

    @UserCommandGroup.command(name="info",description="ユーザー情報を取得します。")
    async def LookupUser(self, ctx, member : Option(discord.Member,"取得するユーザーを選択。")):
        if (not isinstance(member, discord.Member)):
            embed = msgFormat("error", "failed", "member", ctx)
            await ctx.respond(embed=embed)
            return
        await ctx.defer()
        lookupinfos = [
            discord.Embed(title=f'{str(member)}の情報 - 基本情報',description=f"**ID** {member.id}",colour=member.color),
            discord.Embed(title=f'{str(member)}の情報 - 詳細情報',description=f"**ID** {member.id}",colour=member.color),
            discord.Embed(title=f'{str(member)}の情報 - アイコン',description=f"",colour=member.color)
        ]

        utc = member.created_at.timestamp()
        jst = datetime.datetime.fromtimestamp(utc, datetime.timezone(datetime.timedelta(hours=9))).timestamp()
        
        lookupinfos[0].add_field(name="アカウント作成日",value=f"<t:{floor(jst)}>")

        dutc = member.joined_at.timestamp()
        djst = datetime.datetime.fromtimestamp(dutc, datetime.timezone(datetime.timedelta(hours=9))).timestamp()
        
        lookupinfos[0].add_field(name="サーバー参加日",value=f"<t:{floor(djst)}>")
        lookupinfos[1].add_field(name="権限番号 (ハッシュ)",value=f"{hash(member.guild_permissions)}")

        if (member.timed_out):
            lookupinfos[1].add_field(name="タイムアウトされてるか?",value=f"はい、タイムアウトされています。")
        else:
            lookupinfos[1].add_field(name="タイムアウトされてるか?",value=f"いいえ")

        role_mentioned = []
        for role in member.roles:
            role_mentioned = role_mentioned + [role.mention]

        amention = ", ".join(role_mentioned)
        lookupinfos[1].add_field(name="ロールリスト",value=amention,inline=False)

        if (member.guild_avatar is None):
            if (member.avatar is None):
                lookupinfos[0].set_thumbnail(url=member.default_avatar.url)
                lookupinfos[1].set_thumbnail(url=member.default_avatar.url)
                lookupinfos[2].description = member.default_avatar.url
                lookupinfos[2].set_image(url=member.default_avatar.url)
            else:
                lookupinfos[2].description = member.avatar.url
                lookupinfos[2].set_image(url=member.avatar.url)
                lookupinfos[0].set_thumbnail(url=member.avatar.url)
                lookupinfos[1].set_thumbnail(url=member.avatar.url)
        else:
            lookupinfos[2].description = member.guild_avatar.url
            lookupinfos[2].set_image(url=member.guild_avatar.url)
            lookupinfos[0].set_thumbnail(url=member.guild_avatar.url)
            lookupinfos[2].set_thumbnail(url=member.guild_avatar.url)
        pageManager = pages.Paginator(pages=lookupinfos)
        await pageManager.respond(ctx.interaction,ephemeral=True)    

    @UserCommandGroup.command(name="mute", description="ユーザーのマイクをミュートします。")
    async def ServerMute(self, ctx : ApplicationContext, member : Option(discord.Member, "ミュートをするメンバーを選択"), reason : Option(str, "理由を入力", required=False)):
        if (ctx.author.guild_permissions.mute_members):
            if (not member.voice is None):
                if (not member.voice.mute):
                    embed = discord.Embed(title="ミュートしました。", description=f"**対象**: {member.mention}", color=discord.Color.green())
                    await member.edit(mute=True, reason=reason)
                else:
                    embed = discord.Embed(title="ミュートを解除しました。", color=discord.Color.green())
                    await member.edit(mute=False, reason=reason)
            else:
                embed = msgFormat("error", "voice", "not_connected_mute", ctx)
        else:
            embed = msgFormat("error", "permissions", "manage_user_mute")
        await ctx.respond(embed=embed)
    
    @UserCommandGroup.command(name="deafen", description="ユーザーのスピーカーをミュートします。")
    async def ServerDeafen(self, ctx : ApplicationContext, member : Option(discord.Member, "スピーカーミュートをするメンバーを選択"), reason : Option(str, "理由を入力", required=False)):
        if (ctx.author.guild_permissions.deafen_members):
            if (not member.voice is None):
                if (not member.voice.deaf):
                    embed = discord.Embed(title="スピーカーミュートしました。", description=f"**対象**: {member.mention}", color=discord.Color.green())
                    await member.edit(deafen=True, reason=reason)
                else:
                    embed = discord.Embed(title="スピーカーミュートを解除しました。", color=discord.Color.green())
                    await member.edit(deafen=False, reason=reason)
            else:
                embed = msgFormat("error", "voice", "not_connected_mute")
        else:
            embed = msgFormat("error", "permissions", "manage_user_deafen")
        await ctx.respond(embed=embed)

    @UserCommandGroup.command(name="ban", description="ユーザーをBANします。")
    async def BanMember(self, ctx : ApplicationContext, member : Option(discord.Member, "BANするメンバーを選択"), reason : Option(str, "理由を入力", required=False)):
        if (ctx.author.guild_permissions.ban_members):
            embed = discord.Embed(title=f"{str(member)}のアクセスを禁止しました。", description="Banned by an operator.", color=discord.Color.green())
            await member.ban(reason=reason)
            await ctx.respond(embed=embed)
        else:
            embed = msgFormat("error", "permissions", "manage_user_ban")
            await ctx.respond(embed=embed)

    @UserCommandGroup.command(name="kick", description="ユーザーをKickします。")
    async def KickMember(self, ctx : ApplicationContext, member : Option(discord.Member, "Kickするメンバーを選択"), reason : Option(str, "理由を入力", required=False)):
        if (ctx.author.guild_permissions.kick_members):
            embed = discord.Embed(title=f"{str(member)}を追放しました。", description="Kicked by an operator.", color=discord.Color.green())
            await member.kick(reason=reason)
            await ctx.respond(embed=embed)
        else:
            embed = msgFormat("error", "permissions", "manage_user_kick", ctx)
            await ctx.respond(embed=embed)

    @UserCommandGroup.command(name="disconnect", description="ユーザーをボイスチャンネルから切断します。")
    async def DisconnectMember(self, ctx : ApplicationContext, member : discord.Member, reason : Option(str, "理由を入力", required=False)):
        if (ctx.author.guild_permissions.move_members):
            if (not ctx.author.voice is None):
                if (reason is None):
                    reason = "なし"
                embed = discord.Embed(title=f"{str(member)}を切断しました。", description=f"**既存の接続先**: {member.voice.channel.mention}\n**理由**: {reason}", color=discord.Color.green())
                await member.edit(voice_channel=None, reason=reason)
            else:
                embed = msgFormat("error", "voice", "author_not_connected", ctx, member.mention)
        elif (ctx.author == member):
            if (reason is None):
                reason = "なし"
            embed = discord.Embed(title=f"あなたを切断しました。", description=f"**既存の接続先**: {member.voice.channel.mention}\n**理由**: {reason}", color=discord.Color.green())
            await ctx.author.edit(voice_channel=None, reason=reason)
        else:
            embed = msgFormat("error", "permissions", "manage_user_move", ctx)
        await ctx.respond(embed=embed)

def setup(bot):
    return bot.add_cog(userCommand(bot))