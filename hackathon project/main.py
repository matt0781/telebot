import openai
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import telegram_utils 

TOKEN: Final = '6973180139:AAG69PKg0sodJNZeSSH2K_hCmr8AebYI4XU'
BOT_USERNAME: Final = '@TimetableAgent_bot'
openai.api_key = "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"


def main():
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()
    
    # Connect to Google Calander (optional)
    """
    Code to connect google calander
    """
    
    # Commands
    app.add_handler(CommandHandler('start', telegram_utils.start_command))
    app.add_handler(CommandHandler('sync_google_calendar', telegram_utils.connect_gc))
    app.add_handler(CommandHandler('unsync_google_calendar', telegram_utils.disconnect_gc))
    
    # Messages
    app.add_handler(MessageHandler(filters.TEXT, telegram_utils.handle_message))
    
    # Errors
    app.add_error_handler(telegram_utils.error)
    

    # Polls the bot
    print("Polling...")
    app.run_polling(poll_interval=3)
        

if __name__ == '__main__':
    main()