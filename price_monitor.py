import requests
from bs4 import BeautifulSoup
import time
import os
import json
from urllib.parse import urlparse, parse_qs

# ==========================================
# تنظیمات تلگرام (از بخش Secrets گیت‌هاب خوانده می‌شود)
# ==========================================
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# ==========================================
# لیست کامل محصولات شما
# ==========================================
PRODUCTS = [
    # --- محصولات اسنپ شاپ ---
    {"name": "اسنپ شاپ 1", "url": "https://snappshop.ir/product/snp-1756493232?seller_id=gelbk1", "platform": "snappshop"},
    {"name": "اسنپ شاپ 2", "url": "https://snappshop.ir/product/snp-577868979?seller_id=gelbk1", "platform": "snappshop"},
    {"name": "اسنپ شاپ 3", "url": "https://snappshop.ir/product/snp-1546729394?seller_id=gelbk1", "platform": "snappshop"},
    {"name": "اسنپ شاپ 4", "url": "https://snappshop.ir/product/snp-801013101?seller_id=gelbk1", "platform": "snappshop"},
    {"name": "اسنپ شاپ 5", "url": "https://snappshop.ir/product/snp-1114930220?seller_id=gelbk1", "platform": "snappshop"},
    {"name": "اسنپ شاپ 6", "url": "https://snappshop.ir/product/snp-1756579678?seller_id=gelbk1", "platform": "snappshop"},
    {"name": "اسنپ شاپ 7", "url": "https://snappshop.ir/product/snp-1631592397?seller_id=gelbk1", "platform": "snappshop"},
    {"name": "اسنپ شاپ 8", "url": "https://snappshop.ir/product/snp-79735725?seller_id=gelbk1", "platform": "snappshop"},
    {"name": "اسنپ شاپ 9", "url": "https://snappshop.ir/product/snp-1123437551?seller_id=gelbk1", "platform": "snappshop"},
    {"name": "اسنپ شاپ 10", "url": "https://snappshop.ir/product/snp-400216674?seller_id=gelbk1", "platform": "snappshop"},
    {"name": "اسنپ شاپ 11", "url": "https://snappshop.ir/product/snp-108680457?seller_id=gelbk1", "platform": "snappshop"},
    {"name": "اسنپ شاپ 12", "url": "https://snappshop.ir/product/snp-1910261867?seller_id=gelbk1", "platform": "snappshop"},
    {"name": "اسنپ شاپ 13", "url": "https://snappshop.ir/product/snp-1437293668?seller_id=gelbk1", "platform": "snappshop"},
    {"name": "اسنپ شاپ 14", "url": "https://snappshop.ir/product/snp-1740815358?seller_id=gelbk1", "platform": "snappshop"},
    {"name": "اسنپ شاپ 15", "url": "https://snappshop.ir/product/snp-1002287098?seller_id=gelbk1", "platform": "snappshop"},
    {"name": "اسنپ شاپ 16", "url": "https://snappshop.ir/product/snp-222563420?seller_id=gelbk1", "platform": "snappshop"},
    {"name": "اسنپ شاپ 17", "url": "https://snappshop.ir/product/snp-1571033956?seller_id=gelbk1", "platform": "snappshop"},
    {"name": "اسنپ شاپ 18", "url": "https://snappshop.ir/product/snp-881809643?seller_id=gelbk1", "platform": "snappshop"},
    {"name": "اسنپ شاپ 19", "url": "https://snappshop.ir/product/snp-1082631628?seller_id=gelbk1", "platform": "snappshop"},
    {"name": "اسنپ شاپ 20", "url": "https://snappshop.ir/product/snp-1780156546?seller_id=gelbk1", "platform": "snappshop"},
    
    # --- محصولات دیجی کالا ---
    {"name": "چمدان سینسنت کارینا S", "url": "https://www.digikala.com/product/dkp-17266458/", "platform": "digikala"},
    {"name": "چمدان سینسنت کارینا L", "url": "https://www.digikala.com/product/dkp-17266942/", "platform": "digikala"},
    {"name": "چمدان سینسنت کارینا M", "url": "https://www.digikala.com/product/dkp-17266700/", "platform": "digikala"},
    {"name": "ست سه عددی چمدان کارینا", "url": "https://www.digikala.com/product/dkp-18277955/", "platform": "digikala"},
    {"name": "کیف اداری مردانه امیج", "url": "https://www.digikala.com/product/dkp-18203599/", "platform": "digikala"},
    {"name": "ساک سفری چرخ دار P323", "url": "https://www.digikala.com/product/dkp-10849475/", "platform": "digikala"},
    {"name": "ست سه عددی چمدان CK40157", "url": "https://www.digikala.com/product/dkp-20038191/", "platform": "digikala"},
    {"name": "ساک سفری فایبر 4 طبقه", "url": "https://www.digikala.com/product/dkp-12389016/", "platform": "digikala"},
    {"name": "کراس بادی مدل 01", "url": "https://www.digikala.com/product/dkp-22000330/", "platform": "digikala"},
    {"name": "ساک سفری چرخ دار 4 طبقه", "url": "https://www.digikala.com/product/dkp-5391060/", "platform": "digikala"},
    {"name": "کاور چمدان مجموعه 3 عددی", "url": "https://www.digikala.com/product/dkp-4478348/", "platform": "digikala"},
    {"name": "ساک چرخدار سفری M65", "url": "https://www.digikala.com/product/dkp-17073744/", "platform": "digikala"},
    {"name": "ساک سفری چرخ دار 140", "url": "https://www.digikala.com/product/dkp-10538143/", "platform": "digikala"},
    {"name": "کاور چمدان مجموعه سه عددی", "url": "https://www.digikala.com/product/dkp-10926020/", "platform": "digikala"},
    {"name": "کاور چمدان شیشه ای 28", "url": "https://www.digikala.com/product/dkp-4478611/", "platform": "digikala"},
    {"name": "کیف لپ تاپ امیج OM-903", "url": "https://www.digikala.com/product/dkp-13575764/", "platform": "digikala"},
    {"name": "کیف لپ تاپ امیج OM-200", "url": "https://www.digikala.com/product/dkp-10460792/", "platform": "digikala"},
    {"name": "کوله پشتی بنج BG7520", "url": "https://www.digikala.com/product/dkp-20501855/", "platform": "digikala"},
    {"name": "کیف لپ تاپ امیج 900", "url": "https://www.digikala.com/product/dkp-10752811/", "platform": "digikala"},
    {"name": "کاور چمدان شیشه ای 24", "url": "https://www.digikala.com/product/dkp-4478558/", "platform": "digikala"},
    {"name": "کاور چمدان شیشه ای 19", "url": "https://www.digikala.com/product/dkp-4723362/", "platform": "digikala"},
    {"name": "کیف لپ تاپ امیج OM-907", "url": "https://www.digikala.com/product/dkp-21018131/", "platform": "digikala"},
]

