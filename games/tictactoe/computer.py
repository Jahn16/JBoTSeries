import random
from sys import maxsize
import copy
class Computer():

    def __init__(self,player,difficult):
        self.player = player
        self.difficult = difficult

    def setName(self,name):
        self.name = name
        
    def makeMove(self,board):
        higherValue = -maxsize
        possibleMoves = board.getPossibleMoves()

        values = []
        for move in possibleMoves:
            move.setPlayer(self.player)
            boardCopy = copy.deepcopy(board)
            boardCopy.makeMove(move)
            value = self.min(boardCopy,self.difficult)
            values.append(value)
            if value > higherValue:
                higherValue = value
                bestMove = move
        print(values)
        return bestMove

    def max(self,board,limit):
        if board.checkForWinner() != "No Winner" or board.boardIsFull() or limit==0:
            return self.avaluateBoard(board,self.player)+limit
        higherValue = -100
        possibleMoves = board.getPossibleMoves()

        for move in possibleMoves:
            move.setPlayer(self.player)
            boardCopy = copy.deepcopy(board)
            boardCopy.makeMove(move)
            value = self.min(boardCopy,limit-1)
            if value >= higherValue:
                higherValue = value
        return higherValue
            
        
    def min(self,board,limit):
        if board.checkForWinner() != "No Winner" or board.boardIsFull() or limit==0:
            return self.avaluateBoard(board,self.player) + limit
        lowestValue = 100
        possibleMoves = board.getPossibleMoves()

        opponentPlayer = self.getOpponentPlayer()
        for move in possibleMoves:
            move.setPlayer(opponentPlayer)
            boardCopy = copy.deepcopy(board)
            boardCopy.makeMove(move)
            value = self.max(boardCopy,limit-1)
            if value <= lowestValue:
                lowestValue = value
        return lowestValue
          

    def avaluateBoard(self,board,player):
        winner = board.checkForWinner()
        if winner == player:
            return 100
        elif winner == "No Winner":
            return 0
        else:
            return -100

    def get_moves(self,board):
        moves = {}
        possibleMoves = board.getPossibleMoves()


        for move in possibleMoves:
            move.setPlayer(self.player)
            boardCopy = copy.deepcopy(board)
            boardCopy.makeMove(move)
            value = self.min(boardCopy, self.difficult)
            moves[move] = value
        return moves

    def getOpponentPlayer(self):
        if self.player == "X":
            return "O"
        else:
            return "X"