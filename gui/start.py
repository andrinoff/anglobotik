import telegram

MENU, ESSAY, LETTER = range(3)
MENU_ESSAY, MENU_LETTER, TEACHER_ESSAY, CHATGPT_ESSAY, TEACHER_LETTER, CHATGPT_LETTER = range(6)
EGE, OGE = range(2)

async def start(update: Update, context: CallbackContext):
    keyboard = [
        [telegram.InlineKeyboardButton('Essay', callback_data='essay')], 
        [telegram.InlineKeyboardButton('Letter', callback_data='letter')]
    ]
    reply_markup = telegram.InlineKeyboardMarkup(keyboard)
    await update.user.reply("Hello! I'm Essay Checker Bot. Please select one of the options below:", reply_markup=reply_markup)
    return MENU

async def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    if query.data == 'essay':
        await query.edit_message_text("Please send me the essay you want to check.")
        return ESSAY
    elif query.data == 'letter':
        await query.edit_message_text("Please send me the letter you want to check.")
        return LETTER
    else:
        await query.edit_message_text("Invalid option selected. Please try again.")
        return MENU



async def essay_start (update: Update, context: CallbackContext):
    keyboard2 = [
        [telegram.InlineKeyboardButton('Teacher', callback_data='teacher')],
        [telegram.InlineKeyboardButton('ChatGPT', callback_data='chatgpt')]
    ]
    reply_markup2 = telegram.InlineKeyboardMarkup(keyboard2)
    await update.user.reply("Please select one of the options below:", reply_markup=reply_markup2)
    return MENU_ESSAY

async def essay_button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    if query.data == 'teacher':
        await query.edit_message_text("To use this feature, you have to pay to BANK NUMBER. And send the essay to @SOMEONE")
        return TEACHER_ESSAY
    elif query.data == 'chatgpt':
        await query.edit_message_text("Please send me the essay you want to check.")
        return CHATGPT_ESSAY
    else:
        await query.edit_message_text("Invalid option selected. Please try again.")
        return MENU_ESSAY
    
async def letter_start (update: Update, context: CallbackContext):
    keyboard2 = [
        [telegram.InlineKeyboardButton('Teacher', callback_data='teacher')],
        [telegram.InlineKeyboardButton('ChatGPT', callback_data='chatgpt')]
    ]
    reply_markup2 = telegram.InlineKeyboardMarkup(keyboard2)
    await update.user.reply("Please select one of the options below:", reply_markup=reply_markup2)
    return MENU_LETTER

async def letter_button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    if query.data == 'teacher':
        await query.edit_message_text("To use this feature, you have to pay to BANK NUMBER. And send the letter to @SOMEONE")
        return TEACHER_LETTER
    elif query.data == 'chatgpt':
        await query.edit_message_text("Please send me the letter you want to check.")
        return CHATGPT_LETTER
    else:
        await query.edit_message_text("Invalid option selected. Please try again.")
        return MENU_LETTER