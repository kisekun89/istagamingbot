import telebot
import requests
import time
from bs4 import BeautifulSoup

# === CONFIGURAZIONE ===
BOT_TOKEN = '7267062520:AAHPb1Wy1VbsvZ9qBYO-pbaQ6G7PqQbF_KQ'
CHANNEL_ID = '@mangagaming_deals'
AFFILIATE_CODE = '?igr=gamer-1ded01f'

# === FUNZIONE PER OTTENERE OFFERTE ===
def get_offer():
    url = 'https://www.instant-gaming.com/it/offerte/'
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    first_game = soup.select_one('div[class*="item main"]')

    if not first_game:
        return None

    title = first_game.select_one('div.name').text.strip()
    price = first_game.select_one('div.price').text.strip()
    image = first_game.select_one('img')['data-src']
    relative_link = first_game.select_one('a')['href']
    full_link = 'https://www.instant-gaming.com' + relative_link + AFFILIATE_CODE

    messaggio = f"🎮 <b>{title}</b>\n💸 Prezzo: <b>{price}</b>\n🔗 <a href='{full_link}'>Clicca qui per acquistare</a>"

    return messaggio, image

# === INVIA MESSAGGIO SU TELEGRAM ===
def invia_messaggio(bot):
    try:
        offerta = get_offer()
        if offerta:
            messaggio, immagine = offerta
            bot.send_photo(CHANNEL_ID, immagine, caption=messaggio, parse_mode='HTML')
    except Exception as e:
        print(f'❌ Errore nell’invio: {e}')

# === LOOP AUTOMATICO ===
if __name__ == '__main__':
    bot = telebot.TeleBot(BOT_TOKEN)
    while True:
        invia_messaggio(bot)
        print("✅ Offerta inviata. Attendo 1 ora...")
        time.sleep(3600)
