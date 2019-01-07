![Randomovie](randomovie/icon/logo.png "Randomovie")
# Introduction
>Ever wanted to watch a movie and needed a suggestion?
You can specify a minimum release year, genres and a minimum IMDB user ratings.
Then you can always get a random movie based on your filter.

This bot basically provides you the ability to set custom rules then fetch a random movie based on these rules.

# Inspired by:
An obselete bot called [@movie_adviser_bot](https://t.me/movie_adviser_bot), but this bot focuses on more simplisity.

# Movie Database:
Movie database was fetched from [IMDB](https://www.imdb.com/interfaces/).

There are only two databases used:
- title.basics.tsv.gz
    (Contains the following information for titles):
- title.ratings.tsv.gz (Contains the IMDb rating and votes information for titles)

# Local database:
I made a script `randomovie/data/build.py` which automates local database building steps.

# Requirements:
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)

# Installation:
- Create a new bot using [@botfather](https://t.me/botfather).
- Create a new [heroku](https://www.heroku.com/) account or sign in if you have one.
- Create a new app.
- Install [heroku cli](https://devcenter.heroku.com/articles/heroku-cli)
- Now open your terminal and type:
    - `git clone https://github.com/akkk33/randomovie.git`
    - `cd randomovie/`
    - `git remote add heroku <YOUR HEROKU APP NAME>`
    - `heroku login`
    - `heroku config:set telegram_token=<YOUR TELEGRAM BOT TOKEN>`
    - `heroku`
    - `git push heroku master`
# Credits:
- [Free Software Foundation](https://www.fsf.org/)
- [Telegram](https://telegram.org/)
- [Heroku](https://www.heroku.com)