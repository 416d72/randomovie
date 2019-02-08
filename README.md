![Randomovie](randomovie/icon/logo.png "Randomovie")

# Introduction

>Ever wanted to watch a movie and needed a suggestion?
You can specify a minimum release year, genres and a minimum IMDB user ratings.
Then you can get a random movie based on your filter any time.

This bot basically provides you the ability to set custom rules then fetch a random movie based on these rules.
It was *inspired* by an obsolete bot called `movie_adviser_bot`, but this one focuses on more simplicity.

# Usage

You can [try](https://t.me/randomovie_bot) this bot now .

Or with directly starting chat with user `@randomovie_bot`

# Known bugs:

- User filter is inconsistent, and user may have to re-create his/her filter after a while [see details](https://github.com/akkk33/randomovie#support-me).
- Suggestion algorithm is a bit primitive, eg.. you may like Action movies but don't like Sci-Fi movies so you select Action from genres and skip Sci-Fi , Current algorithm may suggest you an Action-Sci-Fi movie because it hase at least one genre you set (in this case "Action"). I'm going to fix that in a future update.

# Movie Database:

Movie database was legally fetched from [IMDB](https://www.imdb.com/interfaces/).

There are only two databases used:

- title.basics.tsv.gz
    (Contains the following information for titles):
- title.ratings.tsv.gz (Contains the IMDb rating and votes information for titles)

## Local database:

I made a script `randomovie/data/sqlite_build.py` which automates local movies database building.

## PostgreSQL:

I made a script `randomovie/data/pg_build.py` which automates Postgres users database building.

# Requirements:

- Python >= 3.6
- `python-telegram-bot`

# Developing:

- Create a new bot using [@botfather](https://t.me/botfather).
- Create a new [heroku](https://www.heroku.com/) account or sign in if you have one.
- Install [heroku cli](https://devcenter.heroku.com/articles/heroku-cli)
- Now open your terminal and type:
  - `git clone https://github.com/akkk33/randomovie.git`
  - `cd randomovie/`
  - `pip3 install -r requirements.txt`
  - `heroku login`
  - `heroku create`
  - `heroku git:remote -a <YOUR APP NAME>`
  - `heroku config:set telegram_token=<YOUR TELEGRAM BOT TOKEN>`
  - `heroku addons:create heroku-postgresql:hobby-dev`
  - `git push heroku master`
- Then open a bash shell to your 'dyno' with `heroku run bash`
- The next step before trying the bot is to build the Postgres users database.
- Within your **heroku** bash shell enter.

  - `python3 randomovie/data/pg_build.py`