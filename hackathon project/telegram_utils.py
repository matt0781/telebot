import openai
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import json
from google_calander import google_handler, connect_to_google
import datetime
import db_api

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"User's username name: ({update.message.chat.username}) commanded /start")
    db_api.add_user(update.message.chat.username)
    await update.message.reply_text(f"""Hi {update.message.chat.first_name}, I am your speedy timetable agent. Tell me what your event is and I will add for you.""")
    
async def connect_gc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"User's first name: ({update.message.chat.first_name}) commanded /sync_gc")
    connect_to_google(update.message.chat.first_name)
    db_api.connect_google_calendar(update.message.chat.username, True)
    await update.message.reply_text(f"""You have connected to your google calendar.""")
    
async def disconnect_gc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"User's username: ({update.message.chat.username}) commanded /unsync_gc")
    db_api.connect_google_calendar(update.message.chat.username, True)
    await update.message.reply_text(f"""You have disconnected from your google calendar.""")

# Messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type
    user_msg = update.message.text
    # User's information
    print(f"User's fullname: ({update.message.chat.first_name} {update.message.chat.last_name}) in {message_type}: {user_msg}")
    
    # Processing response
    response = handle_response(user_msg, update.message.chat.username)
        
    print('Bot: ', response)
    # Provide response
    await update.message.reply_text(response)  
    
    
# Responses
def handle_response(msg, username):
    example_json = {
        "summary": "",
        "location": "",
        "start_dateTime": "2024-MM-DDTHH:mm:ss+08:00",

        "end_dateTime": "2024-MM-DDTHH:mm:ss+08:00",
    }
        
    messages = [
        {"role": "system", "content": "Provide output in valid JSON. The data schema should be like this: " + json.dumps(example_json)},
        {"role": "system", "content": """
            Rule 1: Strictly follow the dateTime format from the given data schema template. 
            Rule 2: If user says the time is next Thursday, you should be able to calculate the dateTime based on today date.
            Rule 3: The start_dateTime should be the dateTime specify by the user.
            Rule 4: If user doesn't specify how long the event or when the event ends, assume the end_dateTime is 1 hour from the start_dateTime.
        """},
        {"role": "system", "content": f"Today time is {datetime.datetime.now()}"},
        {"role": "user", "content": msg}
    ]

    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo-1106",
        max_tokens = 500,
        response_format = {"type": "json_object"},
        messages = messages

    )

    print("gpt response: ", response["choices"][0]["message"]["content"])

    gpt_response =  response["choices"][0]["message"]["content"]
    
    # ------------ Pass it to google -------------- #
    google_handler(json.loads(gpt_response), username)
    
    return f"The following update is done.\n{gpt_response}"

# Error
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")