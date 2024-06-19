import requests

def send_telegram_message(message):
    token = 'YOUR_TELEGRAM_BOT_TOKEN'
    chat_id = 'YOUR_CHAT_ID'
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {'chat_id': chat_id, 'text': message}
    requests.post(url, data=data)