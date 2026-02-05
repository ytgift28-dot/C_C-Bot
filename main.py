import telebot
import requests
import random
import os
import threading
from flask import Flask

# =========================================
# 🌐 WEB SERVER FOR 24/7 HOSTING (RENDER)
# =========================================
app = Flask('')

@app.route('/')
def home():
    return "SH SUPREME BOT IS LIVE!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    threading.Thread(target=run, daemon=True).start()

# =========================================
# 🔧 CONFIGURATION & CREDITS
# =========================================
# Render-এর Environment Variable-এ 'BOT_TOKEN' নামে টোকেন সেভ করবেন
TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# আপনার নিজের Telegram ID দিন (ব্রডকাস্টের জন্য)
ADMIN_ID = 6941003064  

CHANNELS = ["@SH_tricks", "@SH_tricks_chat"]
OWNER_TAG = "@Suptho1"
CREDIT_CHANNEL = "@SH_tricks"

# ইউজার আইডি সেভ করার জন্য ফাইল
USER_FILE = "users.txt"

def add_user(user_id):
    if not os.path.exists(USER_FILE):
        with open(USER_FILE, "w") as f: pass
    with open(USER_FILE, "r") as f:
        users = f.read().splitlines()
    if str(user_id) not in users:
        with open(USER_FILE, "a") as f:
            f.write(str(user_id) + "\n")

# =========================================
# 🛡️ ADVANCE FORCE JOIN CHECKER
# =========================================
def is_joined(user_id):
    if user_id == ADMIN_ID: return True
    try:
        for ch in CHANNELS:
            status = bot.get_chat_member(ch, user_id).status
            if status not in ["member", "administrator", "creator"]:
                return False
        return True
    except:
        return False

# =========================================
# 🤖 BOT COMMANDS (STYLISH UI)
# =========================================

@bot.message_handler(commands=['start'])
def start_cmd(message):
    uid = message.from_user.id
    add_user(uid) 
    
    if not is_joined(uid):
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(telebot.types.InlineKeyboardButton("📢 Main Channel", url=f"https://t.me/{CHANNELS[0][1:]}"))
        markup.row(telebot.types.InlineKeyboardButton("💬 Discussion Group", url=f"https://t.me/{CHANNELS[1][1:]}"))
        markup.row(telebot.types.InlineKeyboardButton("🔄 Verify Membership", callback_data="verify"))
        
        msg = (
            "❌ **ACCESS RESTRICTED!**\n\n"
            "আমাদের সার্ভার ব্যবহার করতে নিচের দুটি চ্যানেলে জয়েন থাকা বাধ্যতামূলক।\n\n"
            "সবাই আমাদের সাথে থাকলে এখানে পাবেন:\n"
            "✅ Free Earning Methods\n"
            "✅ YouTube Premium Giveaway\n"
            "✅ Premium VPN & Private Tools\n\n"
            f"👑 Developed by {CREDIT_CHANNEL}"
        )
        bot.send_message(message.chat.id, msg, reply_markup=markup, parse_mode="Markdown")
        return

    welcome_text = (
        f"🚀 **SYSTEM INITIALIZED: SH SUPREME HUB**\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"স্বাগতম! **{message.from_user.first_name}**\n\n"
        f"এটি {CREDIT_CHANNEL}-এর অফিসিয়াল অটোমেশন বট। আমাদের সাথে থাকলে আপনি পাবেন:\n\n"
        f"💸 **Earn Daily:** গোপন আর্নিং মেথডস।\n"
        f"📺 **YT Premium:** ফ্রি প্রিমিয়াম সাবস্ক্রিপশন ও গিভঅ্যাওয়ে।\n"
        f"🎁 **Daily Giveaways:** VPN, RDP ও প্রিমিয়াম টুলস।\n"
        f"🔧 **Tools:** বোম্বার, বিন চেকার ও অ্যান্ড্রয়েড হ্যাকস।\n\n"
        f"📍 /bin - BIN Lookup\n"
        f"📍 /gen - CC Generator\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👑 **Owner:** {OWNER_TAG} | **Credit:** {CREDIT_CHANNEL}"
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown")

# =========================================
# 📢 ADMIN BROADCAST SYSTEM
# =========================================
@bot.message_handler(commands=['broadcast'])
def broadcast(message):
    if message.from_user.id != ADMIN_ID: return
    
    msg_text = message.text.replace("/broadcast ", "")
    if msg_text == "/broadcast" or msg_text == "":
        bot.send_message(ADMIN_ID, "⚠️ ব্যবহার: `/broadcast আপনার মেসেজ`")
        return

    if not os.path.exists(USER_FILE): return
    
    with open(USER_FILE, "r") as f:
        users = f.read().splitlines()
        
    success = 0
    for user in users:
        try:
            bot.send_message(user, f"📢 **IMPORTANT ANNOUNCEMENT**\n\n{msg_text}\n\n{CREDIT_CHANNEL}", parse_mode="Markdown")
            success += 1
        except: pass
    bot.send_message(ADMIN_ID, f"✅ ব্রডকাস্ট সফল! {success} জন মেম্বার মেসেজ পেয়েছে।")

# =========================================
# 🔘 CALLBACK HANDLER
# =========================================
@bot.callback_query_handler(func=lambda call: call.data == "verify")
def verify_callback(call):
    if is_joined(call.from_user.id):
        bot.answer_callback_query(call.id, "✅ ভেরিফিকেশন সফল!")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        start_cmd(call) 
    else:
        bot.answer_callback_query(call.id, "⚠️ আপনি এখনো সব চ্যানেলে জয়েন করেননি!", show_alert=True)

# =========================================
# 🚀 EXECUTION
# =========================================
if __name__ == "__main__":
    keep_alive()
    print(f"--- SH SUPREME HUB RUNNING (Credit: {CREDIT_CHANNEL}) ---")
    bot.polling(non_stop=True)
