
from ..database import database
from pydantic import BaseModel
from typing import List
from fastapi import APIRouter
from ..database import tweets


router = APIRouter()


class TweetIn(BaseModel):
    text: str
    approved: bool


class Tweet(BaseModel):
    id: int
    text: str
    approved: bool


@router.get("/tweets/", response_model=List[Tweet])
async def read_tweets():
    query = tweets.select()
    return await database.fetch_all(query)


@router.post("/tweets/", response_model=Tweet)
async def create_tweet(tweet: TweetIn):
    print(tweet)
    query = tweets.insert().values(text=tweet.text, approved=tweet.approved)
    last_record_id = await database.execute(query)
    return {**tweet.dict(), "id": last_record_id}
