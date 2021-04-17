class Action():

    def __init__(self, round_number):
        self.round_number = round_number

    def get_round_number(self):
        return self.round_number

    def set_player_responsible(self, player_responsible):
        self.player_responsible = player_responsible

    def get_player_responsible(self):
        return self.player_responsible

    def set_player_affected(self,player_affected):
        self.player_affected = player_affected

    def get_player_affected(self):
        return self.player_affected

    def set_type(self,action_type):
        self.type = action_type

    def get_type(self):
        return self.type

    def set_role(self,role):
        self.role = role

    def get_role(self):
        return self.role
