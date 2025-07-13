import telebot
import requests
import time
from bs4 import BeautifulSoup

# === CONFIGURAZIONE ===
BOT_TOKEN = '7267062520:AAHPb1Wy1VbsvZ9qBYO-pbaQ6G7PqQbF_KQ'
CHANNEL_ID = '@mangagaming_deals'  # oppure ID numerico tipo -1001234567890
AFFILIATE_CODE = '?igr=gamer-1ded01f'

# === FUNZIONE PER OTTENERE OFFERTE DA INSTANT GAMING ===
def get_offer():
    url = 'https://www.instant-gaming.com/it/offerte/'
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    first_game = soup.select_one('.item')

    if not first_game:
        print("❌ Nessuna offerta trovata.")
        return None

    title = first_game.select_one('.name').text.strip()
    price = first_game.select_one('.price').text.strip()
    link = 'https://www.instant-gaming.com' + first_game['href'] + AFFILIATE_CODE

    print("🎮 TITOLO:", title)
    print("💸 PREZZO:", price)
    print("🔗 LINK:", link)

    messaggio = f"🎮 <b>{title}</b>\n💸 Prezzo: <b>{price}</b>\n🔗 <a href='{link}'>Clicca qui per acquistare</a>"
    return messaggio

# === INVIA MESSAGGIO TESTUALE SU TELEGRAM ===
def invia_messaggio(bot):
    try:
        messaggio = get_offer()
        if messaggio:
            bot.send_message(CHANNEL_ID, messaggio, parse_mode='HTML')
            print("✅ Offerta inviata. Attendo 1 ora...\n")
        else:
            print("⚠️ Nessun messaggio da inviare.")
    except Exception as e:
        print(f'❌ Errore nell’invio: {e}')

# === AVVIO BOT ===
if __name__ == '__main__':
    bot = telebot.TeleBot(BOT_TOKEN)

    while True:
        invia_messaggio(bot)
        time.sleep(3600)  # ogni ora
