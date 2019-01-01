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
from sqlite3 import connect, Error
from random import choice
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import TelegramError, ChatAction, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from os import environ
from .database import *

# Constants
default_genres = ['Action', 'Adventure', 'Animation', 'Drama', 'Comedy', 'Documentary', 'Romance', 'Thriller',
                  'Family', 'Crime', 'Horror', 'Music', 'Fantasy', 'Sci-Fi', 'Mystery', 'Biography', 'Sport',
                  'History', 'Musical', 'Western', 'War', 'News']


def random_reply_markup(url):
    button_list = [
        [
            InlineKeyboardButton("Get one more", callback_data="random"),
            InlineKeyboardButton("Watch or Download", url=url),
        ]
    ]
    return InlineKeyboardMarkup(button_list)


def last_command(update, command):
    """
    Insert the last response sent by bot in user's database
    :param update:
    :param command:
    :return: Bool
    """
    con = connect('data/randomovie.db')
    cursor = con.cursor()
    user_id = update.effective_user.id
    cursor.execute(f'UPDATE `users` SET `last_command` = {command} WHERE `uid` = {user_id}')
    con.commit()


def create_markup(genre_index: int):
    button_list = [
        [
            InlineKeyboardButton(f"Yes I like {default_genres[genre_index]}", callback_data=f"genre{genre_index}"),
            InlineKeyboardButton(f"No", callback_data='skip_genre'),
        ],
        [
            InlineKeyboardButton("Add All genres", callback_data='add_all_genres'),
            InlineKeyboardButton("I'm done", callback_data='finish_genres'),
        ]
    ]
    return InlineKeyboardMarkup(button_list)


def command_start(bot, update):
    bot_description = 'This bot was created to provide you a random movie based on your preference including ' \
                      'movie genres, minimum rating and oldest release year.\n' \
                      'You can start creating your own filter using /create \n' \
                      'After you complete setting your filter, you can use /random to get a random movie based ' \
                      'on your preferences\n.' \
                      'Whenever you need help just send /help\n' \
                      'Have fun 😊'
    bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
    bot.send_message(chat_id=update.effective_message.chat_id, parse_mode=ParseMode.MARKDOWN,
                     text=f"Hello *{update.effective_user.full_name}*\n{bot_description}")


def command_create(bot, update):  # Create a new filter starting with oldest year, then minimum rating
    # and finally genres
    con = connect('data/randomovie.db')
    cursor = con.cursor()
    user_id = update.effective_user.id

    con.close()
    bot.send_message(chat_id=update.effective_message.chat_id, text="Great !! Let's create a new filter 😃")
    create_year(bot, update, 'new')


def create_year(bot, update, step: str):
    """
    Prompt the user for setting the oldest release year that he would get movies newer than
    :param bot:
    :param update:
    :param step:
    :return:
    """
    if step == 'new':  # Send a simple message
        bot.send_message(chat_id=update.effective_message.chat_id,
                         text="So what is the minimum release year that all movies I suggest will be newer than?\n "
                              "Type a year in range of 1911 to 2018.",
                         )
    elif step == 'set':  # Verify the received number and take the appropriate response
        pass


def create_rating(bot, update, step: str):
    """
        Prompt the user for setting the oldest release year that he would get movies newer than
        :param bot:
        :param update:
        :param step:
        :return:
        """
    if step == 'new':  # Send a simple message
        bot.send_message(chat_id=update.effective_message.chat_id,
                         text="All movies have a rating between 1-9, Send me a number between those"
                         )
    elif step == 'set':  # Verify the received number and take the appropriate response
        pass


def create_genres(bot, update, query):
    """
    Handles genres creation
    :param bot:
    :param update:
    :param query:
    :return: None
    """
    """
    insert or replace into users() values(coalesce((select id from users_genres where uid = 15 and genre={genre}),
    {genre}));
    """
    if query == 'new':
        bot.send_message(chat_id=update.effective_message.chat_id, text=f"Do you like Action movies ?",
                         reply_markup=create_markup(0))
    elif query == 'skip':  # Just get the next genre
        bot.send_message(chat_id=update.effective_message.chat_id, text=f"Do you like Action movies ?",
                         reply_markup=create_markup(0))
    elif query == 'done':  # Finish the setup wizard
        pass
    else:
        con = connect('data/randomovie.db')
        cursor = con.cursor()
        user_id = update.effective_user.id
        if query == 'append':  # Append the current genre to user's database and Get the next genre and prompt user
            bot.send_message(chat_id=update.effective_message.chat_id, text=f"Do you like Action movies ?",
                             reply_markup=create_markup(0))
        elif query == 'all':  # Update user's genre cell with all default genres
            pass


def command_reset(bot, update):
    con = connect('data/randomovie.db')
    cursor = con.cursor()
    user_id = update.effective_user.id
    cmd = f'UPDATE `users` SET `genres` = Null , `year` = Null ,`rating` = Null WHERE `uid` = {user_id}'
    cursor.execute(cmd)
    con.commit()
    con.close()
    bot.send_message(chat_id=update.effective_message.chat_id, text="Ok .. Your filters have been successfully reset!")


