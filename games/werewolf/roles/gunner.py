from ..action import Action
from asyncio import TimeoutError
class Gunner():

    def __init__(self):
        self.team = 'Villagers'
        self.ammunition = 2


    def set_client(self, client):
        self.client = client

    def set_player(self,player):
        self.player = player


    def __str__(self):
        return "Gunner"

    def get_team(self):
        return self.team

    async def make_action(self, round_number,players, actions):

        options = []
        if self.ammunition > 0:
            options.append(f'Atirar')
        options.append('Passar')

        for index,option in enumerate(options,start=1):
            await self.player.get_discord_member().send(f'**{index}.** _{option}_')

        await self.player.get_discord_member().send('**Selecione uma opção:**')

        def check(msg):
            try:
                index = int(msg.content)
            except ValueError:
                return False
            else:
                return msg.author == self.player.get_discord_member() and (index > 0 and index <= len(options))
        try:
            selection = await self.client.wait_for('message', timeout=45, check=check)
        except TimeoutError:
            await self.player.get_discord_member().send('Tempo esgotou!')
        else:
            index = int(selection.content) - 1
            option_selected = options[index]
            if option_selected == 'Atirar':
                await self.player.get_discord_member().send('**Jogadores:**')
                for index, player in enumerate(players, start=1):
                    player_string = f'**{index}.** _{player.get_name()}_'
                    await self.player.get_discord_member().send(player_string)

                await self.player.get_discord_member().send('**Selecione um jogador para atirar:**')

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
                    if player_selected != self.player:
                        action = Action(round_number)
                        action.set_player_responsible(self.player)
                        action.set_player_affected(player_selected)
                        action.set_role(self)
                        action.set_type('KILL')
                        self.ammunition -= 1

                    else:
                        await self.player.get_discord_member().send('Não é possível se selecionar!')

        action = Action(round_number)
        action.set_player_responsible(self.player)
        action.set_player_affected(None)
        action.set_role(self)
        action.set_type('NOTHING')
        return action

