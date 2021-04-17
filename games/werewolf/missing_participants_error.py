
class MissingParticipantsError(Exception):
    def __init__(self,number_of_players):
        super().__init__(f'Jogadores insuficientes, apenas {number_of_players}. ')
