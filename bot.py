import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Assicurati che il token venga letto correttamente
TOKEN = os.getenv("TOKEN")

# Se il token è None, il programma deve lanciare un errore
if not TOKEN:
    raise ValueError("TOKEN non trovato nelle variabili d'ambiente!")

async def start(update: Update, context: CallbackContext):
    """Risponde al comando /start."""
    await update.message.reply_text("Ciao! Sono il tuo bot Telegram.")

async def handle_message(update: Update, context: CallbackContext):
    """Gestisce i messaggi ricevuti."""
    await update.message.reply_text(f"Hai detto: {update.message.text}")

def main():
    """Avvia il bot in modalità polling."""
    app = Application.builder().token(TOKEN).build()

    # Aggiungi i comandi e i gestori dei messaggi
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Bot avviato!")
    app.run_polling()

if __name__ == "__main__":
    main()
