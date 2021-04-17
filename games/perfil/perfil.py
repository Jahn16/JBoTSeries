from .player import Player
import json
from asyncio import TimeoutError,sleep
import random
from difflib import SequenceMatcher
import discord
import os
from math import fabs

class Perfil():

    def __init__(self,ctx,client):
        self.ctx = ctx
        self.client = client
        self.characters = self.get_characters()

    def get_gamemode(self):
        return "Perfil"

    def set_player_one(self,player_one):
        self.player_one = Player(player_one)

    def set_player_two(self,player_two):
        self.player_two = Player(player_two)

    def get_characters(self):
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'characters.json')
        with open(filename,encoding="utf-8") as f:
            data = json.load(f)
        characters = data['characters']

        random.shuffle(characters)
        return characters

    async def start(self):
        max_rounds = 4
        game_info = discord.Embed(title='Perfil',
                                  colour = discord.Colour.purple())
        game_info.add_field(name='Regras:', value= f'''A cada rodada um **personagem real ou fictício** será escolhido, dicas com características desse personagem serão enviadas e os jogadores têm que **acertar quem é**. Quem obter mais pontos em **{max_rounds}** rodadas vence.
                                                    **OBS:** Quanto **mais** dicas foram usadas, **menor** será a pontuação obtida no caso de acerto. O jogador só terá direito a **uma tentativa** por personagem.   
        ''')
        game_info.set_image(url = 'https://pbs.twimg.com/media/CbDqppJUkAE2Q3S?format=jpg&name=small')
        await self.ctx.send(embed=game_info)

        competing_role = discord.utils.get(self.ctx.guild.roles, name = 'Competindo')
        round_number = 0

        await sleep(20)
        while ((round_number < max_rounds and (fabs(self.player_one.get_points() - self.player_two.get_points())  <= (5 * ((max_rounds) - round_number))))  or (self.player_one.get_points() == self.player_two.get_points())):

            await self.ctx.send(f'**{round_number + 1}º Personagem!**')
            character = self.characters[round_number]
            self.player_one.set_guessed(False)
            self.player_two.set_guessed(False)
            print(character['name'])
            if competing_role != None:
                for player in [self.player_one.get_discord_member(),self.player_two.get_discord_member()]:
                    await player.add_roles(competing_role)

            for index,hint in enumerate(character['hints']):
                await self.ctx.send(f'**Dica {index + 1}:** {hint}')
                guessed_right = await self.get_answers(character,index)
                if guessed_right or (self.player_one.made_a_guess() and self.player_two.made_a_guess()):
                    break
            if index == len(character['hints']) - 1:
                await self.ctx.send('Tempo acabou!')

            round_number += 1
            await self.ctx.send(f'**{self.player_one.get_name()}:** _{self.player_one.get_points()}_')
            await self.ctx.send(f'**{self.player_two.get_name()}:** _{self.player_two.get_points()}_')

        if self.player_one.get_points() > self.player_two.get_points():
            await self.ctx.send(f'**{self.player_one.get_name()}** ganhou!')
            self.winner = self.player_one

        else:
            await self.ctx.send(f'**{self.player_two.get_name()}** ganhou!')
            self.winner  = self.player_two




    async def get_answers(self,character,index):
        competing_role = discord.utils.get(self.ctx.guild.roles, name='Competindo')

        def check(msg):
            return msg.author in [self.player_one.get_discord_member(), self.player_two.get_discord_member()]

        while not self.player_one.made_a_guess() or not self.player_two.made_a_guess():
            try:
                answer = await self.client.wait_for('message',check=check, timeout=15)
            except TimeoutError:
                break
            else:
                def check_answer(answer,character_name):
                    if SequenceMatcher(None, answer.lower(), character_name.lower()).ratio() > 0.7:
                        return True
                    else:
                        if " " in character_name:
                            character_last_name = character_name.split(" ")[-1]
                            if SequenceMatcher(None, answer.lower(), character_last_name.lower()).ratio() > 0.7:
                                return True
                    return False

                if answer.author == self.player_one.get_discord_member():
                    if not self.player_one.made_a_guess():
                        self.player_one.set_guessed(True)
                        if competing_role != None:
                            await self.player_one.get_discord_member().remove_roles(competing_role)
                        if check_answer(answer.content,character['name']):
                            points_obtained = len(character['hints']) - index
                            await self.ctx.send(f'**{self.player_one.get_name()}** acertou, obtendo **{points_obtained}** pontos!')
                            self.player_one.add_points(points_obtained)
                            return True

                    else:
                        await self.ctx.send(f'**{self.player_one.get_name()}** já fez uma tentativa anteriormente!')
                else:
                    if not self.player_two.made_a_guess():
                        self.player_two.set_guessed(True)
                        if competing_role != None:
                            await self.player_two.get_discord_member().remove_roles(competing_role)
                        if check_answer(answer.content, character['name']):
                            points_obtained = len(character['hints']) - index
                            await self.ctx.send(f'**{self.player_two.get_name()}** acertou, obtendo **{points_obtained}** pontos!')
                            self.player_two.add_points(points_obtained)
                            return True

                    else:
                        await self.ctx.send(f'{self.player_two.get_name()} já fez uma tentativa anteriormente!')
        return False

    def get_winner(self):
        return self.winner