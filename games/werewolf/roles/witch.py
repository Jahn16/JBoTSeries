from ..action import Action
from asyncio import TimeoutError
class Witch():

    def __init__(self):
        self.team = 'Villagers'
        self.elixir_potions = 1
        self.poison_potions = 1


    def set_client(self, client):
        self.client = client

    def set_player(self,player):
        self.player = player

    def __str__(self):
        return "Witch"

    def get_team(self):
        return self.team

    def make_action(self, round_number,players, actions):

        options = []
        if self.elixir_potions > 0:
            options.append('Elixir')
        if self.poison_potions > 0:
            options.append('Poison')
        options.append('Pass')
        if len(options) > 1:
            for index,option in enumerate(options,start=1):
                print(f'{index} - {option}')
            while True:
                print('Select an option to use:')
                index = int(input()) - 1
                if index >= 0 and index < len(options):
                    option_selected = options[index]
                    break
                else:
                    print('Invalid option!')
            if option_selected == 'Poison':
                for index,player in enumerate(players,start = 1):
                    print(f'{index} - {player.get_name()}')
                while True:
                    print('Select a player to affect:')
                    index = int(input()) - 1
                    if index >= 0 and index < len(players):
                        if players[index] != self.player:
                            action = Action(round_number)
                            action.set_player_responsible(self.player)
                            action.set_role(self)
                            action.set_type('KILL')
                            action.set_player_affected(players[index])
                            self.poison_potions -= 1
                        else:
                            print("Can't select yourself!")
            elif option_selected == 'Poison':
                action = Action(round_number)
                action.set_player_responsible(self.player)
                action.set_role(self)
                action.set_type('PROTECT')
                action.set_player_affected(players)
                self.elixir_potions -= 1
            else:
                action = Action(round_number)
                action.set_player_responsible(self.player)
                action.set_role(self)
                action.set_type('NOTHING')
            return action
