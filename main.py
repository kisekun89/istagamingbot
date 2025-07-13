import requests
import time
import telebot
from bs4 import BeautifulSoup

# === CONFIG ===
TOKEN = '7267062520:AAHPb1Wy1VbsvZ9qBYO-pbaQ6G7PqQbF_KQ'
CHANNEL_ID = "@mangagaming_deals"
AFFILIATE_TAG = "?igr=gamer-1ded01f"

URLS = [
    "https://www.instant-gaming.com/it/ricerca/?platform%5B0%5D=1",
    "https://www.instant-gaming.com/it/ricerca/?platform%5B0%5D=2",
    "https://www.instant-gaming.com/it/ricerca/?platform%5B0%5D=3",
    "https://www.instant-gaming.com/it/ricerca/?platform%5B0%5D=4"
]

# === AVVIO ===
bot = telebot.TeleBot(TOKEN)

def estrai_offerte(url):
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(r.text, "html.parser")
        giochi = []

        items = soup.select("div.item")
        for item in items:
            titolo = item.select_one("div.name")
            prezzo = item.select_one("div.price")
            link = item.find("a", href=True)
            img = item.find("img")

            if not titolo or not prezzo or not link or not img:
                continue

            titolo_txt = titolo.text.strip()
            prezzo_txt = prezzo.text.strip()
            link_url = "https://www.instant-gaming.com" + link["href"] + AFFILIATE_TAG
            img_url = img["src"]

            giochi.append({
                "titolo": titolo_txt,
                "prezzo": prezzo_txt,
                "link": link_url,
                "img": img_url
            })

        return giochi

    except Exception as e:
        print(f"❌ Errore parsing: {e}")
        return []

def invia_offerta(gioco):
    try:
        testo = f"🎮 <b>{gioco['titolo']}</b>\n💰 Prezzo: {gioco['prezzo']}\n🔗 <a href='{gioco['link']}'>Compra ora su Instant Gaming</a>"
        bot.send_photo(CHANNEL_ID, gioco["img"], caption=testo, parse_mode="HTML")
        print("✅ Inviato:", gioco["titolo"])
    except Exception as e:
        print(f"❌ Errore invio: {e}")

# === MAIN LOOP ===
if __name__ == "__main__":
    tutte = []
    for url in URLS:
        tutte += estrai_offerte(url)
        time.sleep(2)

    if tutte:
        invia_offerta(tutte[0])  # puoi cambiare per inviarne più di una
    else:
        print("⚠️ Nessuna offerta trovata.")
