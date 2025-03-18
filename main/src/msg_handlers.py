import telegram
from telegram import Update
from telegram.ext import ApplicationBuilder, CallbackContext
import os


MENU, ESSAY, LETTER, TEACHER, AI = range(5)



async def start(update: Update, context: CallbackContext):
    keyboard = [
        [telegram.InlineKeyboardButton('Teacher', callback_data='teacher')], 
        [telegram.InlineKeyboardButton('AI', callback_data='ai')]
    ]
    reply_markup = telegram.InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Hello! I'm Essay Checker Bot. Please select one of the options below:", reply_markup=reply_markup)
    query = telegram.CallbackQuery()
    await query.answer()
    if query.data == 'teacher':
        await query.edit_message_text("Please send me the essay, or the letter you want to check.")
        return TEACHER
    elif query.data == 'ai':
        keyboard = [
            [telegram.InlineKeyboardButton('Essay', callback_data='essay')], 
            [telegram.InlineKeyboardButton('Letter', callback_data='letter')],
            [telegram.InlineKeyboardButton('Back', callback_data='back')]
        ]
        reply_markup = telegram.InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Great! Now please select one of the options below:", reply_markup=reply_markup)
        await query.answer()
        if query.data == 'essay':
            await query.edit_message_text("Please send me the essay you want to check.")
            return ESSAY
        elif query.data == 'letter':
            await query.edit_message_text("Please send me the letter you want to check.")
            return LETTER
        elif query.data == 'back':
            await query.edit_message_text("Please select one of the options below:")
            return MENU
        else:
            await query.edit_message_text("Invalid option selected. Please try again.")
            return AI
    else:
        await query.edit_message_text("Invalid option selected. Please try again.")
        return MENU


    

async def teacher (update: Update, context: CallbackContext):
    essay = update.message.text
    await update.message.reply_text(f"Great! The essay has been sent to the teacher. Please, await the response! \n Your teacher credentials are: \n Username: {os.getenv('TEACHER_USERNAME')} \n Name: {os.getenv('TEACHER_NAME')}")
    await context.bot.send_message(chat_id=os.getenv("YOUR_ID"), text=f"Hi, (@{update.effective_user.username}) wants you to check the essay: \n{essay}")
    return MENU