import os
import databases
import sqlalchemy as sa
from sqlalchemy import ForeignKey
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]

database = databases.Database(DATABASE_URL)

metadata = sa.MetaData()

tweets = sa.Table('tweets',
                  metadata,
                  sa.Column('id', sa.Integer, primary_key=True),
                  sa.Column('text', sa.String),
                  sa.Column('approved', sa.Boolean))

schedule = sa.Table('schedule',
                    metadata,
                    sa.Column('id', sa.Integer, primary_key=True),
                    sa.Column('time', sa.DateTime),
                    sa.Column('tweet_id', ForeignKey('tweets.id')))

users = sa.Table(
    "users",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("username", sa.String),
    sa.Column("hashed_password", sa.String)
)

engine = sa.create_engine(
    DATABASE_URL
)
