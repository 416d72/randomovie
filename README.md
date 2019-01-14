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
I've hosted my bot on a free heroku account which limits users to only 500 maximum.

So if database reached the 500th user, the bot will start deleting users from oldest to newer, You may be deleted some day along with your filter (sorry for that) but this is the best I can do for now ..
I'm unemployed and I can't afford a paid account, so if you like my bot, please consider supporting it via [Patreon](https://www.patreon.com/akkk33) and I'll upgrade heroku's account as soon as I get $7/month, Thank you ❤️

# Thanks to:
- [Free Software Foundation](https://www.fsf.org/)
- [Heroku](https://www.heroku.com)
- [JetBrains](https://www.jetbrains.com/)
- My supporters 💘
- And to anyone contributes to this repository.
