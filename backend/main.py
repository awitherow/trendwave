from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import database

from routers import users
from routers import tweets
from routers import twitter_auth


app = FastAPI()
app.include_routers(users.router)  # type: ignore
app.include_routers(tweets.router)  # type: ignore
app.include_routers(twitter_auth.router)  # type: ignore

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
