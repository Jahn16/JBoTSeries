class Player():

    def __init__(self,discord_member, discord_client):
        self.discord_member = discord_member
        self.discord_client = discord_client
        self.name = discord_member.display_name
        self.discussion_votes = 0
        self.werewolf_votes = 0

    def __eq__(self,other):
        if isinstance(other, Player):
            return self.name == other.get_name()
        else:
            return False


    def set_name(self,name):
        self.name = name

    def get_name(self):
        return self.name

    def get_discord_member(self):
        return self.discord_member

    def set_role(self,role):
        self.role = role
        self.role.set_player(self)

    def get_role(self):
        return self.role

    def set_discussion_votes(self, votes):
        self.discussion_votes = votes

    def get_discussion_votes(self):
        return self.discussion_votes

    def set_werewolf_votes(self, votes):
        self.werewolf_votes = votes

    def get_werewolf_votes(self):
        return self.werewolf_votes

    async def make_action(self,round_number,players,actions):
        await self.discord_member.send('**--------------- JOGADA -------------**')
        action = await self.role.make_action(round_number,players,actions)
        return action


    def vote(self,players):
        print('**Votação:**')
        for index,player in enumerate(players,start = 1):
            if player != self:
                print(f'**{index}.** {player.get_name()} [ {player.get_discussion_votes()} ]')
        return players[index]


