
from constant import (
    RANDOM_TIME_ENABLED,
    ACCOUNT_NAME,
    TIME_START,
    TIME_END,
    SLEEP_MINUTES,
    TIME_INCLUDED_RATE,
    URL,
    BASE_MESSAGES,
    EMOJIS,

)
import traceback
from tweepy import Client
from datetime import datetime
from random import randint
from time import sleep
from discordwebhook import Discord
import os
from dotenv import load_dotenv
import logging

logging.basicConfig(format='[%(asctime)s]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)
load_dotenv()


host = "https://api.twitter.com"
hook = os.getenv("DISCORD_HOOK")

SHIT_HOOK = hook if os.getenv("SHIT_HOOK") is None else os.getenv("SHIT_HOOK")

bearer_token = os.getenv("BEARER_TOKEN")
consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
access_key = os.getenv("ACCESS_KEY")
access_secret = os.getenv("ACCESS_SECRET")


def check_if_current_hour_is_between(current_hour, start_hour, end_hour) -> bool:
    return start_hour <= current_hour < end_hour


def randbool(winrate: int = 50) -> bool:
    return randint(0, 100) < winrate


if __name__ == '__main__':
    discord = Discord(url=hook)

    checked_hour = datetime.now().hour + 1
    if not check_if_current_hour_is_between(checked_hour, TIME_START, TIME_END):
        exit()
    if RANDOM_TIME_ENABLED:
        # Tweet instantly -> wait for x minutes first
        random_sleep = randint(0, SLEEP_MINUTES) * 60
        logging.info('Sleep for %s minutes', SLEEP_MINUTES)
        sleep(random_sleep)
    while True:
        try:

            client = Client(
                consumer_key=consumer_key, consumer_secret=consumer_secret, access_token=access_key, access_token_secret=access_secret)

            tweet_id = 0
            is_failed = False

            for _ in range(10):
                try:
                    now = datetime.now()
                    formatted_time = now.strftime("%H:%M")

                    tweet_text = ""
                    rand_int = 0

                    is_time_included = randbool(TIME_INCLUDED_RATE)

                    if is_time_included:
                        rand_int = randint(1, len(BASE_MESSAGES) - 1)
                    else:
                        rand_int = randint(0, 1)

                    random_section = BASE_MESSAGES[rand_int]
                    random_emoji = EMOJIS[randint(0, len(EMOJIS) - 1)]

                    tweet_text = f'''
                    {random_section} {formatted_time if is_time_included else random_emoji}
                    {URL}
                    '''
                    response = client.create_tweet(text=tweet_text)
                    tweet_id = response.data['id']
                    if _ == 10:
                        is_failed = True
                    break
                except Exception as e:
                    logging.error(f'Error: {e}')
                    sleep(10)
                    pass
            if is_failed:
                logging.error(f'Failed to post tweet. Possibly rate limited')
                discord.post(embeds=[
                    {
                        "title": f"[🚨] Nana's Ads is failed",
                        "description": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    }
                ])

                break
            try:
                logging.info('Tweet is posted')
                discord.post(embeds=[
                    {
                        "title": f"[🪽] Nana's Ads is posted",
                        "description": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    }
                ])
                discord.post(
                    content=f"https://twitter.com/user/status/{tweet_id}")
            except Exception as e:
                date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logging.error(f'Error: {e}')
                discord.post(embeds=[
                    {
                        "title": f"[‼️][TWITTER][BOT][NANA-ADS] Bot is down @{date}",
                        "description": f"```{traceback.format_exc()}```",
                    }
                ])
            break
        except Exception as e:
            discord = Discord(url=SHIT_HOOK)
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logging.error(f'Error: {e}')
            discord.post(embeds=[
                {
                    "title": f"[‼️][TWITTER][BOT][NANA-ADS] Bot is down @{date}",
                    "description": f"```{traceback.format_exc()}```",
                }
            ])
            break
