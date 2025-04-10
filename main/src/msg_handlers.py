import telegram
from telegram import Update
from telegram.ext import CallbackContext
import os
from telegram.ext._handlers.conversationhandler import ConversationHandler
from src.ai.ai import check_essay, check_letter
from telegram import constants

# Stages
START, TEACHER_OR_AI, TEACHER, AI, EGE_OR_OGE, LETTER_OR_ESSAY = range(6)

# Stages = range(9)


async def start(update: Update, context: CallbackContext):
    # keyboard = [
    #     [telegram.InlineKeyboardButton(f'Teacher [{os.getenv("PRICE")}]', callback_data='TEACHER')],
    #     [telegram.InlineKeyboardButton('AI', callback_data='AI')]
    # ]
    keyboard = [
        [telegram.InlineKeyboardButton('ЕГЭ', callback_data='EGE')],
        [telegram.InlineKeyboardButton('ОГЭ', callback_data='OGE')],
        ]
    reply_markup = telegram.InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Привет! Я Англоботик, который поможет проверить твою письменную работу для экзаменов. Выбери, какой экзамен ты сдаёшь: ОГЭ или ЕГЭ....:", reply_markup=reply_markup)
    return EGE_OR_OGE


async def EgeOrOge (update: Update, context: CallbackContext): 
    query = update.callback_query
    await query.answer()
    if query.data == "EGE":
        print("chose ege")
        context.user_data["type_exam"] = "EGE"
        keyboard = [
        [telegram.InlineKeyboardButton(f'Эссе', callback_data='ESSAY')],
        [telegram.InlineKeyboardButton('Личное письмо', callback_data='LETTER')],
        [telegram.InlineKeyboardButton('Назад', callback_data='BACK')]
        ]
        reply_markup = telegram.InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Отлично! Теперь выбери, что будем проверять: эссе или личное письмо.", reply_markup=reply_markup)
        return LETTER_OR_ESSAY
    if query.data == "OGE":
        print(f"chose OGE")
        context.user_data["type_exam"] = "OGE"
        keyboard = [
        [telegram.InlineKeyboardButton('Личное письмо', callback_data='LETTER')],
        [telegram.InlineKeyboardButton('Назад', callback_data='BACK')]
        ]
        reply_markup = telegram.InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Отлично! Теперь выбери, что будем проверять", reply_markup=reply_markup)
        return LETTER_OR_ESSAY


async def letterOrEssay(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    if query.data == 'LETTER':
        print("Letter button pressed")
        context.user_data["type"] = "LETTER"
    elif query.data == 'ESSAY':
        print("Essay button pressed")
        context.user_data["type"] = "ESSAY"
    elif query.data == "BACK": 
        print("Back button pressed")
        await query.edit_message_text(text="Have a good dat, to start over type /start ")
        return ConversationHandler.END
    else:
        print("Unexpected button pressed")
        await query.edit_message_text(text="Error: Unexpected button pressed. Please try again.")
        return ConversationHandler.END
    keyboard = [
        [telegram.InlineKeyboardButton(f'🔹 Учитель ({os.getenv("PRICE")}, детальный разбор)', callback_data='TEACHER')],
        [telegram.InlineKeyboardButton('🔹 Искусственный интеллект (бесплатно, быстрая проверка)', callback_data='AI')],
        [telegram.InlineKeyboardButton('Назад', callback_data='BACK')]
        ]
    reply_markup = telegram.InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="Последний шаг! Кто будет проверять твою работу? \nВыбери вариант:", reply_markup=reply_markup)
    return TEACHER_OR_AI
    


async def TeacherOrAi(update: Update, context: CallbackContext):
    print("made it to TeacherOrAi")
    query = update.callback_query
    await query.answer()
    if query.data == 'TEACHER':
        await query.edit_message_text(text="Отлично! Отправь мне текст для проверки:")
        print("Teacher button pressed")
        return TEACHER

    elif query.data == 'AI':
        await query.edit_message_text(text="Отлично! Пришли мне текст для проверки:")
        return AI
    elif query.data == 'BACK':
        print("Back button pressed")
        await query.edit_message_text(text="Чтобы начать с начала напиши /start ")
        return ConversationHandler.END
    else: 
        await query.edit_message_text(text="Что-то пошло не так. Попробуйте еще раз.")
        return ConversationHandler.END

    
async def ai(update: Update, context: CallbackContext):
    essay = update.message.text
    await update.message.reply_text(f'Great, AI is thinking...')
    if context.user_data['type'] == 'LETTER':
        feedback = check_letter(letter=essay, exam=context.user_data["type_exam"])
    elif context.user_data["type"] == "ESSAY":
        feedback = check_essay(essay=essay, exam=context.user_data["type_exam"])
    await update.message.reply_text(f'{feedback} \n\n\n /start чтобы начать снова!')
    return ConversationHandler.END
    


async def teacher(update: Update, context: CallbackContext):
    work = update.message.text
    print(work)
    await context.bot.send_message(chat_id=os.getenv('TEACHER_CHAT_ID'), text=f"@{update.effective_chat.username} sent you a {context.user_data['type'].lower()} to check {context.user_data['type_exam']}: \n {work}")
    await update.message.reply_text(f'Отлично. Твой текст был отправлен учителю. Оплати по {os.getenv("PHONE_NUMBER")} и отправь чек в личку! \n Их контакты: {os.getenv("NAME")}, @{os.getenv("USERNAME")}')
    return ConversationHandler.END