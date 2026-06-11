import os
import requests
import json
from flask import Flask, request

app = Flask(__name__)

TOKEN = "8331261864:AAEwUvKxZyQTLxGDytEntv-Xjq2-M_gKiPg"
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

def send_message(chat_id, text):
    requests.post(f"{BASE_URL}/sendMessage", json={
        "chat_id": chat_id, "text": text, "parse_mode": "HTML"
    })

def check_key(key):
    try:
        r = requests.get(f"https://ars-vpn.site/api/check_key.php?key={key}", timeout=5)
        return r.json()
    except:
        return {"found": False}

@app.route("/")
def home():
    return "Bot is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if not data or "message" not in data:
        return "ok"
    
    msg = data["message"]
    chat_id = msg["chat"]["id"]
    text = msg.get("text", "").strip()
    username = msg["from"].get("username", "user")
    
    if text == "/start":
        reply = f"👋 Привет, @{username}!\n\n🔑 /buy — купить\n📊 /status КЛЮЧ\n👥 /partner\n💬 /support"
    elif text == "/buy":
        reply = "🛒 Тарифы:\n• 1д — 25₽\n• 1м — 220₽\n• 3м — 450₽\n• Год — 1300₽\n\n🔗 https://ars-vpn.site/buy"
    elif text.startswith("/status"):
        key = text.replace("/status", "").strip()
        if key:
            data = check_key(key)
            if data.get("found"):
                reply = f"✅ Активен\n📅 {data['days_left']} дн\n📱 {data['devices']}/3\n🔗 https://ars-vpn.site/{key}"
            else:
                reply = "❌ Не найден"
        else:
            reply = "/status КЛЮЧ"
    elif text == "/partner":
        reply = "💰 50% с продаж\n🔗 https://ars-vpn.site/partner/register.php"
    elif text == "/support":
        reply = "📨 @mirroradm\n📢 @Dictatorvpn"
    else:
        reply = "Команды: /start /buy /status /partner /support"
    
    send_message(chat_id, reply)
    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
