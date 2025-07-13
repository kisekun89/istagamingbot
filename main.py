import telebot
import requests
import time
from bs4 import BeautifulSoup

BOT_TOKEN = '7267062520:AAHPb1Wy1VbsvZ9qBYO-pbaQ6G7PqQbF_KQ'
CHANNEL_ID = '@mangagaming_deals'
AFFILIATE_CODE = '?igr=gamer-1ded01f'

def get_offer():
    url = 'https://www.instant-gaming.com/it/pc/'
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    first_game = soup.select_one('.item')

    if not first_game:
        return None

    title = first_game.select_one('.name').get_text(strip=True)
    price = first_game.select_one('.price').get_text(strip=True)

    image_tag = first_game.select_one('img')
    image = image_tag['data-src'] if image_tag and image_tag.has_attr('data-src') else None

    link_tag = first_game.select_one('a')
    if not link_tag or not link_tag.get('href'):
        return None

    link = 'https://www.instant-gaming.com' + link_tag.get('href') + AFFILIATE_CODE
    message = f"🎮 <b>{title}</b>\n💸 Prezzo: <b>{price}</b>\n👉 <a href='{link}'>Compra ora su Instant Gaming</a>"
    return message, image

def send_offer(bot):
    try:
        offer = get_offer()
        if offer:
            message, image = offer
            if image and image.startswith('http'):
                bot.send_photo(CHANNEL_ID, image, caption=message, parse_mode='HTML')
            else:
                bot.send_message(CHANNEL_ID, message, parse_mode='HTML')
            print("✅ Offerta inviata.")
        else:
            print("⚠️ Nessuna offerta trovata.")
    except Exception as e:
        print(f"❌ Errore invio: {e}")

if __name__ == '__main__':
    bot = telebot.TeleBot(BOT_TOKEN)
    while True:
        send_offer(bot)
        time.sleep(3600)
