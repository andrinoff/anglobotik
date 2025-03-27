import telegram
from telegram import Update
from telegram.ext import CallbackContext
import os
from telegram.ext._handlers.conversationhandler import ConversationHandler
from src.ai.ai import check_essay, check_letter
from telegram import constants


# Stages
START, TEACHER_OR_AI, TEACHER, AI, TEACHER_TYPE, AI_TYPE, EGE, OGE, EGE_OR_OGE = range(9)






async def start(update: Update, context: CallbackContext):
    keyboard = [
        [telegram.InlineKeyboardButton(f'Teacher [{os.getenv("PRICE")}]', callback_data='TEACHER')],
        [telegram.InlineKeyboardButton('AI', callback_data='AI')]
    ]
    reply_markup = telegram.InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Hello! I'm Essay Checker Bot. Please select one of the options below:", reply_markup=reply_markup)
    return TEACHER_OR_AI


async def TeacherOrAi(update: Update, context: CallbackContext):
    print("made it to TeacherOrAi")
    query = update.callback_query
    await query.answer()
    if query.data == 'TEACHER':
        print("Teacher button pressed")
        context.user_data["check_method"] = "teacher"
        keyboard = [
        [telegram.InlineKeyboardButton('EGE', callback_data='EGE')],
        [telegram.InlineKeyboardButton('OGE', callback_data='OGE')]
        ]
        reply_markup = telegram.InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Great! Please, choose what exam you want a teacher to check:", reply_markup=reply_markup)
        
        return EGE_OR_OGE
    elif query.data == 'AI':
        print("AI button pressed")
        context.user_data["check_method"] = "ai"
        keyboard = [
        [telegram.InlineKeyboardButton('EGE', callback_data='EGE')],
        [telegram.InlineKeyboardButton('OGE', callback_data='OGE')]
        ]
        reply_markup = telegram.InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Great! Please, select what exam you want an AI to check:", reply_markup=reply_markup)
        return EGE_OR_OGE
    else: 
        await query.edit_message_text(text="Something went wrong. Please, try again.")
        return ConversationHandler.END
    
    
async def EgeOrOge (update: Update, context: CallbackContext):    
    query = update.callback_query
    await query.answer()
    if query.data == "EGE":
        print("chose ege")
        context.user_data["type_exam"] = "EGE"
        keyboard = [
        [telegram.InlineKeyboardButton(f'Essay', callback_data='ESSAY')],
        [telegram.InlineKeyboardButton('Letter', callback_data='LETTER')]
        ]
        reply_markup = telegram.InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Wonderful! Now choose the type of a text you want to check: ", reply_markup=reply_markup)
        if context.user_data["check_method"] == "ai":
            return AI_TYPE
        elif context.user_data["check_method"] == "teacher":
            return TEACHER_TYPE
        else: 
            update.message.reply_text("Error occurred, try again. /start")
    if query.data == "OGE":
        print(f"chose OGE")
        context.user_data["type_exam"] = "OGE"
        keyboard = [
            [telegram.InlineKeyboardButton('Letter', callback_data='LETTER')]
        ]
        reply_markup = telegram.InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Choose the text type", reply_markup=reply_markup)
        print(context.user_data["check_method"])
        if context.user_data["check_method"] == "ai":
            return AI_TYPE
        elif context.user_data["check_method"] == "teacher":
            print("teacher selected")
            return TEACHER_TYPE
        else: 
            update.message.reply_text("Error occurred, try again. /start")
    

async def choose_ai_type(update: Update, context: CallbackContext):
    
    query = update.callback_query
    await query.answer()
    if context.user_data["type_exam"] == "EGE":
        if query.data == 'LETTER':
            print("Letter button pressed")
            await query.edit_message_text(text="Great! Please send your letter:")
            context.user_data['type'] = 'LETTER'
            return AI  # Now move to AI state to receive text input

        elif query.data == 'ESSAY':
            print("Essay button pressed")
            await query.edit_message_text(text="Great! Please send your essay:")
            context.user_data['type'] = 'ESSAY'
            return AI  # Now move to AI state to receive text input

        else:
            await query.edit_message_text(text="Error occurred, try again")
            return ConversationHandler.END
    if context.user_data["type_exam"] == "OGE":
            context.user_data["type"] = "LETTER"
            print("Letter button pressed")
            await query.edit_message_text(text="Great! Please send your letter:")
            context.user_data['type'] = 'LETTER'
            return AI  # Now move to AI state to receive text input


    
async def ai(update: Update, context: CallbackContext):
    essay = update.message.text
    await update.message.reply_text(f'Great, AI is thinking...')
    if context.user_data['type'] == 'LETTER':
        feedback = check_letter(letter = essay, exam =  context.user_data["type_exam"])
    elif context.user_data["type"] == "ESSAY":
        feedback = check_essay(essay = essay, exam =  context.user_data["type_exam"])
    await update.message.reply_text(f'{feedback} \n\n\n /start to start again!')
    return ConversationHandler.END
    
    

async def choose_teacher_type(update: Update, context: CallbackContext):
    print("at choose_teacher_type")
    print(context.user_data["type_exam"])
    query = update.callback_query
    await query.answer()
    if context.user_data["type_exam"] == "EGE":
        if query.data == 'LETTER':
            print("Letter button pressed")
            await query.edit_message_text(text="Great! Please send your letter:")
            context.user_data['type'] = 'LETTER'
            return TEACHER  # Now move to AI state to receive text input

        elif query.data == 'ESSAY':
            print("Essay button pressed")
            await query.edit_message_text(text="Great! Please send your essay:")
            context.user_data['type'] = 'ESSAY'
            return TEACHER  # Now move to AI state to receive text input

        else:
            await query.edit_message_text(text="Error occurred, try again")
            return ConversationHandler.END
    if context.user_data["type_exam"] == "OGE":
            context.user_data["type"] = "LETTER"
            print("Letter button pressed")
            await query.edit_message_text(text="Great! Please send your letter:")
            context.user_data['type'] = 'LETTER'
            return TEACHER  # Now move to AI state to receive text input

async def teacher(update: Update, context: CallbackContext):
    type_of_work = context.user_data['type']
    work = update.message.text
    await context.bot.send_message(chat_id=os.getenv('CHAT_ID'), text=f"@{update.effective_chat.username} sent you a {type_of_work.lower()} to check {context.user_data["type_exam"]}: \n {work}")
    await update.message.reply_text(f'Great. Your {type_of_work.lower()} has been sent to the teacher. \n Their credentials: {os.getenv("NAME")}, @{os.getenv("USERNAME")}')
    return ConversationHandler.END
