class Card:
    def __init__(self,identifier,color):
        self.identifier = identifier
        self.color = color
    
    def get_text_based_card(self):
        return f"{self.identifier} {self.color}"
    
    def get_image(self):
        return f"c:/JboTSeries/games/uno/uno_cards/{self.color.capitalize()}/{self.identifier}.png"
        
    def get_color(self):
        return self.color

    def get_identifier(self):
        return self.identifier

    def set_color(self,color):
        self.color = color

    def is_legal_to_put_on_top(self,card_to_put_on_top):
        if self.get_color() == card_to_put_on_top.get_color():
            return True
        elif self.get_identifier() == card_to_put_on_top.get_identifier():
            return True
        elif card_to_put_on_top.get_color() == "black":
            return True
        return False

