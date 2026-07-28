import requests
import os
import json
import re

# تنظیمات تلگرام (از Secrets گیت‌هاب خوانده می‌شود)
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# لیست محصولات دیجی‌کالا شما
PRODUCTS = [
    {"name": "چمدان سینسنت کارینا S", "url": "https://www.digikala.com/product/dkp-17266458/?variant_id=75877216"},
    {"name": "چمدان سینسنت کارینا L", "url": "https://www.digikala.com/product/dkp-17266942/?variant_id=75874022"},
    {"name": "چمدان سینسنت کارینا M", "url": "https://www.digikala.com/product/dkp-17266700/?variant_id=76143108"},
    {"name": "ست سه عددی چمدان کارینا", "url": "https://www.digikala.com/product/dkp-18277955/?variant_id=75858296"},
    {"name": "کیف اداری مردانه امیج", "url": "https://www.digikala.com/product/dkp-18203599/?variant_id=76039595"},
    {"name": "ساک سفری چرخ دار P323", "url": "https://www.digikala.com/product/dkp-10849475/?variant_id=78634482"},
    {"name": "ست سه عددی چمدان CK40157", "url": "https://www.digikala.com/product/dkp-20038191/?variant_id=80163011"},
    {"name": "ساک سفری فایبر 4 طبقه", "url": "https://www.digikala.com/product/dkp-12389016/?variant_id=78657953"},
    {"name": "کراس بادی مدل 01", "url": "https://www.digikala.com/product/dkp-22000330/?variant_id=80262111"},
    {"name": "ساک سفری چرخ دار 4 طبقه", "url": "https://www.digikala.com/product/dkp-5391060/?variant_id=78994146"},
    {"name": "کاور چمدان مجموعه 3 عددی", "url": "https://www.digikala.com/product/dkp-4478348/?variant_id=81257296"},
    {"name": "ساک چرخدار سفری M65", "url": "https://www.digikala.com/product/dkp-17073744/?variant_id=76441230"},
    {"name": "ساک سفری چرخ دار 140", "url": "https://www.digikala.com/product/dkp-10538143/?variant_id=78994175"},
    {"name": "کاور چمدان مجموعه سه عددی", "url": "https://www.digikala.com/product/dkp-10926020/?variant_id=80166566"},
    {"name": "کاور چمدان شیشه ای 28", "url": "https://www.digikala.com/product/dkp-4478611/?variant_id=80262803"},
    {"name": "کیف لپ تاپ امیج OM-903", "url": "https://www.digikala.com/product/dkp-13575764/?variant_id=76265594"},
    {"name": "کیف لپ تاپ امیج OM-200", "url": "https://www.digikala.com/product/dkp-10460792/?variant_id=81214384"},
    {"name": "کوله پشتی بنج BG7520", "url": "https://www.digikala.com/product/dkp-20501855/?variant_id=80256905"},
    {"name": "کیف لپ تاپ امیج 900", "url": "https://www.digikala.com/product/dkp-10752811/?variant_id=76039485"},
    {"name": "کاور چمدان شیشه ای 24", "url": "https://www.digikala.com/product/dkp-4478558/?variant_id=80263322"},
    {"name": "کاور چمدان شیشه ای 19", "url": "https://www.digikala.com/product/dkp-4723362/?variant_id=80263397"},
    {"name": "کیف لپ تاپ امیج OM-907", "url": "https://www.digikala.com/product/dkp-21018131/?variant_id=79128097"},
]

def send_msg(text ):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID: return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "Markdown"}, timeout=15 )
    except:
        pass

def get_digikala_price(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/114.0.0.0 Safari/537.36'}
    try:
        # استخراج variant_id از لینک
        v_match = re.search(r'variant_id=(\d+)', url)
        v_id = v_match.group(1) if v_match else None
        
        response = requests.get(url, headers=headers, timeout=20)
        content = response.text
        
        if v_id:
            # جستجوی قیمت در نزدیکی کد تنوع در متن صفحه
            pattern = rf'"id":{v_id}.*?"selling_price":(\d+)'
            match = re.search(pattern, content)
            if match:
                return int(match.group(1)) // 10 # تبدیل ریال به تومان
        return None
    except:
        return None

if __name__ == "__main__":
    history_file = 'price_history.json'
    if os.path.exists(history_file):
        with open(history_file, 'r') as f:
            try: history = json.load(f)
            except: history = {}
    else:
        history = {}

    new_history = history.copy()
    first_run_count = 0

    for p in PRODUCTS:
        print(f"Checking {p['name']}...")
        price = get_digikala_price(p['url'])
        
        if price:
            key = p['url']
            old_price = history.get(key)
            
            if old_price:
                if price < old_price:
                    send_msg(f"🚨 *کاهش قیمت!*\n📦 {p['name']}\n💰 جدید: {price:,} تومان\n📉 قبلی: {old_price:,} تومان\n🔗 [لینک محصول]({p['url']})")
            else:
                first_run_count += 1
            
            new_history[key] = price

    # در اولین اجرا فقط یک پیام تایید بفرست
    if first_run_count > 0 and not history:
        send_msg(f"🚀 *ربات دیجی‌کالا فعال شد!*\nتعداد {first_run_count} محصول با موفقیت شناسایی و قیمت‌های فعلی ثبت شدند. از این پس فقط کاهش قیمت‌ها اطلاع‌رسانی می‌شود.")

    # ذخیره تاریخچه
    with open(history_file, 'w') as f:
        json.dump(new_history, f, indent=4)
