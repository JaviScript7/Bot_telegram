import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup,ReplyKeyboardMarkup, KeyboardButton,ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes, ConversationHandler,CallbackContext,Updater
from formulario import start_form, name_handler, contacto_handler, tipo_equipo_handler, marca_handler, modelo_handler,problema_handler, accesorios_handler,observaciones_handler,cancel_handler
from formulario import NAME_C,CONTACTO, TIPO_EQUIPO, MARCA, MODELO, PROBLEMA, ACCESORIOS, OBSERVACIONES
from database import create_table

from consulta_reparacion import start_consult,folio_handler
from consulta_reparacion import FOLIO

import colorlog



import os
from dotenv import load_dotenv #Esta linea puedes ignorarlo, lo ocupe para que durante el desarrollo no exponga mi key




#-----------------------------------------------------------
# Configuración básica de colorlog con colores 
handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    "%(log_color)s%(asctime)s | %(name)s | %(levelname)-8s | ➤ %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S',
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }
))

logger = colorlog.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Función para log con el símbolo ➤ antes del mensaje
def log_message(level, message):
    if level == 'debug':
        logger.debug(message)
    elif level == 'info':
        logger.info(message)
    elif level == 'warning':
        logger.warning(message)
    elif level == 'error':
        logger.error(message)
    elif level == 'critical':
        logger.critical(message)




#-----------------------------------------------------------

# Definir el teclado personalizado con valores asociados



# Definición de comandos
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('¡Hola! Usa /menu para ver las opciones.')

# Función para manejar las opciones
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    custom_keyboard = [['Reparación 🛠️'], ['Consulta 📲'],['Almacen 📦','💰','📊','⚙']]
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
        await start_consult(update, context)
        return FOLIO
        #return ConversationHandler.END
    elif user_reply  == 'Almacen 📦':
        await update.message.reply_text(text="¡Presionaste para almacen!",reply_markup=ReplyKeyboardRemove())
        #return ConversationHandler.END
    elif user_reply  == '💰':
        await update.message.reply_text(text="¡Presionaste el consulta de saldo",reply_markup=ReplyKeyboardRemove())
        #return ConversationHandler.END
    elif user_reply  == '⚙':
        await update.message.reply_text(text="¡Presionaste de configuracion!",reply_markup=ReplyKeyboardRemove())
        #return ConversationHandler.END
    
    #elif user_reply  == 'cancel':
        #return await cancel_handler(update, context)



        
#Boton especifico para cancelar registro de reparacion
async def button_regcancel(update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    query.answer()
    if query.data == 'cancel':
        query.message.reply_text('Registro cancelado.')
        return await cancel_handler(update, context)

# Función principal para iniciar el bot
def main():
    # Crear la tabla en la base de datos
    create_table()

    #Estas lineas las podemos ignorar, esto lo ocupe para proteger mi token duranta el desarrollo y subir repositorios
    load_dotenv()
    API_TOKEN = os.getenv("API_TOKEN")
    
    
    # Token de API del bot (reemplaza 'API_TOKEN' con tu token real)
    token = API_TOKEN

    # Crear la aplicación y pasarle el token del bot
    app = ApplicationBuilder().token(token).build()

    # Añadir manejadores de comandos
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu))

    # Configuración del ConversationHandler para manejar la consulta de folio
    convFolio_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex('^Consulta 📲$'), button)],
        states={
            FOLIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, folio_handler)]
        },
        fallbacks=[CallbackQueryHandler(button_regcancel, pattern='^cancel$')],
        #fallbacks=[MessageHandler(filters.Regex('^cancel$'), button)]
    )
    app.add_handler(convFolio_handler)

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
        fallbacks=[CallbackQueryHandler(button_regcancel, pattern='^cancel$')],
        #fallbacks=[MessageHandler(filters.Regex('^cancel$'), button)]

    )

    app.add_handler(conv_handler)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, button))
    
  

    # Iniciar el bot
    app.run_polling()

if __name__ == '__main__':
    main()
