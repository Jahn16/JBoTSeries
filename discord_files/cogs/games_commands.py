import discord
from discord.ext import commands
from discord.ext.commands import has_permissions,CheckFailure
from games.uno.uno_game import Uno
from games.tictactoe.tictactoe import TicTacToe
from games.trivia.trivia import Trivia
from games.typeracer.typeracer import TypeRacer
from games.music_quiz.music_quiz import MusicQuiz
from games.guess_drawing.guess_drawing import GuessDrawings
from games.perfil.perfil import Perfil
from games.tournament.tournament import Tournament
from games.werewolf.game import Game
import time

class GamesCommands(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command()
    async def uno(self, ctx):
        uno_game = Uno(ctx,self.client)
        await uno_game.start_game()

    @commands.command()
    async def velha(self, ctx):
        tictactoe = TicTacToe(ctx,self.client)
        await tictactoe.start()

    @commands.command()
    async def velhateste(self, ctx, member: discord.Member):
        tictactoe = TicTacToe(ctx, self.client)
        tictactoe.set_player_one(ctx.author)
        tictactoe.set_player_two(member)
        await tictactoe.start()
        winner = tictactoe.get_winner()
        print(type(winner))
        print(winner)

    @commands.command()
    async def trivia(self, ctx, member: discord.Member):
        trivia = Trivia(ctx,self.client)
        trivia.set_player_one(ctx.author)
        trivia.set_player_two(member)
        await trivia.start()

    @commands.command()
    async def typeracer(self, ctx , member: discord.Member):
        typeracer = TypeRacer(ctx, self.client)
        typeracer.set_player_one(ctx.author)
        typeracer.set_player_two(member)
        await typeracer.start()
        print(typeracer.get_winner().get_discord_member())

    @commands.command()
    async def musicquiz(self, ctx,player2: discord.Member,player1: discord.Member = None):

        musicquiz = MusicQuiz(ctx, self.client)
        if player1 == None:
            musicquiz.set_player_one(ctx.author)
        else:
            musicquiz.set_player_one(player1)
        musicquiz.set_player_two(player2)
        await musicquiz.start()


    @commands.command(aliases=['gd'])
    async def guessdrawings(self, ctx, member: discord.Member=None):
        guessdrawings = GuessDrawings(ctx,self.client)
        guessdrawings.set_player_one(ctx.author)
        guessdrawings.set_player_two(member)
        await guessdrawings.start()



    @commands.command()
    @has_permissions(administrator=True)
    async def torneio(self, ctx ):
        tournament = Tournament(ctx,self.client)
        await tournament.start()

    @commands.command()
    async def torneio_backup(self, ctx,number_upper_bracket_players,number_lower_bracket_players,round_to_be_played,*,members_string):
        tournament = Tournament(ctx, self.client)
        member_converter = discord.ext.commands.MemberConverter()
        members = []
        for member_string in members_string.split(" "):
            member = await member_converter.convert(ctx, member_string)
            members.append(member)
        await tournament.backup(number_upper_bracket_players,number_lower_bracket_players,round_to_be_played,members)

    @commands.command()
    async def torneio_teste(self, ctx, member: discord.Member):
        tournament = Tournament(ctx, self.client)
        tournament.set_players(member)
        await tournament.start()

    @commands.command()
    async def perfil(self, ctx,member: discord.Member):
        game = Perfil(ctx,self.client)
        game.set_player_one(ctx.author)
        game.set_player_two(member)
        await game.start()

    @commands.command()
    async def werewolf(self, ctx):
        if str(ctx.author) == 'Jahn#2779':
            game = Game(ctx,self.client)
            await game.start()
        else:
            await ctx.send('Beta Test eh so pros bonitos')

    @commands.command()
    @has_permissions(administrator=True)
    async def resetorneio(self,ctx):
        guild = ctx.guild
        text_channels = guild.text_channels
        voice_channels = guild.voice_channels
        categories = guild.categories
        roles = guild.roles
        for text_channel in text_channels:
            if text_channel.name.title() in ['Bracket','Partidas','Torcida']:
                await text_channel.delete()
        for voice_channel in voice_channels:
            if voice_channel.name.title() == 'Music Quiz 🎵':
                await voice_channel.delete()
        for category in categories:
            if category.name == 'Torneio':
                await category.delete()
        for role in roles:
            if role.name == 'Competindo':
                await role.delete()



def setup(client):
    client.add_cog(GamesCommands(client))