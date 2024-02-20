from constants import *

# set proxy
import os
os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"


import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    commands = ["/start", "/echo", "/caps", "/buttons"]
    keyboard = [[InlineKeyboardButton(command, callback_data=command)] for command in commands]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!", reply_markup=reply_markup)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

async def buttons(update, context):
    choices = ["Clear", "System"]
    buttons = list(map(lambda x: InlineKeyboardButton(x, callback_data=x), choices))
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Choose a button:", reply_markup=InlineKeyboardMarkup([buttons]))

async def Clear(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Clear")

async def System(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="System")

async def unknown(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="抱歉，我不明白你在说什么。")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    caps_handler = CommandHandler('caps', caps)
    buttons_handler = CommandHandler('buttons', buttons)
    clear_handler = CallbackQueryHandler(Clear, pattern="Clear")
    system_handler = CallbackQueryHandler(System, pattern="System")
    unknown_handler = MessageHandler(filters.COMMAND, unknown)


    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.add_handler(caps_handler)
    application.add_handler(buttons_handler)
    application.add_handler(clear_handler)
    application.add_handler(system_handler)
    application.add_handler(unknown_handler)

    
    application.run_polling()