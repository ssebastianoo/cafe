import discord
from discord.ext import commands 
import json
import os

class Cafe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 

    @commands.command(usage = "title | story")
    async def post(self, ctx, *, args):
        args = args.split(" | ")
        title = args[0]
        story = args[1]

        file_name = str(title.replace(" ", "_").lower())

        end = False

        number = 0
        while not end:
            if f"{file_name}.txt" in os.listdir("./data/stories"):
                number += 1
                if number > 1:
                    file_name = (file_name[:-1] + "_" + str(number))
                else:
                    file_name = (file_name + "_" + str(number))
                end = False

            else:
                end = True

        filepath = f"data/stories/{file_name}.txt"
        
        file = open(filepath, "w")
        file.write(story)
        file.close()

        with open("data/stories.json", "r") as f:
            l = json.load(f)

        l[str(file_name)] = {"title": str(title), "file": str(f"{file_name}.txt"), "writer": {"id": int(ctx.author.id), "name": str(ctx.author)}}

        with open("data/stories.json", "w") as f:
            json.dump(l, f, indent = 4)

        await ctx.send(f"Done! Published at https://cafe.seba.gq/{file_name}")

    @commands.command(aliases = ["delete", "del"])
    async def remove(self, ctx, *, story):

      "Remove a story you created"

      with open("data/stories.json", "r") as f:
        l = json.load(f)

      try:
        story_ = l[str(story)]

      except KeyError:
        return await ctx.send("Story not found.")

      if int(story_["writer"]["id"]) != ctx.author.id:
        return await ctx.send("You are not the author of this story.")

      os.remove(f"data/stories/{story_['file']}")
      
      l.pop(str(story))

      with open("data/stories.json", "w") as f:
        json.dump(l, f, indent = 4)

      await ctx.send("Done!")

    @commands.command()
    async def list(self, ctx, *, member: discord.Member = None):

      "List of all the stories."

      with open("data/stories.json", "r") as f:
        l = json.load(f)

      if not member:
        res = ""
        for a in l:
          res += f"[{l[a]['title']}](https://cafe.seba.gq/{a})\n"
          # res += f"https://cafe.seba.gq/{a}\n"

      else:
        res = ""
        for a in l:
          if int(l[a]["writer"]["id"]) == member.id: 
            res += f"[{l[a]['title']}](https://cafe.seba.gq/{a})\n"

      if res == "" or res == " ":
        emb = discord.Embed(description = f"{member.mention} has no stories!", colour = discord.Colour.red())
        return await ctx.send(embed = emb)

      emb = discord.Embed(description = res, colour = 0x204566)
      emb.set_author(name = "Stories List", url = "https://cafe.seba.gq", icon_url = str(self.bot.user.avatar_url_as(static_format = "png")))
        
      await ctx.send(embed = emb)
        
def setup(bot):
    bot.add_cog(Cafe(bot))