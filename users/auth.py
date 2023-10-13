import datetime
import jwt
from django.conf import settings
import pytz

IST = pytz.timezone('Asia/Kolkata')

def generate_access_token(user):

    access_token_payload = {
        'user_id': user.id,
        'exp': datetime.datetime.now(IST) + datetime.timedelta(days=0, minutes=15),
        'iat': datetime.datetime.now(IST),
    }
    access_token = jwt.encode(access_token_payload,
                              settings.SECRET_KEY, algorithm='HS256')
    return access_token , access_token_payload['exp']


def generate_refresh_token(user):
    refresh_token_payload = {
        'user_id': user.id,
        'exp': datetime.datetime.now(IST) + datetime.timedelta(hours=5),
        'iat': datetime.datetime.now(IST)
    }
    refresh_token = jwt.encode(
        refresh_token_payload, settings.SECRET_KEY, algorithm='HS256')

    return refresh_token