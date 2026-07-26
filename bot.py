import os
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "8863288731:AAHOMK0CcMvvLds3jKjiMvwcm0iO_1IS2f8")
WEB_APP_URL = "https://kedirk1.github.io/bingo-app/"

# Dummy HTTP server so Render Web Service stays alive
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bingo Bot is running alive!")

def run_http_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    print(f"HTTP Server running on port {port}")
    server.serve_forever()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎮 Bingo ተጫወት (Play)", web_app_url=WebAppInfo(url=WEB_APP_URL))],
        [InlineKeyboardButton("💳 Deposit", callback_data='deposit'), InlineKeyboardButton("🏧 Withdraw", callback_data='withdraw')],
        [InlineKeyboardButton("💰 Balance", callback_data='balance')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("👋 እንኳን ወደ Nigat Gashena Bingo በደህና መጡ!\n\nለመጫወት ወይም አካውንትዎን ለማስተዳደር ከታች ያሉትን ቁልፎች ይጠቀሙ፦", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'deposit':
        msg = (
            "💳 **የክፍያ ማድረጊያ አካውንቶች**\n\n"
            "📱 **ቴሌብር (Telebirr):**\n`0924231353`\n👤 ንጋት እባቡ\n\n"
            "🏦 **የኢትዮጵያ ንግድ ባንክ (CBE):**\n`1000754912409`\n👤 ንጋት እባቡ\n\n"
            "📌 *ገንዘቡን ገቢ ካደረጉ በኋላ ደረሰኙን ወይም ስክሪንሾቱን እዚህ ይላኩት።*"
        )
        await query.edit_message_text(msg, parse_mode='Markdown')
    elif query.data == 'withdraw':
        await query.edit_message_text("🏧 **ወጪ ለማድረግ (Withdraw):**\n\nእባክዎን ማውጣት የሚፈልጉትን የብር መጠን እና የአካውንት ቁጥርዎን ለአድሚኑ ይላኩ።", parse_mode='Markdown')
    elif query.data == 'balance':
        await query.edit_message_text("💰 **የአሁኑ ሂሳብዎ፦** 0.00 ብር", parse_mode='Markdown')

if __name__ == '__main__':
    # Start Web Server thread for Render
    threading.Thread(target=run_http_server, daemon=True).start()

    # Start Telegram Bot
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("Bot is running...")
    app.run_polling()
