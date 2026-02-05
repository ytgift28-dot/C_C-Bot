import telebot
import requests
import random
import os
from flask import Flask, request

# =========================================
# 🔧 CONFIGURATION & CREDITS
# =========================================
TOKEN = os.environ.get('BOT_TOKEN')
# আপনার রেন্ডার ইউআরএল (যেমন: https://your-app.onrender.com)
WEBHOOK_URL = os.environ.get('WEBHOOK_URL') 
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

ADMIN_ID = 6941003064  
CHANNELS = ["@SH_tricks", "@SH_tricks_chat"]
OWNER_TAG = "@Suptho1"
CREDIT_CHANNEL = "@SH_tricks"

# =========================================
# 🎲 CC GENERATOR & CHECKER LOGIC
# =========================================
def luhn_check(card_no):
    n_digits = len(card_no)
    n_sum = 0
    is_second = False
    for i in range(n_digits - 1, -1, -1):
        d = ord(card_no[i]) - ord('0')
        if is_second: d = d * 2
        n_sum += d // 10
        n_sum += d % 10
        is_second = not is_second
    return (n_sum % 10 == 0)

def generate_cc(bin_code):
    cc = str(bin_code)
    if len(cc) < 6: return "❌ Invalid BIN!"
    while len(cc) < 15:
        cc += str(random.randint(0, 9))
    for i in range(10):
        if luhn_check(cc + str(i)):
            cc += str(i)
            break
    month = str(random.randint(1, 12)).zfill(2)
    year = random.randint(2026, 2031)
    cvv = str(random.randint(100, 999))
    return f"{cc}|{month}|{year}|{cvv}"

def check_cc(cc_details):
    statuses = ["LIVE ✅", "DEAD ❌", "LIVE (Trial OK) ✅", "LIVE (High Vibe) 🔥"]
    return random.choice(statuses)

# =========================================
# 🛡️ FORCE JOIN CHECKER
# =========================================
def is_joined(user_id):
    if user_id == ADMIN_ID: return True
    try:
        for ch in CHANNELS:
            status = bot.get_chat_member(ch, user_id).status
            if status not in ["member", "administrator", "creator"]: return False
        return True
    except: return False

# =========================================
# 🤖 BOT COMMANDS
# =========================================
@bot.message_handler(commands=['start'])
def start(message):
    welcome_text = (
        f"🚀 **WELCOME TO SH CC GEN & CHECKER**\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📍 `/gen <BIN>` - ১০টি কার্ড জেনারেট করুন।\n"
        f"📍 `/check <CC>` - কার্ড লাইভ কি না দেখুন।\n\n"
        f"👑 **Owner:** {OWNER_TAG} | **Credit:** {CREDIT_CHANNEL}"
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown")

@bot.message_handler(commands=['gen'])
def gen_cmd(message):
    if not is_joined(message.from_user.id):
        bot.reply_to(message, "⚠️ আমাদের চ্যানেলে জয়েন করুন আগে!")
        return
    args = message.text.split()
    if len(args) > 1:
        bin_num = args[1][:6]
        result = f"✨ **SH CC GEN - RESULTS**\n📍 **BIN:** `{bin_num}`\n━━━━━━━━━━━━━━━━━━━━\n"
        for _ in range(10):
            cc_data = generate_cc(bin_num)
            result += f"`{cc_data}` - {check_cc(cc_data)}\n"
        result += f"━━━━━━━━━━━━━━━━━━━━\n👑 **Credit:** {CREDIT_CHANNEL}"
        bot.send_message(message.chat.id, result, parse_mode="Markdown")
    else:
        bot.reply_to(message, "ব্যবহার: `/gen 444444`", parse_mode="Markdown")

# =========================================
# 🌐 WEBHOOK & FLASK ROUTES
# =========================================
@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL + TOKEN)
    return "SH WEBHOOK SET SUCCESSFULLY!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
