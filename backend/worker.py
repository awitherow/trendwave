from random import shuffle, randint
from operator import itemgetter

from celery import Celery
from celery.utils.log import get_task_logger
from celery.schedules import crontab
from datetime import timedelta, datetime

from .database import users, tweets, schedule
from .constants import best_times_to_post

# Create the celery app and get the logger
celery_app = Celery('tasks', broker='pyamqp://guest@rabbit//')
logger = get_task_logger(__name__)

app = Celery('tasks')
app.config_from_object('tasks.config', namespace='CELERY')

app.conf.beat_schedule = {
    "trigger-email-notifications": {
        "task": "select users tweets for scheduling",
        "schedule": crontab(minute="0", hour="0", day="*")
    }
}


def get_random_time(start_hour, end_hour):
    start = timedelta(hours=start_hour, minutes=0, seconds=0)
    end = timedelta(hours=end_hour, minutes=0, seconds=0)
    random_seconds = randint(start.total_seconds(),  # type: ignore
                             end.total_seconds())  # type: ignore

    return timedelta(seconds=random_seconds)


@celery_app.task(name="select users tweets for scheduling")
def schedule_tweets_for_users():

    all_users = users.select()
    all_tweets = tweets.select()

    for user in all_users:

        # check if user is authenticated with twitter
        # if not handle w/ email to relink
        # break

        def schedule_tweet(tweet_id):
            curr_day = datetime.now().weekday()
            start, end = itemgetter('start', 'end')(
                best_times_to_post[curr_day])

            schedule.insert().values(time=get_random_time(
                start_hour=start, end_hour=end))

        def check_enabled_category(tweet):
            for category in user.enabled_categories:
                if category in tweet.categories:
                    return True
                else:
                    return False

        enabled_tweets = filter(check_enabled_category, all_tweets)
        shuffle(enabled_tweets)
        del enabled_tweets[user.tweet_limit:]

        for tweet in enabled_tweets:
            schedule_tweet(tweet.id)


@celery_app.task(name="schedule tweet")
def post_tweets(user, tweet):
    # todo: check database for tweets this minute
    # if datetime.now() minutes === tweet.time.minutes() post
