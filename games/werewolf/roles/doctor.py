from ..action import Action
from asyncio import TimeoutError
class Doctor():

    def __init__(self):
        self.team = 'Villagers'

    def set_client(self, client):
        self.client = client

    def set_player(self,player):
        self.player = player

    def __str__(self):
        return "Doctor"

    def get_team(self):
        return self.team

    async def make_action(self, round_number,players, actions):
        await self.player.get_discord_member().send('**Jogadores:**')
        for index, player in enumerate(players, start=1):
            player_string = f'**{index}.** _{player.get_name()}_'
            await self.player.get_discord_member().send(player_string)

        await self.player.get_discord_member().send('**Selecione um jogador para proteger:**')

        def check(msg):
            try:
                index = int(msg.content)
            except ValueError:
                return False
            else:
                return msg.author == self.player.get_discord_member() and (index > 0 and index <= len(players))

        try:
            selection = await self.client.wait_for('message', timeout=45, check=check)
        except TimeoutError:
            await self.player.get_discord_member().send('Tempo esgotou!')
        else:
            index = int(selection.content) - 1
            player_selected = players[index]
            protected_player_last_night = False
            for action in actions:
                if action.get_player_responsible() == self.player:
                    if action.get_round_number() == round_number - 1:
                        if action.get_player_affected() == player_selected:
                            protected_player_last_night = True
                            break
            if player_selected != self.player and not protected_player_last_night:


                action = Action(round_number)
                action.set_player_responsible(self.player)
                action.set_player_affected(player_selected)
                action.set_role(self)
                action.set_type('PROTECT')
                return action
            elif player_selected == self.player:
                await self.player.get_discord_member().send('Não é possível se selecionar!')
            else:
                await self.player.get_discord_member().send('Não é possível proteger um jogador por 2 vezes seguidas!')

        action = Action(round_number)
        action.set_player_responsible(self.player)
        action.set_player_affected(None)
        action.set_role(self)
        action.set_type('NOTHING')
        return action

