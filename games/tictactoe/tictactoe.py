import discord
from games.tictactoe.board import Board
from games.tictactoe.human import Human
from games.tictactoe.computer import Computer
from discord.ext.commands import UserConverter,BadArgument

import asyncio
import copy
import random
import time

class TicTacToe:

    def __init__(self,ctx,client):
        self.client = client
        self.ctx = ctx
        self.player_one = None
        self.player_two = None

    def get_gamemode(self):
        return "Jogo da Velha"
    
    def set_player_one(self,player_one):
        self.player_one = Human(self.client, "X")
        self.player_one.set_discord_member(player_one)
        self.player_one.setName(player_one.name)


    def set_player_two(self, player_two):
        self.player_two = Human(self.client, "O")
        self.player_two.set_discord_member(player_two)
        self.player_two.setName(player_two.name)

    def get_winner(self):
        return self.winner
    async def start(self):
        self.player_one = Human(self.client, "X")
        self.player_one.set_discord_member(self.ctx.author)
        self.player_one.setName(self.ctx.author.display_name)
        self.player_two = Computer("O", 15)
        self.player_two.setName("IsButSeries")
        if self.player_one == None:
            await self.choosePlayers()

        game_info = discord.Embed(title = 'Jogo da Velha' ,
                                  color= discord.Colour.purple())
        game_info.add_field(name = 'Regras:',
                            value = '''No começo do jogo um jogador será escolhido como **ofensivo** e outro como **defensivo**.
                                   O objetivo do jogador ofensivo é ganhar qualquer uma das **3 rodadas** que serão jogadas, já a do defensivo é se defender em todas elas. 
                                  **OBS:** O jogador defensivo, como não é seu objetivo, caso ganhe uma rodada não ganha o jogo.'''
                            )
        game_info.set_image(url='https://img2.ugamezone.com/201901/2019/1122/be/0/813218/hd200.jpg')
        await self.ctx.send(embed= game_info)
        #time.sleep(30)
        #offensive_player, defensive_player = random.sample([self.player_one, self.player_two], 2)
        offensive_player, defensive_player = [self.player_one, self.player_two]
        await self.ctx.send(f'**{offensive_player.name}** foi escolhido para ser o jogador **ofensivo**.')
        for round in range(3):
            await self.ctx.send("**-----------------------------------------------**")
            if self.player_one == offensive_player:
                await self.ctx.send(f":x: -> _{self.player_one.name}_ **[OFENSIVO]**")
                await self.ctx.send(f":o: -> _{self.player_two.name}_ **[DEFENSIVO]**")
            else:
                await self.ctx.send(f":x: -> _{self.player_one.name}_ **[DEFENSIVO]**")
                await self.ctx.send(f":o: -> _{self.player_two.name}_ **[OFENSIVO]**")
            await self.ctx.send("**-----------------------------------------------**")
            #time.sleep(15)

            currentPlayer = offensive_player
            await self.ctx.send(f"**{currentPlayer.name}** começa jogando!")
            board = Board()
            await board.printBoard(self.ctx)
            while board.checkForWinner() == "No Winner" and not board.boardIsFull() and not board.checkForTie():
                await self.ctx.send(f"Vez de **{currentPlayer.name}**:")
                try:
                    if isinstance(currentPlayer,Human):
                        try:
                            move = await currentPlayer.makeMove(self.ctx,copy.deepcopy(board))
                            board.makeMove(move)
                        except asyncio.TimeoutError:
                            await self.ctx.send(f"**{currentPlayer.name}** não fez uma jogada!")
                            await self.ctx.send("Perdeu por **WO**")
                            if currentPlayer == self.player_one:
                                self.winner = self.player_two
                                return 0
                            else:
                                self.winner = self.player_one
                                return 0
                    else:
                        board.makeMove(currentPlayer.makeMove(copy.deepcopy(board)))
                except ValueError:
                    await self.ctx.send("Jogada Inválida")
                await board.printBoard(self.ctx)
                if currentPlayer == self.player_one:
                    currentPlayer = self.player_two
                else:
                    currentPlayer = self.player_one
                if board.checkForWinner() == offensive_player.player:
                    await self.ctx.send(f"**{offensive_player.name}** ganhou! :trophy:")
                    self.winner = offensive_player
                    return 0
                elif board.checkForWinner() == defensive_player.player:
                    await self.ctx.send(f"**{defensive_player.name}** ganhou a rodada, mas como é um jogador defensivo não ganhou o jogo ainda.")
                elif board.checkForTie() or board.boardIsFull():
                    await self.ctx.send("Deu velha!")
            if round != 3:
                await self.ctx.send('Recomecando...')
        await self.ctx.send(f"**{defensive_player.name}** se defendeu todas as rodadas, sendo assim o vencedor. :trophy:")
        self.winner = defensive_player


    #Choose self.player 1 and self.player 2
    async def choosePlayers(self):

        def check(msg):
            return len(msg.content) > 0 and not msg.author.bot

        player = self.ctx.author

        isFirstPlayer = random.choice((True,False))

        await self.ctx.send("Escolha seu oponente: ")
        await self.ctx.send("**----------------------------------**")
        await self.ctx.send("**Trupeiro:**")
        await self.ctx.send("Mande uma mensagem marcando ele")
        await self.ctx.send("**Robôs:** :robot:")
        await self.ctx.send("**I** - IsBuTSeries **[IMPOSSIBLE]**")
        await self.ctx.send("**J2** - JBotSeries2 **[HARD]**")
        await self.ctx.send("**J1** - JBotSeries **[MEDIUM]**")
        await self.ctx.send("**J** - Jammal **[EASY]**")
        await self.ctx.send("**----------------------------------**")
        try:
            selectOpponent = await self.client.wait_for('message',check=check,timeout=30.0)
        except asyncio.TimeoutError:
            await self.ctx.send("Não responde nessa merda!")
            raise ValueError("Players Not Selected")
        else:
            isValidUser = await self.isValidUser(selectOpponent.content)
            if isFirstPlayer:
                self.player_one = Human(self.client,"X")
                self.player_one.setName(player.name)
                if selectOpponent.content.upper() == "I":
                    self.player_two = Computer("O",15)
                    self.player_two.setName("IsButSeries")
                elif selectOpponent.content.upper() == "J2":
                    self.player_two = Computer("O",5)
                    self.player_two.setName("JBoT2")
                elif selectOpponent.content.upper() == "J1":
                    self.player_two = Computer("O",1)
                    self.player_two.setName("JBoT")
                elif selectOpponent.content.upper() == "J":
                    self.player_two = Computer("O",0)
                    self.player_two.setName("Jammal")
                elif isValidUser:
                    self.player_two = Human(self.client,"O")
                    opponent = await UserConverter().convert(self.ctx,selectOpponent.content)
                    self.player_two.setName(opponent.name)
                else:
                    raise ValueError("Invalid Player Selection")
            else:
                self.player_two = Human(self.client,"O")
                self.player_two.setName(player.name)
                if selectOpponent.content.upper() == "I":
                    self.player_one = Computer("X",15)
                    self.player_one.setName("IsButSeries")
                elif selectOpponent.content.upper() == "J2":
                    self.player_one = Computer("X",5)
                    self.player_one.setName("JBoT2")
                elif selectOpponent.content.upper() == "J1":
                    self.player_one = Computer("X",1)
                    self.player_one.setName("JBoT")
                elif selectOpponent.content.upper() == "J":
                    self.player_one = Computer("X",0)
                    self.player_one.setName("Jammal")
                elif isValidUser:
                    self.player_one = Human(self.client,"X")
                    opponent = await UserConverter().convert(self.ctx,selectOpponent.content)
                    self.player_one.setName(opponent.name)
                else:
                    raise ValueError("Invalid Player Selection")





    async def isValidUser(self,msg):
        try:
            converter = UserConverter()
            await converter.convert(self.ctx,msg)
            return True
        except BadArgument:
            return False

   