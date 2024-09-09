import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
import asyncio

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)
active = False
target_user_id = '478794727232241664'  # replace with the ID of the user you want to track

async def search_steam_sales():
    while True:
        if active:
            url = "https://store.steampowered.com/search/?filter=topsellers&specials=1"
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')

            games = soup.find_all('div', {'class': 'responsive_search_name_combined'})

            for game in games:
                discount = game.find('div', {'class': 'col search_discount responsive_secondrow'}).get_text(strip=True)
                if discount == "-100%":
                    title = game.find('span', {'class': 'title'}).get_text(strip=True)
                    reviews = game.find('span', {'class': 'search_review_summary'})
                    if reviews:
                        reviews = reviews['data-tooltip-html'].split('<br>')[0]
                    else:
                        reviews = "No reviews"
                    await bot.get_channel(1249009867558223873).send(f"Title: {title}\nDiscount: {discount}\nReviews: {reviews}")
        await asyncio.sleep(64800)  # wait for 18 hours

@bot.event
async def on_member_update(before, after):
    global active
    if str(after.id) == target_user_id and str(after.status) == 'online':
        active = True
    elif str(after.id) == target_user_id and str(after.status) == 'offline':
        active = False

@bot.event
async def on_ready():
    bot.loop.create_task(search_steam_sales())

bot.run('MTA4MjE5NjAxMjQ4MDg2NDMwOA.GehZX3.cf18n0qPAjsLD9aqFG7TtVOpYSX8R0XIgeP0B0')
