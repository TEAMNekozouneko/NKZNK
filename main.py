import discord
from discord.commands import *
import asyncio

bot = discord.Bot()

bot.load_extension("help_command")
bot.load_extension("user_command")
bot.load_extension("voice_command")

bot.run("Your token here.")
