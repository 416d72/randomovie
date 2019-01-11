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
from os import environ
from sqlite_build import default_genres
import psycopg2

db_url = environ.get('DATABASE_URL')
if not db_url:
    db_url = "dbname=users user=postgres"


def create_users():
    con = psycopg2.connect(db_url)
    cursor = con.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS genres (id SERIAL PRIMARY KEY , genre TEXT UNIQUE);')
    cursor.execute('CREATE TABLE IF NOT EXISTS users (uid INTEGER PRIMARY KEY ,year SMALLINT, rating SMALLINT, '
                   'last_step TEXT);')
    cursor.execute('CREATE TABLE IF NOT EXISTS user_genres (id SERIAL PRIMARY KEY ,uid INTEGER REFERENCES users(uid), '
                   'genre_id SMALLINT REFERENCES genres (id));')
    con.commit()
    con.close()


def test_insert():
    """
    Insert a test row
    :return:
    """
    con = psycopg2.connect(db_url)
    cursor = con.cursor()
    cursor.execute('INSERT INTO users (uid, year,rating,last_step) VALUES (%s,%s,%s,%s);', (1, 1993, 7, 'test'))
    con.commit()
    con.close()


if __name__ == '__main__':
    create_users()
    test_insert()
