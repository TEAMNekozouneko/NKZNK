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

import os
from discord.ext import commands
from discord import ApplicationContext, Guild, Option, SlashCommandGroup, option
from discord.ext import pages
import discord
import aiohttp

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
    async def urlplay(self, ctx: ApplicationContext, url : Option(str,"URLを入力...",required=False),volume: Option(int,"ボリューム 0% から 100%",required=False)):
        if (ctx.author.guild.voice_client.is_paused()):
            ctx.author.guild.voice_client.resume()
            await ctx.respond("再開しました。")
            return
        if (not volume is None):
            volume = volume / 100
        else:
            volume = 1
        await ctx.defer()
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                urlResponse = await r.read()
                if (not os.path.exists("temp/")):
                    os.mkdir("temp/")
                with open(f"temp/{ctx.guild_id}_TEMP.mp3",mode="wb") as f:
                    f.write(urlResponse)
        embed = discord.Embed(title="音楽を再生します...", color=discord.Color.purple())
        ctx.guild.voice_client.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(f"temp/{ctx.guild_id}_TEMP.mp3"), volume=volume))
        await ctx.respond(embed=embed)

    @commands.slash_command(name="stop",description="音楽を停止します。")
    async def musicstop(self,ctx):
        try:
            ctx.guild.voice_client.stop()
            await ctx.respond("停止しました。")
        except:
            await ctx.respond("すでに停止しています。")      

    @commands.slash_command(name="speak",description="Google TTSで喋ります")
    async def speak(self, ctx, string : Option(str,"喋るテキスト")):
        await ctx.defer()
        if (not ctx.author.guild.voice_client.is_playing()):
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://www.google.com/speech-api/v1/synthesize?text={string}&nc=mpeg&lang=ja&speed=0.5&client=lr-language-tts') as speak:
                    if (not os.path.exists("temp/")):
                        os.mkdir("temp/")
                    with open(f"temp/{ctx.guild.id}_SPEAK_TEMP.mp3", mode="wb") as f:
                        f.write(await speak.read())
            ctx.guild.voice_client.play(discord.FFmpegPCMAudio(f"temp/{ctx.guild_id}_SPEAK_TEMP.mp3"))      
            await ctx.respond(f"{str(ctx.author)}: {string}")
    
    @commands.slash_command(name="pause", description="音楽を一時停止します。")
    async def pausem(self, ctx : ApplicationContext):
        if (ctx.guild.voice_client is None):
            await ctx.respond("すでに音楽が再生されていないか、一時停止済みです。")
        else:
            ctx.author.guild.voice_client.resume()
            await ctx.respond("一時停止しました。")

def setup(bot):
    bot.add_cog(voiceCommand(bot))