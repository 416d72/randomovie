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
database_file = data + '/randomovie.db'


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
