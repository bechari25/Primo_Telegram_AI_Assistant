from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import os, asyncio

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
            await app.shutdown()  # Chiude in modo sicuro
            break
        active_users.clear()

async def main():
    """Avvia il bot."""
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot avviato!")
    asyncio.create_task(stop_bot(app))  # Avvia il sistema di spegnimento automatico
    await app.run_polling()

# ✅ FIX: Usa asyncio.get_event_loop() invece di asyncio.run()
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())  # Avvia il bot senza bloccare il loop
    loop.run_forever()  # Mantiene il bot attivo
