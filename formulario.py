from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
import asyncio
import logging

# Definición de estados del formulario
#NAME, AGE, GENDER = range(3)
#Definicion de estados del formulario para registrar equipos
#Datos del cliente 
NAME_C,CONTACTO, TIPO_EQUIPO, MARCA, MODELO, PROBLEMA, ACCESORIOS, OBSERVACIONES = range(8)

async def start_form(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message:
        await update.message.reply_text(
            '👤Nombre del Cliente:',
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Cancelar", callback_data='cancel')]])
        )
    elif update.callback_query:
        await update.callback_query.message.reply_text(
            '👤Nombre del Cliente:',
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Cancelar", callback_data='cancel')]])
        )
    return NAME_C

async def name_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['name_c'] = update.message.text
    await update.message.reply_text(
        '📞 Número de Contacto:',
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Cancelar", callback_data='cancel')]])
    )
    return CONTACTO

async def contacto_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['contacto'] = update.message.text
    await update.message.reply_text(
        'Tipo de de equipo: \n💻 Computadora\n📱 Movil\n🛠️ Otro',
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Cancelar", callback_data='cancel')]])
    )
    return TIPO_EQUIPO

async def tipo_equipo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['tipo_equipo'] = update.message.text
    await update.message.reply_text(
        '📱💻 Marca del equipo:',
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Cancelar", callback_data='cancel')]])
    )
    return MARCA
async def marca_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['marca'] = update.message.text
    await update.message.reply_text(
        '📱💻 Modelo del equipo:',
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Cancelar", callback_data='cancel')]])
    )
    return MODELO
async def modelo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['modelo'] = update.message.text
    await update.message.reply_text(
        '⚠️ Problema que presenta:',
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Cancelar", callback_data='cancel')]])
    )
    return PROBLEMA
async def problema_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['problema'] = update.message.text
    await update.message.reply_text(
        '⚠️ Accesorios que dejan con el equipo:',
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Cancelar", callback_data='cancel')]])
    )
    return ACCESORIOS
async def accesorios_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['accesorios'] = update.message.text
    await update.message.reply_text(
        '🔍 Observaciones: ',
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Cancelar", callback_data='cancel')]])
    )
    return OBSERVACIONES

async def observaciones_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['observaciones'] = update.message.text
    await update.message.reply_text(
        f"Gracias por completar el registro!\n\n"
        f"👤 Nombre del cliente: {context.user_data['name_c']}\n"
        f"📞 Contacto: {context.user_data['contacto']}\n"
        f"📱 Tipo de equipo: {context.user_data['tipo_equipo']}\n"
        f"📱 Marca: {context.user_data['marca']}\n"
        f"📱 Modelo: {context.user_data['modelo']}\n"
        f"⚠️ Problema: {context.user_data['problema']}\n"
        f"⚠️ Accesorios: {context.user_data['accesorios']}\n"
        f"🔍 Observaciones: {context.user_data['observaciones']}\n"

    )
    return ConversationHandler.END


async def cancel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.callback_query.message.reply_text(f'Formulario cancelado.')
    return ConversationHandler.END


