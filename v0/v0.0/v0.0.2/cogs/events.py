import discord
from discord.ext import commands
from discord import Webhook, AsyncWebhookAdapter
import aiohttp
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path = ".env")

class Events(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.webhook_url = os.environ.get("webhook")

  @commands.Cog.listener()
  async def on_member_join(self, member):
    content = f"**{member.mention} benvenuto!**"
    emb = discord.Embed(description = "Assicurati di leggere <#647039714095792140> e di prendere i ruoli in <#649133528008884266>!", colour = discord.Colour.blurple())
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(self.webhook_url, adapter=AsyncWebhookAdapter(session))
        await webhook.send(content, username = str(member), avatar_url = str(member.avatar_url_as(static_format = "png")), embed = emb)

  @commands.Cog.listener()
  async def on_member_remove(self, member):
    emb = discord.Embed(description = f"Addio {member.mention}...", colour = discord.Colour.red())
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(self.webhook_url, adapter=AsyncWebhookAdapter(session))
        await webhook.send(username = str(member), avatar_url = str(member.avatar_url_as(static_format = "png")), embed = emb)

def setup(bot):
  bot.add_cog(Events(bot))