def command_random(bot, update):
    bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
    user_id = update.effective_user.id
    con = connect('data/randomovie.db')
    cursor = con.cursor()
    cmd = f'SELECT movies.imdb_id, movies.title, movies.year, movies.genres, movies.rating FROM `movies` INNER JOIN' \
          f'`users` ON users.uid = {user_id} AND movies.rating > users.rating AND movies.year > users.year ' \
          f'AND movies.genres LIKE users.genres ORDER BY RANDOM() LIMIT 1'
    cursor.execute(f'SELECT `genres`, `rating`, `year` FROM `users` WHERE users.uid = {user_id}')
    preferences = cursor.fetchone()
    if preferences[0]:
        genre = choice(preferences[0].split(',') or None)
        cursor.execute(f"SELECT imdb_id,title,year,genres,rating FROM `movies` WHERE rating > {preferences[1]} AND "
                       f"year > {preferences[2]} AND genres LIKE '%{genre}%' ORDER BY RANDOM() LIMIT 1")
        movie = cursor.fetchone()
        if movie:
            title = f'Download full movie {movie[1]}'.replace(' ', '+')
            url = f"https://www.google.com.eg/search?q={title}"
            msg = f"*Title:* {movie[1]}\n" \
                  f"*Release year:* {movie[2]}\n" \
                  f"*Rating:* {movie[4]}\n" \
                  f"*Genres:* {movie[3]}\n" \
                  f"*IMDB:* https://www.imdb.com/title/{movie[0]}"
            bot.send_message(chat_id=update.effective_message.chat_id, text=msg,
                             reply_markup=random_reply_markup(url), parse_mode=ParseMode.MARKDOWN)
            bot.send_message(chat_id=update.effective_message.chat_id, text="Enjoy 😊")
        else:
            msg = "Oops 😞 I found nothing matches your filter !!\nTry /reset and /create a new filter with " \
                  "more tolerant parameters like more genres, less rating and older release year"
    else:  # User hasn't created his filter yet
        msg = "Look's like you haven't created your filter yet!\nTry /create for creating a new filter"
    bot.send_message(chat_id=update.effective_message.chat_id, text=msg)


def command_help(bot, update):
    help_msg = "Help message"
    bot.send_message(chat_id=update.effective_message.chat_id, text=help_msg)


def non_command_msg(bot, update):
    msg = update.effective_message.text
    if msg.isdigit():  # Check the previous message that was sent by bot
        if 1911 < int(msg) < 2018:  # Minimum release year
            bot.send_message(chat_id=update.effective_message.chat_id,
                             text=f"Great, I'll suggest movies that are newer than {msg}")
            # Initialise the next /create step which is: minimum rating
            create_rating(bot, update, 'new')
        elif 0 < int(msg) < 10:  # Minimum rating
            bot.send_message(chat_id=update.effective_message.chat_id,
                             text=f"Ok, I'll only suggest movies that have a rating more than {msg}/10")
            # Initialise the next /create step which is: genres
            create_genres(bot, update, 'new')
        else:
            unknown_command(bot, update)
    else:
        unknown_command(bot, update)


def unknown_command(bot, update):
    bot.send_message(chat_id=update.effective_message.chat_id,
                     text="Sorry, I couldn't understand that!!\nTry /help")


def query_handler(bot, update):
    query = update.callback_query
    btn = query.data
    if btn == 'random':  # Fetch a new movie
        command_random(bot, update)
    else:
        if btn.startswith('genre'):  # User is creating a new filter
            create_genres(bot, update, 'append')
        elif btn == 'skip_genre':  # get the next genre
            create_genres(bot, update, 'skip')
        elif btn == 'add_all_genres':  # Add all genres
            create_genres(bot, update, 'all')
        elif btn == 'finish_genres':  # User has selected all genres he needs
            create_genres(bot, update, 'done')


if __name__ == "__main__":

    # Secrets
    TOKEN = '397386217:AAGx3KBG6xzFRg4R_FBZEDQATXjAWJqLy4s'
    # PORT = int(environ.get('PORT', '8443'))

    # Telegram connection
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    # Received messages Handlers
    dp.add_handler(CommandHandler('start', command_start))
    dp.add_handler(CommandHandler('create', command_create))
    dp.add_handler(CommandHandler('reset', command_reset))
    dp.add_handler(CommandHandler('random', command_random))
    dp.add_handler(CommandHandler('help', command_help))
    dp.add_handler(MessageHandler(Filters.text, non_command_msg))
    dp.add_handler(CallbackQueryHandler(query_handler))

    # Webhook Initialisation on heroku
    # updater.start_webhook(listen="0.0.0.0", port=int(PORT), url_path=TOKEN)
    # updater.bot.setWebhook(f"https://randomovie.herokuapp.com/{TOKEN}")

    # Simple home server
    updater.start_polling()
    updater.idle()
