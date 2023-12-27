from imp import cache_from_source
import jwt
import time
from django.core.cache import cache

from askme.settings import CENTRIFUGO_TOKEN_HMAC_SECRET_KEY, CENTRIFUGO_WS_URL, CENTRIFUGO_API_KEY, CENTRIFUGO_API_URL
from app.models import Profile, Tag


def get_centrifugo_data(user_id: int, channel: str):
    return {
        "centrifugo": {
            "token": jwt.encode({"sub": str(user_id), "exp": int(time.time()) + 10*60}, CENTRIFUGO_TOKEN_HMAC_SECRET_KEY, algorithm="HS256"),
            "ws_url": CENTRIFUGO_WS_URL,
            "api_url": CENTRIFUGO_API_URL,
            "api_key": CENTRIFUGO_API_KEY,
            "channel": channel,
        }
    }


def cache_best_members():
    best_members = Profile.objects.best_members(5)
    cache.set('best_members', best_members, (60+60*60))


def get_best_members():
    best_members = cache.get('best_members')
    return {'best_memebers': best_members}


def cache_popular_tags():
    popular_tags = Tag.objects.popular_tags(8)
    cache.set('popular_tags', popular_tags, (60+60*60))


def get_popular_tags():
    popular_tags = cache.get('popular_tags')
    return {'popular_tags': popular_tags}