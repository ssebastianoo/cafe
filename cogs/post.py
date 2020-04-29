import discord
from discord.ext import commands 
import json
import os

class Post(commands.Cog):
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

        # filepath = os.path.join(r'C:\Users\mediaworld\Documents\Python\cafe\data\stories', f'{file_name}.txt')

        filepath = f"data/stories/{file_name}.txt"
        
        file = open(filepath, "w")
        file.write(story)
        file.close()

        with open("data/stories.json", "r") as f:
            l = json.load(f)

        l[str(file_name)] = {"title": str(title), "file": str(f"{file_name}.txt")}

        with open("data/stories.json", "w") as f:
            json.dump(l, f, indent = 4)

        await ctx.send(f"Done! Published at https://CafeAPI.ssebastianoo.repl.co/{file_name}")

def setup(bot):
    bot.add_cog(Post(bot))