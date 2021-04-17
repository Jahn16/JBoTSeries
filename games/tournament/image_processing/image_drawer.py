from PIL import Image,ImageDraw,ImageFont
import requests
import os



def draw_match_data(match):
    coordinates = {
        1: ((49,49), (120, 55 )),
        2: ((49, 219), (120, 225)),
        3: ((49,389), (120, 395)),
        4: ((49,559), (120,565)),
        5: ((49, 729), (120, 735)),
        6: ((49, 899), (120, 905)),
        7: ((445, 135 ) , (516, 141 )),
        8: ((445,473), (516,479)),
        9: ((445,729),(516,735)),
        10: ((445,899),(516,905)),
        11: ((841,303),(912,309)),
        12: ((843,814),(914,820)),
        13: ((1240, 814), (1311, 820)),
        14: ((1240, 303), (1311, 309))
    }

    path = 'c:/JboTSeries/games/tournament/image_processing/imgs/ready_bracket.webp'
    if os.path.exists(path):
        bracket_template = Image.open(path)
    else:
        bracket_template = Image.open('c:/JboTSeries/games/tournament/image_processing/imgs/bracket_template2.webp').copy()

    draw = ImageDraw.Draw(bracket_template)
    font = ImageFont.truetype(font='c:/JboTSeries/games/tournament/image_processing/fonts/Redwing-Medium.otf', size=50, index=0, encoding='', layout_engine=None)
    player_one = match.get_player_one().get_discord_member()
    player_two = match.get_player_two().get_discord_member()
    player_one_avatar = Image.open(requests.get(player_one.avatar_url_as(static_format='webp'), stream=True).raw).resize((64,64))
    player_two_avatar = Image.open(requests.get(player_two.avatar_url_as(static_format='webp'), stream=True).raw).resize((64, 64))
    x,y = coordinates[match.get_id()][0]
    bracket_template.paste(player_one_avatar,(x,y))
    bracket_template.paste(player_two_avatar, (x, y + 66))
    x, y = coordinates[match.get_id()][1]
    draw.text((x,y), player_one.display_name , font=font)
    draw.text((x,y+66), player_two.display_name, font=font)
    ready_bracket = bracket_template
    ready_bracket.save(path)
    #ready_bracket.show()
    return path

def draw_champion(champion):
    path = 'c:/JboTSeries/games/tournament/image_processing/imgs/champion.webp'
    champion_discord_member = champion.get_discord_member()
    background = Image.open(path).copy()
    draw = ImageDraw.Draw(background)
    font = ImageFont.truetype(font='c:/JboTSeries/games/tournament/image_processing/fonts/Redwing-Light.otf', size=96,
                              index=0, encoding='', layout_engine=None)
    x = 960 - (font.getsize(champion_discord_member.display_name)[0]/2)
    draw.text((x,100),champion_discord_member.display_name,font=font)
    champion_avatar_url = champion_discord_member.avatar_url_as(static_format='webp')
    champion_avatar = Image.open(requests.get(champion_avatar_url, stream=True).raw).resize((496, 496))
    background.paste(champion_avatar,(712,294))
    path = 'c:/JboTSeries/games/tournament/image_processing/imgs/champion_ready.webp'
    background.save(path)
    return path


def draw_podium(player,place):
    original_path = 'c:/JboTSeries/games/tournament/image_processing/imgs/podium.jpg'
    save_path = r'c:/JboTSeries/games/tournament/image_processing/imgs/champion_ready.jpg'
    if os.path.exists(save_path):
        background = Image.open(save_path)
    else:
        background = Image.open(original_path).copy()
    draw = ImageDraw.Draw(background)
    font_size = (48 + (( 3 - place) * 16))
    font = ImageFont.truetype(font='c:/JboTSeries/games/tournament/image_processing/fonts/Redwing-Light.otf', size=font_size,
                              index=0, encoding='', layout_engine=None)
    discord_member = player.get_discord_member()
    name = discord_member.display_name
    avatar_url = discord_member.avatar_url_as(static_format='jpg')
    avatar = Image.open(requests.get(avatar_url, stream=True).raw).resize((316, 316))
    if place == 1:
        x = 960 - (font.getsize(name)[0] / 2)
        draw.text((x, 890), name, font=font)
        background.paste(avatar, (803, 30))

    if place == 2:
        x = 480 - (font.getsize(name)[0] / 2)
        draw.text((x, 980), name, font=font)
        background.paste(avatar, (365, 77))
    if place == 3:
        x = 1430 - (font.getsize(name)[0] / 2)
        draw.text((x, 1020), name, font=font)
        background.paste(avatar, (1256, 101))



    background.save(save_path)
    return save_path

