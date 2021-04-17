from games.tournament.match import Match
from games.tournament.image_processing.image_drawer import draw_match_data,draw_podium
from .player import Player
from .missing_participants_error import MissingParticipantsError
import discord
from asyncio import TimeoutError
import time
from datetime import date
import os
import random
import pickle
from games.trivia.trivia import Trivia
from games.typeracer.typeracer import TypeRacer
from games.music_quiz.music_quiz import MusicQuiz
from games.guess_drawing.guess_drawing import GuessDrawings
from games.perfil.perfil import Perfil


class Tournament:

    def __init__(self,ctx,client):
        self.ctx = ctx
        self.client = client
        self.upper_bracket_players = []
        self.lower_bracket_players = []


    async def get_participants(self):
        today = date.today().strftime("%d/%m/%Y")
        confirmation_phrase = 'Li e concordo com as instruções, e quero participar.'
        tournament_info = discord.Embed(title = 'ISBUTSERIES ' + today,
                                        description= f'''Você tem a chance de participar do torneio mais competitivo da **América Latina!**
                                                    \n **Leia, as instruções.**
                                                    \n :one: Antes de entrar, certifique-se que você tem disponibilidade de tempo para jogar todas as partidas **(Máximo 5 partidas)**  
                                                    \n :two: O campeonato é baseado no sistema de **dupla eliminatória**, em que todos os perdedores têm uma segunda chance de disputar, passando para uma **"chave de perdedores"**, onde disputam uma nova série eliminatória.  
                                                    \n :three: Em cada partida será disputada um minigame aleatório entre 3 opções **(Jogo da Velha, Corrida de Digitação, e Quiz)**
                                                    \n :four: Para participar mande no chat abaixo: \n**{confirmation_phrase}**''',
                                        color= discord.Colour.from_rgb(255,165,0))
        tournament_info.set_image(url="https://ih1.redbubble.net/image.509923249.4195/flat,750x,075,f-pad,750x1000,f8f8f8.u8.jpg")
        members = self.ctx.guild.members
        await self.ctx.send(embed=tournament_info)
        while len(self.upper_bracket_players) < 8:
            def check(msg):
                return msg.content == confirmation_phrase and msg.author in members
            try:
                message = await self.client.wait_for('message', check=check, timeout = 60)
            except TimeoutError:
                number_of_players = len(self.upper_bracket_players)
                exception = MissingParticipantsError(number_of_players)
                await self.ctx.send(str(exception))
                raise exception
            else:
                participant = Player(message.author)
                if participant not in self.upper_bracket_players:
                    self.upper_bracket_players.append(participant)
                    await self.ctx.send(f'Participação confirmada de **{message.author.display_name}!**')








    def set_players(self,member):
        for _ in range(4):
            new_player = Player(self.ctx.author)
            self.upper_bracket_players.append(new_player)
            new_player = Player(member)
            self.upper_bracket_players.append(new_player)

    async def start(self):
        await self.get_participants()
        random.shuffle(self.upper_bracket_players)
        category, self.announcement_text_channel, self.matches_text_channel, bench_text_channel, competing_role = await self.create_discord_objects()
        self.shuffle_gamemodes()
        bracket_path = 'c:/JboTSeries/games/tournament/image_processing/imgs/ready_bracket.webp'
        podium_path = r'C:\Users\jpfer\OneDrive\Desktop\Tournament\champion_ready.jpg'
        if os.path.exists(bracket_path):
            os.remove(bracket_path)
        if os.path.exists(podium_path):
            os.remove(podium_path)
        await self.upper_bracket_round(1)
        time.sleep(60)
        await self.delete_discord_objects([category,self.announcement_text_channel,self.matches_text_channel,bench_text_channel,competing_role])


    def shuffle_gamemodes(self):
            channel = self.matches_text_channel
            self.gamemodes = []
            games_names = ['Trivia','TypeRacer','MusicQuiz','GuessDrawings','Perfil']

            for _ in range(3):
                random.shuffle(games_names)
                for game_name in games_names:
                    if game_name == 'Trivia':
                        game = Trivia(channel, self.client)
                    elif game_name == 'TypeRacer':
                        game = TypeRacer(channel, self.client)
                    elif game_name == 'MusicQuiz':
                        game = MusicQuiz(channel, self.client)
                    elif game_name == 'GuessDrawings':
                        game = GuessDrawings(channel, self.client)
                    elif game_name == 'Perfil':
                        game = Perfil(channel, self.client)
                    self.gamemodes.append(game)



    async def create_discord_objects(self):
        guild = self.ctx.guild
        category = await guild.create_category('Torneio', position=3)
        self.announcement_text_channel = await category.create_text_channel('Bracket')
        self.matches_text_channel = await category.create_text_channel('Partidas')
        bench_text_channel = await category.create_text_channel('Torcida')
        competing_role = await guild.create_role(name='Competindo', hoist=True,
                                                 colour=discord.Colour.from_rgb(255, 165, 0))
        await bench_text_channel.set_permissions(competing_role, read_messages=False)
        await self.announcement_text_channel.set_permissions(guild.default_role, send_messages=False)
        await self.announcement_text_channel.set_permissions(guild.default_role, read_messages=True)
        await self.matches_text_channel.set_permissions(guild.default_role, send_messages=False)
        await self.matches_text_channel.set_permissions(competing_role, send_messages=True)
        return category,self.announcement_text_channel,self.matches_text_channel,bench_text_channel,competing_role

    async def delete_discord_objects(self,discord_objects_list):
        for discord_object in discord_objects_list:
            await discord_object.delete()



    async def backup(self,number_upper_bracket_players,number_lower_bracket_players,round_to_be_played,members):
        players = []
        for member in members:
            player = Player(member)
            players.append(player)


        self.upper_bracket_players = players[:number_upper_bracket_players]
        self.lower_bracket_players = players[:number_lower_bracket_players]
        category, self.announcement_text_channel, self.matches_text_channel, bench_text_channel, competing_role = await self.create_discord_objects()
        if round_to_be_played in [1,7,11,14]:
            await self.upper_bracket_round(round_to_be_played)
        elif round_to_be_played in [5,9,12,13]:
            await self.lower_bracket_round(round_to_be_played)
        time.sleep(60)
        await self.delete_discord_objects([category, self.announcement_text_channel, self.matches_text_channel, bench_text_channel, competing_role])
        

    def make_matches(self,players,match_id):
        matches = []
        for i in range(0, len(players) - 1, 2):
            new_match = Match(self.matches_text_channel, self.client)
            new_match.set_player_one(players[i])
            new_match.set_player_two(players[i + 1])
            new_match.set_id(match_id)
            new_match.set_game(self.gamemodes[match_id])
            matches.append(new_match)
            match_id += 1
        return matches,match_id

    def draw_matches(self,matches):
        for match in matches:
            draw_match_data(match)

    async def upper_bracket_round(self,match_id):
        matches,match_id = self.make_matches(self.upper_bracket_players,match_id)
        if len(matches) > 0:
            self.draw_matches(matches)
            await self.announcement_text_channel.send(file=discord.File('c:/JboTSeries/games/tournament/image_processing/imgs/ready_bracket.webp'))
            await self.announcement_text_channel.send('**Próximas partidas válidas pelo Upper Bracket:**')
            for match in matches:
                await self.announcement_text_channel.send(f'`{match.get_player_one().get_discord_member().display_name} x {match.get_player_two().get_discord_member().display_name} | MODO DE JOGO: {match.get_game().get_gamemode()}`')
            time.sleep(30)
            for match in matches:
                await match.start()
                winner = match.get_winner()
                loser = match.get_loser()
                if match.get_id() == 14:
                    draw_podium(loser,2)
                    podium_path = draw_podium(winner,1)
                    await self.ctx.send(f'**{winner.get_discord_member().display_name}** foi o campeão  do Torneio! ', file = discord.File(podium_path))
                    return winner
                else:
                    await self.matches_text_channel.send(f'**{winner.get_discord_member().display_name}** ganhou e segue no Upper! **{loser.get_discord_member().display_name}** perdeu e desceu para a Lower!')
                self.upper_bracket_players.remove(loser)
                self.lower_bracket_players.append(loser)

        await self.lower_bracket_round(match_id)


    async def lower_bracket_round(self,match_id):
        matches,match_id = self.make_matches(self.lower_bracket_players,match_id)
        if len(matches) > 0:
            self.draw_matches(matches)

            await self.announcement_text_channel.send(file=discord.File('c:/JboTSeries/games/tournament/image_processing/imgs/ready_bracket.webp'))

            await self.announcement_text_channel.send('**Próximas partidas válidas pelo Lower Bracket:**')
            for match in matches:
                await self.announcement_text_channel.send(f'`{match.get_player_one().get_discord_member().display_name} x {match.get_player_two().get_discord_member().display_name} | MODO DE JOGO: {match.get_game().get_gamemode()}`')
            time.sleep(30)
            for match in matches:
                await match.start()
                loser = match.get_loser()
                winner = match.get_winner()

                self.lower_bracket_players.remove(loser)
                if match.get_id() == 13:
                    winner = match.get_winner()
                    loser = match.get_loser()
                    draw_podium(loser,3)
                    self.upper_bracket_players.append(winner)
                    await self.matches_text_channel.send(f'**{winner.get_discord_member().display_name}** ganhou e sobe para a Grande Final! **{loser.get_discord_member().display_name}** perdeu e foi eliminado da competição!')

                else:
                    await self.matches_text_channel.send(f'**{winner.get_discord_member().display_name}** ganhou e segue na Lower! **{loser.get_discord_member().display_name}** perdeu e foi eliminado da competição!')

        await self.upper_bracket_round(match_id)


    def backup(self):
        backup_file = open('backup','w')
        {

        }
        pickle.dump(self.ctx,backup_file)

    def recover_backup(self):
        backup_file = open('backup', 'r')
        backup = pickle.load(backup_file)
        self.ctx = backup['ctx']
        self.client = backup['client']
        self.upper_bracket_players = backup['upper_bracket_players']
        self.lower_bracket_players = backup['lower_bracket_players']

