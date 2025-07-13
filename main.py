import requests
import time
import random
from telebot import TeleBot

# Token e ID del canale
TOKEN = "7267062520:AAHPb1Wy1VbsvZ9qBYO-pbaQ6G7PqQbF_KQ"
CHANNEL_ID = -1002755987703  # @mangagaming_deals

bot = TeleBot(TOKEN)

# Lista giochi (aggiungi qui tutti quelli che vuoi)
giochi = [
    {
        "titolo": "Elden Ring (PC)",
        "link": "https://www.instant-gaming.com/it/10854-comprare-elden-ring-pc-gioco-steam/?igr=gamer-1ded01f",
        "prezzo": "29.99€",
        "immagine": "https://images.instantgaming.com/products/10854/616x353/elden-ring-pc-gioco-steam-cover.jpg"
    },
    {
        "titolo": "EA FC 24 (PS5)",
        "link": "https://www.instant-gaming.com/it/15352-comprare-ea-sports-fc-24-ps5-gioco-psn/?igr=gamer-1ded01f",
        "prezzo": "24.99€",
        "immagine": "https://images.instantgaming.com/products/15352/616x353/ea-sports-fc-24-ps5-gioco-psn-cover.jpg"
    },
    {
        "titolo": "Zelda: Tears of the Kingdom (Switch)",
        "link": "https://www.instant-gaming.com/it/14868-comprare-the-legend-of-zelda-tears-of-the-kingdom-switch-gioco-nintendo/?igr=gamer-1ded01f",
        "prezzo": "39.90€",
        "immagine": "https://images.instantgaming.com/products/14868/616x353/the-legend-of-zelda-tears-of-the-kingdom-switch-gioco-nintendo-cover.jpg"
    }
]

def immagine_valida(url):
    try:
        response = requests.get(url)
        return response.status_code == 200
    except:
        return False

def pubblica_offerta():
    gioco = random.choice(giochi)
    testo = f"""🎮 <b>{gioco['titolo']}</b>
💰 Prezzo: <b>{gioco['prezzo']}</b>
🛒 <a href="{gioco['link']}">Clicca qui per acquistare</a>"""

    if immagine_valida(gioco["immagine"]):
        try:
            bot.send_photo(CHANNEL_ID, gioco["immagine"], caption=teso, parse_mode="HTML")
        except Exception as e:
            print("Errore nell'invio con immagine:", e)
            bot.send_message(CHANNEL_ID, testo, parse_mode="HTML")
    else:
        print("Immagine non valida, invio solo testo.")
        bot.send_message(CHANNEL_ID, testo, parse_mode="HTML")

# Ciclo ogni ora
while True:
    pubblica_offerta()
    time.sleep(3600)
