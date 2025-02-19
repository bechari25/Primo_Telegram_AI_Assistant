


from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import os, asyncio

TOKEN = os.getenv("TOKEN")

# Timeout per spegnere il bot dopo inattività Primo_TelegramAssistant-IA
TIMEOUT = 600  # 10 minuti
active_users = set()

async def start(update: Update, context: CallbackContext):
    global active_users
    active_users.add(update.message.chat_id)
    await update.message.reply_text("Ciao! Sono il tuo assistente AI.")

async def handle_message(update: Update, context: CallbackContext):
    global active_users
    active_users.add(update.message.chat_id)
    await update.message.reply_text(f"Hai detto: {update.message.text}")

async def stop_bot():
    while True:
        await asyncio.sleep(TIMEOUT)
        if not active_users:
            print("Nessuna attività, spengo il bot...")
            os.system("kill 1")  # Spegne Railway
            break
        active_users.clear()

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot avviato!")
    asyncio.create_task(stop_bot())  # Avvia il sistema di spegnimento automatico
    app.run_polling()

if __name__ == "__main__":
    main()
