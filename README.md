# Twitter BOT for ads
![Alt Text](https://github.com/klemonade/nana-love-ads-twitter/blob/master/readme/nana-love-ads.gif?raw=true)
### Set up
- apply for **Twitter Developer Account** (for reason just put educational purpose) read more [here](https://developer.twitter.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api)
- (optional) set up discord webhook. [how](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks)

install dependencies

    pip install -r requirement.txt
edit `.env` file [about twitter env](prerequisite)

    DISCORD_HOOK= (opt if use discord noti version)
    SHIT_HOOK= (opt if none will use discord hook)
	BEARER_TOKEN=
	CONSUMER_KEY=
	CONSUMER_SECRET=
	ACCESS_KEY=
	ACCESS_SECRET=

 
 edit every **TODO** comments if needed
 

    RANDOM_TIME_ENABLED: if want random sleep time before tweet
    ACCOUNT_NAME: twitter account name
    TIME_START: start working hour (in 24)
	TIME_END: end working hour (in 24)
	SLEEP_MINUTES: max sleep time
	TIME_INCLUDED_RATE: rate for tweet message to include time
	URL: tweet with video you want to quote
	BASE_MESSAGE: base message for tweet **can be appeded only**
	EMOJIS: emojis

test run by `python nana_ads_twitter.py`

### Set up cron job
can be set to run periodically via `crontab` [how to install](https://www.digitalocean.com/community/tutorials/how-to-use-cron-to-automate-tasks-ubuntu-1804)

open cron job schedule

    crontab -e
In cron job file, put this at the bottom

    0 * * * * <python env> <script location> (optinal) >> <log file location>
[example on scheduling cronjob](https://crontab.guru/)

### Example output
![Alt Text](https://github.com/klemonade/nana-love-ads-twitter/blob/master/readme/example.png?raw=true)

### Remarks
- account could be marked as bot (since we're actually botting).
- twitter has some hard rate limit which can break the code. read more [here](https://developer.twitter.com/en/docs/twitter-api/tweets/manage-tweets/migrate)
- make sure to keep secrets safe since anyone have these means **they have access to your account**

### Appendix
- [Tweepy](https://github.com/tweepy/tweepy)
- [Twitter Developer Docs](https://developer.twitter.com/en/docs/twitter-api)
- [Nana CGM48 Social](https://nanapenpichaya.vercel.app/social)
- [Nana Love Ads Full version](https://www.tiktok.com/@nana.cgm48official/video/7365116235329195272)