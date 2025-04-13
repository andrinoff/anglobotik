import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, ApplicationBuilder, CallbackQueryHandler
import logging

import os
from telegram.ext import ConversationHandler
from src.msg_handlers import (
    teacher, ai, START, TEACHER, AI, start, TeacherOrAi,
    TEACHER_OR_AI,
    EGE_OR_OGE, EgeOrOge, LETTER_OR_ESSAY, letterOrEssay
)

# Loads the .env file in here
from dotenv import load_dotenv
load_dotenv()

# logging 
# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     level=logging.INFO
# )

# start the bot and add handlers
if __name__ == '__main__':
    application = ApplicationBuilder().token(os.getenv('TELEGRAM_TOKEN')).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            # Add states for the functions have an opportunity to send forward and get query
            START: [
                CallbackQueryHandler(start, pattern="^START$"),
                CallbackQueryHandler(start, pattern="^BACK$")
            ],
            TEACHER_OR_AI: [
                    CallbackQueryHandler(TeacherOrAi, pattern="^TEACHER$"),
                    CallbackQueryHandler(TeacherOrAi, pattern="^AI$"),
                    CallbackQueryHandler(TeacherOrAi, pattern='^BACK$')
            ],
            LETTER_OR_ESSAY: [
                CallbackQueryHandler(letterOrEssay, pattern="^LETTER$"),
                CallbackQueryHandler(letterOrEssay, pattern="^ESSAY$"),
                CallbackQueryHandler(letterOrEssay, pattern="^BACK$")
            ],
            EGE_OR_OGE: [
                CallbackQueryHandler(EgeOrOge, pattern="^EGE$"),
                CallbackQueryHandler(EgeOrOge, pattern="^OGE$"),
                CallbackQueryHandler(EgeOrOge, pattern="^BACK$")

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
    # add handler and start
    application.add_handler(conv_handler)

    application.run_polling()
