from aiohttp import ClientConnectionError
from games.tictactoe.tictactoe import TicTacToe
from games.trivia.trivia import Trivia
from games.typeracer.typeracer import TypeRacer
from games.music_quiz.music_quiz import MusicQuiz
from games.guess_drawing.guess_drawing import GuessDrawings
from games.perfil.perfil import Perfil
from asyncio import sleep
import random
import time

class Match():

    def __init__(self,ctx,client):
        self.ctx = ctx
        self.client = client

    def set_player_one(self,player_one):
        self.player_one = player_one

    def set_player_two(self,player_two):
        self.player_two = player_two


    def set_id(self,id):
        self.id = id

    def get_id(self):
        return self.id

    def get_player_one(self):
        return  self.player_one

    def get_player_two(self):
        return self.player_two

    def set_game(self,game):
        self.game = game

    def get_game(self):
        return self.game

    async def start(self):
        self.game.set_player_one(self.player_one.get_discord_member())
        self.game.set_player_two(self.player_two.get_discord_member())
        time_to_start = 0
        if time_to_start > 0:
            for player in [self.player_one.get_discord_member(),self.player_two.get_discord_member()]:
                await player.send(f'Você jogará uma partida em **{time_to_start}** segundos.')
            time.sleep(time_to_start)
        await self.ctx.send(f'{self.get_player_one().get_discord_member().mention} {self.get_player_two().get_discord_member().mention}')
        await self.ctx.send(f'`{self.get_player_one().get_discord_member().display_name} x {self.get_player_two().get_discord_member().display_name} | MODO DE JOGO: {self.game.get_gamemode()}`')
        for _ in range(2):
            try:
                await self.game.start()
            except ClientConnectionError as e:
                print(f'Error while trying to play match({self.get_game()}): {str(e)}')
                await sleep(300)
                await self.ctx.send('Um erro ocorreu na partida!')
            else:
                self.winner = self.game.get_winner()
                if self.winner != self.player_one:
                    self.loser = self.player_one
                else:
                    self.loser = self.player_two
                break


    def get_winner(self):
        return self.winner

    def get_loser(self):
        return self.loser

