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
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from os import environ
from flask import Flask, request, abort


def command_start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Hello")


def command_create(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Create..")


def command_reset(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Reset")


def command_random(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Random")


def command_help(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Help")


def command_unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I couldn't understand that!!\nTry /help")


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    abort(403)


if __name__ == "__main__":
    # Set these variable to the appropriate values

    TOKEN = '397386217:AAGx3KBG6xzFRg4R_FBZEDQATXjAWJqLy4s'
    PORT = int(environ.get('PORT', '8443'))

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

    # Start the webhook
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook(f"https://randomovie.herokuapp.com/{TOKEN}")
    updater.idle()
