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

import discord, os, aiohttp

from discord import ApplicationContext, Option
from discord.commands import permission, permissions
from discord.ext import commands

from Cog.Util.messages import msgFormat

class voiceCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.slash_command(name="join",description="ボイスチャットに接続します")
    async def ConnectVoiceChannel(self, ctx: ApplicationContext, channel: Option(discord.VoiceChannel,"ボイスチャンネルを選択 (ステージは別コマンド参照)",required=False)):
        if (channel is None):
            if (ctx.author.voice is None):
                embed = msgFormat("error", "voice", "cant_connect_voice", ctx)
                await ctx.respond(embed=embed)
                return
            if (not ctx.guild.voice_client is None):
                await ctx.guild.voice_client.disconnect()
            await ctx.author.voice.channel.connect(timeout=30.0,reconnect=True)
            embed = discord.Embed(title="正常にチャンネルに接続しました。",description=f"正常に {ctx.author.voice.channel.mention} に接続しました", color=discord.Color.green())
            await ctx.respond(embed=embed)
        else:
            if (not ctx.guild.voice_client is None):
                await ctx.guild.voice_client.disconnect()
            await channel.connect(timeout=30.0,reconnect=True)
            embed = discord.Embed(title="正常にチャンネルに接続しました。",description=f"正常に {channel.mention} に接続しました", color=discord.Color.green())
            await ctx.respond(embed=embed)

    @commands.slash_command(name="joins",description="ステージチャットに接続します")
    async def ConnectStageChannel(self, ctx, channel: Option(discord.StageChannel,"ステージチャンネルを選択 (ボイスチャットは別コマンド参照)",required=False)):
        if (channel is None):
            if (ctx.author.voice is None):
                embed = msgFormat("error", "voice", "cant_connect_stage", ctx)
                await ctx.respond(embed=embed)
                return
            if (not ctx.guild.voice_client is None):
                await ctx.guild.voice_client.disconnect()
            await ctx.author.voice.channel.connect(timeout=30.0,reconnect=True)
            embed = discord.Embed(title="正常にチャンネルに接続しました。",description=f"正常に {ctx.author.voice.channel.mention} に接続しました", color=discord.Color.green())
            await ctx.respond(embed=embed)
        else:
            if (not ctx.guild.voice_client is None):
                await ctx.guild.voice_client.disconnect()
            await channel.connect(timeout=30.0,reconnect=True)
            embed = discord.Embed(title="正常にチャンネルに接続しました。",description=f"正常に {channel.mention} に接続しました", color=discord.Color.green())
            await ctx.respond(embed=embed)
    
    @commands.slash_command(name="disconnect",description="ボイス | ステージチャンネルから切断します。")
    async def DisconnectVS(self, ctx):
        if (ctx.guild.voice_client is None):
            embed = msgFormat("error", "voice", "already_disconnected", ctx)
        else:
            embed = discord.Embed(title="正常にチャンネルから切断しました。",description=f"正常に {ctx.guild.voice_client.channel.mention} から切断しました", color=discord.Color.red())
            await ctx.guild.voice_client.disconnect()
        await ctx.respond(embed=embed)

    @commands.slash_command(name="play",description="音楽をURL経由で再生します。(YouTubeは再生できません。)")
    async def PlayMusic(self, ctx: ApplicationContext, attachment: Option(discord.Attachment, "ファイルを添付して再生します。", required=False), url: Option(str,"URLを入力...",required=False),volume: Option(int,"ボリューム 0% から 100%",required=False)):
        await ctx.defer()

        if (not volume is None):
            volume = volume / 100
        else:
            volume = 1

        if (ctx.author.guild.voice_client is None):
            embed = msgFormat("error", "voice", "not_connected", ctx)
        elif (ctx.author.guild.voice_client.is_paused()):
            ctx.author.guild.voice_client.resume()
            embed = discord.Embed(title="音楽を再開しました。", color=discord.Color.purple())
        elif (ctx.author.guild.voice_client.is_playing()):
            embed = msgFormat("error", "voice", "already_played", ctx)
        elif (url is None):
            await attachment.save(f"temp/{ctx.guild_id}_TEMP.mp3")
            embed = discord.Embed(title="音楽を再生します...", color=discord.Color.purple())
            ctx.guild.voice_client.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(f"temp/{ctx.guild_id}_TEMP.mp3"), volume=volume))
        else:
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
    async def StopMusic(self, ctx: ApplicationContext):
        await ctx.defer()
        if (ctx.guild.voice_client is None):
            embed = msgFormat("error", "voice", "not_connected", ctx)
        else:
            ctx.guild.voice_client.stop()
            embed = discord.Embed(title="音楽を停止しました。", color=discord.Color.purple())
        await ctx.respond(embed=embed)

    @commands.slash_command(name="speak",description="Google TTSで喋ります")
    async def SpeakTTS(self, ctx, string : Option(str,"喋るテキスト")):
        await ctx.defer()
        if (not ctx.author.guild.voice_client.is_playing()):
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://www.google.com/speech-api/v1/synthesize?text={string}&nc=mpeg&lang=ja&speed=0.5&client=lr-language-tts') as speak:
                    if (not os.path.exists("temp/")):
                        os.mkdir("temp/")
                    with open(f"temp/{ctx.guild.id}_SPEAK_TEMP.mp3", mode="wb") as f:
                        f.write(await speak.read())
            ctx.author.guild.voice_client.play(discord.FFmpegPCMAudio(f"temp/{ctx.guild_id}_SPEAK_TEMP.mp3"))      
            await ctx.respond(f"{str(ctx.author)}: {string}")
    
    @commands.slash_command(name="pause", description="音楽を一時停止します。")
    async def PauseMusic(self, ctx : ApplicationContext):
        if (ctx.author.guild.voice_client is None):
            embed = msgFormat("error", "voice", "not_connected", ctx)
        else:
            ctx.author.guild.voice_client.pause()
            embed = discord.Embed(title="音楽を一時停止しました。", color=discord.Color.purple())

        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(voiceCommand(bot))