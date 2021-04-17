from ..action import Action
from asyncio import TimeoutError
class Seer():

    def __init__(self):
        self.team = 'Villagers'

    def set_client(self, client):
        self.client = client

    def set_player(self,player):
        self.player = player


    def __str__(self):
        return "Seer"

    def get_team(self):
        return self.team

    async def make_action(self, round_number,players, actions):
        await self.player.get_discord_member().send('**Jogadores:**')
        for index, player in enumerate(players, start=1):
            player_string = f'**{index}.** _{player.get_name()}_'

            for action in actions:
                if action.get_round_number() == round_number:
                    if action.get_type() == 'SEE' and action.get_player_responsible() == self.player:
                        player_affected = action.get_player_affected()
                        if player_affected == player:
                            player_string += f' **[{player_affected.get_role()}]**'
                            break
            await self.player.get_discord_member().send(player_string)

        await self.player.get_discord_member().send('**Selecione um jogador para ver sua função:**')
        def check(msg):
            try:
                index = int(msg.content)
            except ValueError:
                return False
            else:
                return msg.author == self.player.get_discord_member() and (index > 0 and index <= len(players))
        try:
            selection = await self.client.wait_for('message',timeout=45,check=check)
        except TimeoutError:
            await self.player.get_discord_member().send('Tempo esgotou!')
            action = Action(round_number)
            action.set_player_responsible(self.player)
            action.set_player_affected(None)
            action.set_role(self)
            action.set_type('NOTHING')
            return action
        else:
            index = int(selection.content) - 1
            player_selected = players[index]
            await self.player.get_discord_member().send(f"A função de _{player_selected.get_name()}_ é **{player_selected.get_role()}!**")
            action = Action(round_number)
            action.set_player_responsible(self.player)
            action.set_role(self)
            action.set_type('SEE')
            action.set_player_affected(players[index])
            return action
