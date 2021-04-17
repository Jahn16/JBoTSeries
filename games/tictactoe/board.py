import discord
from games.tictactoe.move import Move
import copy

class Board():
    def __init__(self):
        self.board = [" "] * 9 #Create empty board 

    async def printBoard(self,ctx):
        board_embed = discord.Embed(color=discord.Color.purple())
        board = ""
        for i in range(0,3):
            row = ""
            for j in range(0,3):
                if self.board[(i*3)+j] == "X":
                    row += ":x:"
                elif self.board[(i*3)+j] == "O":
                    row += ":o:"
                else:
                    row += ":black_large_square:"
            board += row + '\n'
        board_embed.add_field(name = 'Tabuleiro',value=board)
        await ctx.send(embed = board_embed)

                
    def makeMove(self,move):
        if self.board[move.coordinate] == " ":
            self.board[move.coordinate] = move.player
        else:
            raise ValueError("Position already ocuppied")


    def checkCollum(self,board = None):
        if board == None:
            board = self.board
        for player in ["O","X"]:
            for collum in range(0,3):
                for row in range(0,3):
                    playerOnPosition = board[collum+(row*3)]
                    if playerOnPosition != player or playerOnPosition == " ": #Checks if opponent or none player is ocuppying this position
                        break
                    elif row == 2: #If player won return it
                        return player 
        return "No Winner"
    
    def checkRow(self,board = None):
        if board == None:
            board = self.board
        for player in ["O","X"]:
            for row in range(0,3):
                for collum in range(0,3):
                    playerOnPosition = board[(row*3)+collum]
                    if playerOnPosition != player or playerOnPosition == " ":
                        break
                    elif collum == 2:
                        return player
        return "No Winner"
    
    def checkDiagonal(self,board = None):
        if board == None:
            board = self.board
        for player in ["O","X"]:
            for diagonal in range(0,3):
                playerOnPosition = board[diagonal*4]
                if playerOnPosition != player or playerOnPosition == " ":
                    break
                elif diagonal == 2:
                    return player
        return "No Winner"

    def checkSecondaryDiagonal(self, board = None):
        if board == None:
            board = self.board
        for player in ["O","X"]:
            for diagonal in range(0,3):
                playerOnPosition = board[(diagonal*2)+2]
                if playerOnPosition != player or playerOnPosition == " ":
                    break
                elif diagonal == 2:
                    return player
        return "No Winner"

    def checkForTie(self, board = None):
        if board == None:
            board = self.board
        for player in ["O", "X"]:
            board_copy = copy.deepcopy(board)
            for index,position in enumerate(board_copy):
                if position == " ":
                    board_copy[index] = player

            if self.checkForWinner(board_copy) != "No Winner":
                return False
        return True



    def checkForWinner(self,board = None):
        if board == None:
            board = self.board
        if self.checkCollum(board) != "No Winner":
            return self.checkCollum(board)

        elif self.checkRow(board) != "No Winner": #If there's a winner
            return self.checkRow(board) #Return the Winner

        elif self.checkDiagonal(board) != "No Winner": #If there's a winner
            return self.checkDiagonal(board) #Return the Winner

        elif self.checkSecondaryDiagonal(board) != "No Winner": #If there's a winner
            return self.checkSecondaryDiagonal(board) #Return the Winner
        
        return "No Winner" #In case there's no winner
        
    def boardIsFull(self):
        for player in self.board:
            if player == " ": #if there's no player in that position
                return False
        return True



    def getPossibleMoves(self):
        possibleMoves = []
        for move in range(9):
            if self.board[move] == " ":
                move = Move(move)
                possibleMoves.append(move)
        return possibleMoves
                    
    def turnNumber(self):
        number = 0
        for player in self.board:
            if player != " ": #if there's no player in that position
                number += 1 
        return number

    def getBoard(self):
        return self.board

    def printTerminalBoard(self,board):
        for i in range(0,9):
            print("|"+board[i] , end = "")
            if (i+1) % 3 == 0:
                print("|")