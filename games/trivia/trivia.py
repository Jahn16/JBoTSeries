from .player import Player
import json
from asyncio import TimeoutError,sleep
import random
import time
import discord

class Trivia():

    def __init__(self,ctx,client):
        self.ctx = ctx
        self.client = client
        self.get_questions()

    def get_gamemode(self):
        return "Trivia"

    def get_questions(self):
        with open(r'C:\JboTSeries\games\trivia\questions.json',encoding="utf-8") as f:
            data = json.load(f)
        self.questions = data['questions']
        for question in self.questions:
            if question['question'] == '' or question['choices'] == '' or question['answer'] == '':
                self.questions.remove(question)
        random.shuffle(self.questions)

    def set_player_one(self,player_one):
        self.player_one = Player(player_one)

    def set_player_two(self,player_two):
        self.player_two = Player(player_two)

    async def start(self):
        points_to_win = 3
        wrong_answers_to_lose = 3

        roles = self.ctx.guild.roles
        competing_role = discord.utils.get(roles, name='Competindo')
        game_info = discord.Embed(title = 'Trivia',
                                  color= discord.Colour.purple())
        game_info.add_field(name = 'Regras:' , value = f'''A cada rodada uma pergunta será enviada, aquele jogador que responder corretamente recebe **1** ponto, se errar **-1** , caso nenhum jogador responda a pergunta é pulada sem nenhuma penalidade.
        O jogador que chegar a **{points_to_win}** pontos primeiro vence.
        ''')
        game_info.set_image(url = 'https://static.semrush.com/blog/uploads/media/49/b2/49b23bcb2ff12c60203bfe93c204cef7/quiz-01.png')
        await self.ctx.send(embed = game_info)

        def check(msg):
            return msg.content.lower() in ['a','b','c','d','e'] and msg.author in [self.player_one.get_discord_member(),self.player_two.get_discord_member()]
        await sleep(20)
        round_number = 0
        while points_to_win not in [self.player_one.get_points(),self.player_two.get_points()] and wrong_answers_to_lose not in [self.player_one.get_wrong_answers_number(),self.player_two.get_wrong_answers_number()]:
            question = self.questions[round_number]
            time.sleep(7)
            await self.ctx.send('**' + question['question'] + '**')
            await self.ctx.send(question['choices'])
            if competing_role != None:
                for player in [self.player_one.get_discord_member(),self.player_two.get_discord_member()]:
                    await player.add_roles(competing_role)
            try:
                answer = await self.client.wait_for('message',check=check,timeout=25.0)
            except TimeoutError:
                await self.ctx.send('**Ninguém respondeu, passando para a próxima pergunta!**')

            else:
                if competing_role != None:
                    for player in [self.player_one.get_discord_member(), self.player_two.get_discord_member()]:
                        await player.remove_roles(competing_role)
                if answer.content.lower() == question['answer']:
                    await self.ctx.send('**Correta, a resposta!**')
                    if answer.author == self.player_one.get_discord_member():
                        await self.ctx.send(f'**+1** ponto para **{self.player_one.get_name()}**.')
                        self.player_one.add_points(1)
                    else:
                        await self.ctx.send(f'**+1** ponto para **{self.player_two.get_name()}**.')
                        self.player_two.add_points(1)

                else:
                    await self.ctx.send('**Resposta errada!**')
                    if answer.author == self.player_one.get_discord_member():
                        await self.ctx.send(f'**+1** erro para **{self.player_one.get_name()}**.')
                        self.player_one.set_wrong_answers_number(self.player_one.get_wrong_answers_number() + 1)

                    else:
                        await self.ctx.send(f'**+1** erro para **{self.player_two.get_name()}**.')
                        self.player_two.set_wrong_answers_number(self.player_two.get_wrong_answers_number() + 1)

            round_number += 1

            await self.ctx.send(f'**{self.player_one.get_name()}:** {self.player_one.get_points()} [{self.player_one.get_wrong_answers_number()}]')
            await self.ctx.send(f'**{self.player_two.get_name()}:** {self.player_two.get_points()} [{self.player_two.get_wrong_answers_number()}]')

        if self.player_one.get_points() == points_to_win:
            await self.ctx.send(f'**{self.player_one.get_name()}** chegou a **{points_to_win}** pontos primeiro, ganhando a partida.')
            self.winner = self.player_one

        elif self.player_two.get_points() == points_to_win:
            await self.ctx.send(f'**{self.player_two.get_name()}** chegou a **{points_to_win}** pontos primeiro, ganhando a partida.')
            self.winner  = self.player_two

        elif self.player_one.get_wrong_answers_number() == wrong_answers_to_lose:
            await self.ctx.send(f'**{self.player_one.get_name()}** chegou a **{wrong_answers_to_lose}** erros e foi eliminado.')
            await self.ctx.send(f'**{self.player_two.get_name()}** ganhou a partida.')
            self.winner = self.player_two


        elif self.player_two.get_wrong_answers_number() == wrong_answers_to_lose:
            await self.ctx.send(f'**{self.player_two.get_name()}** chegou a **{wrong_answers_to_lose}** erros e foi eliminado.')
            await self.ctx.send(f'**{self.player_one.get_name()}** ganhou a partida.')
            self.winner = self.player_one




    def get_winner(self):
        return self.winner





