import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# Logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# የቦቱ ቶከን
TOKEN = "8863288731:AAHOMK0CcMvvLds3jKjiMvwcm0iO_1IS2f8"

# የተጫዋቾች የባላንስ መዝገብ (ለጊዜው በዲክሽነሪ ተይዟል)
user_balances = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    
    if user_id not in user_balances:
        user_balances[user_id] = 0.0

    balance = user_balances[user_id]
    
    # የ Mini App ሊንክዎ
    web_app_url = "https://kedirk1.github.io/bingo-app/"

    keyboard = [
        [InlineKeyboardButton("🎮 Play Bingo (10 ETB)", web_app=WebAppInfo(url=web_app_url))],
        [InlineKeyboardButton("💰 My Balance", callback_data="balance"),
         InlineKeyboardButton("📥 Deposit", callback_data="deposit")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_text = (
        f"ሰላም <b>{user.first_name}</b>! እንኳን ወደ <b>Nigat Gashena Bingo</b> በደህና መጡ።\n\n"
        f"💳 ቀሪ ሂሳብዎ፦ <b>{balance:.2f} ETB</b>\n\n"
        f"⚠️ <i>ለመጫወት ቢያንስ 10 ብር ባላንስ ሊኖርዎት ይገባል። ከሌለዎት <b>Deposit</b> በመጫን ሂሳብ ይሙሉ!</i>"
    )

    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="HTML")

async def balance_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    balance = user_balances.get(user_id, 0.0)
    await update.message.reply_text(f"💰 የእርስዎ ቀሪ ሂሳብ፦ {balance:.2f} ETB")

async def deposit_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    deposit_text = (
        "📥 <b>ገንዘብ ገቢ ለማድረግ (Deposit):</b>\n\n"
        "እባክዎን ከታች ባሉት የባንክ/ቴሌብር አካውንቶች ገንዘብ ያስተላልፉ፦\n"
        "• ቴሌብር፦ <b>0924231353</b> (ንጋት እባቡ)\n"
        "• ንግድ ባንክ (CBE)፦ <b>1000754912409</b> (ንጋት እባቡ)\n\n"
        "ክፍያውን ከፈጸሙ በኋላ የግብይቱን ቁጥር (TID ወይም Receipt) ለዚህ ቦት ይላኩ። ወዲያውኑ ባላንስዎ ይስተካከላል!"
    )
    await update.message.reply_text(deposit_text, parse_mode="HTML")

def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("balance", balance_command))
    application.add_handler(CommandHandler("deposit", deposit_command))

    print("Bot is running...")
    application.run_polling()

if __name__ == '__main__':
    main()
