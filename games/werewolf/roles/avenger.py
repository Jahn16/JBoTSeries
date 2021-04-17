from ..action import Action
from asyncio import TimeoutError
class Avenger():

    def __init__(self):
        self.team = 'Villagers'


    def set_client(self, client):
        self.client = client

    def set_player(self,player):
        self.player = player

    def __str__(self):
        return "Avenger"

    def get_team(self):
        return self.team

    def make_action(self, round_number,players, actions):

        for index,player in enumerate(players,start = 1):
            print(f'{index} - {player.get_name()}')
        while True:
            print('Select a player to kill with you:')
            index = int(input()) - 1
            if index >= 0 and index < len(players):
                if players[index] != self.player:
                    action = Action(round_number)
                    action.set_player_responsible(self.player)
                    action.set_role(self)
                    action.set_type('AVENGE')
                    action.set_player_affected(players[index])
                    return action
                else:
                    print("Can't select yourself!")