import discord
from discord.ext import commands 
import os
from dotenv import load_dotenv
from threading import Thread

bot = commands.Bot(command_prefix = '"', case_insensitive = True)
bot.load_extension("jishaku")
bot.colour = 0x204566

@bot.event
async def on_ready():
    print("Ready as", bot.user)

for a in os.listdir("./cogs"):
    if a.endswith(".py"):
        bot.load_extension(f"cogs.{a[:-3]}")

def bot_run():
    load_dotenv(dotenv_path=".env")
    token = os.environ.get("token")
    bot.run(token)

def run_bot():
    t = Thread(target=bot_run)
    t.start()