import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "8863288731:AAHOMK0CcMvvLds3jKjiMvwcm0iO_1IS2f8")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_first_name = update.effective_user.first_name
    
    # የ Mini App ሊንክ (የ GitHub Pages ወይም Render URL)
    web_app_url = "https://kedirk1.github.io/bingo-app/"
    
    keyboard = [
        [InlineKeyboardButton("🎮 Bingo ተጫወት (Play)", web_app_url=dict(url=web_app_url))],
        [InlineKeyboardButton("💳 ገንዘብ ማስገቢያ (Deposit)", callback_data='deposit'),
         InlineKeyboardButton("💰 ሂሳብ ማረጋገጫ (Balance)", callback_data='balance')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_msg = f"ሰላም {user_first_name}! 👋\nእንኳን ወደ Nigat Gashena Bingo በደህና መጡ!\n\nመጫወት ለመጀመር ከታች ያለውን ቁልፍ ይጫኑ።"
    await update.message.reply_text(welcome_msg, reply_markup=reply_markup)

async def deposit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    deposit_info = (
        "💳 **የክፍያ ማድረጊያ አካውንቶች**\n\n"
        "📱 **ቴሌብር (Telebirr):**\n"
        "`0924231353`\n"
        "👤 ስም፦ ንጋት እባቡ\n\n"
        "🏦 **የኢትዮጵያ ንግድ ባንክ (CBE):**\n"
        "`1000754912409`\n"
        "👤 ስም፦ ንጋት እባቡ\n\n"
        "📌 *ገንዘቡን ገቢ ካደረጉ በኋላ ደረሰኙን ወይም ስክሪንሾቱን እዚህ ይላኩት።*"
    )
    await query.edit_message_text(deposit_info, parse_mode='Markdown')

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("💰 **የአሁኑ ሂሳብዎ፦** 0.00 ብር\n\nለመጫወት እባክዎን መጀመሪያ ገንዘብ ያስገቡ።", parse_mode='Markdown')

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    from telegram.ext import CallbackQueryHandler
    app.add_handler(CallbackQueryHandler(deposit, pattern='^deposit$'))
    app.add_handler(CallbackQueryHandler(balance, pattern='^balance$'))
    
    print("Bot is running...")
    app.run_polling()
