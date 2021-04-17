import discord
from discord.ext import commands

import asyncio
import random
import string
import time
from googletrans import Translator
from games.tournament.image_processing.image_drawer import draw_podium
from games.tournament.player import Player
class MiscelaniousCommands(commands.Cog):
    def __init__(self,client):
        self.client = client
        self.changing_names = False


    
    @commands.command(aliases = ['lc'])
    async def limparchato(self, ctx,number_of_messages: int,*,message_content = None):
        if number_of_messages <= 100:
            await ctx.channel.purge(limit=number_of_messages)
        else:
            await ctx.send('O maximo eh 100 amigo')

    


    @commands.command()
    async def ddos(self,ctx):

        def generate_random_name():
            name = ''
            name_len = random.randrange(5, 20)
            letters = string.ascii_letters
            numbers = range(10)
            for _ in range(name_len):
                random_fifty_fifty_choice = random.choice([True, False])
                if random_fifty_fifty_choice:
                    letter = random.choice(letters)
                    random_fifty_fifty_choice = random.choice([True, False])
                    if random_fifty_fifty_choice:
                        letter.upper()
                    name += letter
                else:
                    number = random.choice(numbers)
                    name += str(number)
            return name


        if not self.changing_names:
            self.changing_names = True
            await ctx.send(f'{ctx.author.name} comecou um ataque DDOS!',tts = True)
            await ctx.send('**RUUNNNNNNNN!!!!**', tts = True)
            guild = ctx.guild
            guild_members = guild.members

            original_names = []
            original_roles = []
            randomized_roles = []
            randomized_names = ['Kummerspeck','Shemomedjamo','Mencolek' ,'Tingo','Seigneur-terraces','Badruka','丝','进步','带回','功效','一','感','接纳','路','兼顾','测量','注意深い','日本酒','ジャガイモ','漏れる','響く','トースト','摩擦','ついで','転がす','光る','das Picknick','der Elefant','gefühlt','zwingen','die Speisekarte','christlich','der Auftritt','die Schwester','Spitze!','der Eindruck','платиться','присутствующий','разгореться','выдача','каморка','революционер','отчётный','право','охлаждать','знаменитый','celui','tiers','un sauvetage','un enjeu','surprenant','une traversée','rapidement','prévisible','un empire','une proximité']
            for _ in range(random.randrange(1, round(len(guild_members)/2))):
                randomized_role = await guild.create_role(name=f'HacKeD{random.randrange(999)}', hoist=True,
                                                          colour=discord.Colour.from_rgb(random.randrange(255),
                                                                                         random.randrange(255),
                                                                                         random.randrange(255)))
                randomized_roles.append(randomized_role)
            try:
                for member in guild_members:
                    original_names.append(member.display_name)
                    member_roles = member.roles
                    original_roles.append(member_roles)
                    try:
                        await member.edit(nick=random.choice(randomized_names), reason='Hacker Attack!')
                        for role in member_roles[1:]:
                            if role.name != member.name:
                                await member.remove_roles(role, reason='Hacker Attack!')
                        await member.add_roles(random.choice(randomized_roles))
                    except discord.Forbidden:
                        pass
            except Exception as e:
                print(str(e))
                pass
            time.sleep(180)
            await ctx.send(f'Consegui deter o meliante {ctx.author.name}!')
            await ctx.send(f'Estou tentando normalizar a situacao!')



            for randomized_role in randomized_roles:
                await randomized_role.delete()

            for index, member in enumerate(guild_members):
                try:
                    member_roles = original_roles[index]
                    await member.edit(nick=original_names[index],
                                      reason='IsButSeries killed the Hacker and saved the day')

                    for role in member_roles[1:]:
                        await member.add_roles(role)
                except discord.Forbidden:
                    pass


            self.changing_names = False
            await ctx.send('Mais um dia salvo por IsButSeries')
        else:
            await ctx.send('Ja estao tentado hackear aqui, to tentando matar o meliante.')

    @commands.command()
    async def reset(self, ctx):
        guild = ctx.guild
        guild_roles = guild.roles
        for role in guild_roles:
            if 'HacKeD' in role.name:
                await role.delete()
        for member in guild.members:
            try:
                await member.edit(nick=member.name, reason='Reseting...')
                if not member.bot:
                    trupe_role = discord.utils.get(guild.roles, name = 'Members')
                    await member.add_roles(trupe_role)
                else:
                    bot_role = discord.utils.get(guild.roles, name = 'BOTs')
                    #await member.add_roles(bot_role)
            except discord.Forbidden:
                pass

    @commands.command()
    async def troca(self, ctx):
        if not self.changing_names:
            self.changing_names = True
            guild = ctx.guild
            guild_members = guild.members
            random.shuffle(guild_members)
            members_names = []
            members_roles = []
            await ctx.send('Danca das cadeiras!')
            for member in guild_members:
                members_names.append(member.display_name)
                member_roles = []
                for role in member.roles:
                    if role.name != member.name:
                        member_roles.append(role)
                members_roles.append(member_roles)
            for i in range(round(len(guild_members)/2)):
                member_one = guild_members[i]
                member_two = guild_members[len(guild_members)-1-i]
                try:
                    member_one_name = member_one.display_name
                    member_one_roles = member_one.roles
                    member_two_name = member_two.display_name
                    member_two_roles = member_two.roles
                    try:
                        await member_one.edit(nick = member_two_name)
                    except discord.Forbidden:
                        pass
                    try:
                        await member_two.edit(nick = member_one_name)
                    except discord.Forbidden:
                        pass

                    for role in member_one_roles:
                        if role.name != member_one_name and not role.is_default() and not role.managed:
                            try:
                                await member_one.remove_roles(role)
                            except discord.Forbidden:
                                pass
                    for role in member_two_roles:
                        if role.name != member_two_name and not role.is_default() and not role.managed:
                            try:
                                await member_two.remove_roles(role)
                            except discord.Forbidden:
                                pass
                    for role in member_two_roles:
                        if role.name != member_two_name and not role.is_default() and not role.managed:
                            try:
                                await member_one.add_roles(role)
                            except discord.Forbidden:
                                pass
                    for role in member_one_roles:
                        if role.name != member_one_name and not role.is_default() and not role.managed:
                            try:
                                await member_two.add_roles(role)
                            except discord.Forbidden:
                                pass

                except discord.Forbidden:
                    pass
            time.sleep(120)
            await ctx.send('Arrumando a bagunca!')
            for member,name,roles in zip(guild_members,members_names, members_roles):
                try:
                    await member.edit(nick = name)
                except discord.Forbidden:
                    pass
                member_roles = member.roles
                for role in member_roles:
                    if role.name != member.name and not role.is_default() and not role.managed:
                        try:
                            await member.remove_roles(role)
                        except discord.Forbidden:
                            pass
                for role in roles:
                    if role.name != member.name and not role.is_default() and not role.managed:
                        try:
                            await member.add_roles(role)

                        except discord.Forbidden:
                            pass
                self.changing_names = False
        else:
            await ctx.send('Ja to mudando os nomes aqui  zop!')




    @commands.command()
    async def adoro(self, ctx):
        if not self.changing_names:
            self.changing_names = True
            guild = ctx.guild
            guild_members = guild.members
            members_names = []
            for member in guild_members:
                members_names.append(member.display_name)
            for member in guild_members:
                try:
                    random_name =  random.choice(members_names)
                    love_or_hate = random.choice(['ADORO','ODEIO'])
                    if random_name in ['LavaGrr','marininha','MariMari','hanna_lemos','luamuzzi','poti','marinalimeres','Ayana']:
                        artigo = 'A'
                    else:
                        artigo = 'O'
                    new_name = f'{love_or_hate} {artigo} {random_name.upper()}'
                    while len(new_name) > 32:
                        random_name = random.choice(members_names)
                        if random_name in ['LavaGrr', 'marininha', 'MariMari', 'hanna_lemos', 'luamuzzi', 'poti',
                                           'marinalimeres','Ayana']:
                            artigo = 'A'
                        else:
                            artigo = 'O'
                        new_name = f'{love_or_hate} {artigo} {random_name.upper()}'
                    await member.edit(nick=new_name)

                except discord.Forbidden:
                    pass
            time.sleep(120)
            for i, member in enumerate(guild.members):
                try:
                    await member.edit(nick=members_names[i])
                except discord.Forbidden:
                    pass
        else:
            await ctx.send('Ja to mudando os nomes aqui  po!')
            self.changing_names = False



    @commands.command()
    async def geradordenome(self, ctx):
        if not self.changing_names:
            self.changing_names = True
            def generate_name():
                first_names = ['Gabriel','Gustavo','Felipe','Thiago','Pedro','Bruno','Ian','Lucas']
                last_names = ['Jammal','Coelho','Machado','Baptista','MaeSilva','Neder','Vital','Leal','Castelo Branco','Dias','Ceolin','Giori','Lucas','Lage','Rocha']
                random.shuffle(last_names)
                return ' '.join([random.choice(first_names),last_names[0],last_names[1]])

            guild = ctx.guild
            guild_members = guild.members
            members_names = []
            for member in guild_members:
                members_names.append(member.display_name)
            for member in guild_members:
                try:
                    name = generate_name()
                    while len(name) > 32:
                        name = generate_name()
                    await member.edit(nick=generate_name())
                except discord.Forbidden:
                    pass
            time.sleep(180)
            for i, member in enumerate(guild.members):
                try:
                    await member.edit(nick=members_names[i])
                except discord.Forbidden:
                    pass
        else:
            await ctx.send('Ja to mudando os nomes aqui parceiro')
            self.changing_names = False

    @commands.command()
    async def historiadofelipao(self, ctx , felipao: discord.Member):
        await ctx.send('Hora da historia do Felipao...')
        await felipao.send('Oi felipao manda suas frases bacanas pra mim aqui.')
        historia = ''
        while True:
            def check(msg):
                return msg.author == felipao
            await felipao.send('Mande uma frase, ou mande "fim" para acabar')
            try:
                frase = await self.client.wait_for('message',check=check, timeout=60)
            except asyncio.TimeoutError:
                break
            else:
                historia +=  frase.content.title() + random.choice([',','.'])
                if frase.content == 'fim':
                    break
        await ctx.send('A historia: ')
        await ctx.send(historia,tts = True)



    @commands.command()
    async def sorteio(self, ctx):
        confirmation_phrases =  ['Sim, como descobriu que quero particar?','Declaro ter lido todas as normas com atenção comprometendo-me a respeitá-las.','Sou maior de 13 anos e sou seguidor de ojmol','Eu são de mente, em idade legal, não agindo sobre pressão ou influência desmedida e entendendo totalmente a natureza e extensão de toda minha propriedade, deixo tudo para Jammal.']
        def check(msg):
            return msg.content == confirmation_phrase and msg.author == member
        if ctx.author.guild_permissions.administrator:
            guild = ctx.guild
            guild_members = guild.members
            giveaway_participants = []
            confirmation_phrase = random.choice(confirmation_phrases)
            giveaway_embed = discord.Embed(title = 'Você tem a chance de ganhar de um sorteio **oficial do discord!**',
                                           description = f'''Nós estamos distribuindo algumas recompensas para a nossa comunidade.
                                                         \n Leia, e siga as instruções.
                                                         \n :one: Siga este canal na twitch: **https://www.twitch.tv/ojmol**
                                                         \n :two: Mande no chat: **{confirmation_phrase}**''',
                                           colour = discord.Colour.red()
                                           )
            giveaway_embed.set_image(url='https://vakilsearch.com/advice/wp-content/uploads/2017/11/gift-11.jpg')
            giveaway_embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/635103218963185704/9b133025ecb81c1357c1bea2dae1f32c.png?size=1024")
            await ctx.send('Um sorteio começou, fique esperto!',tts=True)
            sorteio_role = discord.utils.get(guild.roles, name='Sorteio')
            for member in guild_members:
                if str(member.status) == 'online' and not member.bot :
                    try:
                        await member.send(embed=giveaway_embed)
                    except Exception:
                        pass
                    else:
                        try:
                            await self.client.wait_for('message',check=check,timeout=60)
                        except asyncio.TimeoutError:
                            await member.send('Perdeu a maior oportunidade da sua vida :disappointed_relieved: ')
                        except discord.Forbidden:
                            pass
                        else:
                            giveaway_participants.append(member)
                            await member.send('Participação confirmada!')
                            try:

                                await member.add_roles(sorteio_role)
                            except discord.Forbidden:
                                pass
            time.sleep(30)
            giveaway_result_annoucement = ''
            for member in giveaway_participants:
                giveaway_result_annoucement += member.mention + ' '
            if len(giveaway_participants) > 0:

                await ctx.send(giveaway_result_annoucement)
                await ctx.send('O resultado do sorteio será anunciado em instantes!',tts=True)
                time.sleep(40)
                giveaway_winner = random.choice(giveaway_participants)
                await ctx.send(':drum: :drum: :drum: :drum: :drum: :drum: :drum: :drum: :drum: ')
                await ctx.send('O vencedor do sorteio foi...',tts=True)
                time.sleep(10)
                await ctx.send(f'{giveaway_winner.mention} Parabéns!',tts=True)
                await ctx.send('Parabéns!', tts=True)
                maioral_role = discord.utils.get(guild.roles, name = 'Vencedor do Sorteio')
                await giveaway_winner.add_roles(maioral_role)
            for member in giveaway_participants:
                try:
                    await member.remove_roles(sorteio_role)
                except discord.Forbidden:
                    pass
        else:
            await ctx.send('So ADMs podem iniciar um sorteio.')

    @commands.command()
    async def transicao(self, ctx ,new_voice_channel_name,current_voice_channel_name=None):
        member = ctx.author
        if member.voice != None or current_voice_channel_name != None:
            channel_converter = discord.ext.commands.VoiceChannelConverter()
            if current_voice_channel_name == None:
                current_voice_channel = member.voice.channel
            else:
                try:
                    current_voice_channel = await channel_converter.convert(ctx=ctx, argument=str(current_voice_channel_name))
                except discord.ext.commands.BadArgument:
                    await ctx.send('Canal nao existe.')
            try:
                new_voice_channel = await channel_converter.convert(ctx= ctx, argument = str(new_voice_channel_name))
            except discord.ext.commands.BadArgument:
                await ctx.send('Canal nao existe.')
            else:
                for member in current_voice_channel.members:
                    await member.move_to(new_voice_channel)
                await ctx.send(f'Trancionados os membros de {current_voice_channel.name} para {new_voice_channel.name}!')

    @commands.command()
    async def maesilva(self, ctx):
        await ctx.send('Procurando o MaeSilva...')
        message = await ctx.send(ctx.author.display_name)
        guild = ctx.guild
        members = guild.members
        random.shuffle(members)

        for member in members:
            await message.edit(content = member.display_name + '...')
            if member.id == 567011004454535188:
                await ctx.send('Achei ele!')
                await member.edit(nick = 'PedroMa')
                return 0
        await ctx.send('Nao encontrei o PedroMa!')


    @commands.command()
    async def test(self, ctx, member: discord.Member):
        print(member.id)

    @commands.command()
    async def voltanome(self,ctx):
        if not self.changing_names:
            await ctx.send('Voltando nomes...')
            self.changing_names = True
            guild = ctx.guild
            for member in guild.members:

                if member.name != member.display_name:
                    print(f'{member}: {member.display_name}  -> {member.name}')
                    try:

                        await member.edit(nick=member.name, reason='Reseting...')
                    except discord.Forbidden:
                        pass
            self.changing_names = False
        else:
            await ctx.send('Ja to mudando os nomes aqui  po!')
            self.changing_names = False

    @commands.command()
    async def download(self,ctx,description,speed: float,total: float, progress=0.0):
        start = time.time()
        message = await ctx.send('Download de ' + description)
        while progress < total:
            progress += (time.time() - start) * (speed / 1000)
            start = time.time()
            time_to_complete = (total - progress) / (speed / 1000)
            await message.edit(content = f'**{description}** Velocidade: {speed} Mbps Progresso: {round(progress,2)}/{total} Tempo estimado: {round(time_to_complete / 60)} min')
        await ctx.send(f'**{description} acabou!**')


    @commands.command()
    async def penis(self, ctx):
        if not self.changing_names:
            self.changing_names = True
            guild = ctx.guild
            string_to_insert = 'penis'
            blacklist = ['LavaGrr#3090','marininha#0465','MariMari#3900','hanna_lemos#7381','luamuzzi#6408','poti#9107','marinalimeres#6633','Ayana#8911']
            for member in guild.members:
                if str(member) not in blacklist:
                    index = random.randint(0,len(member.display_name))
                    new_name = member.display_name[:index] + string_to_insert + member.display_name[index:]
                    if len(new_name) <= 32:
                        try:
                            await member.edit(nick=new_name, reason='Inapenistavel...')
                        except discord.Forbidden:
                            pass
            time.sleep(30)
            for member in guild.members:
                old_name = member.display_name.replace(string_to_insert,"")
                try:
                    await member.edit(nick=old_name, reason='Inapenistavel...')
                except discord.Forbidden:
                    pass
        else:
            await ctx.send('Ja to mudando os nomes aqui mano!')
            self.changing_names = False

    @commands.command()
    async def vazar(self, ctx):
        await ctx.message.delete()
        await ctx.send('Estou sendo **hackeado!**')
        msg = await ctx.send('**Vazando** informações')
        start = time.time()

        progress = 0
        total = 300
        message = await ctx.send('Vazando o IP do server')
        while progress < total:
            progress += time.time() - start
            start = time.time()
            time_to_complete = total - progress
            await message.edit(
                content=f'**Progresso:** _{round(progress, 2)}/{total}_ **Tempo estimado:** _{round(time_to_complete / 60)}_ min')
        await ctx.send(f'**190.115.196.24:10411**')

    @commands.command()
    async def flood(self,ctx,number_of_messages: int,*,message_content):
        await ctx.message.delete()
        max = 10
        if number_of_messages <= max:
            messages = []
            for _ in range(number_of_messages):
                message = await ctx.send(message_content, delete_after=30)
                messages.append(message)

        else:
            await ctx.send(f'Sem patifaria, no maximo {max}!')

    @commands.command()
    async def prank(self, ctx):
        member = ctx.author
        if member.voice != None:
            voice_channel = member.voice.channel
            for member in voice_channel.members:
                mute = random.choice([True,False])
                if mute:
                    await member.edit(mute = True)
                else:
                    await member.edit(deafen = True)
            time.sleep(5)
            for member in voice_channel.members:
                await member.edit(mute = False,deafen = False)

    @commands.command()
    async def filme(self, ctx):
        guild = ctx.guild
        movie = random.choice(['shrek'])
        text_channel = await guild.create_text_channel(movie)
        await text_channel.send(f'Vai comecar o filme! {guild.default_role.mention}')
        await asyncio.sleep(60)
        for line in open(r'C:\Users\jpdeo\Downloads\shrek.txt','r'):
            if repr(line) != "'\\n'":
                await text_channel.send(line)
                await asyncio.sleep(60 * (((len(line) / 5)) / 225 ))
        await text_channel.delete(reason = 'Acabou o filme')
    @commands.command()
    async def ban(self, ctx , member: discord.Member):
        if member.name not in ['Jahn','IsButSeries']:
            votes = 1
            minimum_votes = 10
            member_who_voted = [ctx.author]
            await ctx.send(f'{votes}/{minimum_votes}')
            def check(msg):
                return msg.content == f'{votes + 1}/{minimum_votes}' and msg.author not in member_who_voted
            while votes < minimum_votes:
                try:
                    message = await self.client.wait_for('message',timeout=60,check=check)
                except asyncio.TimeoutError:
                    await ctx.send(f'**{member.display_name}** escapou!')
                    return False
                else:
                    await ctx.send('Voto confirmado!')
                    votes += 1
                    member_who_voted.append(message.author)
            last_words = 'Não teve ultímas palavras.'
            async for message in ctx.history(limit=200):
                if message.author == member:
                    last_words = message.content
                    break

            embed = discord.Embed(title = 'R.I.P ' + member.display_name,
                                 description= 'Um grande amigo e pai.')
            embed.add_field(name = 'Ultímas palavras',value = last_words)
            embed.set_image(url = member.avatar_url)
            await ctx.send(embed = embed)
            time.sleep(45)
            await member.kick()
            await ctx.send('F')
            return True
        else:
            await ctx.send('Nada, esse cara eh gente boa.')





def setup(client):
    client.add_cog(MiscelaniousCommands(client))