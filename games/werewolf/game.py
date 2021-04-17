import discord
from games.werewolf.missing_participants_error import MissingParticipantsError
from games.werewolf.player import Player
from games.werewolf.roles.werewolf import Werewolf
from games.werewolf.roles.villager import Villager
from games.werewolf.roles.seer import Seer
from games.werewolf.roles.doctor import Doctor
from games.werewolf.roles.avenger import Avenger
from games.werewolf.roles.witch import Witch
from games.werewolf.roles.gunner import Gunner
from games.werewolf.roles.jailer import Jailer
from .utils import establish_chat
from asyncio import TimeoutError
import time
import asyncio
import random
class Game():

    def __init__(self, ctx, client):
        self.ctx = ctx
        self.client = client

    async def get_players(self):
        game_info = discord.Embed(title = 'Lobisomem',
                                  description= '''Werewolf é ambientado em uma pequena aldeia que é assombrado por lobisomens.
                                  Cada jogador é atribuído um papel secretamente: Lobisomem, aldeão, Seer, etc.
                                  O jogo alterna entre fases de noite e dia. À noite, a Lobisomens escolhem secretamente um aldeão para matar. Durante o dia, o morador que foi morto é revelado e está fora do jogo. Os demais moradores, em seguida, votam em um jogador que suspeitam ser um Lobisomem.''')
        game_info.add_field(name='Objetivo:',value = 'Lobisomens ganham quando há um número igual de Moradores e Lobisomens. Os moradores ganham quando eles matarem todos os Lobisomens.')
        game_info.set_image(url = 'https://lh3.googleusercontent.com/uCqN5KLj9bdlMabolZyblmmAgacwynsd0VFbmyMjRsX1i-tAdJde541dIiurpxLrTw')
        message = await self.ctx.send(embed = game_info)
        await message.add_reaction('🐺')
        self.players = []
        while True:
            def check(reaction,user):
                return str(reaction.emoji) == '🐺' and not user.bot
            try:
                reaction,user = await self.client.wait_for('reaction_add', timeout=20.0, check=check)
            except TimeoutError:
                break
            else:
                player = Player(user, self.client)
                if player not in self.players:
                    self.players.append(player)


        if len(self.players) < 4:
            pass
            #raise MissingParticipantsError(len(self.players))
        await self.ctx.send('**Jogadores:**')
        for player in self.players:
            await self.ctx.send(f'● {player.get_name()}')
        await self.shuffle_roles()



    async def shuffle_roles(self):
        roles_config = {
            'Werewolf': round(len(self.players) / 3) * 0,
            'Seer': 0,
            'Doctor': 0,
            'Witch': 0,
            'Avenger': 0,
            'Gunner': 0,
            'Jailer': 1
        }

        roles = []
        await self.ctx.send('**Configuração:**')
        for role_config in roles_config.items():
            role_name,number_of_role = role_config
            if len(roles) + number_of_role <= len(self.players):
                await self.ctx.send(f'● _{role_name}_: {number_of_role}')
                for _ in range(number_of_role):
                    roles.append(role_name)
            else:
                break

        if len(roles) < len(self.players):
            for _ in range(len(self.players) - len(roles)):
                roles.append('Villager')

        for role_name,player in zip(roles,self.players):
            if role_name == 'Werewolf':
                role = Werewolf()
            elif role_name == 'Seer':
                role = Seer()
            elif role_name == 'Witch':
                role = Witch()
            elif role_name == 'Doctor':
                role = Doctor()
            elif role_name == 'Avenger':
                role = Avenger()
            elif role_name == 'Gunner':
                role = Gunner()
            elif role_name == 'Jailer':
                role = Jailer()
            else:
                role = Villager()
            role.set_client(self.client)
            player.set_role(role)



    async def start(self):
        await self.get_players()

        round_number = 1
        all_actions = []
        day_embed = discord.Embed(title = 'Dia',
                                  description= 'Durante este período todos votam e discutem quem são os lobisomens.',
                                  color = discord.Colour.orange())
        day_embed.set_image(url = 'https://i.pinimg.com/564x/ba/c4/e1/bac4e1901c992e4a37861fea55c59899.jpg')
        night_embed = discord.Embed(title='Noite',
                                    description='Durante este período os personagens realizam suas ações',
                                    color=discord.Colour.dark_purple())
        night_embed.set_image(url='https://i.pinimg.com/originals/89/80/10/898010310ecadc4e9d7789a25b559792.png')
        while True:
            await self.ctx.send(embed = night_embed)
            round_actions = []
            werewolfs = []
            for player in self.players:
                if player.get_role().get_team() == 'Werewolfes':
                    werewolfs.append(player)
            if len(werewolfs) > 1:
                await establish_chat(self.client,werewolfs,'Chat dos lobisomens:')
            for player in self.players:
                action = await player.make_action(round_number,self.players,all_actions)
                all_actions.append(action)
                round_actions.append(action)
            await self.ctx.send(embed=day_embed)
            await self.interpret_actions(round_actions)
            round_number += 1

    async def interpret_actions(self,round_actions):
        players_killed = []
        most_werewolf_voted_player = None
        for action in round_actions:
            if str(action.get_role()) == 'Werewolf' and action.get_type() == 'KILL_VOTE':
                player_affected = action.get_player_affected()
                if player_affected != None:
                    player_affected.set_werewolf_votes(player_affected.get_werewolf_votes() + 1)
                    if most_werewolf_voted_player == None:
                        most_werewolf_voted_player = player_affected
                    elif player_affected.get_werewolf_votes() > most_werewolf_voted_player.get_werewolf_votes():
                        most_werewolf_voted_player = player_affected
                    elif player_affected.get_werewolf_votes() == most_werewolf_voted_player.get_werewolf_votes():
                        most_werewolf_voted_player = random.choice((player_affected,most_werewolf_voted_player))

        for player in self.players:
            player.set_werewolf_votes(0)
        if most_werewolf_voted_player != None:
            players_killed.append(most_werewolf_voted_player)
        if most_werewolf_voted_player != None:
            for action in round_actions:
                if action.get_type() == 'PROTECT' and (action.get_player_affected() == most_werewolf_voted_player or str(action.get_role()) == 'Witch'):
                    players_killed.remove(most_werewolf_voted_player)

        for action in round_actions:
            if action.get_type() == 'KILL':
                if str(action.get_role()) == 'Gunner':
                    await self.ctx.send(f'O Gunner,{action.get_player_responsible().get_name()} atirou na última noite!')
                if action.get_player_affected() not in players_killed:
                    players_killed.append(action.get_player_affected())

        for action in round_actions:
            if str(action.get_role()) == 'Avenger':
                if action.get_player_responsible() in players_killed:
                    player_affected = action.get_player_affected()
                    if player_affected not in players_killed:
                        players_killed.append(player_affected)
                        await self.ctx.send(f'O Avenger morreu, e levou {player_affected.get_name()} com ele!')

        for action in round_actions:
            if str(action.get_role()) == 'Gunner' and action.get_type() == 'KILL':

                player_affected = action.get_player_affected()
                if player_affected not in players_killed:
                    players_killed.append(player_affected)

                await self.ctx.send(f'O Gunner,{action.get_player_responsible().get_name()} atirou na última noite!')


        if len(players_killed) > 0:
            await self.ctx.send('**Jogadores mortos última noite:**')
            for player_killed in players_killed:
                await self.ctx.send('● ' + player_killed.get_name())
                self.players.remove(player_killed)
        else:
            await self.ctx.send('**Nenhum jogador morto última noite**')


    def discussion(self):
        print('**Discussão:**')
        for player in self.players:
            player_voted = player.vote()
            player_voted.set_discussion_votes(player_voted.get_discussion_votes() + 1)
        most_voted_player = None
        for player in self.players:
            if most_voted_player == None:
                most_voted_player = player
            elif player.get_discussion_votes() > most_voted_player:
                most_voted_player = player

        for player in self.players:
            pass






