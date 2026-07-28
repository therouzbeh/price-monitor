import requests
from bs4 import BeautifulSoup
import os
import json

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# تست فقط با ۳ محصول برای اطمینان از سرعت و عملکرد
PRODUCTS = [
    {"name": "چمدان کارینا S", "url": "https://www.digikala.com/product/dkp-17266458/", "platform": "digikala"},
    {"name": "کیف اداری امیج", "url": "https://www.digikala.com/product/dkp-18203599/", "platform": "digikala"},
    {"name": "محصول اسنپ شاپ", "url": "https://snappshop.ir/product/snp-1756493232?seller_id=gelbk1", "platform": "snappshop"},
]

def send_msg(text ):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": text}, timeout=10 )

def get_price(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/110.0.0.0 Safari/537.36'}
    try:
        res = requests.get(url, headers=headers, timeout=15)
        if res.status_code == 403: return "خطای دسترسی (403)"
        soup = BeautifulSoup(res.text, 'html.parser')
        # تلاش برای پیدا کردن قیمت در ساختار جدید دیجی کالا
        price_tag = soup.find('span', {'data-testid': 'price-final'})
        if price_tag: return price_tag.text
        return "قیمت پیدا نشد"
    except: return "خطا در اتصال"

if __name__ == "__main__":
    send_msg("🔄 شروع بررسی آزمایشی...")
    for p in PRODUCTS:
        status = get_price(p['url'])
        send_msg(f"📦 {p['name']}\nوضعیت: {status}")
    send_msg("🏁 پایان بررسی.")
