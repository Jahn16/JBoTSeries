from ..action import Action
from asyncio import TimeoutError
class Werewolf():

    def __init__(self):
        self.team = 'Werewolfes'
        self.priority = 3

    def set_client(self,client):
        self.client = client

    def set_player(self,player):
        self.player = player


    def get_player(self):
        return self.player

    def __str__(self):
        return "Werewolf"

    def get_team(self):
        return self.team

    async def make_action(self, round_number,players, actions):
        await self.player.get_discord_member().send('**Jogadores:**')
        for index,player in enumerate(players,start = 1):
            player_string = f'**{index}.** _{player.get_name()}_'
            if str(player.get_role()) == 'Werewolf':
                player_string += f' **[{player.get_role()}]**'
            for action in actions:
                if action.get_round_number() == round_number:
                    if action.get_type() == 'KILL_VOTE' and str(action.get_role()) == 'Werewolf':
                        if action.get_player_affected() == player:
                            player_string += f' **({action.get_player_responsible().get_name()})**'
            await self.player.get_discord_member().send(player_string)


        await self.player.get_discord_member().send('**Vote em um jogador para matar:**')
        def check(msg):
            try:
                index = int(msg.content)
            except ValueError:
                return False
            else:
                return msg.author == self.player.get_discord_member() and (index > 0 and index <= len(players))
        try:
            selection = await self.client.wait_for('message',timeout=60,check=check)
        except TimeoutError:
            await self.player.get_discord_member().send('Tempo esgotou!')
        else:
            index = int(selection.content) - 1
            player_selected = players[index]
            if player_selected.get_role().get_team() != 'Werewolfes':
                action = Action(round_number)
                action.set_player_responsible(self.player)
                action.set_player_affected(player_selected)
                action.set_role(self)
                action.set_type('KILL_VOTE')
                return action
            else:
                await self.player.get_discord_member().send('Não se pode votar em um lobisomem.')

        action = Action(round_number)
        action.set_player_responsible(self.player)
        action.set_player_affected(None)
        action.set_role(self)
        action.set_type('NOTHING')
        return action






