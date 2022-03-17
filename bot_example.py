#!/usr/bin/python3

import logging

from telegram.ext import Updater,CallbackQueryHandler,CommandHandler, CallbackContext
from telegram import  ReplyKeyboardRemove,ParseMode, Update

import telegramcalendar
import messages
import os

# Go to botfather and create a bot and copy the token and paste it here in token
TOKEN = "5245043648:AAEYlV84JtcfVgwy6ZdHfc2c9hVjHTSYobw" # token of the bot
PORT = int(os.environ.get('PORT', '8443'))

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def start(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=messages.start_message.format(update.message.from_user.first_name),
        parse_mode=ParseMode.HTML)

# A simple command to display the calender
def calendar_handler(update, context):
    update.message.reply_text(text=messages.calendar_message,
                    reply_markup=telegramcalendar.create_calendar())

def inline_handler(update, context):
    inline_calendar_handler(update, context)


def inline_calendar_handler(update, context):
    selected,date = telegramcalendar.process_calendar_selection(update, context)
    if selected:
        context.bot.send_message(chat_id=update.callback_query.from_user.id,
                        text=messages.calendar_response_message % (date.strftime("%d_%m_%Y")),
                        reply_markup=ReplyKeyboardRemove())


updater = Updater(TOKEN,use_context=True)
dp=updater.dispatcher

dp.add_handler(CommandHandler("start",start))
dp.add_handler(CommandHandler("calendar",calendar_handler))
dp.add_handler(CallbackQueryHandler(inline_handler))

updater.start_webhook(listen="0.0.0.0",
                      port=PORT,
                      url_path=TOKEN,
                      webhook_url="https://kgv-calendar.herokuapp.com/" + TOKEN)
updater.idle()
