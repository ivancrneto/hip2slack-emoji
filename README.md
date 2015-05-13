# hit2slack-emoji

![https://img.shields.io/pypi/dm/hip2slack-emoji.svg](https://img.shields.io/pypi/dm/hip2slack-emoji.svg)

Did you migrate from Hipchat to Slack and now miss the funny emojis? Your problems are over!

## Install

1. We use [splinter](http://splinter.readthedocs.org/en/latest/index.html) to make the browser interactions needed to upload the emojis and as we are using only chromedriver for now, you have to first follow [these instructions](http://splinter.readthedocs.org/en/latest/drivers/chrome.html) to setup chromedriver in your machine.
2. Make sure to create and activate a Python 3 virtualenv, then type the following:

``` bash
(venv) $ pip install hip2slack-emoji
```

## Run

You need thre environment variables:
 - __SLACK_TEAM__: your Slack team's name as in https:/<yourteam>.slack.com/
 - __SLACK_EMAIL__: your Slack email
 - __SLACK_PASS__: your Slack password

So you can run by doing this:
``` bash
(venv) $ env SLACK_TEAM=yourslackteam SLACK_EMAIL=your@slack.email SLACK_PASS=yourslackpass catchemall
```
If you want, you can just run:
``` bash
(venv) $ catchemall
```
And you will get an interactive prompt asking for Slack info.

Make sure you have permissions in your team to upload emojis.


Enjoy!
