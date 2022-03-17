import logging
import messages
import telegramcalendar
import telegramtime
import spotsmongo
import os

from telegram.ext import Updater,CallbackQueryHandler,CommandHandler, MessageHandler,Filters
from telegram import  ReplyKeyboardRemove,ParseMode


def start(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=messages.start_message.format(update.message.from_user.first_name),
        parse_mode=ParseMode.HTML)

def calendar_handler(update, context):
    update.message.reply_text(text=messages.calendar_message,
                    reply_markup=telegramcalendar.create_calendar())

def inline_handler(update, context):
    data = update.callback_query.data
    if '_at_' in data:
        inline_time_handler(update, context)
    else:
        inline_calendar_handler(update, context)


def inline_calendar_handler(update, context):
    selected,date = telegramcalendar.process_calendar_selection(update, context)
    if selected:
        context.bot.send_message(chat_id=update.callback_query.from_user.id,
                        text=messages.time_selection_message,
                        reply_markup=telegramtime.create_time_data(f'/confirm_{date.strftime("%d_%m_%Y")}'))

def inline_time_handler(update, context):
    selected,data = telegramtime.process_time_selection(update, context)
    if selected:
        context.bot.send_message(chat_id=update.callback_query.from_user.id,
                        text=data,
                        reply_markup=ReplyKeyboardRemove())

def time_handler(update, context):
    update.message.reply_text(text=messages.calendar_message,
                    reply_markup=telegramtime.create_time_data())

def confirm_handler(update, context):
    try:
        spotsmongo.save(update)
        update.message.reply_text(text=messages.spot_saved_message)
        return
    except Exception as e:
        update.message.reply_text(text=messages.command_not_found_message)

def remove_handler(update, context):
    try:
        result = spotsmongo.remove(update)
        if result:
            update.message.reply_text(text=messages.spot_removed_message)
    except:
        update.message.reply_text(text=messages.command_not_found_message)

def list_handler(update, context):
    watching_spots = spotsmongo.list(update)
    if watching_spots:
        update.message.reply_text(text=messages.active_spots_message.format(watching_spots))
        return
    update.message.reply_text(text=messages.no_spots_message)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

PORT = int(os.environ.get('PORT', '8443'))
TOKEN = "5245043648:AAEYlV84JtcfVgwy6ZdHfc2c9hVjHTSYobw"
updater = Updater(TOKEN,use_context=True)
dp=updater.dispatcher

dp.add_handler(CommandHandler("start",start))
dp.add_handler(CommandHandler("add",calendar_handler))
dp.add_handler(CommandHandler("time",time_handler))
dp.add_handler(CommandHandler("list",list_handler))
dp.add_handler(MessageHandler(Filters.regex('/confirm_*'), confirm_handler))
dp.add_handler(MessageHandler(Filters.regex('/remove_*'), remove_handler))
dp.add_handler(CallbackQueryHandler(inline_handler))

updater.start_webhook(listen="0.0.0.0",
                    port=PORT,
                    url_path=TOKEN,
                    webhook_url="https://kgv-calendar.herokuapp.com/" + TOKEN)
updater.idle()
