import discord
import asyncio
from . import card

class Human:
    def __init__(self,member,client):
        self.member = member
        self.name = member.name
        self.client = client
        
    def set_hand(self,hand):
        self.hand = hand
    
    async def make_move(self,card_on_top,stack_card=False):
        def check(msg):
            return msg.author == self.member and (("red" in msg.content) or ("green" in msg.content) or ("yellow" in msg.content) or ("blue" in msg.content) or ("black" in msg.content)) 
        self.sort_cards()
        await self.member.send("**---------------SUA MAO-------------------**")
        if not stack_card:
            for card in self.hand:
                if card_on_top.is_legal_to_put_on_top(card):
                    text_based_card = f"**{card.get_text_based_card()}**"
                else:
                    text_based_card = card.get_text_based_card()
                await self.member.send(content=text_based_card,file=discord.File(card.get_image()))

            card_selection = await self.client.wait_for("message",check=check,timeout=90.0)
            for card in self.hand:
                if card.get_text_based_card()  == card_selection.content:
                    self.hand.remove(card)
                    return card
        else:
            for card in self.hand:
                if card.get_identifier() == card_on_top.get_identifier():
                    text_based_card = f"**{card.get_text_based_card()}**"
                else:
                    text_based_card = card.get_text_based_card()
                await self.member.send(content=text_based_card,file=discord.File(card.get_image()))
            card_selection = await self.client.wait_for("message",timeout=90.0)
            for card in self.hand:
                if card.get_identifier() == card_on_top.get_identifier():
                    self.hand.remove(card)
                    return card
        raise ValueError("Invalid Move!")
    
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
        def check(msg):
            return msg.author == self.member and msg.content in ["🔴","🔵","🟢","🟡"] 
        await self.member.send("Selecione uma cor:")
        await self.member.send(":red_circle:")
        await self.member.send(":blue_circle:")
        await self.member.send(":green_circle:")
        await self.member.send(":yellow_circle:")
        color_circle = await self.client.wait_for("message",check=check,timeout=45.0)
        colors = {
            "🔴" :"red",
            "🔵": "blue",
            "🟢": "green",
            "🟡": "yellow"
        }
        return colors[color_circle.content]

        
        
    def sort_cards(self):
        def swap(i,j):
            aux = self.hand[i]
            self.hand[i] = self.hand[j]
            self.hand[j] = aux
        def get_string_value(str):
            str_value = 0
            for char in list(str):
                str_value += ord(char)
            return str_value

        for i in range(0,len(self.hand)):
            for j in range(0,len(self.hand)):
                if get_string_value(self.hand[i].get_color()[2]) < get_string_value(self.hand[j].get_color()[2]):
                    swap(i,j)
                elif get_string_value(self.hand[i].get_color()) == get_string_value(self.hand[j].get_color()):
                    if get_string_value(self.hand[i].get_identifier()) < get_string_value(self.hand[j].get_identifier()):
                        swap(i,j)

    def get_name(self):
        return self.name
                
        
