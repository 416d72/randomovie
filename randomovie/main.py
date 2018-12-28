#!usr/bin/env python3
# -*- coding: utf-8; -*-
"""
MIT License
Copyright (c) 2018 Amr Khamis
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import (
    ChatAction, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton,
    ReplyKeyboardMarkup, ReplyKeyboardRemove,
)
from os import environ


def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


# Constants
def random_reply_markup(url):
    button_list = [
        InlineKeyboardButton("Get one more", callback_data="random"),
        InlineKeyboardButton("Watch or Download", url=url),
    ]
    return InlineKeyboardMarkup(build_menu(button_list, n_cols=2))


def create_markup():
    button_list = [
        [KeyboardButton("Action"), KeyboardButton("Horror"), KeyboardButton("Action"), KeyboardButton("Action")],
        [KeyboardButton("Action"), KeyboardButton("Action"), KeyboardButton("Load more")]
    ]
    return ReplyKeyboardMarkup(button_list)


def command_start(bot, update):
    bot_description = 'This bot was created to provide a random movie based on user\'s filter including genres,' \
                      'minimum rating and minimum release year.\n' \
                      'You can start creating your own filter using /create command\n' \
                      'After you complete creating your filter, you can use /random command to get a random movie based ' \
                      'on your preferences\n.' \
                      'Whenever you need help just send /help\n' \
                      'Have fun 😊'
    bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
    bot.send_message(chat_id=update.effective_message.chat_id, parse_mode=ParseMode.MARKDOWN,
                     text=f"Hello *{update.effective_user.full_name}*\n{bot_description}")


def command_create(bot, update):
    bot.send_message(chat_id=update.effective_message.chat_id, text="Create..", reply_markup=create_markup())


def command_reset(bot, update):
    bot.send_message(chat_id=update.effective_message.chat_id, text="Your filters have been successfully reset!")


def command_random(bot, update):
    title = 'Download full movie Interstellar 2014'.replace(' ', '+')
    url = f"https://www.google.com.eg/search?q={title}"
    bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
    bot.send_message(chat_id=update.effective_message.chat_id, text="Random",
                     reply_markup=random_reply_markup(url))


def command_help(bot, update):
    bot.send_message(chat_id=update.effective_message.chat_id, text="Help")


def command_unknown(bot, update):
    bot.send_message(chat_id=update.effective_message.chat_id, text="I couldn't understand that!!\nTry /help")


def query_handler(bot, update):
    query = update.callback_query
    btn = query.data
    if btn == 'random':
        command_random(bot, update)


if __name__ == "__main__":
    TOKEN = '397386217:AAGx3KBG6xzFRg4R_FBZEDQATXjAWJqLy4s'
    # PORT = int(environ.get('PORT', '8443'))

    # Set up the Updater
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    # Handlers
    dp.add_handler(CommandHandler('start', command_start))
    dp.add_handler(CommandHandler('create', command_create))
    dp.add_handler(CommandHandler('reset', command_reset))
    dp.add_handler(CommandHandler('random', command_random))
    dp.add_handler(CommandHandler('help', command_help))
    dp.add_handler(MessageHandler(Filters.text, command_unknown))
    dp.add_handler(CallbackQueryHandler(query_handler))
    # Start the webhook
    # updater.start_webhook(listen="0.0.0.0", port=int(PORT), url_path=TOKEN)
    # updater.bot.setWebhook(f"https://randomovie.herokuapp.com/{TOKEN}")
    updater.start_polling()
    updater.idle()
