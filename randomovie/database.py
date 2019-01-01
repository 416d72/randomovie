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
import sqlite3
import os

data = os.path.dirname(__file__) + '/data'
database_file = data + '/bot.db'


def create_user(user_id: int):
    """
    Create a new user
    :param user_id:
    :return:
    """
    try:
        con = sqlite3.connect(database_file)
        cursor = con.cursor()
        cursor.execute("INSERT OR IGNORE INTO `users`(uid) VALUES(?)", [user_id])
        con.commit()
        con.close()
    except sqlite3.Error as e:
        return f"SQLite Error: {e}"


def update_user(user_id: int, update_type: str, new_data):
    """
    Update type is like "genre" or "year"
    :param user_id:
    :param update_type:
    :param new_data:
    :return: None
    """
    con = sqlite3.connect(database_file)
    cursor = con.cursor()
    if update_type in ['year', 'rating']:
        # Update the users table
        cursor.execute(f"UPDATE `users` SET `{update_type}` = ? WHERE uid = ?", [new_data, user_id])
    else:  # genre
        cursor.execute(f"INSERT INTO `user_genres`(`user_id`,`genre_id`) VALUES(?,?))", [user_id, new_data])
    con.commit()
    con.close()


def last_step(user_id) -> str:
    """
    Get the last step user was at
    :param user_id:
    :return: str
    """
    con = sqlite3.connect(database_file)
    cursor = con.cursor()
    cursor.execute("SELECT `last_step` FROM `users` WHERE `uid` = ?", [user_id])
    result = cursor.fetchone()[0]
    con.close()
    return result


def fetch(user_id):
    """
    Fetches records from database using provided arguments
    :param user_id:
    :return: list
    """
    try:
        con = sqlite3.connect(database_file)
        cursor = con.cursor()

        cursor.execute(f"select imdb_id, title,genres,year,rating,votes from movies where imdb_id in "
                       f"(select movie_id from movie_genres where genre_id in "
                       f"(select genre_id from user_genres where user_id = {user_id} order by random())) "
                       f"and movies.rating > (select users.rating from users where uid = {user_id}) "
                       f"and movies.year > (select users.year from users where uid = {user_id}) "
                       f"order by random() limit 1")
        result = cursor.fetchone()
        if not result:
            return None
        return [f"https://www.imdb.com/title/{result[0]}", *result[1:]]
    except sqlite3.Error as e:
        return f"SQLite Error: {e}"


if __name__ == '__main__':
    print(fetch(1))
    print(last_step(1))
