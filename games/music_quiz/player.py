import random
class Player():


    def __init__(self,discord_member):
        self.discord_member = discord_member
        self.name = discord_member.name
        self.points = 0

    def set_name(self,name):
        self.name = name

    def get_name(self):
        return self.name


    def set_points(self,points):
        self.points = points

    def get_points(self):
        return self.points

    def set_discord_member(self,discord_member):
        self.discord_member = discord_member

    def get_discord_member(self):
        return self.discord_member

    def add_points(self,added_points = 1 ):
        self.points += added_points

