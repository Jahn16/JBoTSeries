import discord
import asyncio
import random
import time
from . import card
from . import deck
from . import human_player
from . import bot_player


class Uno:
    def __init__(self,ctx,client):
        self.ctx = ctx
        self.client = client

    async def selectPlayers(self):
        def checkIsHumanOrBot(msg):
            return msg.content.lower() == "humano" or msg.content.lower() == "bot"
        self.players = []
        bot_names = ["Bot Hannibal","Bot Cuei","Bot TeamFox","Bot Vialdo"]
        players_names =  []
        await self.ctx.send("Digite 'humano' para entrar no jogo")
        await self.ctx.send("Digite 'bot' para um bot entrar no jogo")
        await self.ctx.send("Participantes:")
        while len(self.players) < 4:
            try:
                player_selection = await self.client.wait_for("message",check=checkIsHumanOrBot,timeout=30.0)
                await self.ctx.channel.purge(limit=1)
                if player_selection.content.lower() == "humano":
                    new_player = human_player.Human(player_selection.author,self.client)
                    if new_player.get_name() not in players_names:
                        players_names.append(new_player.get_name())
                        self.players.append(new_player)
                        await self.ctx.send(f"**[JOGADOR]** {new_player.get_name()}")
                else:
                    name = random.choice(bot_names)
                    bot_names.remove(name)
                    new_player = bot_player.Bot(name)
                    self.players.append(new_player)
                    await self.ctx.send(f"**[BOT]** {new_player.get_name()}")
                
            except asyncio.TimeoutError:
                await self.ctx.send("Nao houve jogadores suficientes!")
                raise ValueError("Not enough players")
        await self.ctx.send("Tudo pronto para comecar!")


    def give_cards(self):
        initial_hand_number_of_cards = 7
        for player in self.players:
            player_initial_hand = self.deck.draw_cards(initial_hand_number_of_cards)
            player.set_hand(player_initial_hand)


    async def start_game(self):
        game_is_over = False
        await self.selectPlayers()
        self.deck = deck.Deck()
        self.give_cards()
        self.rotation = '→'
        players_on_order = self.players
        card_on_top = self.deck.draw_cards(1)[0]
        while card_on_top.get_color() == "black":
            card_on_top = self.deck.draw_cards(1)[0]
        await self.ctx.send(content="Carta Inicial:",file=discord.File(card_on_top.get_image()))
        cards_to_be_draw = 0
        i = 0
        while not game_is_over:
            await self.print_situation()
            i = i % 4
            while i < 4 and not self.game_is_over():
                player = players_on_order[i]
                await self.ctx.send(f"Vez de {player.get_name()}!")
                
                if cards_to_be_draw == 0:
                    if not player.has_legal_cards(card_on_top):
                        await self.ctx.send(f"{player.get_name()} não tem cartas válidas para jogar!")
                        while not player.has_legal_cards(card_on_top):
                            time.sleep(1.2)
                            await self.ctx.send(f"{player.get_name()} comeu 1 carta!")
                            player.draw_cards(self.deck.draw_cards(1))
                    try:
                        card = await player.make_move(card_on_top)
                    except asyncio.TimeoutError:
                        await self.ctx.send(f"{player.get_name()} nao fez uma jogada, passando a vez!")
                    except ValueError:
                        await self.ctx.send(f"{player.get_name()} fez uma jogada invalida, passando a vez!")
                    else:
                        if card_on_top.is_legal_to_put_on_top(card):
                            await self.ctx.send(content =f"{player.get_name()} jogou {card.get_text_based_card()}!",file=discord.File(card.get_image()))
                            if card.get_identifier() == "🛇":
                                await self.ctx.send(f"Vez de {players_on_order[(i+1)%4].get_name()} foi pulada")
                                i += 1
                            elif card.get_identifier() == "4+":
                                cards_to_be_draw += 4
                            elif card.get_identifier() == "2+":
                                cards_to_be_draw += 2
                            elif card.get_identifier() == "⤡":
                                players_on_order = self.rotate_players(players_on_order,i)
                                i = -1
                            if card.get_color() == "black":
                                try:
                                    color_selected = await player.select_color()
                                except asyncio.TimeoutError:
                                    await self.ctx.send(f"{player.get_name()} não selecionou uma cor")
                                    await self.ctx.send(f"Selecionando :red_circle: por padrão.")
                                    card.set_color("red")
                                else:
                                    card.set_color(color_selected)
                                    await self.ctx.send(f"{player.get_name()} selecionou :{color_selected}_circle:")
                            card_on_top = card
                            

                else:
                    if player.can_stack_draw_card(card_on_top):
                        card = await player.make_move(card_on_top,stack_card=True)
                        if card.get_identifier() == card_on_top.get_identifier():
                            await self.ctx.send(content =f"{player.get_name()} jogou {card.get_text_based_card()}!",file=discord.File(card.get_image()))
                            if card.get_identifier() == "4+":
                                cards_to_be_draw += 4
                                try:
                                    color_selected = await player.select_color()
                                except asyncio.TimeoutError:
                                    await self.ctx.send(f"{player.get_name()} não selecionou uma cor")
                                    await self.ctx.send(f"Selecionando :red_circle: por padrão.")
                                    card.set_color("red")
                                else:
                                    card.set_color(color_selected)
                                    await self.ctx.send(f"{player.get_name()} selecionou :{color_selected}_circle:")
                            if card.get_identifier() == "2+":
                                cards_to_be_draw += 2
                            card_on_top = card
                        else:
                            await self.ctx.send(f"{player.get_name()} comeu {cards_to_be_draw} cartas!")
                            player.draw_cards(self.deck.draw_cards(cards_to_be_draw))
                            cards_to_be_draw = 0
                    else:
                        await self.ctx.send(f"{player.get_name()} comeu {cards_to_be_draw} cartas!")
                        player.draw_cards(self.deck.draw_cards(cards_to_be_draw))
                        cards_to_be_draw = 0
                i += 1
                if player.get_how_many_cards() == 0:
                    await self.ctx.send(f"**{player.get_name()} ganhou!** :partying_face: :trophy: ")
                    game_is_over = True
                    break

    def rotate_players(self,lst,i):
        if self.rotation == '→':
            self.rotation = '←'
        else:
            self.rotatation = '→'
        rotated_lst = []
        while len(rotated_lst) != len(lst):
            i = (i-1)%4
            rotated_lst.append(lst[i])
        return rotated_lst
    

    def game_is_over(self):
        for player in self.players:
             if player.get_how_many_cards() == 0:
                 return True
        return False
    
    

    async def print_situation(self):
        await self.ctx.send("Situação do jogo:")
        await self.ctx.send(f"{self.players[0].get_name()}**[{self.players[0].get_how_many_cards()}]** {self.rotation} {self.players[1].get_name()}**[{self.players[1].get_how_many_cards()}]** {self.rotation} {self.players[2].get_name()}**[{self.players[2].get_how_many_cards()}]** {self.rotation} {self.players[3].get_name()}**[{self.players[3].get_how_many_cards()}]**")


        
       