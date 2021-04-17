import discord
from discord.ext import commands
from webscrap import meme_scraper


class WebCommands(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command()
    async def meme(self, ctx):
        await ctx.send(embed=meme_scraper.get_meme())



def setup(client):
    client.add_cog(WebCommands(client))