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

import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from os import environ
from flask import Flask, request, abort

# Constants
TOKEN = "397386217:AAGx3KBG6xzFRg4R_FBZEDQATXjAWJqLy4s"
PORT = environ.get('PORT')


def start(bot, update):
    update.effective_message.reply_text("Hi!")


def echo(bot, update):
    update.effective_message.reply_text(update.effective_message.text)


def error(bot, update, error):
    update.effective_message.reply_text('Update "%s" caused error "%s"', update, error)


# Bot
updater = Updater(TOKEN)
dp = updater.dispatcher
# Add handlers

# API
app = Flask(__name__)


@app.route('/hook', methods=['POST'])
def webhook_handler():
    if request.method == "POST":
        # retrieve the message in JSON and then transform it to Telegram object
        dp.add_handler(CommandHandler('start', start))
        dp.add_handler(MessageHandler(Filters.text, echo))
        dp.add_error_handler(error)
    return 'ok'


@app.route('/set_webhook', methods=['GET', '[POST]'])
def set_webhook():
    cmd = updater.bot.setWebhook('https://randomovie.herokuapp.com/hook')
    if cmd:
        return "Success"
    else:
        abort(401)


@app.route('/')
def index():
    abort(403)


if __name__ == '__main__':
    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN)
    updater.bot.setWebhook(f"https://randomovie.herokuapp.com/{TOKEN}")
    updater.idle()
