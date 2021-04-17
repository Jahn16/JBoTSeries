
class Player():


    def __init__(self,discord_member):
        self.discord_member = discord_member
        self.name = discord_member.name

    def __eq__(self,other):
        return self.discord_member == other.get_discord_member()

    def set_name(self,name):
        self.name = name

    def get_name(self):
        return self.name


    def set_discord_member(self,discord_member):
        self.discord_member = discord_member

    def get_discord_member(self):
        return self.discord_member


