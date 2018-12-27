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
import random
import os
import json

data = os.path.dirname(__file__) + '/data'
database_file = data + '/movies.db'
imdb_basic = data + "/imdb_basic.tsv"  # Download link: https://datasets.imdbws.com/title.basics.tsv.gz
imdb_ratings = data + "/imdb_ratings.tsv"  # Download link: https://datasets.imdbws.com/title.ratings.tsv.gz


def build_basic():
    """
    Build initial movies database from tsv file provided by IMDB
    :return: int
    """
    try:
        con = sqlite3.connect(database_file)
        cursor = con.cursor()
        cursor.execute("PRAGMA synchronous = OFF")
        cursor.execute("PRAGMA journal_mode = MEMORY")
        cursor.execute("BEGIN TRANSACTION")
        cursor.execute("CREATE TABLE `basic`("
                       "`id` INTEGER PRIMARY KEY AUTOINCREMENT, "
                       "`imdb_id` TEXT,"
                       "`title` TEXT,"
                       "`adult` INT,"
                       "`year` INT,"
                       "`genres` TEXT"
                       ")")
        with open(imdb_basic, 'r') as file:
            basic = [x.split('\t') for x in file.readlines()[1:]]
        for item in basic:
            if item[1] == 'movie':
                cursor.execute("INSERT INTO `basic` (`imdb_id`,`title`,`adult`,`year`,`genres`) "
                               "VALUES (?,?,?,?,?)", [item[0], item[2], item[4], item[5], item[8]])
        cursor.execute('END TRANSACTION')
        con.commit()
        con.close()
        return 1
    except sqlite3.Error as e:
        return f"SQLite error: {e}"


def build_ratings():
    """
    Build initial ratings database from tsv file provided by IMDB
    :return: int
    """
    try:
        con = sqlite3.connect(database_file)
        cursor = con.cursor()
        cursor.execute("PRAGMA synchronous = OFF")
        cursor.execute("PRAGMA journal_mode = MEMORY")
        cursor.execute("BEGIN TRANSACTION")
        cursor.execute("CREATE TABLE `ratings`("
                       "`id` INTEGER PRIMARY KEY AUTOINCREMENT, "
                       "`imdb_id` TEXT,"
                       "`rating` REAL,"
                       "`votes` INTEGER"
                       ")")
        with open(imdb_ratings, 'r') as file:
            ratings = [x.split('\t') for x in file.readlines()[1:]]
        for item in ratings:
            cursor.execute("INSERT INTO `ratings` (`imdb_id`,`rating`,`votes`) VALUES (?,?,?)",
                           [item[0], item[1], item[2]])
        cursor.execute('END TRANSACTION')
        con.commit()
        con.close()
        return 1
    except sqlite3.Error as e:
        return f"SQLite error: {e}"


def merge_tables():
    """
    Build initial movies database from tsv file provided by IMDB
    :return: int
    """
    try:
        con = sqlite3.connect(database_file)
        cursor = con.cursor()
        cursor.execute("PRAGMA synchronous = OFF")
        cursor.execute("PRAGMA journal_mode = MEMORY")
        cursor.execute("BEGIN TRANSACTION")
        cursor.execute("CREATE TABLE `movies`("
                       "`id` INTEGER PRIMARY KEY AUTOINCREMENT, "
                       "`imdb_id` TEXT,"
                       "`title` TEXT,"
                       "`year` TEXT,"
                       "`genres` TEXT,"
                       "`rating` TEXT,"
                       "`votes` TEXT"
                       ")")
        cursor.execute("INSERT INTO `movies`(`imdb_id`,`title`,`year`,`genres`,`rating`,`votes`) "
                       "SELECT basic.imdb_id,`title`,`year`,`genres`,`rating`,`votes` FROM `basic` INNER JOIN "
                       "`ratings` ON ratings.imdb_id = basic.imdb_id WHERE ratings.votes > 999 AND basic.adult = 0")
        cursor.execute('END TRANSACTION')
        con.commit()
        con.close()
        return 1
    except sqlite3.Error as e:
        return f"SQLite error: {e}"


def build_all():
    """
    Automate building database
    :return: int
    """
    try:
        os.remove(database_file)
    except FileNotFoundError:
        print("File doesn't exists")
    finally:
        build_basic()
        build_ratings()
        merge_tables()
        con = sqlite3.connect(database_file)
        cursor = con.cursor()
        cursor.execute("DROP TABLE `basic`")
        cursor.execute("DROP TABLE `ratings`")
        con.commit()
        con.close()
        return 1


def fetch(year: int = 1800, genres: list = None, rating: float = 0):
    """
    Fetches records from database using provided arguments
    :param year:
    :param genres:
    :param rating:
    :return: list
    """
    try:
        if not genres:
            genres = ['Action', 'Adventure', 'Animation', 'Drama', 'Comedy', 'Documentary', 'Romance', 'Thriller',
                      'Family', 'Crime', 'Horror', 'Music', 'Fantasy', 'Sci-Fi', 'Mystery', 'Biography', 'Sport',
                      'History', 'Musical', 'Western', 'War', 'News']
        selected_genre = random.choice(genres)
        con = sqlite3.connect(database_file)
        cursor = con.cursor()
        cursor.execute(f"SELECT `imdb_id`,`title`,`year`, `rating`,`genres` FROM `movies` WHERE "
                       f"`year` >= ? "
                       f"AND `rating` >= ? "
                       f"AND `genres` LIKE ? "
                       f"ORDER BY RANDOM() "
                       f"LIMIT 1"
                       , [year, rating, f"%{selected_genre}%"])
        fetched = cursor.fetchone()
        return [f'https://www.imdb.com/title/{fetched[0]}', fetched[3], fetched[4].replace('\n', '')]
    except sqlite3.Error as e:
        return f"SQLite Error: {e}"


if __name__ == '__main__':
    print(fetch())
