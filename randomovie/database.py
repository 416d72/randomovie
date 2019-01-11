#!usr/bin/env python3
# -*- coding: utf-8; -*-
"""
MIT License
Copyright (c) 2019 Amr Khamis
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
from os import path, environ
import psycopg2
from sqlite3 import connect, Error

data = path.dirname(__file__) + '/data'
database_file = data + '/bot.db'

db_url = environ.get('DATABASE_URL')
if not db_url:
    db_url = "dbname=bot user=postgres"


def user_create(user_id: int):
    """
    Create a new user
    :param user_id:
    :return:
    """
    try:
        con = psycopg2.connect(db_url)
        cursor = con.cursor()
        cursor.execute("INSERT INTO users(uid) VALUES(%s) ON CONFLICT DO NOTHING;", (user_id,))
        con.commit()
        con.close()
    except Error as e:
        return f"SQLite Error: {e}"


def user_has_genres(user_id: int):
    """
    Check if user has any genres set before submitting a new filter
    :param user_id:
    :return:bool
    """
    try:
        con = psycopg2.connect(db_url)
        cursor = con.cursor()
        cursor.execute("SELECT genre_id FROM user_genres WHERE uid = %s ORDER BY RANDOM() LIMIT 1;", (user_id,))
        return cursor.fetchone()[0]
    except Error as e:
        print(e)


def user_update(user_id: int, update_type: str, new_data):
    """
    Update type is like "genre" or "year"
    :param user_id:
    :param update_type:
    :param new_data:
    :return: None
    """
    con = psycopg2.connect(db_url)
    cursor = con.cursor()
    if update_type in ['year', 'rating']:
        # Update the users table
        cursor.execute(f"UPDATE users SET {update_type} = %s WHERE uid = %s;", (new_data, user_id))
    elif update_type == 'genre':  # genre
        # Update the user_genres table
        cursor.execute("INSERT INTO user_genres(uid,genre_id) VALUES(%s,%s);", (user_id, new_data))
    elif update_type == 'all_genres':  # All
        cursor.execute("INSERT INTO user_genres SELECT Null, %s, id FROM genres;", (user_id,))
    con.commit()
    con.close()


def user_get_year_rating(user_id: int):
    """
    Get the last step user was at
    :param user_id:
    :return: str
    """
    con = psycopg2.connect(db_url)
    cursor = con.cursor()
    cursor.execute("SELECT year,rating FROM users WHERE uid = %s", (user_id,))
    return cursor.fetchone()


def user_get_last_step(user_id) -> str:
    """
    Get the last step user was at
    :param user_id:
    :return: str
    """
    con = psycopg2.connect(db_url)
    cursor = con.cursor()
    cursor.execute("SELECT last_step FROM users WHERE uid = %s", (user_id,))
    return cursor.fetchone()[0]


def user_set_last_step(user_id, new_step):
    """
    Set the last step user has just
    :param user_id:
    :param new_step:
    :return: None
    """
    con = psycopg2.connect(db_url)
    cursor = con.cursor()
    cursor.execute("UPDATE users SET last_step= %s WHERE uid = %s", (new_step, user_id))
    con.commit()
    con.close()


def user_reset(user_id):
    """
    Deletes all user's genres
    :param user_id:
    :return: None
    """
    con = psycopg2.connect(db_url)
    cursor = con.cursor()
    cursor.execute('UPDATE users SET rating = null, year = null, last_step = null WHERE uid = %s', (user_id,))
    cursor.execute("DELETE FROM user_genres WHERE user_id = %s", (user_id,))
    con.commit()
    con.close()


def fetch(user_id: int):
    """
    Fetches records from database using provided arguments
    :param user_id:
    :return: list
    """
    try:
        year, rating = user_get_year_rating(user_id)
        random_genre = user_has_genres(user_id)
        if not random_genre:
            return None
        con = connect(database_file)
        cursor = con.cursor()
        cursor.execute("SELECT imdb_id, title,genres,year,rating,votes from movies where imdb_id in "
                       "(select movie_id from movie_genres where genre_id = ?)"
                       "AND movies.rating > ? AND movies.year > ? ORDER BY RANDOM() LIMIT 1",
                       [random_genre, rating, year])
        result = cursor.fetchone()
        if not result:
            return None
        return [f"https://www.imdb.com/title/{result[0]}", *result[1:]]
    except Error as e:
        return f"SQLite Error: {e}"


if __name__ == '__main__':
    print(fetch(1))
    # print(user_has_genres(1))
    # update_user(1, 'genre', 'horror')
    # user_set_last_step(1, None)
    # print(user_get_last_step(1))
