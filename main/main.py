import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

# logging 
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# start the bot and add handlers
if __name__ == '__main__':
    application = ApplicationBuilder().token(os.getenv('TELEGRAM_TOKEN')).build()
    application.run_polling()