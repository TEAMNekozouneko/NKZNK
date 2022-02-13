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

import traceback
import discord

bot = discord.Bot()

print("Loading Cogs")
print("Loading HelpCommand Cog")
bot.load_extension("Cog.HelpCommand")

print("OK. Loading User Command Cog")
bot.load_extension("Cog.UserCommand")

print("OK. Loading Voice Command Cog")
bot.load_extension("Cog.VoiceCommand")

print("OK. Loading Guild Command Cog")
bot.load_extension("Cog.GuildCommand")

print("OK. Loading Utility Command Cog")
bot.load_extension("Cog.UtilityCommand")

print("OK. Loading Channel Command Cog")
bot.load_extension("Cog.ChannelCommand")

print("OK. Loading Event Cog")
bot.load_extension("Cog.EventListener")
print("Loaded all cog")

print("Authorizing discord bot token.")

bot.run("your bot token here.")