def send_telegram_message(message ):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID: return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try: requests.post(url, json=payload, timeout=10 )
    except: pass

def get_digikala_prices(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124 Safari/537.36'}
    try:
        # استخراج variant_id از لینک اگر وجود داشته باشد
        parsed_url = urlparse(url)
        target_variant = parse_qs(parsed_url.query).get('variant_id', [None])[0]
        
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        script_tag = soup.find('script', id='__NEXT_DATA__')
        if not script_tag: return {}
        
        data = json.loads(script_tag.string)
        product_data = data.get('props', {}).get('pageProps', {}).get('product', {})
        variants = product_data.get('variants', [])
        
        prices = {}
        for v in variants:
            v_id = str(v.get('id'))
            # اگر لینک شامل variant_id خاصی بود، فقط همان را چک کن
            if target_variant and v_id != target_variant: continue
            
            color = v.get('color', {}).get('title') or v.get('size', {}).get('title', 'Default')
            price_raw = v.get('price', {}).get('selling_price', 0)
            if price_raw > 0: prices[f"{color} (کد:{v_id})"] = price_raw // 10
        return prices
    except: return {}

def get_snappshop_prices(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124 Safari/537.36', 'Referer': 'https://snappshop.ir/'}
    try:
        response = requests.get(url, headers=headers, timeout=15 )
        if response.status_code == 403: return "403"
        # استخراج قیمت از اسنپ شاپ (نیاز به بررسی مداوم ساختار دارد)
        return {"Default": None}
    except: return {}

def main():
    history_file = 'price_history.json'
    if os.path.exists(history_file):
        with open(history_file, 'r', encoding='utf-8') as f:
            try: history = json.load(f)
            except: history = {}
    else: history = {}

    new_history = history.copy()
    for product in PRODUCTS:
        name, url, platform = product['name'], product['url'], product['platform']
        print(f"Checking {name}...")
        
        prices = get_digikala_prices(url) if platform == 'digikala' else {}
        if platform == 'snappshop':
            res = get_snappshop_prices(url)
            if res != "403": prices = res
        
        for color, current_price in prices.items():
            if not current_price: continue
            key = f"{url}#{color}"
            old_price = history.get(key)
            if old_price and current_price < old_price:
                msg = (f"🚨 *کاهش قیمت رقیب!*\n\n📦 محصول: {name}\n🎨 تنوع: {color}\n💰 قیمت جدید: {current_price:,} تومان\n📉 قیمت قبلی: {old_price:,} تومان\n🔗 [مشاهده محصول]({url})")
                send_telegram_message(msg)
            new_history[key] = current_price

    with open(history_file, 'w', encoding='utf-8') as f:
        json.dump(new_history, f, ensure_ascii=False, indent=4)

if __name__ == "__main__": main()
