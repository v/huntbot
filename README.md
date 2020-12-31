# Huntbot

A Discord bot that facilitates the solving of MIT Mystery Hunt.

It responds to commands to create channels and spreadsheets when a new puzzle is started.

## Setup 

Tested on `Python 3.8.5`

### Install virtualenv and all required packages

```
pip3 install virtualenv --user
virtualenv ENV
source ENV/bin/activate
pip3 install -r requirements.txt
```

### Create discord bot

1. Follow the [discordpy docs](https://discordpy.readthedocs.io/en/latest/discord.html) to create an application and bot in discord.
1. Make note of the discord bot token, and export it as an environment variable. `export DISCORD_TOKEN=...`.
1. Run hellobot.py to make sure that a basic bot works. `python3 hellobot.py`
1. Typing `$hello` in a channel should make the bot respond with `hello`

![image of bot working](https://s3-us-west-2.amazonaws.com/vaibhav-imgshare/bottest_-_Discord_2020-12-31_11-51-09.jpg)

Close out of `hellobot.py`.

### Set up google drive

1. Enable the [Google Drive API](https://developers.google.com/drive/api/v3/enable-drive-api).
1. Download the credentials and save them as `credentials.json` in the huntbot folder.
1. Create a folder in Google Drive where you want puzzle spreadsheets to be created, 
1. Make note of the Google Drive folder ID and export it as an environment variable. `export HUNT_FOLDER_ID=...`

### Run the bot

1. Set up the local sqlite DB: `python3 models.py`
1. Set up the google drive credentials: `python3 gdrive.py`
1. Start the bot `python3 main.py`

If everything works, you should be able to type commands like:

```
huntbot start Insider Trading
```

and get a response like:
```
Puzzle Insider Trading started
Visit channel #insider-trading
Solve using spreadsheet: https://docs.google.com/spreadsheets/d/somelink/edit
```

![image of bot creating channel & sheet](https://s3-us-west-2.amazonaws.com/vaibhav-imgshare/bottest_-_Discord_2020-12-31_11-59-28.jpg)
