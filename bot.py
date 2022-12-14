import os
import uuid
import messages
import telegramcalendar
import telegramtime
import spotsmongo

from telegram.ext import Updater, CallbackQueryHandler, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardRemove, ParseMode


# Command handler
def start_handler(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=messages.start_message.format(update.message.from_user.first_name),
        parse_mode=ParseMode.HTML)

def add_handler(update, context):
    update.message.reply_text(
        text=messages.calendar_message,
        reply_markup=telegramcalendar.create_calendar())

def list_handler(update, context):
    watching_spots = spotsmongo.list(update)
    if watching_spots:
        update.message.reply_text(text=messages.active_spots_message.format(watching_spots))
        return
    update.message.reply_text(text=messages.no_spots_message)


# Message handler
def confirm_handler(update, context):
    try:
        spotsmongo.save(update)
        update.message.reply_text(text=messages.spot_saved_message)
        return
    except:
        update.message.reply_text(text=messages.command_not_found_message)

def remove_handler(update, context):
    try:
        result = spotsmongo.remove(update)
        if result:
            update.message.reply_text(text=messages.spot_removed_message)
    except:
        update.message.reply_text(text=messages.command_not_found_message)


# Callback handler
def inline_handler(update, context):
    data = update.callback_query.data
    if '_at_' in data:
        inline_time_handler(update, context)
    else:
        inline_calendar_handler(update, context)

def inline_calendar_handler(update, context):
    selected,date = telegramcalendar.process_calendar_selection(update, context)
    if selected:
        context.bot.send_message(
            chat_id=update.callback_query.from_user.id,
            text=messages.time_selection_message,
            reply_markup=telegramtime.create_time_data(f'/confirm_{date.strftime("%d_%m_%Y")}'))

def inline_time_handler(update, context):
    selected,data = telegramtime.process_time_selection(update, context)
    if selected:
        context.bot.send_message(
            chat_id=update.callback_query.from_user.id,
            text=data,
            reply_markup=ReplyKeyboardRemove())


# Adding handlers and start webhook
BOT_TOKEN = os.environ.get('BOT_TOKEN')
updater = Updater(BOT_TOKEN,use_context=True)
dp=updater.dispatcher

dp.add_handler(CommandHandler("start", start_handler))
dp.add_handler(CommandHandler("add", add_handler))
dp.add_handler(CommandHandler("list", list_handler))
dp.add_handler(MessageHandler(Filters.regex('/confirm_*'), confirm_handler))
dp.add_handler(MessageHandler(Filters.regex('/remove_*'), remove_handler))
dp.add_handler(CallbackQueryHandler(inline_handler))

PORT = int(os.environ.get('PORT', '8443'))
UUID_PATH = str(uuid.uuid4())
updater.start_webhook(listen="0.0.0.0",
                    port=PORT,
                    url_path=UUID_PATH,
                    webhook_url="https://kgv-calendar.herokuapp.com/" + UUID_PATH)
updater.idle()