from urllib.request import urlretrieve
from discord.ext import commands
from discord import Option, option
from discord.ext import pages
import discord
import requests

class voiceCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.slash_command(name="join",description="ボイスチャットに接続します")
    async def join(self, ctx, channel: Option(discord.VoiceChannel,"ボイスチャンネルを選択 (ステージは別コマンド参照)",required=False)):
        if (channel is None):
            if (ctx.author.voice is None):
                embed = discord.Embed(title="エラーが発生しました。",description="例外が発生しました。以下の内容を参照してください。",color=discord.Color.dark_red())
                embed.add_field(name="対処方法",value="・ボイスチャンネルへ接続\n・ボイスチャンネルを選択する")
                await ctx.respond(embed=embed)
                return
            await ctx.author.voice.channel.connect(timeout=30.0,reconnect=True)
            embed = discord.Embed(title="正常にチャンネルに接続しました。",description=f"正常に {ctx.author.voice.channel.mention} に接続しました", color=discord.Color.green())
            await ctx.respond(embed=embed)
        else:
            await channel.connect(timeout=30.0,reconnect=True)
            embed = discord.Embed(title="正常にチャンネルに接続しました。",description=f"正常に {channel.mention} に接続しました", color=discord.Color.green())
            await ctx.respond(embed=embed)

    @commands.slash_command(name="joins",description="ステージチャットに接続します")
    async def joins(self, ctx, channel: Option(discord.StageChannel,"ステージチャンネルを選択 (ボイスチャットは別コマンド参照)",required=False)):
        if (channel is None):
            if (ctx.author.voice is None):
                embed = discord.Embed(title="エラーが発生しました。",description="例外が発生しました。以下の内容を参照してください。",color=discord.Color.dark_red())
                embed.add_field(name="対処方法",value="・ステージチャンネルへ接続\n・ステージチャンネルを選択する")
                await ctx.respond(embed=embed)
                return
            await ctx.author.voice.channel.connect(timeout=30.0,reconnect=True)
            embed = discord.Embed(title="正常にチャンネルに接続しました。",description=f"正常に {ctx.author.voice.channel.mention} に接続しました", color=discord.Color.green())
            await ctx.respond(embed=embed)
        else:
            await channel.connect(timeout=30.0,reconnect=True)
            embed = discord.Embed(title="正常にチャンネルに接続しました。",description=f"正常に {channel.mention} に接続しました", color=discord.Color.green())
            await ctx.respond(embed=embed)
    
    @commands.slash_command(name="disconnect",description="ボイス | ステージチャンネルから切断します。")
    async def dc(self, ctx):
        if (ctx.guild.voice_client is None):
            await ctx.respond("おそらくすでに切断されています。")
            return
        else:
            embed = discord.Embed(title="正常にチャンネルから切断しました。",description=f"正常に {ctx.guild.voice_client.channel.mention} から切断しました", color=discord.Color.red())
            await ctx.guild.voice_client.disconnect()
            await ctx.respond(embed=embed)

    @commands.slash_command(name="play",description="音楽をURL経由で再生します。(YouTubeは再生できません。)")
    async def urlplay(self, ctx, url : Option(str,"URLを入力...",required=False),volume: Option(int,"ボリューム 0% から 100%",required=False)):
        if (not volume is None):
            volume = volume / 100
        else:
            volume = 1
        await ctx.defer()
        urlResponse = requests.get(url).content
        with open(f"temp/{ctx.guild_id}_TEMP.mp3",mode="wb") as f:
            f.write(urlResponse)
        ctx.guild.voice_client.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(f"temp/{ctx.guild_id}_TEMP.mp3"), volume=volume))
        await ctx.respond("Playing...")

    @commands.slash_command(name="stop",description="音楽を停止します。")
    async def musicstop(self,ctx):
        try:
            ctx.guild.voice_client.stop()
            await ctx.respond("停止しました。")
        except:
            await ctx.respond("すでに停止しています。")

def setup(bot):
    bot.add_cog(voiceCommand(bot))
