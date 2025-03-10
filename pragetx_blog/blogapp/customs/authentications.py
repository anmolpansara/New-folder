import datetime
import jwt
from django.contrib.auth import get_user_model
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header

User = get_user_model()


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if auth and len(auth) == 2:
            token = auth[1].decode("utf-8")
            print('token: ', token)
            id, fcm_token = decode_access_token(token)
            print('id: ', id)
            print('fcm_token: ', fcm_token)
            try:
                user = User.objects.get(id=id)
                if user.fcm_token != fcm_token:
                    raise exceptions.AuthenticationFailed(
                        {"message": "Multiple Devices Logged in! Please login again."}
                    )
                if not user.is_active:
                    raise exceptions.AuthenticationFailed(
                        {
                            "message": "Your account has been disabled! Please contact the administrator for assistance."
                        }
                    )
                else:
                    return (user, None)
            except Exception:
                # reraise the same exception
                raise exceptions.AuthenticationFailed(
                    {"message": "Unauthenticated User"}
                )
        raise exceptions.AuthenticationFailed({"message": "Unauthenticated User"})


def create_access_token(id, fcm_token):
    return jwt.encode(
        {
            "user_id": id,
            "fcm_token": fcm_token,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=10),
            "iat": datetime.datetime.utcnow(),
        },
        "access_secret",
        algorithm="HS256",
    )


def decode_access_token(token):
    try:
        payload = jwt.decode(token, "access_secret", algorithms="HS256")
        return payload["user_id"], payload["fcm_token"]
    except Exception:
        raise exceptions.AuthenticationFailed("Unauthenticated")


def create_refresh_token(id, fcm_token):
    return jwt.encode(
        {
            "user_id": id,
            "fcm_token": fcm_token,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7),
            "iat": datetime.datetime.utcnow(),
        },
        "refresh_secret",
        algorithm="HS256",
    )


def decode_refresh_token(token):
    try:
        payload = jwt.decode(token, "refresh_secret", algorithms="HS256")
        return payload["user_id"], payload["fcm_token"]
    except Exception:
        raise exceptions.AuthenticationFailed("Unauthenticated")
