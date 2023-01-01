import requests
from config import config


def test_get_tweets():
    r = requests.get(f'{config.API_URL}/tweets/')
    assert r.status_code == 200


def test_post_note():
    payload = {"text": "hello world", "approved": False}
    r = requests.post(f'{config.API_URL}/tweets/', json=payload)
    assert r.status_code == 200
