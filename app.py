from constants import *
import logging
import os

# set proxy
os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

from telegram import BotCommand
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, Updater
from chat import ChatGPT

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


commands = [
    BotCommand("start", "开始"),
    BotCommand("clear", "清空对话记录"),
    BotCommand("system", "设置人设"),
    BotCommand("back", "撤回"),
]
"""
start - 开始
clear - 清空对话记录
system - 设置人设
back - 撤回
"""

chat_pool = {}


def get_user_meta(update):
    user_id = update.effective_user.id
    if user_id not in chat_pool:
        chat_pool[user_id] = {
            'gpt': ChatGPT([], user_id)
        }
    return chat_pool[user_id]


def handle_bot_status(message,gpt):
    if gpt.bot_status.is_waiting:
        return '你好，我是你的助手，你可以输入“/system”来设置人设，输入“/clear”来清空对话记录'
    elif gpt.bot_status.is_saving:
        gpt.save(message)
        gpt.bot_status.set_status('chatting')
        return '好的，已存档'
    elif gpt.bot_status.is_loading:
        message,ok = gpt.load(message).parse()
        if ok:
            gpt.bot_status.set_status('chatting')
        return message
    elif gpt.bot_status.is_system:
        gpt.set_system(message)
        gpt.bot_status.set_status('chatting')
        return '你好呀'
    message,ok = gpt.ask(message).parse()
    return message


async def start(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="你好，这里是BOBQWERA")

async def clear(update, context):
    gpt = get_user_meta(update)['gpt']
    gpt.clear()
    gpt.bot_status.set_status('waiting')
    await context.bot.send_message(chat_id=update.effective_chat.id, text="已清空对话记录")

async def system(update, context):
    gpt = get_user_meta(update)['gpt']
    gpt.bot_status.set_status('system')
    await context.bot.send_message(chat_id=update.effective_chat.id, text="请输入人设")

async def back(update, context):
    gpt = get_user_meta(update)['gpt']
    if gpt.messages:
        gpt.messages.pop()
        gpt.messages.pop()
        message = "已撤回"
    else:
        message = "无消息可撤回"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

async def chat(update, context):
    gpt = get_user_meta(update)['gpt']
    message = update.message.text
    message = handle_bot_status(message,gpt)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

async def unknown(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="抱歉，我不明白你在说什么。")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    bot = application.bot

    bot.set_my_commands(commands)

    start_handler = CommandHandler('start', start)
    clear_handler = CommandHandler('clear', clear)
    system_handler = CommandHandler('system', system)
    back_handler = CommandHandler('back', back)
    chat_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), chat)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)

    application.add_handler(start_handler)
    application.add_handler(clear_handler)
    application.add_handler(system_handler)
    application.add_handler(back_handler)
    application.add_handler(chat_handler)
    application.add_handler(unknown_handler)



    application.run_polling()