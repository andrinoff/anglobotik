import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, ApplicationBuilder, CallbackQueryHandler
import logging

import os
from telegram.ext import ConversationHandler
from src.msg_handlers import teacher, ai, START, TEACHER, AI, start, TeacherOrAi, TEACHER_OR_AI, TEACHER_TYPE, choose_teacher_type, AI_TYPE, choose_ai_type



# logging 
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# start the bot and add handlers
if __name__ == '__main__':
    application = ApplicationBuilder().token(os.getenv('TELEGRAM_TOKEN')).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            START: [
                CallbackQueryHandler(TeacherOrAi)
            ],
            TEACHER_OR_AI: [
                    CallbackQueryHandler(TeacherOrAi, pattern="^TEACHER$"),
                    CallbackQueryHandler(TeacherOrAi, pattern="^AI$")
            ],
            TEACHER_TYPE: [
                    
                    CallbackQueryHandler(choose_teacher_type, pattern="^ESSAY$"),
                    CallbackQueryHandler(choose_teacher_type, pattern="^LETTER$")
            ],
            AI_TYPE: [
                CallbackQueryHandler(choose_ai_type, pattern="^ESSAY$"),
                CallbackQueryHandler(choose_ai_type, pattern="^LETTER$")
            ],
            TEACHER: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, teacher)
            ],
            AI: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, ai)
            ],
        },
        fallbacks=[
            CommandHandler('start', start)
        ]

    )
    application.add_handler(conv_handler)

    application.run_polling()
