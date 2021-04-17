import discord
from .player import Player
import json
import os
import random
import time
from asyncio import sleep

class TypeRacer():

    def __init__(self,ctx,client):
        self.ctx = ctx
        self.client = client
        self.get_texts()

    def get_gamemode(self):
        return "Corrida de digitação "

    def get_texts(self):
        dirname = os.path.dirname(__file__)
        path = os.path.join(dirname, 'texts.json')
        with open(path,encoding="utf-8") as f:
            data = json.load(f)
        self.texts = data['texts']
        random.shuffle(self.texts)

    def set_player_one(self,player_one):
        self.player_one = Player(player_one)

    def set_player_two(self,player_two):
        self.player_two = Player(player_two)

    async def start(self):
        def check(msg):
            return (msg.author.name == self.player_one.name or msg.author.name == self.player_two.name)

        async def check_message_content(message,original_text):
            msg_content = message.content.replace("  "," ")
            msg_words = msg_content.split(" ")
            original_words = original_text.split(" ")
            missing_words = []
            words_typed_wrong = 0
            for index,original_word in enumerate(original_words):
                if index  < len(msg_words):
                    if msg_words[index] != original_word:
                        msg_words[index] = '**' + msg_words[index] + '**'
                        words_typed_wrong += 1
                else:
                    missing_words.append(original_word)

            if words_typed_wrong > 0:
                await self.ctx.send('**Palavras erradas:** ' + (' '.join(msg_words)))
            if len(missing_words) > 0:
                await self.ctx.send('**Palavras faltando:** ' + str(missing_words))
            if len(msg_words) > len(original_words):
                await self.ctx.send('**Palavras sobrando:** ' + str(msg_words[len(original_words):]))
            return msg_content == original_text

        points_to_win = 3
        game_info = discord.Embed(title='Corrida de digitação',
                                  colour = discord.Colour.purple())
        game_info.add_field(name='Regras:',value=f'''A cada round uma **imagem contendo um texto** será enviada, aquele jogador que primeiro digitar este texto **perfeitamente** ganha um ponto.
                                                    Primeiro a chegar a **{points_to_win}** pontos vence.''')
        game_info.set_image(url = 'https://hackernoon.com/hn-images/1*UXQAvi5QYkzksq8lsIhy5A.png')

        await self.ctx.send(embed=game_info)
        await sleep(20)
        i = 0
        roles = self.ctx.guild.roles
        competing_role = discord.utils.get(roles, name='Competindo')
        while self.player_one.get_points() != points_to_win and self.player_two.get_points() != points_to_win:
            text = self.texts[i]

            dirname = os.path.dirname(__file__)
            imgs_folder = os.path.join(dirname, 'imgs')
            img_path = os.path.join(imgs_folder, text['img_path'])

            await self.ctx.send(file=discord.File(img_path))
            if not self.player_one.get_discord_member().guild_permissions.administrator and not self.player_two.get_discord_member().guild_permissions.administrator and competing_role != None:
                await sleep(1)
                await self.ctx.send('**Preparar...**')
                await sleep(1)
                await self.ctx.send('1.')
                await sleep(1)
                await self.ctx.send('2..')
                await sleep(1)
                await self.ctx.send('3...')
                await sleep(1)
                await self.ctx.send('**Já!**')

            if competing_role != None:
                for player in random.sample([self.player_one,self.player_two],2):
                    await player.discord_member.add_roles(competing_role)
            start = time.time()
            while True:
                msg = await self.client.wait_for('message',check=check)
                if await check_message_content(msg,text['text']) == True:
                    end = time.time()
                    time_taken = end - start
                    number_of_words = len(text["text"])/5
                    wpm = number_of_words / (time_taken/60)
                    await self.ctx.send(f'**{msg.author.name}** acabou primeiro, com uma velocidade de **{round(wpm)} WPM!**')
                    if msg.author.name == self.player_one.name:
                        self.player_one.add_points()
                    else:
                        self.player_two.add_points()
                    if competing_role != None:
                        await self.player_one.discord_member.remove_roles(competing_role)
                        await self.player_two.discord_member.remove_roles(competing_role)
                    break
            await self.ctx.send(f'**{self.player_one.name}**: {self.player_one.get_points()}')
            await self.ctx.send(f'**{self.player_two.name}**: {self.player_two.get_points()}')
            i += 1
        if self.player_one.get_points() == points_to_win:
            await self.ctx.send(f'**{self.player_one.name}** chegou primeiro aos **{points_to_win}** pontos, e ganhou!')
            self.winner = self.player_one

        elif self.player_two.get_points() == points_to_win:
            await self.ctx.send(f'**{self.player_two.name}** chegou primeiro aos **{points_to_win}** pontos, e ganhou!')
            self.winner = self.player_two



    def get_winner(self):
        return self.winner

