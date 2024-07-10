import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup,ReplyKeyboardMarkup, KeyboardButton,ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes, ConversationHandler,CallbackContext
from formulario import start_form, name_handler, contacto_handler, tipo_equipo_handler, marca_handler, modelo_handler,problema_handler, accesorios_handler,observaciones_handler,cancel_handler
from formulario import NAME_C,CONTACTO, TIPO_EQUIPO, MARCA, MODELO, PROBLEMA, ACCESORIOS, OBSERVACIONES

# Configuración de logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


# Definir el teclado personalizado con valores asociados


# Definición de comandos
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('¡Hola! Usa /opciones para ver las opciones.')

# Función para manejar las opciones
async def opciones(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    custom_keyboard = [['Reparación 🛠️'], ['Consulta 📲'],['Almacen 📦','💰','⚙']]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
    await update.message.reply_text('Por favor, elige una opción:', reply_markup=reply_markup)


# Función para manejar los botones
async def button(update: Update, context: CallbackContext) -> None:
    #query = update.callback_query
    #await query.answer()
    user_reply = update.message.text

    if  user_reply  == 'Reparación 🛠️':
        await start_form(update, context)
        return NAME_C
    elif user_reply  == 'Consulta 📲':
        await update.message.reply_text(text="¡Presionaste el Botón 2!",reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
    elif user_reply  == 'Almacen 📦':
        await update.message.reply_text(text="¡Presionaste para almacen!",reply_markup=ReplyKeyboardRemove())
        #return ConversationHandler.END
    elif user_reply  == '💰':
        await update.message.reply_text(text="¡Presionaste el consulta de saldo",reply_markup=ReplyKeyboardRemove())
        #return ConversationHandler.END
    elif user_reply  == '⚙':
        await update.message.reply_text(text="¡Presionaste de configuracion!",reply_markup=ReplyKeyboardRemove())
        #return ConversationHandler.END
    
    elif user_reply  == 'cancel':
        return await cancel_handler(update, context)
    
# Función principal para iniciar el bot
def main():
    # Token de API del bot (reemplaza 'YOUR_API_TOKEN_HERE' con tu token real)
    token = '7232414239:AAFdUuSQ5i1B9eWnaWILkuMg_0imHM6BeRA'

    # Crear la aplicación y pasarle el token del bot
    app = ApplicationBuilder().token(token).build()

    # Añadir manejadores de comandos
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("opciones", opciones))

    # Configuración del ConversationHandler para manejar el formulario
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex('^Reparación 🛠️$'), button)],
        states={
            NAME_C: [MessageHandler(filters.TEXT & ~filters.COMMAND, name_handler)],
            CONTACTO: [MessageHandler(filters.TEXT & ~filters.COMMAND, contacto_handler)],
            TIPO_EQUIPO: [MessageHandler(filters.TEXT & ~filters.COMMAND, tipo_equipo_handler)],
            MARCA: [MessageHandler(filters.TEXT & ~filters.COMMAND, marca_handler)],
            MODELO: [MessageHandler(filters.TEXT & ~filters.COMMAND, modelo_handler)],
            PROBLEMA: [MessageHandler(filters.TEXT & ~filters.COMMAND, problema_handler)],
            ACCESORIOS: [MessageHandler(filters.TEXT & ~filters.COMMAND, accesorios_handler)],
            OBSERVACIONES: [MessageHandler(filters.TEXT & ~filters.COMMAND, observaciones_handler )],
        },
        fallbacks=[CallbackQueryHandler(button, pattern='^cancel$')],
    )

    app.add_handler(conv_handler)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, button))

    # Iniciar el bot
    app.run_polling()

if __name__ == '__main__':
    main()
