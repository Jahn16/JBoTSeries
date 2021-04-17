from selenium import webdriver
import bs4 as bs
import os
import random
import discord


class Meme():

    def set_title(self, title):
        self.title = title

    def set_img(self, img):
        self.img = img

    def set_rating(self, rating):
        self.rating = rating

    def get_title(self):
        return self.title

    def get_img(self):
        return self.img

    def get_rating(self):
        return self.rating

memes = []

def scrap_memes():

    driver = webdriver.Chrome('c:/JboTSeries/webscrap/webdriver/chromedriver.exe')
    driver.get('https://pt.memedroid.com/memes/top/day')
    res = driver.execute_script("return document.documentElement.outerHTML")
    driver.quit()
    soup = bs.BeautifulSoup(res, 'html5lib')
    memes_containers = soup.find_all('div', class_='item-aux-container')
    for meme_container in memes_containers:
        try:
            meme_title = meme_container.find('a', class_='item-header-title').get_text()
            meme_img = meme_container.find('img', class_='img-responsive')
            integer_meme_rating = int(meme_container.find('span', class_='green-1').get_text().replace("%",""))
            meme = Meme()
            meme.set_title(meme_title)
            meme.set_img(meme_img['src'])
            if integer_meme_rating >= 96:
                emoji_meme_rating = '🤣'
            elif integer_meme_rating >= 94:
                emoji_meme_rating = '😆'
            elif integer_meme_rating >= 92:
                emoji_meme_rating = '😐'
            else:
                emoji_meme_rating = '🤢'
            meme.set_rating(emoji_meme_rating)
            memes.append(meme)
        except TypeError:
            print('Error: Image not found.')

def get_meme():
    if len(memes) == 0:
        scrap_memes()
    randomMeme = random.choice(memes)
    memes.remove(randomMeme)
    embed = discord.Embed(
        title = randomMeme.get_title(),
        colour = discord.Color.green()
    )
    embed.set_image(url=randomMeme.get_img())
    embed.set_footer(text= 'Qualidade: ' + randomMeme.get_rating())
    return embed
