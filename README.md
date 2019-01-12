![Randomovie](randomovie/icon/logo.png "Randomovie")
# Introduction
>Ever wanted to watch a movie and needed a suggestion?
You can specify a minimum release year, genres and a minimum IMDB user ratings.
Then you can get a random movie based on your filter any time.

This bot basically provides you the ability to set custom rules then fetch a random movie based on these rules.

# Inspired by:
An obsolete bot called [@movie_adviser_bot](https://t.me/movie_adviser_bot), but this bot focuses on more simplicity.

# Usage
Through this [link](https://t.me/randomovie_bot) which opens Telegram on your device.

Or with directly starting chat with user `@randomovie_bot`


# Movie Database:
Movie database was legally fetched from [IMDB](https://www.imdb.com/interfaces/).

There are only two databases used:
- title.basics.tsv.gz
    (Contains the following information for titles):
- title.ratings.tsv.gz (Contains the IMDb rating and votes information for titles)

# Local database:
I made a script `randomovie/data/sqlite_build.py` which automates local database building steps.

# PostgreSQL:
I made a script `randomovie/data/pg_build.py` which automates Postgres database building steps.

# Requirements:
- Python >= 3.6

# Developing:
- Create a new bot using [@botfather](https://t.me/botfather).
- Create a new [heroku](https://www.heroku.com/) account or sign in if you have one.
- Create a new app.
- Install [heroku cli](https://devcenter.heroku.com/articles/heroku-cli)
- Install PostgreSQL with `heroku addons:create heroku-postgresql:hobby-dev`
- Now open your terminal and type:
    - `git clone https://github.com/akkk33/randomovie.git`
    - `cd randomovie/`
    - `pip3 install -r requirements.txt`
    - `heroku login`
    - `heroku create`
    - `heroku git:remote -a <YOUR APP NAME>`
    - `heroku config:set telegram_token=<YOUR TELEGRAM BOT TOKEN>`
    - `git push heroku master`
- Then open a bash shell to your 'dyno' with `heroku run bash`
- The next step before trying the bot is to build the Postgres users database.
- Within your *heroku* bash shell enter.
    - `cd randomovie/data/`
    - `python3 pg_build.py`
Now you're done with installation.

# Support me:
On [Patreon](https://www.patreon.com/akkk33)

# Thanks to:
- [Free Software Foundation](https://www.fsf.org/)
- [Heroku](https://www.heroku.com)
- [JetBrains](https://www.jetbrains.com/)
And to anyone contributes to this repository.