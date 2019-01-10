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

from sqlite3 import connect

db_file = "bot.db"
default_genres = ['Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family',
                  'Fantasy', 'History', 'Horror', 'Music', 'Mystery', 'Romance', 'Sci-Fi', 'Sport', 'Thriller', 'War',
                  'Western']
skipped_genres = ['Adult', 'Film-Noir', 'Short', 'Game-Show', 'Musical', 'News', 'Talk-Show', 'Reality-TV']


def create_db():
    con = connect(db_file)
    cursor = con.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS 'genres' ( `id` INTEGER PRIMARY KEY AUTOINCREMENT, `name` TEXT UNIQUE )")
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS `movie_genres` ( `id` INTEGER PRIMARY KEY AUTOINCREMENT, '
        '`movie_id` INTEGER, `genre_id` INTEGER, FOREIGN KEY(`movie_id`) REFERENCES `movies`(`imdb_id`), '
        'FOREIGN KEY(`genre_id`) REFERENCES `genres`(`id`) )')
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS "movies" ( `id` INTEGER PRIMARY KEY AUTOINCREMENT, `imdb_id` TEXT UNIQUE,'
        ' `title` TEXT, `genres` TEXT, `year` INTEGER ,`rating` INTEGER, `votes` INTEGER)')
    con.commit()
    con.close()


def build_genres():
    con = connect(db_file)
    cursor = con.cursor()
    cursor.execute("PRAGMA synchronous = OFF")
    cursor.execute("BEGIN TRANSACTION")
    for g in default_genres:
        cursor.execute("INSERT INTO `genres`(`name`) VALUES(?)", [g])
    cursor.execute("END TRANSACTION")
    con.commit()
    con.close()


def build_basic():
    con = connect(db_file)
    cursor = con.cursor()
    cursor.execute("PRAGMA synchronous = OFF")
    cursor.execute("BEGIN TRANSACTION")
    with open("imdb_basic.tsv", 'r') as file:
        lines = file.readlines()[1:]
        for line in lines:
            row = line.split('\t')
            """
            imdb_id = row[0]
            title = row[3]
            year = row[5]
            genres = row[-1].replace('\n','').split(',')
            """
            if row[1] == 'movie':
                genres = row[-1].replace('\n', '').replace('\\N', '')
                genres_list = genres.split(',')
                if genres_list[0] and len(row[5]) == 4 and int(row[5]) <= 2018 \
                        and not set(skipped_genres).intersection(genres_list):
                    cursor.execute("INSERT OR IGNORE INTO `movies`(`imdb_id`,`title`,`genres`,`year`) VALUES(?,?,?,?)",
                                   [row[0], row[3], genres, row[5]])
                    for g in genres_list:
                        cursor.execute("INSERT INTO movie_genres(movie_id,genre_id) VALUES(?,(SELECT `id` FROM "
                                       "`genres` WHERE `name` = ?))", [row[0], g])
    cursor.execute("END TRANSACTION")
    con.commit()
    con.close()


def build_ratings():
    con = connect(db_file)
    cursor = con.cursor()
    cursor.execute("PRAGMA synchronous = OFF")
    cursor.execute("BEGIN TRANSACTION")
    with open("imdb_ratings.tsv", 'r') as file:
        lines = file.readlines()[1:]
        for line in lines:
            row = line.split('\t')
            """
            imdb_id = row[0]
            rating = row[1]
            votes = row[2].replace('\n','')
            """
            cursor.execute("UPDATE `movies` SET `rating` = ? , `votes` = ? WHERE `imdb_id` = ?",
                           [row[1], row[2].replace('\n', ''), row[0]])
    cursor.execute("END TRANSACTION")
    con.commit()
    con.close()


def sanitise():
    con = connect(db_file)
    cursor = con.cursor()
    cursor.execute("DELETE FROM `movies` WHERE `rating` IS NULL OR `votes` IS NULL OR `votes` < 500")
    con.commit()
    con.close()


def build_database():
    create_db()
    build_genres()
    build_basic()
    build_ratings()
    sanitise()


def basic_movie(id: str) -> list:
    with open("imdb_basic.tsv", 'r') as file:
        lines = file.readlines()[1:]
        for line in lines:
            row = line.split('\t')
            if row[0] == id:
                genres = row[-1].replace('\n', '').replace('\\N', '').split(',')
                if genres[0]:
                    return row
        return ["Couldn't find a thing"]


if __name__ == '__main__':
    # print(basic_movie('tt7806054'))
    # build_database()
    pass
