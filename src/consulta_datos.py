from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from datetime import datetime
from database import get_data_for_time

RANGO_FECHA = range(1)



async def start_consult_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message:
        await update.message.reply_text(
            'Consulta tus datos en el siguiente formato: \n\nDía: YYYY-MM-DD\nSemana: YYYY-MM-DD YYYY-MM-DD\nMes YYYY-MM',
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Cancelar", callback_data='cancel')]])
        )
    elif update.callback_query:
        await update.callback_query.message.reply_text(
            'Quiere consultar datos por: \nDIA\nSemana\nMes',
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Cancelar", callback_data='cancel')]])
        )
    return RANGO_FECHA 

async def datos_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['rango_fecha'] = update.message.text
    fecha = context.user_data['rango_fecha']
    #Mandamos a llamar la funcion para consultar un equipo con el folio
    datos = get_data_for_time(fecha)
    #print(datos)
    if datos:
        await update.message.reply_text(
            f"Hola sus datos estan siendo procesdos por {datos[1]}"
        )
        IMAGE_FILE_PATH = f"analisis/{datos[0]}.png"

        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=open(IMAGE_FILE_PATH, 'rb'),
            caption=f"Datos por {datos[1]}.",
        )
    else:
        await update.message.reply_text(f'Los datos por {fecha} no fue encontrado en la base de datos.')

    return ConversationHandler.END


async def cancel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.callback_query.message.reply_text(f'⚠️ Consulta cancelada ⚠️')
    return ConversationHandler.END