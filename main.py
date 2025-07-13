import requests
import time
import random
from telebot import TeleBot

TOKEN = "7267062520:AAHPb1Wy1VbsvZ9qBYO-pbaQ6G7PqQbF_KQ"
CHANNEL_ID = -1002755987703  # @mangagaming_deals

bot = TeleBot(TOKEN)

giochi = [
    {
        "titolo": "Bee Simulator (Xbox One)",
        "link": "https://www.instant-gaming.com/it/4873-comprare-bee-simulator-xbox-one-gioco-xbox-live/?igr=gamer-1ded01f",
        "prezzo": "7.82€",
        "immagine": "https://images.instantgaming.com/products/4873/616x353/bee-simulator-xbox-one-gioco-xbox-live-cover.jpg"
    },
    {
        "titolo": "Elden Ring (PC)",
        "link": "https://www.instant-gaming.com/it/10854-comprare-elden-ring-pc-gioco-steam/?igr=gamer-1ded01f",
        "prezzo": "29.99€",
        "immagine": "https://images.instantgaming.com/products/10854/616x353/elden-ring-pc-gioco-steam-cover.jpg"
    },
    {
        "titolo": "Zelda: Tears of the Kingdom (Switch)",
        "link": "https://www.instant-gaming.com/it/14868-comprare-the-legend-of-zelda-tears-of-the-kingdom-switch-gioco-nintendo/?igr=gamer-1ded01f",
        "prezzo": "39.90€",
        "immagine": "https://images.instantgaming.com/products/14868/616x353/the-legend-of-zelda-tears-of-the-kingdom-switch-gioco-nintendo-cover.jpg"
    }
]

def pubblica_offerta():
    gioco = random.choice(giochi)
    testo = f"<b>{gioco['titolo']}</b>\nPrezzo: <b>{gioco['prezzo']}</b>\n<a href='{gioco['link']}'>Clicca qui per acquistare</a>"

    try:
        bot.send_message(CHANNEL_ID, messaggio, parse_mode='HTML')
        print(f"Inviato: {gioco['titolo']}")
    except Exception as e:
        print(f"Errore: {e}")

while True:
    pubblica_offerta()
    time.sleep(3600)  # ogni ora

