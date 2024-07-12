from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from datetime import datetime
from database import get_equipo_by_folio

#Definicion de estados del formulario para registrar equipos
#Datos del cliente 
FOLIO = range(1)

async def start_consult(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message:
        await update.message.reply_text(
            'Ingresa el folio: ',
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Cancelar", callback_data='cancel')]])
        )
    elif update.callback_query:
        await update.callback_query.message.reply_text(
            'Ingresa el Folio',
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Cancelar", callback_data='cancel')]])
        )
    return FOLIO


async def folio_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['folio'] = update.message.text
    folio = context.user_data['folio']
    #Mandamos a llamar la funcion para consultar un equipo con el folio
    datos = get_equipo_by_folio(folio)
    print(datos)
    if datos:
        await update.message.reply_text(
            f"La informacion de su consulta:\n\n"
            f"🏷️ Folio: {datos[1]}\n"
            f"📅 Fecha de registro: {datos[10]}\n"
            f"👤 Nombre del cliente: {datos[2]}\n"
            f"📞 Contacto: {datos[3]}\n"
            f"📱 Tipo de equipo: {datos[4]}\n"
            f"📱 Marca: {datos[5]}\n"
            f"📱 Modelo: {datos[6]}\n"
            f"⚠️ Problema: {datos[7]}\n"
            f"⚠️ Accesorios: {datos[8]}\n"
            f"🔍 Observaciones: {datos[9]}"
    )
    else:
        await update.message.reply_text(f'El folio {folio} no fue encontrado en la base de datos.')

    return ConversationHandler.END
    

    



async def cancel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.callback_query.message.reply_text(f'⚠️ Consulta cancelada ⚠️')
    return ConversationHandler.END


