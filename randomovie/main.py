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
from flask import Flask, request
from os import environ

TOKEN = '397386217:AAGx3KBG6xzFRg4R_FBZEDQATXjAWJqLy4s'
PORT = int(environ.get('PORT', '8443'))

app = Flask(__name__)


# handlers
def start(bot, update):
    update.effective_message.reply_text("Hi!")


def echo(bot, update):
    update.effective_message.reply_text(update.effective_message.text)


@app.route('/', methods=['GET'])
def index():
    return "Test"


@app.route(f'/{TOKEN}', methods=['POST'])
def telegram_request():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    # Add handlers
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.text, echo))
    updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
    updater.idle()
