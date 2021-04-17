from . import card

class Bot:
    def __init__(self,name):
        self.name = name
    
    def set_hand(self,hand):
        self.hand = hand

    async def make_move(self,card_on_top,stack_card=False):
        if not stack_card:
            for card in self.hand:
                if card_on_top.is_legal_to_put_on_top(card):
                    self.hand.remove(card)
                    return card
        else:
            for card in self.hand:
                if card_on_top.get_identifier() == card.get_identifier():
                    self.hand.remove(card)
                    return card
    
    def draw_cards(self,cards):
        for card in cards:
            self.hand.append(card)

    def has_legal_cards(self,card_on_top):
        for card in self.hand:
            if card_on_top.is_legal_to_put_on_top(card):
                return True
        return False
    def get_how_many_cards(self):
        return len(self.hand)
    
    def can_stack_draw_card(self,card_to_be_stacked):
        for card in self.hand:
            if card.get_identifier() == card_to_be_stacked.get_identifier():
                return True
        return False

    async def select_color(self):
        return "red"
    
    def get_name(self):
        return self.name