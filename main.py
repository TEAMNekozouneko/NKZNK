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

print("Starting...")

print("Loading Modules")

import discord, json, sys, os
import Cog.Util.util_func as func

if (not os.path.exists("config.json")):
    print("Generating Default Config...")
    func.resetConfig()
    print("Generated. please check config.json file")
    sys.exit()

# 設定を読み込む
config_file = open("config.json", "r")

config_dict = json.load(config_file)

if (not config_dict["accept_license"]):
    print("you is not accepted licese, please check config.json file")
    sys.exit()

bot = discord.Bot()

print("Loading Default Exetensions")

for exts in config_dict["extensions"]["default_exts"]:
    print(f"loading {exts}...")
    bot.load_extension(exts)

print("Loading Add-on Exetensions")

for aexts in config_dict["extensions"]["addon_exts"]:
    print(f"loading {aexts}...")

print("Loaded all cog")

print("Authorizing discord bot token.")

try:
    token = str(config_dict["settings"]["token"])
    bot.run(token)
except discord.errors.LoginFailure:
    print("Failed login. please check config.json file")
    sys.exit()
