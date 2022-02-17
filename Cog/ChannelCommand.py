import discord

from discord import SlashCommandGroup, ApplicationContext, Option, StageChannel, TextChannel, VoiceChannel, VoiceRegion

from discord.ext import commands

import Cog.AC as auto_complete

class ChannelCommand(commands.Cog):

    def __init__(self, bot : discord.Bot):
        self.bot = bot
        self._last_member_ = None

    channelGroup = SlashCommandGroup("channel","チャンネル関係のコマンドです。")

    TextChannelGroup = channelGroup.create_subgroup("text", "テキストチャンネルのコマンドです。")

    @TextChannelGroup.command(name="nsfw",description="NSFWの有無効化ができます。")
    async def nsfw(self, ctx : ApplicationContext, channel : Option(TextChannel, "NSFWを設定するチャンネルを選択"), nsfw : Option(bool, "はいならTrue、いいえならFalse"), reason : Option(str, "理由を入力", required=False)):
        await ctx.defer()
        if (ctx.author.guild_permissions.manage_channels or ctx.author.guild_permissions.manage_guild):
            if (nsfw):
                await channel.edit(nsfw=nsfw, reason=reason)
                embed = discord.Embed(title=f"🔞 {channel.name} のNSFWを無効化しました。")
            else:
                await channel.edit(nsfw=nsfw, reason=reason)
                embed = discord.Embed(title=f"🔞 {channel.name} のNSFWを有効化しました。")
        else:
            embed = discord.Embed(title="権限がありません。",description="権限 `サーバーを管理` または `チャンネルの管理`が必要です。",color=discord.Color.dark_red())
        await ctx.respond(embed=embed)

    @TextChannelGroup.command(name="lock",description="@everyoneからの送信をできなくします。(再実行で解除)")
    async def lock(self, ctx : ApplicationContext, channel : Option(TextChannel,"ロックするチャンネルを選択"), reason : Option(str, "理由を入力", required=False)):
        await ctx.defer()
        print()
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
        await ctx.defer()
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
    async def setSlow(self, ctx : ApplicationContext, channel : Option(TextChannel, "遅延を設定するチャンネルを入力"), slow : Option(int, "遅延時間を入力"),reason : Option(str, "理由を設定します。", required=False)):
        await ctx.defer()
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

    VoiceChannelGroup = channelGroup.create_subgroup("voice", "ボイスチャンネルのコマンドです")

    @VoiceChannelGroup.command(name="info", description="ボイスチャンネルの情報を取得します。")
    async def vinfo(self, ctx : ApplicationContext, channel : Option(VoiceChannel, "ボイスチャンネルを選択")):
        await ctx.defer()
        embed = discord.Embed(title=f":loud_sound: {channel.name} の情報", description=f"**ID**: {channel.id}", color=discord.Color.light_grey())

        if (not channel.category is None):
            embed.add_field(name="カテゴリ名", value=f"{str(channel.category)}")

        embed.add_field(name="ビットレート", value=f"{channel.bitrate / 1000} Kbps (最大: {channel.guild.bitrate_limit / 1000} Kbps)")
        
        if (channel.rtc_region is None):
            embed.add_field(name="サーバー", value="自動", inline=False)
        else:
            if (channel.rtc_region == VoiceRegion.amsterdam):
                embed.add_field(name="サーバー", value=":flag_nl: アムステルダム（オランダ）", inline=False)
            elif (channel.rtc_region == VoiceRegion.brazil):
                embed.add_field(name="サーバー", value=":flag_br: ブラジル", inline=False)
            elif (channel.rtc_region == VoiceRegion.dubai):
                embed.add_field(name="サーバー", value=":flag_ae: ドバイ（アラブ首長国連邦）", inline=False)
            elif (channel.rtc_region == VoiceRegion.eu_central):
                embed.add_field(name="サーバー", value=":flag_eu: EU（中央）", inline=False)
            elif (channel.rtc_region == VoiceRegion.eu_west):
                embed.add_field(name="サーバー", value=":flag_eu: EU（西）", inline=False)
            elif (channel.rtc_region == VoiceRegion.frankfurt):
                embed.add_field(name="サーバー", value=":flag_hk: フランクフルト（ドイツ）", inline=False)
            elif (channel.rtc_region == VoiceRegion.hongkong):
                embed.add_field(name="サーバー", value=":flag_hk: 香港", inline=False)
            elif (channel.rtc_region == VoiceRegion.india):
                embed.add_field(name="サーバー", value=":flag_in: インド", inline=False)
            elif (channel.rtc_region == VoiceRegion.japan):
                embed.add_field(name="サーバー", value=":flag_jp: 日本", inline=False)
            elif (channel.rtc_region == VoiceRegion.london):
                embed.add_field(name="サーバー", value=":flag_gb: ロンドン（イギリス）", inline=False)
            elif (channel.rtc_region == VoiceRegion.russia):
                embed.add_field(name="サーバー", value=":flag_ru: ロシア連邦", inline=False)
            elif (channel.rtc_region == VoiceRegion.singapore):
                embed.add_field(name="サーバー", value=":flag_sg: シンガポール", inline=False)
            elif (channel.rtc_region == VoiceRegion.southafrica):
                embed.add_field(name="サーバー", value=":flag_za: 南アフリカ", inline=False)
            elif (channel.rtc_region == VoiceRegion.south_korea):
                embed.add_field(name="サーバー", value=":flag_kr: 韓国", inline=False)
            elif (channel.rtc_region == VoiceRegion.sydney):
                embed.add_field(name="サーバー", value=":flag_au: シドニー", inline=False)
            elif (channel.rtc_region == VoiceRegion.us_central):
                embed.add_field(name="サーバー", value=":flag_us: アメリカ合衆国（中央）", inline=False)
            elif (channel.rtc_region == VoiceRegion.us_east):
                embed.add_field(name="サーバー", value=":flag_us: アメリカ合衆国（東）", inline=False)
            elif (channel.rtc_region == VoiceRegion.us_south):
                embed.add_field(name="サーバー", value=":flag_us: アメリカ合衆国（南）", inline=False)
            elif (channel.rtc_region == VoiceRegion.us_west):
                embed.add_field(name="サーバー", value=":flag_us: アメリカ合衆国（西）", inline=False)
            elif (channel.rtc_region == VoiceRegion.vip_amsterdam):
                embed.add_field(name="サーバー", value=":flag_nl: :gem: VIP用 アムステルダム（オランダ）", inline=False)
            elif (channel.rtc_region == VoiceRegion.vip_us_east):
                embed.add_field(name="サーバー", value=":flag_us: :gem: VIP用 アメリカ合衆国（東）", inline=False)
            elif (channel.rtc_region == VoiceRegion.vip_us_west):
                embed.add_field(name="サーバー", value=":flag_us: :gem: VIP用 アメリカ合衆国（西）", inline=False)

        if (channel.user_limit == 0):
            embed.add_field(name="人数制限", value=f"無制限")
        else:
            embed.add_field(name="人数制限", value=f"{channel.user_limit}人")
        await ctx.respond(embed=embed)
    
    @VoiceChannelGroup.command(name="limit", description="ユーザーの制限数を設定します。")
    async def setLimit(self, ctx : ApplicationContext, channel : Option(VoiceChannel, "制限をつけるチャンネルを選択"), limit : Option(int, "制限人数を入力（0にすると制限解除）"), reason : Option(str, "理由を入力", required=False)):
        await ctx.defer()
        if (ctx.author.guild_permissions.manage_channels or ctx.author.guild_permissions.manage_guild):
            if (limit > 99):
                embed = discord.Embed(title="エラーが発生しました。", description="制限は99までです。\n100以上の制限は課せられません。（{0}）".format(limit))
            embed = discord.Embed(title=f"{channel.name} の制限を設定しました。", description=f"{channel.user_limit} -> {limit} 人", color=discord.Color.green())
            await channel.edit(user_limit=limit, reason=reason)
            await ctx.respond(embed=embed)
        else:
            embed = discord.Embed(title="エラーが発生しました。",description="権限 `サーバーを管理` または `チャンネルの管理`が必要です。",color=discord.Color.dark_red())
            await ctx.respond(embed=embed)
            return

    @VoiceChannelGroup.command(name="region", description="サーバーの地域を選択")
    async def setRegion(self, ctx : ApplicationContext, channel : VoiceChannel, region : Option(str, "地域を選択", autocomplete=auto_complete.regionSelector), reason : Option(str, "理由を入力", required=False)):
        await ctx.defer()
        if (ctx.author.guild_permissions.manage_channels or ctx.author.guild_permissions.manage_guild):
            if (region in auto_complete.regions):
                r = None
                if (region == "amsterdam"):
                    r = VoiceRegion.amsterdam
                elif (region == "brazil"):
                    r = VoiceRegion.brazil
                elif (region == "dubai"):
                    r = VoiceRegion.dubai
                elif (region == "eu_central"):
                    r = VoiceRegion.eu_central
                elif (region == "eu_west"):
                    r = VoiceRegion.eu_west
                elif (region == "frankfurt"):
                    r = VoiceRegion.frankfurt
                elif (region == "hongkong"):
                    r = VoiceRegion.hongkong
                elif (region == "india"):
                    r = VoiceRegion.india
                elif (region == "japan"):
                    r = VoiceRegion.japan
                elif (region == "london"):
                    r = VoiceRegion.london
                elif (region == "russia"):
                    r = VoiceRegion.russia
                elif (region == "singapore"):
                    r = VoiceRegion.singapore
                elif (region == "southafrica"):
                    r = VoiceRegion.southafrica
                elif (region == "south_korea"):
                    r = VoiceRegion.south_korea
                elif (region == "sydney"):
                    r = VoiceRegion.sydney
                elif (region == "us_central"):
                    r = VoiceRegion.us_central
                elif (region == "us_east"):
                    r = VoiceRegion.us_east
                elif (region == "us_south"):
                    r = VoiceRegion.us_south
                elif (region == "us_west"):
                    r = VoiceRegion.us_west
            else:
                r = None
            if (r is None):
                region = "自動"
            embed = discord.Embed(title=f"{channel.name} のサーバー地域を変更しました。", description=f":earth_asia: {region} に変更", color=discord.Color.green())
            await channel.edit(rtc_region=r, reason=reason)
            await ctx.respond(embed=embed)
        else:
            embed = discord.Embed(title="エラーが発生しました。",description="権限 `サーバーを管理` または `チャンネルの管理`が必要です。",color=discord.Color.dark_red())
            await ctx.respond(embed=embed)
            return

    @VoiceChannelGroup.command(name="bitrate", description="ボイスチャンネルのビットレートを変更します。")
    async def setBitrate(self, ctx : ApplicationContext, channel : Option(VoiceChannel, "ビットレートを変更するチャンネルを選択"), bitrate : Option(int, "ビットレートを指定してください（ブーストしてない限り96Kbps以上不可）"), reason : Option(str, "理由を入力", required=False)):
        await ctx.defer()
        if (ctx.author.guild_permissions.manage_channels or ctx.author.guild_permissions.manage_guild):
            bitrate = bitrate * 1000
            if (bitrate > ctx.author.guild.bitrate_limit):
                embed = discord.Embed(title="エラーが発生しました。", description=f"このサーバーでは、{ctx.author.guild.bitrate_limit / 1000}Kbpsまでしか利用できません。",color=discord.Color.dark_red())
                await ctx.respond(embed=embed)
                return
            elif (bitrate < 8000):
                embed = discord.Embed(title="エラーが発生しました。", description=f"最低でも8Kbps以上を指定する必要があります。",color=discord.Color.dark_red())
                await ctx.respond(embed=embed)
                return
            embed = discord.Embed(title=f"{channel.name} のビットレートを設定しました", description=f"{channel.bitrate / 1000}Kbps -> {bitrate / 1000}Kbps",color=discord.Color.green())
            await channel.edit(bitrate=bitrate, reason=reason)
            await ctx.respond(embed = embed)
        else:
            embed = discord.Embed(title="エラーが発生しました。",description="権限 `サーバーを管理` または `チャンネルの管理`が必要です。",color=discord.Color.dark_red())
            await ctx.respond(embed=embed)
            return

    StageChannelGroup = channelGroup.create_subgroup("stage", "ステージチャンネルのコマンドです。")

    @StageChannelGroup.command(name="info", description="ステージチャンネルの情報を取得します。")
    async def sinfo(self, ctx, channel : StageChannel):
        await ctx.defer()
        embed = discord.Embed(title=f":satellite: {channel.name} の情報", description=f"**ID**: {channel.id}", color=discord.Color.light_grey())

        if (not channel.category is None):
            embed.add_field(name="カテゴリ名", value=f"{str(channel.category)}")

        embed.add_field(name="ビットレート", value=f"{channel.bitrate / 1000} Kbps (最大: {channel.guild.bitrate_limit / 1000} Kbps)")
        
        if (channel.rtc_region is None):
            embed.add_field(name="サーバー", value="自動", inline=False)
        else:
            if (channel.rtc_region == VoiceRegion.amsterdam):
                embed.add_field(name="サーバー", value=":flag_nl: アムステルダム（オランダ）", inline=False)
            elif (channel.rtc_region == VoiceRegion.brazil):
                embed.add_field(name="サーバー", value=":flag_br: ブラジル", inline=False)
            elif (channel.rtc_region == VoiceRegion.dubai):
                embed.add_field(name="サーバー", value=":flag_ae: ドバイ（アラブ首長国連邦）", inline=False)
            elif (channel.rtc_region == VoiceRegion.eu_central):
                embed.add_field(name="サーバー", value=":flag_eu: EU（中央）", inline=False)
            elif (channel.rtc_region == VoiceRegion.eu_west):
                embed.add_field(name="サーバー", value=":flag_eu: EU（西）", inline=False)
            elif (channel.rtc_region == VoiceRegion.frankfurt):
                embed.add_field(name="サーバー", value=":flag_hk: フランクフルト（ドイツ）", inline=False)
            elif (channel.rtc_region == VoiceRegion.hongkong):
                embed.add_field(name="サーバー", value=":flag_hk: 香港", inline=False)
            elif (channel.rtc_region == VoiceRegion.india):
                embed.add_field(name="サーバー", value=":flag_in: インド", inline=False)
            elif (channel.rtc_region == VoiceRegion.japan):
                embed.add_field(name="サーバー", value=":flag_jp: 日本", inline=False)
            elif (channel.rtc_region == VoiceRegion.london):
                embed.add_field(name="サーバー", value=":flag_gb: ロンドン（イギリス）", inline=False)
            elif (channel.rtc_region == VoiceRegion.russia):
                embed.add_field(name="サーバー", value=":flag_ru: ロシア連邦", inline=False)
            elif (channel.rtc_region == VoiceRegion.singapore):
                embed.add_field(name="サーバー", value=":flag_sg: シンガポール", inline=False)
            elif (channel.rtc_region == VoiceRegion.southafrica):
                embed.add_field(name="サーバー", value=":flag_za: 南アフリカ", inline=False)
            elif (channel.rtc_region == VoiceRegion.south_korea):
                embed.add_field(name="サーバー", value=":flag_kr: 韓国", inline=False)
            elif (channel.rtc_region == VoiceRegion.sydney):
                embed.add_field(name="サーバー", value=":flag_au: シドニー", inline=False)
            elif (channel.rtc_region == VoiceRegion.us_central):
                embed.add_field(name="サーバー", value=":flag_us: アメリカ合衆国（中央）", inline=False)
            elif (channel.rtc_region == VoiceRegion.us_east):
                embed.add_field(name="サーバー", value=":flag_us: アメリカ合衆国（東）", inline=False)
            elif (channel.rtc_region == VoiceRegion.us_south):
                embed.add_field(name="サーバー", value=":flag_us: アメリカ合衆国（南）", inline=False)
            elif (channel.rtc_region == VoiceRegion.us_west):
                embed.add_field(name="サーバー", value=":flag_us: アメリカ合衆国（西）", inline=False)
            elif (channel.rtc_region == VoiceRegion.vip_amsterdam):
                embed.add_field(name="サーバー", value=":flag_nl: :gem: VIP用 アムステルダム（オランダ）", inline=False)
            elif (channel.rtc_region == VoiceRegion.vip_us_east):
                embed.add_field(name="サーバー", value=":flag_us: :gem: VIP用 アメリカ合衆国（東）", inline=False)
            elif (channel.rtc_region == VoiceRegion.vip_us_west):
                embed.add_field(name="サーバー", value=":flag_us: :gem: VIP用 アメリカ合衆国（西）", inline=False)
        await ctx.respond(embed = embed)

    @StageChannelGroup.command(name="region", description="サーバーの地域を設定します。")
    async def setsRegion(self, ctx : ApplicationContext, channel : StageChannel, region : Option(str, "サーバーの地域を選択", autocomplete=auto_complete.sregionSelector), reason : Option(str, "理由を入力", required=False)):
        await ctx.defer()
        if (ctx.author.guild_permissions.manage_channels or ctx.author.guild_permissions.manage_guild):
            if (region in auto_complete.sregions):
                r = None
                if (region == "amsterdam"):
                    r = VoiceRegion.amsterdam
                elif (region == "brazil"):
                    r = VoiceRegion.brazil
                elif (region == "dubai"):
                    r = VoiceRegion.dubai
                elif (region == "eu_central"):
                    r = VoiceRegion.eu_central
                elif (region == "eu_west"):
                    r = VoiceRegion.eu_west
                elif (region == "frankfurt"):
                    r = VoiceRegion.frankfurt
                elif (region == "hongkong"):
                    r = VoiceRegion.hongkong
                elif (region == "india"):
                    r = VoiceRegion.india
                elif (region == "japan"):
                    r = VoiceRegion.japan
                elif (region == "london"):
                    r = VoiceRegion.london
                elif (region == "russia"):
                    r = VoiceRegion.russia
                elif (region == "singapore"):
                    r = VoiceRegion.singapore
                elif (region == "southafrica"):
                    r = VoiceRegion.southafrica
                elif (region == "south_korea"):
                    r = VoiceRegion.south_korea
                elif (region == "sydney"):
                    r = VoiceRegion.sydney
                elif (region == "us_central"):
                    r = VoiceRegion.us_central
                elif (region == "us_east"):
                    r = VoiceRegion.us_east
                elif (region == "us_south"):
                    r = VoiceRegion.us_south
                elif (region == "us_west"):
                    r = VoiceRegion.us_west
            else:
                r = None
            if (r is None):
                region = "自動"
            embed = discord.Embed(title=f"{channel.name} のサーバー地域を変更しました。", description=f":earth_asia: {region} に変更", color=discord.Color.green())
            await channel.edit(rtc_region=r, reason=reason)
            await ctx.respond(embed=embed)
        else:
            embed = discord.Embed(title="エラーが発生しました。",description="権限 `サーバーを管理` または `チャンネルの管理`が必要です。",color=discord.Color.dark_red())
            await ctx.respond(embed=embed)
            return

def setup(bot : discord.Bot):
    bot.add_cog(ChannelCommand(bot))