import telebot
import requests
import time
from bs4 import BeautifulSoup

# === CONFIG ===
BOT_TOKEN = '7267062520:AAHPb1Wy1VbsvZ9qBYO-pbaQ6G7PqQbF_KQ'
CHANNEL_ID = '@mangagaming_deals'
AFFILIATE_CODE = '?igr=gamer-1ded01f'

# === HTML DEBUG: Stampa anteprima ===
def get_offer():
    url = 'https://www.instant-gaming.com/it/offerte/'
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print("❌ Errore nella richiesta.")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    games = soup.select('div.item')  # controlla tutti i blocchi gioco

    for game in games:
        title_tag = game.select_one('.title') or game.select_one('.name')
        image_tag = game.select_one('img')
        link_tag = game.select_one('a')
        price_tag = game.select_one('.price') or game.select_one('.price-discount')

        if title_tag and image_tag and link_tag:
            title = title_tag.text.strip()
            image = image_tag.get('src')
            link = 'https://www.instant-gaming.com' + link_tag.get('href') + AFFILIATE_CODE
            price = price_tag.text.strip() if price_tag else "Prezzo non disponibile"

            msg = f"🎮 <b>{title}</b>\n💸 Prezzo: <b>{price}</b>\n🔗 <a href='{link}'>Compra ora su Instant Gaming</a>"
            return msg, image
    
    print("⚠️ HTML trovato, ma nessuna offerta valida.")
    return None

# === INVIO MESSAGGIO ===
def invia_messaggio(bot):
    try:
        offerta = get_offer()
        if offerta:
            messaggio, immagine = offerta
            bot.send_photo(CHANNEL_ID, immagine, caption=messaggio, parse_mode='HTML')
            print("✅ Offerta inviata.")
        else:
            print("⚠️ Nessun messaggio da inviare.")
    except Exception as e:
        print(f"❌ Errore invio messaggio: {e}")

# === LOOP ===
if __name__ == '__main__':
    bot = telebot.TeleBot(BOT_TOKEN)
    while True:
        invia_messaggio(bot)
        time.sleep(3600)
