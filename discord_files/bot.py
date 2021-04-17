import discord
from discord.ext import commands
import os
import random

intent = discord.Intents.all()
client = commands.Bot(command_prefix = '-',intents = intent)
@client.event
async def on_ready():
    load_cogs()
    await client.change_presence(activity=discord.Game(name='-aj para ajuda'))
    print('The Bot is ready.')
    

def load_cogs():
    dirname = os.path.dirname(__file__)
    path = os.path.join(dirname, 'cogs')
    for filename in os.listdir(path):
        if filename.endswith('.py'):
            try:
                client.load_extension(f'cogs.{filename[:-3]}')
            except discord.ext.commands.errors.ExtensionAlreadyLoaded:
                pass

@client.command(aliases=["aj"])
async def ajuda(ctx, specification = "Default"):
    print(len(await ctx.guild.chunk()))
    embed = discord.Embed(
        title = "Comandos",
        description = "Comandos que o IsButSeries consegue executar",
        colour = discord.Colour.blue()
    )
    embed.set_image(url = "https://cdn.discordapp.com/avatars/635103218963185704/9b133025ecb81c1357c1bea2dae1f32c.png?size=1024")
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/635103218963185704/9b133025ecb81c1357c1bea2dae1f32c.png?size=1024")
    embed.set_author(name="Jahn#2779")
    if specification == "Default":
        embed.add_field(name = "limparchato <numero>",value = "Limpa um número de mensagens",inline=False)
        embed.add_field(name = "ban <pessoa>",value = "Inicia um votação para banir alguém",inline=False)
        embed.add_field(name = "corona",value = "Mostra os casos de Corona no Brasil",inline=False)
        embed.add_field(name="d5",value= "Mostra os próximos jogos de CS",inline=False)
        embed.add_field(name="meme",value= "Manda um meme",inline=False)
        embed.add_field(name="Jogos",value= "Digite -ajuda jogos para mais informações",inline=True)
    elif specification == "jogos":
        embed.add_field(name = "jogar <jogo>",value = "Joga determinado jogo",inline=False)
        embed.add_field(name = "velha",value = "Jogo da velha ",inline=False)
        embed.add_field(name = "truco",value = "Jogo do truco ",inline=False)
        embed.add_field(name = "uno",value = "Jogo do uno ",inline=False)
    await ctx.send(embed=embed)











client.run("NjM1MTAzMjE4OTYzMTg1NzA0.XasOHg.WNlYqVdOvDklEsDWN9kGKl9TJ9s")
