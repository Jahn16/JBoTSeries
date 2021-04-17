from quickdraw import QuickDrawData
from .player import Player
from .english_to_portuguese import english_to_portuguese_dictionary
from PIL import Image,ImageDraw
from googletrans import Translator
from difflib import SequenceMatcher
import discord
import unidecode
import copy
import random
from asyncio import sleep,TimeoutError
import time
import os
import shutil



class GuessDrawings():

    def __init__(self, ctx, client):
        self.ctx = ctx
        self.client = client

    def get_gamemode(self):
        return "Adivinhar Desenho"


    def set_player_one(self,player_one):
        self.player_one = Player(player_one)

    def set_player_two(self,player_two):
        self.player_two = Player(player_two)

    def get_drawing(self, recognized=True):
        dirname = os.path.dirname(__file__)
        cache_dir = os.path.join(dirname, '.quickdrawcache')
        qd = QuickDrawData(max_drawings=1,cache_dir = cache_dir)
        group_name = random.choice(qd.drawing_names)
        qd.load_drawings([group_name])
        drawing_data = qd.get_drawing(group_name)
        while drawing_data.recognized != recognized:
            group_name = random.choice(qd.drawing_names)
            qd.load_drawings([group_name])
            drawing_data = qd.get_drawing(group_name)
        drawing_size = drawing_data.get_image().size
        drawing = Image.new('RGB', drawing_size, 'white')
        draw = ImageDraw.Draw(drawing)
        frame = copy.deepcopy(drawing)
        frames = []
        for stroke in drawing_data.strokes:
            draw.line(stroke, 'black')
            frame = copy.deepcopy(drawing)
            frames.append(frame)
        return frames, drawing_data



    async def make_round(self):
        round_begin_message  = await self.ctx.send('**Próximo Desenho!**')
        await self.ctx.send('Baixando próximo desenho...')
        competing_role = discord.utils.get(self.ctx.guild.roles, name='Competindo')
        if competing_role != None:
            for player in [self.player_one, self.player_two]:
                player_discord_member = player.get_discord_member()
                await player_discord_member.add_roles(competing_role)
        frames,drawing_data = self.get_drawing()
        correct_answer = self.translate_answer(drawing_data.name.lower())
        unaccented_correct_answer = unidecode.unidecode(correct_answer).lower()
        dirname = os.path.dirname(__file__)
        save_path = os.path.join(dirname, 'frame.jpg')

        for index,frame in enumerate(frames):
            frame.save(save_path)
            await self.ctx.send(file=discord.File(save_path))

            def check(msg):
                valid_author = msg.author in [self.player_one.get_discord_member(),
                                              self.player_two.get_discord_member()]

                return valid_author

            if index != len(frames) - 1:
                async for message in self.ctx.history(limit=50,after = round_begin_message):
                    if check(message):

                        answer = message.content.lower()
                        if answer == correct_answer or answer == unaccented_correct_answer:
                            print('Catch:' + message.content)
                            if message.author == self.player_one.get_discord_member():
                                await self.ctx.send(f'**{self.player_one.get_name()}** acertou, ganhando **1** ponto!')
                                self.player_one.add_points(1)
                            else:
                                await self.ctx.send(f'**{self.player_two.get_name()}** acertou, ganhando **1** ponto!')
                                self.player_two.add_points(1)
                            return 0
                try:
                    message = await self.client.wait_for('message',check=check,timeout=8)
                except TimeoutError:
                    pass
                else:
                    answer = message.content.lower()
                    if answer == correct_answer or answer == unaccented_correct_answer:
                        if message.author == self.player_one.get_discord_member():
                            await self.ctx.send(f'**{self.player_one.get_name()}** acertou, ganhando **1** ponto!')
                            self.player_one.add_points(1)
                        else:
                            await self.ctx.send(f'**{self.player_two.get_name()}** acertou, ganhando **1** ponto!')
                            self.player_two.add_points(1)
                        return 0
                    else:
                        if SequenceMatcher(None,message.content.lower(),correct_answer.lower()).ratio() > 0.8:
                            try:
                                await message.author.send(f'**{message.content}** está perto!')
                            except discord.Forbidden:
                                pass
            else:
                await self.ctx.send('**Desenho Pronto! Últimos segundos para tentar acertar!**')
                tip = ''
                for index,char in enumerate(correct_answer):
                    if char != ' ':
                        char = '̲   '
                    tip += char
                if tip != '':
                    await self.ctx.send(f'**Dica:**    _{tip}_')
                start = time.time()
                while time.time() - start <= 20:
                    try:
                        message = await self.client.wait_for('message',check=check,timeout=20)
                    except TimeoutError:
                        pass
                    else:
                        answer = message.content.lower()
                        if answer == correct_answer or answer == unaccented_correct_answer:
                            if message.author == self.player_one.get_discord_member():
                                await self.ctx.send(f'**{self.player_one.get_name()}** acertou, ganhando **1** ponto!')
                                self.player_one.add_points(1)
                            else:
                                await self.ctx.send(f'**{self.player_two.get_name()}** acertou, ganhando **1** ponto!')
                                self.player_two.add_points(1)
                            return 0
                        else:
                            if SequenceMatcher(None, message.content.lower(), correct_answer.lower()).ratio() > 0.8:
                                try:
                                    await message.author.send(f'**{message.content}** está perto!')
                                except discord.Forbidden:
                                    pass
        if competing_role != None:
            for player in [self.player_one, self.player_two]:
                player_discord_member = player.get_discord_member()
                await player_discord_member.remove_roles(competing_role)
        await self.ctx.send(f'A resposta era **{correct_answer}!**')


    async def start(self):
        game_info = discord.Embed(title = 'Adivinhar Desenho',
                                  description= '''A cada rodada **um desenho** será escolhido, sendo desenhado **traço por traço** até que um jogador **acerte** o que está sendo desenhado ou o **tempo se esgote**. Caso o jogador acerte o desenho receberá **1** ponto.
                                                **OBS: **Primeiro jogador a obter **2** pontos vence.   
                                  ''',
                                  colour = discord.Colour.dark_purple())
        game_info.set_image(url = 'https://googlediscovery.com/wp-content/uploads/quick-draw.png')
        await self.ctx.send(embed=game_info)
        points_to_win = 2
        #await sleep(20)
        while self.player_one.get_points() < points_to_win and self.player_two.get_points() < points_to_win:
            await self.make_round()
            for player in [self.player_one,self.player_two]:
                await self.ctx.send(f'**{player.get_name()}:** _{player.get_points()}_')

        if self.player_one.get_points() > self.player_two.get_points():
            self.winner = self.player_one
        else:
            self.winner = self.player_two

        await self.ctx.send(f'**{self.winner.get_name()}** ganhou acertando **{self.winner.get_points()}** desenhos primeiro!')
        dirname = os.path.dirname(__file__)
        cache_dir = os.path.join(dirname, '.quickdrawcache')
        if os.path.exists(cache_dir):
            shutil.rmtree(cache_dir)
        if os.path.exists('frame.jpg'):
            os.remove('frame.jpg')




    def translate_answer(self,original_answer):

        translated_answer = english_to_portuguese_dictionary[original_answer]

        return translated_answer



    def get_winner(self):
        return self.winner
