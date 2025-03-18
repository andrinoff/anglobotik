import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, ApplicationBuilder
import logging
from src.msg_handlers import start
import os

# logging 
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# start the bot and add handlers
if __name__ == '__main__':
    application = ApplicationBuilder().token(os.getenv('TELEGRAM_TOKEN')).build()
    application.add_handler(CommandHandler('start', start))
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, button_handler))

    application.run_polling()