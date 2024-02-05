import openai
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes


# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"User's first name: ({update.message.chat.first_name}) commanded /start")
    await update.message.reply_text(f"""Hi {update.message.chat.first_name}, I am your personalized grammanist from Harvard Grammar School. Send me a message so that I can tell if the sentence(s) is/are grammatically correct.""")
async def limit_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"User's first name: ({update.message.chat.first_name}) commanded /limitation")
    await update.message.reply_text("""I cannot deal with a large paragraph due to my maximum tokens limit (500). However, you can break the large paragraph into smaller pieces and send them seperately.""")
    
async def output_query_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"User's first name: ({update.message.chat.first_name}) commanded /output_format")
    await update.message.reply_text("""If your input sentence(s) is/are grammatically correct, I will say it is.
Else, I will provide you the correct version and explain why it is wrong.""")

# Messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type
    text = update.message.text
    # User's information
    print(f"User's fullname: ({update.message.chat.first_name} {update.message.chat.last_name}) in {message_type}: {text}")
    
    # Processing response
    response = handle_response(text)
        
    print('Bot: ', response)
    # Provide response
    await update.message.reply_text(response)  
    
    
# Responses
def handle_response(msg):
    messages = [
        {"role": "system", "content": """You are an English teacher, speciafically teaching grammar. Think step by step. 
If the given sentence(s) is/are grammatically correct, output: It is grammartically perfect. 
If the given sentence(s) is/are not grammatically correct, explain it step by step. 1. The grammartically correct version of the sentence, 2. Explain why it is wrong. You can also provide more than 1 correct version of it""" },
        {"role": "user", "content": "The given input: 'He is not buying the house'"},
        {"role": "assistant", "content": "It is grammatically perfect."},
        {"role": "user", "content": f"The given input: '{msg}'"}
    ]
    
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = messages,
        max_tokens = 500
    )

    return response["choices"][0]["message"]["content"]


# Error
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")