from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def create_time_data(date):
    keyboard = []

    row = []
    row.append(InlineKeyboardButton('18:00',callback_data=f'{date}_at_18_00'))
    row.append(InlineKeyboardButton('18:30',callback_data=f'{date}_at_18_30'))
    row.append(InlineKeyboardButton('19:00',callback_data=f'{date}_at_19_00'))
    row.append(InlineKeyboardButton('19:30',callback_data=f'{date}_at_19_30'))
    keyboard.append(row)

    row = []
    row.append(InlineKeyboardButton('20:00',callback_data=f'{date}_at_20_00'))
    row.append(InlineKeyboardButton('20:30',callback_data=f'{date}_at_20_30'))
    row.append(InlineKeyboardButton('21:00',callback_data=f'{date}_at_21_00'))
    row.append(InlineKeyboardButton('21:30',callback_data=f'{date}_at_21_30'))
    keyboard.append(row)

    row = []
    row.append(InlineKeyboardButton('22:00',callback_data=f'{date}_at_22_00'))
    row.append(InlineKeyboardButton('22:30',callback_data=f'{date}_at_22_30'))
    row.append(InlineKeyboardButton('23:00',callback_data=f'{date}_at_23_00'))
    row.append(InlineKeyboardButton('23:30',callback_data=f'{date}_at_23_30'))
    keyboard.append(row)

    return InlineKeyboardMarkup(keyboard)

def process_time_selection(update, context):
    query = update.callback_query
    context.bot.edit_message_text(text=query.message.text,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id
            )
    data = query.data
    return True,data