import logging
import signal
import sys
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler, ContextTypes

# Configurar logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Definir comandos
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('¡Hola! Soy tu bot de Telegram.')
    await update.message.reply_text('Puedes usar los siguientes comandos:\n/start - Iniciar\n/help - Ayuda\n/opciones - Opciones de reparación')


async def opciones(update: Update, context:ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Agregar Reparacion", callback_data='1')],
        [InlineKeyboardButton("Consultar Reparacion", callback_data='2')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Por favor elige una opcion" ,reply_markup=reply_markup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Puedes usar los siguientes comandos:\n/start - Iniciar\n/help - Ayuda\n/opciones - Opciones de reparación')

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(update.message.text)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == '1':
        await query.edit_message_text(text="¡Presionaste el Botón 1!")
    elif query.data == '2':
        await query.edit_message_text(text="¡Presionaste el Botón 2!")


def main():
    # Token de API del bot (reemplaza 'API_TOKEN' con tu token)
    token = '7232414239:AAFdUuSQ5i1B9eWnaWILkuMg_0imHM6BeRA'

    # Crear la aplicación y pasarle el token del bot
    app = ApplicationBuilder().token(token).build()

    # Añadir manejadores de comandos
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("opciones", opciones))

    # Añadir manejador de mensajes (echo)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    app.add_handler(CallbackQueryHandler(button))
    # Manejar señales de terminación
    def stop_bot(signal, frame):
        logger.info('Deteniendo bot...')
        app.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, stop_bot)
    signal.signal(signal.SIGTERM, stop_bot)

    # Iniciar el bot
    app.run_polling()

if __name__ == '__main__':
    main()
