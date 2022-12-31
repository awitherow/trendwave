import os
import databases
import sqlalchemy as sa

from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

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
    query = tweets.insert().values(text=tweet.text)
    last_record_id = await database.execute(query)
    return {**tweet.dict(), "id": last_record_id}
