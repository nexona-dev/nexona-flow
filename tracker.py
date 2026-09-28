import requests
from bs4 import BeautifulSoup
import time

# --- Telegram Ayarları ---
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN_HER"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID_HERE"

# Takip edilecek ürünün URL'si
PRODUCT_URL = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

# Fiyat eşiği (test için 100 yaptık, kitap 51.77 olduğu için hemen bildirim gönderecek)
PRICE_THRESHOLD = 100.0

def send_telegram_message(message):
    """Telegram üzerinden mesaj gönderir."""
    if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("Telegram ayarları yapılmadı. Mesaj gönderilemedi.")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        response = requests.post(url, data=payload)
        print(f"Telegram yanıtı: {response.status_code}")
        print(f"Telegram cevabı: {response.text}")
    except Exception as e:
        print(f"Telegram mesajı gönderilemedi: {e}")

def get_price():
    """Ürünün mevcut fiyatını çeker."""
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(PRODUCT_URL, headers=headers)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")
    price_text = soup.find("p", class_="price_color").text
    price_clean = "".join(c for c in price_text if c.isdigit() or c == ".")
    price = float(price_clean)
    return price

def main():
    print(f"Fiyat takibi başladı: {PRODUCT_URL}")
    while True:
        try:
            current_price = get_price()
            print(f"Mevcut fiyat: £{current_price}")
            
            if current_price < PRICE_THRESHOLD:
                message = f"🔥 Fiyat Düştü! 🔥\nÜrün: A Light in the Attic\nYeni Fiyat: £{current_price}\nLink: {PRODUCT_URL}"
                send_telegram_message(message)
                print("Bildirim gönderildi!")
                break
            
            time.sleep(60)
        except Exception as e:
            print(f"Bir hata oluştu: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()
