import requests
from bs4 import BeautifulSoup
import os
import json

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def send_msg(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": text} )

if __name__ == "__main__":
    send_msg("🔍 در حال شروع عیب‌یابی...")
    
    url = "https://www.digikala.com/product/dkp-17266458/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64 ) Chrome/114.0.0.0 Safari/537.36'}
    
    try:
        res = requests.get(url, headers=headers, timeout=20)
        send_msg(f"📡 وضعیت پاسخ سایت: {res.status_code}")
        
        soup = BeautifulSoup(res.text, 'html.parser')
        script_tag = soup.find('script', id='__NEXT_DATA__')
        
        if script_tag:
            send_msg("✅ دیتای مخفی سایت پیدا شد. در حال استخراج قیمت...")
            data = json.loads(script_tag.string)
            # نمایش ساختار برای تست
            p_name = data.get('props', {}).get('pageProps', {}).get('product', {}).get('title_fa')
            send_msg(f"📦 نام محصول پیدا شده: {p_name}")
        else:
            send_msg("❌ متاسفانه دیتای مخفی (JSON) در این صفحه پیدا نشد.")
            
    except Exception as e:
        send_msg(f"⚠️ خطای غیرمنتظره: {str(e)}")
