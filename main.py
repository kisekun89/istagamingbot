import telebot
import requests
import time
from bs4 import BeautifulSoup

# === CONFIG ===
BOT_TOKEN = '7267062520:AAHPb1Wy1VbsvZ9qBYO-pbaQ6G7PqQbF_KQ'
CHANNEL_ID = '@mangagaming_deals'
AFFILIATE_CODE = '?igr=gamer-1ded01f'

# === FUNZIONE OFFERTA ===
def get_offer():
    url = 'https://www.instant-gaming.com/it/pc/'  # Pagina meno protetta
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("❌ Errore nella richiesta HTTP.")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    first_game = soup.select_one('.item')

    if not first_game:
        print("❌ Nessuna offerta trovata nel parsing.")
        return None

    # Estrazione dati
    title = first_game.select_one('.name').get_text(strip=True)
    price = first_game.select_one('.price').get_text(strip=True)
    image = first_game.select_one('img')['src']
    link = 'https://www.instant-gaming.com' + first_game['href'] + AFFILIATE_CODE

    messaggio = f"🎮 <b>{title}</b>\n💸 Prezzo: <b>{price}</b>\n🔗 <a href='{link}'>Compra ora su Instant Gaming</a>"
    return messaggio, image

# === INVIA MESSAGGIO ===
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
        print(f"❌ Errore invio: {e}")

# === LOOP ===
if __name__ == '__main__':
    bot = telebot.TeleBot(BOT_TOKEN)
    while True:
        invia_messaggio(bot)
        time.sleep(3600)
