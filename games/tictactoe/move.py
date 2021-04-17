class Move():

    def __init__(self,coordinate):
        self.coordinate = coordinate
        self.value = 0

    def setPlayer(self,player):
        self.player = player

    def set_value(self,value):
        self.value = value

    def get_value(self):
        return self.value