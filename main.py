import json
import logging

import telebot

from data import messages, buttons
from handlers.message_constructors import create_keyboard, add_back_button
from my_config import config

# Initializing bot and logging
telebot.logger.setLevel(logging.INFO)
bot = telebot.TeleBot(config.TOKEN)

# Resetting WebHook
bot.remove_webhook()
bot.set_webhook(url=config.AWS_URL)


# Const data
sections_with_reverse_btn = ['education', 'links', 'education']
# Setting up Bot info
# bot.set_chat_description(339993031, "This is my bot")
# bot.set_chat_title(339993031, "CVbot")


def lambda_handler(event, context):
    try:
        request = json.loads(event['body'])
    except Exception:
        return {
            'statusCode': 403
        }
    update = telebot.types.Update.de_json(json.dumps(request))
    message = update.message
    print(update)
    bot.process_new_updates([update])
    if update.message:
        handle_message(message)
    elif update.callback_query:
        handle_query(update.callback_query)
    else:
        bot.send_message(message.chat.id, messages.help)
    print(config.TOKEN)
    return {
        'statusCode': 200
    }


def handle_message(message):
    if message.text[0] == '/':
        handle_command(message)


def post_start_message(chat_id):
    keyboard = create_keyboard(**buttons.start_buttons)
    bot.send_message(chat_id, messages.greetings,
                     reply_markup=keyboard)


def handle_query(query):
    data = query.data
    chat_id = query.message.chat.id
    keyboard = None
    message = "Ooops! Is it error???"
    if data == 'projects':
        keyboard = create_keyboard(btn_type='url', **buttons.project_buttons)
        message = messages.projects
    elif data == 'education':
        message = messages.education
    elif data == 'links':
        keyboard = create_keyboard(btn_type='url', **buttons.link_buttons)
        message = messages.links
    elif data == 'back':
        keyboard = create_keyboard(**buttons.start_buttons)
        message = messages.greetings
    if data != 'back':
        keyboard = add_back_button(keyboard)
    bot.send_message(chat_id, message, reply_markup=keyboard)


def handle_command(message):
    command = message.text[1:]
    if command == 'start':
        post_start_message(message.chat.id)
    elif command == 'reset':
        post_start_message(message.chat.id)
    else:
        bot.send_message(message.chat.id, messages.help)
