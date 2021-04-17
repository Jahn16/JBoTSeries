from ..action import Action
from asyncio import TimeoutError
class Villager():

    def __init__(self):
        self.team = 'Villagers'

    def set_client(self, client):
        self.client = client

    def set_player(self,player):
        self.player = player


    def __str__(self):
        return 'Villager'

    def get_team(self):
        return self.team

    async def make_action(self, round_number,players, actions):
        await self.player.get_discord_member().send('**Nada para fazer:**')
        await self.player.get_discord_member().send('Digite _PASSAR_')
        def check(msg):
            return msg.author == self.player.get_discord_member() and msg.content == 'PASSAR'
        try:
            selection = await self.client.wait_for('message',timeout=30,check=check)
        except TimeoutError:
            pass
        action = Action(round_number)
        action.set_player_responsible(self.player)
        action.set_player_affected(None)
        action.set_role(self)
        action.set_type('NOTHING')
        return action
