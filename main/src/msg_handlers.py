import telegram
from telegram import Update
from telegram.ext import CallbackContext
import os
from telegram.ext._handlers.conversationhandler import ConversationHandler
from src.ai.ai import check_prompt
from exam_checker.essay_checker_bot.main.src.ai.ai import check_letter,\
    check_essay

# Stages
START, TEACHER_OR_AI, TEACHER, AI, TEACHER_TYPE, AI_TYPE = range(6)






async def start(update: Update, context: CallbackContext):
    keyboard = [
        [telegram.InlineKeyboardButton('Teacher', callback_data='TEACHER')],
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
        keyboard = [
        [telegram.InlineKeyboardButton('Letter', callback_data='LETTER')],
        [telegram.InlineKeyboardButton('Essay', callback_data='ESSAY')]
        ]
        reply_markup = telegram.InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Great! Please, choose what you want a teacher to check:", reply_markup=reply_markup)
        
        return TEACHER_TYPE
    elif query.data == 'AI':
        print("AI button pressed")
        await query.edit_message_text(text="Great! Please, send what you want an AI to check:")
        return AI
    else: 
        await query.edit_message_text(text="Something went wrong. Please, try again.")
        return ConversationHandler.END
    
    
async def choose_ai_type(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
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


    
async def ai(update: Update, context: CallbackContext):
    essay = update.message.text
    if context.user_data['type'] == 'LETTER':
        feedback = check_letter(essay)
    else:
        feedback = check_essay(essay)
    await update.message.reply_text(f'{feedback} \n\n\n let me know if you have any other questions.')
    return ConversationHandler.END
    
    

async def choose_teacher_type(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    if query.data == 'LETTER':
        print("Letter button pressed")
        await query.edit_message_text(text="Great! Please send your letter:")
        context.user_data['type'] = 'LETTER'
        return TEACHER  # Now move to TEACHER state to receive text input

    elif query.data == 'ESSAY':
        print("Essay button pressed")
        await query.edit_message_text(text="Great! Please send your essay:")
        context.user_data['type'] = 'ESSAY'
        return TEACHER  # Now move to TEACHER state to receive text input

    else:
        await query.edit_message_text(text="Error occurred, try again")
        return ConversationHandler.END

async def teacher(update: Update, context: CallbackContext):
    type_of_work = context.user_data['type']
    work = update.message.text
    await context.bot.send_message(chat_id=os.getenv('CHAT_ID'), text=f"@{update.effective_chat.username} sent you a {type_of_work.lower()} to check: \n {work}")
    await update.message.reply_text(f'Great. Your {type_of_work.lower()} has been sent to the teacher. \n Their credentials: {os.getenv("NAME")}, @{os.getenv("USERNAME")}')
    return ConversationHandler.END
