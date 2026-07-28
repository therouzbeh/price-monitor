import requests
from bs4 import BeautifulSoup
import time
import os
import json

# تنظیمات تلگرام (اینها باید از محیط دریافت شوند)
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# لیست محصولات برای مانیتورینگ
# فرمت: {"id": "نام محصول", "url": "لینک محصول", "platform": "digikala/snappshop"}
PRODUCTS = [
    # کاربر باید این لیست را پر کند
]

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Error sending message: {e}")

def get_digikala_price(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # دیجی‌کالا قیمت را در تگ‌های خاصی قرار می‌دهد. 
        # معمولاً در JSON داخل اسکریپت یا تگ‌های دیتا موجود است.
        # این بخش نیاز به تست دقیق روی لینک‌های واقعی دارد.
        price_tag = soup.find('span', {'data-testid': 'price-final'})
        if not price_tag:
            # روش جایگزین: جستجو در متن برای پیدا کردن قیمت
            return None
        
        price_text = price_tag.text.strip().replace(',', '')
        return int(price_text)
    except Exception as e:
        print(f"Error fetching Digikala price: {e}")
        return None

def get_snappshop_price(url):
    # اسنپ‌شاپ معمولاً فیلترینگ IP دارد. 
    # در GitHub Actions چون IP خارج است، احتمالاً نیاز به هدرهای خاص دارد.
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://snappshop.ir/'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 403:
            return "403_FORBIDDEN"
        
        soup = BeautifulSoup(response.text, 'html.parser')
        # ساختار اسنپ‌شاپ باید دقیقاً بررسی شود.
        # به دلیل محدودیت دسترسی در محیط فعلی، این بخش به صورت عمومی نوشته شده است.
        return None
    except Exception as e:
        print(f"Error fetching SnappShop price: {e}")
        return None

def main():
    # لود کردن قیمت‌های قبلی برای مقایسه
    history_file = 'price_history.json'
    if os.path.exists(history_file):
        with open(history_file, 'r') as f:
            history = json.load(f)
    else:
        history = {}

    new_history = {}
    
    for product in PRODUCTS:
        name = product['name']
        url = product['url']
        platform = product['platform']
        
        print(f"Checking {name} on {platform}...")
        
        if platform == 'digikala':
            current_price = get_digikala_price(url)
        elif platform == 'snappshop':
            current_price = get_snappshop_price(url)
        else:
            continue
            
        if current_price and current_price != "403_FORBIDDEN":
            new_history[url] = current_price
            
            old_price = history.get(url)
            if old_price and current_price < old_price:
                msg = f"🚨 *کاهش قیمت رقیب!*\n\n📦 محصول: {name}\n💰 قیمت جدید: {current_price:,} تومان\n📉 قیمت قبلی: {old_price:,} تومان\n🔗 [مشاهده محصول]({url})"
                send_telegram_message(msg)
            elif not old_price:
                print(f"Initial price for {name}: {current_price}")
        elif current_price == "403_FORBIDDEN":
            print(f"Access Denied for {name} on SnappShop. Need proxy or better headers.")

    # ذخیره قیمت‌های جدید
    with open(history_file, 'w') as f:
        json.dump(new_history, f)

if __name__ == "__main__":
    main()
