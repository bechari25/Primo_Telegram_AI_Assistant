import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

TOKEN = os.getenv("TOKEN")

# Timeout per spegnere il bot dopo inattività
TIMEOUT = 600  # 10 minuti
active_users = set()

async def start(update: Update, context: CallbackContext):
    """Risponde al comando /start."""
    global active_users
    active_users.add(update.message.chat_id)
    await update.message.reply_text("Ciao! Sono il tuo assistente AI.")

async def handle_message(update: Update, context: CallbackContext):
    """Gestisce i messaggi di testo."""
    global active_users
    active_users.add(update.message.chat_id)
    await update.message.reply_text(f"Hai detto: {update.message.text}")

async def stop_bot(app: Application):
    """Spegne il bot dopo inattività."""
    while True:
        await asyncio.sleep(TIMEOUT)
        if not active_users:
            print("Nessuna attività, sto chiudendo il bot...")
            await app.shutdown()  # Chiude il bot in modo sicuro
            break
        active_users.clear()

async def run_bot():
    """Avvia il bot."""
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot avviato!")
    asyncio.create_task(stop_bot(app))  # Avvia il sistema di spegnimento automatico
    await app.run_polling()

if __name__ == "__main__":
    try:
        asyncio.run(run_bot())  # Avvia il bot in modo sicuro
    except RuntimeError:
        # FIX per Render: esegue il codice su un event loop già attivo
        loop = asyncio.get_event_loop()
        loop.create_task(run_bot())
        loop.run_forever()
