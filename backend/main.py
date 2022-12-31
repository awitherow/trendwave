import argparse
import databases
import os
import sqlalchemy as sa
import tweepy
import utility.Config as Config
import utility.ErrorResponse as ErrorResponse
import uvicorn

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from utility.TwitterUtil import TwitterUtil

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

database = databases.Database(DATABASE_URL)
metadata = sa.MetaData()

tweets = sa.Table('tweets',
                  metadata,
                  sa.Column('id', sa.Integer, primary_key=True),
                  sa.Column('text', sa.String),
                  sa.Column('approved', sa.Boolean))

engine = sa.create_engine(DATABASE_URL)


class TweetIn(BaseModel):
    text: str
    approved: bool


class Tweet(BaseModel):
    id: int
    text: str
    approved: bool


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/tweets/", response_model=List[Tweet])
async def read_tweets():
    query = tweets.select()
    return await database.fetch_all(query)


@app.post("/tweets/", response_model=Tweet)
async def create_tweet(tweet: TweetIn):
    print(tweet)
    query = tweets.insert().values(text=tweet.text, approved=tweet.approved)
    last_record_id = await database.execute(query)
    return {**tweet.dict(), "id": last_record_id}


# Twitter Auth API

parser = argparse.ArgumentParser()
parser.add_argument("-host", "--host",
                    help="REST service hostname", default=Config.CONNECT.HOST)
parser.add_argument("-port", "--port",  help="REST service port",
                    default=Config.CONNECT.PORT, type=int)

args = parser.parse_args()
twitter = TwitterUtil(Config.KEYS.TW_API_KEY, Config.KEYS.TW_API_SEC)


@app.get('/twitter/request_token')
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


@app.get('/twitter/access_token')
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
