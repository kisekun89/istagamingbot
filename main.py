import telebot
import requests
import time
from bs4 import BeautifulSoup

# === CONFIG ===
BOT_TOKEN = '7267062520:AAHPb1Wy1VbsvZ9qBYO-pbaQ6G7PqQbF_KQ'
CHANNEL_ID = '@mangagaming_deals'
AFFILIATE_CODE = '?igr=gamer-1ded01f'

# === FUNZIONE PER OTTENERE OFFERTE ===
def get_offer():
    url = 'https://www.instant-gaming.com/it/offerte/'
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')

    # Trova primo gioco
    game = soup.select_one('div.cover a')
    if not game:
        print("❌ Nessuna offerta trovata.")
        return None

    title = game.get('title').strip()
    link = 'https://www.instant-gaming.com' + game.get('href') + AFFILIATE_CODE
    img = game.select_one('img').get('src')
    price_tag = game.select_one('div.price')
    price = price_tag.text.strip() if price_tag else 'Prezzo non disponibile'

    message = f"🎮 <b>{title}</b>\n💸 Prezzo: <b>{price}</b>\n🔗 <a href='{link}'>Acquista su Instant Gaming</a>"
    return message, img

# === INVIA MESSAGGIO TELEGRAM ===
def invia_messaggio(bot):
    try:
        offer = get_offer()
        if offer:
            message, image = offer
            bot.send_photo(CHANNEL_ID, image, caption=message, parse_mode='HTML')
            print("✅ Offerta inviata.")
        else:
            print("⚠️ Nessun messaggio da inviare.")
    except Exception as e:
        print(f"❌ Errore invio: {e}")

# === LOOP PRINCIPALE ===
if __name__ == '__main__':
    bot = telebot.TeleBot(BOT_TOKEN)
    while True:
        invia_messaggio(bot)
        time.sleep(3600)  # ogni ora
