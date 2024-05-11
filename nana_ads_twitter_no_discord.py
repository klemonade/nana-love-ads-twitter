
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
from tweepy import Client
from datetime import datetime
from random import randint
from time import sleep
import os
from dotenv import load_dotenv

load_dotenv()


host = "https://api.twitter.com"


bearer_token = os.getenv("BEARER_TOKEN")
consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
access_key = os.getenv("ACCESS_KEY")
access_secret = os.getenv("ACCESS_SECRET")

# Note not working across day (just too lazy to debug)


def check_if_current_hour_is_between(current_hour, start_hour, end_hour) -> bool:
    return start_hour <= current_hour < end_hour


def randbool(winrate: int = 50) -> bool:
    return randint(0, 100) < winrate


if __name__ == '__main__':

    checked_hour = datetime.now().hour
    if not check_if_current_hour_is_between(checked_hour, TIME_START, TIME_END):
        exit()
    if RANDOM_TIME_ENABLED:
        # Tweet instantly -> wait for x minutes first
        random_sleep = randint(0, SLEEP_MINUTES) * 60
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
                    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    formatted_time = now.strftime("%H:%M")

                    tweet_text = ""
                    rand_int = 0

                    is_time_included = randbool(TIME_INCLUDED_RATE)

                    if is_time_included:
                        rand_int = randint(0, 1)
                    else:
                        rand_int = randint(1, len(BASE_MESSAGES) - 1)

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
                    print(f'[{date}]: Error: {e}')
                    sleep(10)
                    pass
            if is_failed:
                date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"[{date}]: Failed to post tweet. Possibly rate limited")
                break
            try:
                date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"[{date}]: Tweet is posted")
                print(
                    f"[{date}]: URL: https://twitter.com/{ACCOUNT_NAME}/status/{tweet_id}")
            except Exception as e:
                date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"[{date}]: Error: {e}")
            break
        except Exception as e:
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{date}]: Error: {e}")
            break
