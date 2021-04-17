from games.tictactoe.move import Move
import asyncio
import discord

class Human(): 
    def __init__(self,client,player):
        self.player = player
        self.client = client
        self.discord_member = None

    def setName(self,name):
        self.name = name
    
    def getName(self):
        return self.name


    def set_discord_member(self,discord_member):
        self.discord_member = discord_member

    def get_discord_member(self):
        return self.discord_member


    async def makeMove(self,ctx,board):

        def checkMove(msg):
            valid_moves = []
            for i in range(1,10):
                valid_moves.append(str(i))
            return msg.author.name == self.name and msg.content in valid_moves


        roles = ctx.guild.roles
        competitor_role = discord.utils.get(roles, name = 'Competindo')
        if self.discord_member != None:
            await self.discord_member.add_roles(competitor_role)
        await ctx.send("Jogada **[1-9]**:")
        move = await self.client.wait_for('message',check=checkMove,timeout=45.0)

        if self.discord_member != None:
            await self.discord_member.remove_roles(competitor_role)
        move = Move(int(move.content) - 1)
        move.setPlayer(self.player)
        return move
                
        
    