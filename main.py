import requests
import time
import telebot
from bs4 import BeautifulSoup

TOKEN = '7267062520:AAHPb1Wy1VbsvZ9qBYO-pbaQ6G7PqQbF_KQ'
CHANNEL_ID = "@mangagaming_deals"
URLS = [
    "https://www.instant-gaming.com/it/ricerca/?platform%5B0%5D=1",
    "https://www.instant-gaming.com/it/ricerca/?platform%5B0%5D=2",
    "https://www.instant-gaming.com/it/ricerca/?platform%5B0%5D=3",
    "https://www.instant-gaming.com/it/ricerca/?platform%5B0%5D=4",
]

AFFILIATE_TAG = "?igr=gamer-1ded01f"
bot = telebot.TeleBot(TOKEN)

def estrai_offerte(url):
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        items = soup.find_all("div", class_="item force-badge")
        giochi = []

        for item in items:
            titolo = item.find("div", class_="name").text.strip()
            prezzo = item.find("div", class_="price").text.strip()
            img_tag = item.find("img")
            link_tag = item.find("a", href=True)

            if not titolo or not prezzo or not img_tag or not link_tag:
                continue

            img = img_tag["src"]
            link = "https://www.instant-gaming.com" + link_tag["href"]

            giochi.append({
                "titolo": titolo,
                "prezzo": prezzo,
                "img": img,
                "link": link + AFFILIATE_TAG
            })

        return giochi

    except Exception as e:
        print(f"Errore estrazione: {e}")
        return []

def invia_offerta(gioco):
    try:
        text = f"🎮 <b>{gioco['titolo']}</b>\n💰 Prezzo: {gioco['prezzo']}\n🔗 <a href='{gioco['link']}'>Compra ora su Instant Gaming</a>"
        bot.send_photo(CHANNEL_ID, gioco["img"], caption=text, parse_mode="HTML")
        print("✔️ Offerta inviata.")
    except Exception as e:
        print(f"❌ Errore invio: {e}")

if __name__ == "__main__":
    tutti_i_giochi = []
    for url in URLS:
        giochi = estrai_offerte(url)
        if giochi:
            tutti_i_giochi.extend(giochi)

    if tutti_i_giochi:
        invia_offerta(tutti_i_giochi[0])
    else:
        print("⚠️ Nessuna offerta trovata.")
