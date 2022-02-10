from discord.ext import commands
from discord import Option
from discord.ext import pages
import discord
import datetime
from math import *

class userCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.slash_command(name="user",description="ユーザー情報を取得します。")
    async def lookup(self, ctx, member : Option(discord.Member,"取得するユーザーを選択。")):
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

    

def setup(bot):
    return bot.add_cog(userCommand(bot))