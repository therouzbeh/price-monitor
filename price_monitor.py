import requests
import os

# تنظیمات تلگرام
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def send_test():
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": "✅ سلام! اتصال ربات با موفقیت برقرار شد. سیستم آماده مانیتورینگ است.",
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload, timeout=10 )
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    send_test()
