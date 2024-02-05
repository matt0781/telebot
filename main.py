import openai
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import telegram_utils 

TOKEN: Final = '6211118095:AAFLKKjvQeqns8eyYOz2a6FdNHscwAFAttU'
BOT_USERNAME: Final = '@The_snoopbot'

openai.api_key = "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"


def main():
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()
    
    # Commands
    app.add_handler(CommandHandler('start', telegram_utils.start_command))
    app.add_handler(CommandHandler('limitation', telegram_utils.limit_command))
    app.add_handler(CommandHandler('output_format', telegram_utils.output_query_command))
    
    # Messages
    app.add_handler(MessageHandler(filters.TEXT, telegram_utils.handle_message))
    
    # Errors
    app.add_error_handler(telegram_utils.error)
    

    # Polls the bot
    print("Polling...")
    app.run_polling(poll_interval=3)
        

if __name__ == '__main__':
    main()
    

