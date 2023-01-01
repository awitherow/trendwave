import argparse
import tweepy
import utility.Config as Config
import utility.ErrorResponse as ErrorResponse
from fastapi import APIRouter

from utility.TwitterUtil import TwitterUtil

router = APIRouter()

parser = argparse.ArgumentParser()
parser.add_argument("-host", "--host",
                    help="REST service hostname", default=Config.CONNECT.HOST)
parser.add_argument("-port", "--port",  help="REST service port",
                    default=Config.CONNECT.PORT, type=int)

args = parser.parse_args()
twitter = TwitterUtil(Config.KEYS.TW_API_KEY, Config.KEYS.TW_API_SEC)


@router.get('/twitter/request_token')
def request_token(oauth_callback: str):
    """
    1- Get initial twitter configurations.
       The callback URL should be defined in the Twitter developer app
    :param oauth_callback:
    :return: config dict.
    """
    try:
        return twitter.request_token(oauth_callback)
    except tweepy.TweepError as e:
        print('Twitter Exception: ', e)
        raise ErrorResponse.tw_request_invalid
    except Exception:
        raise ErrorResponse.tw_request_invalid


@router.get('/twitter/access_token')
def access_token(oauth_token: str, oauth_verifier: str):
    """
    2- Access twitter token and return login tokens
    :param oauth_token:
    :param oauth_verifier:
    :return:
    """
    try:
        return twitter.access_token(oauth_token, oauth_verifier)
    except tweepy.TweepError as e:
        print('Twitter Exception: ', e)
        raise ErrorResponse.tw_access_invalid
