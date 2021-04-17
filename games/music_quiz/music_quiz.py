import discord
#from .player import Player
from games.music_quiz.player import Player
import random
import time
import os
from asyncio import TimeoutError
from difflib import SequenceMatcher
import youtube_dl
from math import fabs
from games.music_quiz.song import Song

class MusicQuiz():

    def __init__(self, ctx, client):
        self.ctx = ctx
        self.client = client
        self.delete_songs()
        self.get_songs()

    def get_songs(self):
        self.songs = []
        dirname = os.path.dirname(__file__)
        songs_path = os.path.join(dirname, 'songs.txt')
        songs_file = open(file=songs_path, mode = 'r',encoding='utf-8')
        lines = songs_file.readlines()

        for line in lines:
            try:
                line = line.rstrip()
                url,author,title = line.split(' - ')
                song = Song()
                song.set_url(url)
                song.set_title(title)
                song.set_author(author)
                self.songs.append(song)
            except Exception:
                pass
        random.shuffle(self.songs)

    def get_gamemode(self):
        return "Quiz de Música"

    def set_player_one(self, player_one):
        self.player_one = Player(player_one)

    def set_player_two(self, player_two):
        self.player_two = Player(player_two)

    async def start(self):

        guild = self.ctx.guild
        categories = guild.categories
        game_info =  discord.Embed(title= 'Music Quiz 🎵',
                                   colour = discord.Colour.purple())
        game_info.add_field(name='Regras:',value='''Serão jogados **5** rounds, em cada um deles uma música será tocada.
                                    O jogadores tem que acertar o **título** e **autor** da música em um tempo de no máximo 90 segundos.
                                    **OBS:** Quanto mais rápido for o acerto mais pontos serão obtidos. 
                                    **OBS 2:** Se o jogador optar, ele pode mandar o autor e o titulo da musica juntos usando esse formato: Autor - Título. **Ex:** Artic Monkeys - Do I Wanna Know'''
                            )
        game_info.set_image(url='https://media.istockphoto.com/photos/music-emoji-with-headphones-isolated-on-white-background-emoticon-picture-id868644688?k=6&m=868644688&s=170667a&w=0&h=khvKWGp77wlbVM9t62aNCd1amQRYJIOWWT-66k7TSIs=')
        await self.ctx.send(embed = game_info)
        championship_category = discord.utils.get(categories, name='Torneio')
        timeout = 45
        minimum_ratio = 0.75
        if championship_category == None:
            self.voice_channel = await guild.create_voice_channel("Music Quiz 🎵")
        else:
            self.voice_channel = await championship_category.create_voice_channel("Music Quiz 🎵")
        voice_channel_to_move_after_end = None
        for player in [self.player_one, self.player_two]:
            player_discord_member = player.get_discord_member()
            player_voice_state = player_discord_member.voice
            if player_voice_state != None:
                if player_voice_state.channel != None:
                    voice_channel_to_move_after_end = player_voice_state.channel
                    await player_discord_member.move_to(self.voice_channel)

        time.sleep(20)
        self.voice_client = await self.connect()
        max_rounds = 5
        round_number = 1
        while ((round_number <= max_rounds and (fabs(self.player_one.get_points() - self.player_two.get_points())  <= (400 * ((max_rounds+1) - round_number))))  or (self.player_one.get_points() == self.player_two.get_points())):
            song = self.songs[round_number]
            factor = ''
            if round_number == max_rounds:
                factor = '**[FINAL ROUND]**'
            elif round_number > max_rounds:
                factor = '**[OVERTIME]**'

            await self.ctx.send(f'**Round:** _{round_number}_ {factor}')
            await self.ctx.send('Baixando próxima música...')
            await self.play_song(song)
            competing_role = discord.utils.get(self.ctx.guild.roles,name='Competindo')
            if competing_role != None:
                for player in [self.player_one, self.player_two]:
                    player_discord_member = player.get_discord_member()
                    await player_discord_member.add_roles(competing_role)
            await self.ctx.send('**Qual o título e autor da que música está tocando?**')
            title_already_guessed = False
            author_already_guessed = False

            start = time.time()
            while time.time() - start <= timeout:
                def check(msg):
                    return msg.author in [self.player_one.get_discord_member(), self.player_two.get_discord_member()]



                try:
                    message_timeout = timeout - round(time.time() - start)
                    message = await self.client.wait_for('message', timeout=message_timeout, check=check)
                except TimeoutError:
                    await self.ctx.send('**Tempo esgotou!**')
                    self.voice_client.stop()
                    break
                else:
                    time_taken = round(time.time() - start)
                    points_obtained = 110 + ((timeout * 2) - time_taken)
                    answer = message.content
                    if ' - ' in answer:
                        try:
                            author, title = answer.split(' - ')
                        except ValueError:
                            await self.ctx.send('Indentação inválida!')
                        else:

                            title_is_right = SequenceMatcher(None, title.lower(), song.get_title().lower()).ratio() > minimum_ratio
                            author_is_right = SequenceMatcher(None, author.lower(), song.get_author().lower()).ratio() > minimum_ratio
                            title_guess_is_valid = title_is_right and not title_already_guessed
                            author_guess_is_valid = author_is_right and not author_already_guessed
                            if title_guess_is_valid or author_guess_is_valid:
                                if title_guess_is_valid and author_guess_is_valid:
                                    points_obtained *= 2
                                    await self.ctx.send(
                                        f'**{message.author.name}** acertou o **título** e o **autor** da música em **{time_taken}** segundos, ganhando **{points_obtained}** pontos!')
                                    author_already_guessed = True
                                    title_already_guessed = True

                                elif title_guess_is_valid:
                                    await self.ctx.send(
                                        f'**{message.author.name}** acertou o título da música em **{time_taken}** segundos, ganhando **{points_obtained}** pontos!')
                                    title_already_guessed = True
                                elif author_guess_is_valid:
                                    await self.ctx.send(
                                        f'{message.author.name} acertou o autor da música em **{time_taken}** segundos, ganhando **{points_obtained}** pontos!')
                                    author_already_guessed = True
                                if message.author == self.player_one.get_discord_member():
                                    self.player_one.add_points(points_obtained)
                                else:
                                    self.player_two.add_points(points_obtained)
                            elif title_is_right and title_already_guessed:
                                await self.ctx.send('**Título** já respondido anteriormente!')
                            elif author_is_right and author_already_guessed:
                                await self.ctx.send('**Autor** já foi respondido anteriormente!')


                    else:
                        title_is_right = SequenceMatcher(None, answer.lower(), song.get_title().lower()).ratio() > minimum_ratio
                        author_is_right = SequenceMatcher(None, answer.lower(), song.get_author().lower()).ratio() > minimum_ratio
                        title_guess_is_valid = title_is_right and not title_already_guessed
                        author_guess_is_valid = author_is_right and not author_already_guessed
                        if title_guess_is_valid or author_guess_is_valid:
                            if title_guess_is_valid:
                                await self.ctx.send(
                                    f'**{message.author.name}** acertou o título da música em **{time_taken}** segundos, ganhando **{points_obtained}** pontos!')
                                title_already_guessed = True
                            if author_guess_is_valid:
                                await self.ctx.send(
                                    f'**{message.author.name}** acertou o autor da música em **{time_taken}** segundos, ganhando **{points_obtained}** pontos!')
                                author_already_guessed = True
                            if message.author == self.player_one.get_discord_member():
                                self.player_one.add_points(points_obtained)
                            else:
                                self.player_two.add_points(points_obtained)
                        elif title_is_right and title_already_guessed:
                            await self.ctx.send('**Título** já respondido anteriormente!')
                        elif author_is_right and author_already_guessed:
                            await self.ctx.send('**Autor** já foi respondido anteriormente!')


                    if title_already_guessed and author_already_guessed:
                        self.voice_client.stop()
                        break
            self.voice_client.stop()
            await self.ctx.send(f'Estava tocando **{song.get_title()}** de **{song.get_author()}!**')

            if competing_role != None:
                for player in [self.player_one, self.player_two]:
                    player_discord_member = player.get_discord_member()
                    await player_discord_member.remove_roles(competing_role)
            await self.ctx.send(f'**{self.player_one.get_name()}**: _{self.player_one.get_points()}_')
            await self.ctx.send(f'**{self.player_two.get_name()}**: _{self.player_two.get_points()}_')
            round_number += 1
        if self.player_one.get_points() > self.player_two.get_points():
            self.winner = self.player_one
        else:
            self.winner = self.player_two
        await self.ctx.send(f'**{self.winner.get_name()}** ganhou com **{self.winner.get_points()}** pontos!')
        await self.voice_client.disconnect()

        if voice_channel_to_move_after_end == None:
            guild = self.ctx.guild
            voice_channels = guild.voice_channels
            if len(voice_channels) > 0:
                if voice_channels[0] != self.voice_channel:
                    voice_channel_to_move_after_end = voice_channels[0]
        members = self.voice_channel.members
        if voice_channel_to_move_after_end != None:
            for member in members:
                try:
                    await member.move_to(voice_channel_to_move_after_end)
                except Exception:
                    pass
        await self.voice_channel.delete()
        self.delete_songs()



    async def connect(self):
        while True:
            try:
                voice_client = await self.voice_channel.connect(reconnect= False,timeout = 5)
            except (TimeoutError,discord.ConnectionClosed) as e:
                print(f'Error while trying to connect: {str(e)}')
            except discord.ClientException as e:
                print(f'Error while trying to connect: {str(e)}')
                print('Trying to disconect...')
                voice_client = discord.utils.get(self.client.voice_clients, guild=self.ctx.guild)
                await voice_client.disconnect()
            else:
                return voice_client

    async def play_song(self,song):

        audio = self.download_song(song)
        while True:
            try:
                self.voice_client.play(audio)
            except (OSError,discord.ClientException) as e:
                print(f'Error while trying to play song: {str(e)}')
                self.voice_client = await self.connect()
                continue
            else:
                break


    def delete_songs(self):
        dirname = os.path.dirname(__file__)
        audio_folder = os.path.join(dirname, 'audios')
        for file in os.listdir(audio_folder):
            if file.endswith(".mp3") or file.endswith(".part"):
                try:
                    os.remove(os.path.join(audio_folder, file))
                except Exception as e:
                    print(f'Error while trying to delete {file}: {str(e)}')

    def download_song(self,song):
        dirname = os.path.dirname(__file__)
        audio_folder = os.path.join(dirname, 'audios')
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': audio_folder + '/%(title)s-%(id)s.%(ext)s'
        }



        while True:
            try:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([song.get_url()])
            except youtube_dl.utils.DownloadError as e:
                print(f'Error while trying to download song: {str(e)}')
                for file in os.listdir(audio_folder):
                    if song.get_url()[-11:] in file:
                        try:
                            os.remove(file)
                        except Exception as e:
                            print(f'Error while trying to delete {file}: {str(e)}')
            else:
                break




        for file in os.listdir(audio_folder):
            if song.get_url()[-11:] in file:
                audio_path = os.path.join(audio_folder, file)
                print(audio_path)
        audio = discord.FFmpegPCMAudio(audio_path)
        return audio


    def get_winner(self):
        return self.winner










