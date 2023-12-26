import jwt
import time
from askme.settings import CENTRIFUGO_TOKEN_HMAC_SECRET_KEY, CENTRIFUGO_WS_URL

def get_centrifugo_data(user_id: int):
    return {
        "centrifugo": {
            "token": jwt.encode({"sub": str(user_id), "exp": int(time.time()) + 10*60}, CENTRIFUGO_TOKEN_HMAC_SECRET_KEY, algorithm="HS256"),
            "ws_url": CENTRIFUGO_WS_URL,
        }
    }