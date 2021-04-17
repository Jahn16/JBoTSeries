from games.uno.card import Card
import random
class Deck:
    def __init__(self):
        self.deck = self.generate_deck()
    
    def generate_deck(self):
        deck = []
        common_cards_identifier = ['1','2','3','4','5','6','7','8','9','🛇','⤡','2+']
        colors = ['red','blue','green','yellow']
        special_cards_identifier = ['4+','⨁']

        for color in colors:
            for identifier in common_cards_identifier:
                card = Card(identifier,color)
                deck.append(card)
    
        for identifier in special_cards_identifier:
            for _ in range(0,2):
                card = Card(identifier,'black')
                deck.append(card)

        return deck
    
    def draw_cards(self,number_of_cards):
        if len(self.deck) - number_of_cards <= 0:
            self.deck = self.generate_deck()
        cards_drown = []
        for _ in range(0,number_of_cards):
            card = random.choice(self.deck)
            self.deck.remove(card)
            cards_drown.append(card)
        return cards_drown
        
    def get_deck(self):
        return self.deck
            
