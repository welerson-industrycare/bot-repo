import requests
import json
import base64
from functools import wraps
from django.http import request
from django.conf import settings
from rest_framework import status
from rest_framework import response

from cryptography.fernet import Fernet


def jwt_remote_authentication(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        request_headers = args[1]._request.headers
        if 'Authorization' in request_headers:

            # get authservice url address from settings
            url = settings.USERAUTH_URL

            # remove JWT from token
            token = args[1]._request.headers['Authorization'].replace(
                'JWT ', '')

            payload = {"token": token}
            headers = {"content-type": "application/json",
                       "server-context": 'default'}

            r = requests.post(url, data=json.dumps(payload), headers=headers)

            # get response status code
            if r.status_code != 200:
                return response.Response(status=status.HTTP_401_UNAUTHORIZED)

            # return to view
            return func(* args, **kwargs)
    return wrapper

def extract_work(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        request_headers = args[1]._request.headers

        if 'uw' in request_headers and request_headers._store.get('uw')[1]:
            values = json.loads( request_headers._store.get('uw')[1] )
            # TODO realiza a decriptação do conteúdo
            key = b'G3TCBFKpG83hV3EXD9dgO7Fjo8VtMU1nUvvUQ77sGJ0='
            f = Fernet(key)
            decrypted_message = f.decrypt(bytes(values[0].encode())).decode()
            
            kwargs.update({'user_id': int(values[1]) })
            kwargs.update({'db_key': decrypted_message })
            kwargs.update({'company': int(values[2]) })
        else:
            kwargs.update({'user_id': None })
            kwargs.update({'db_key': None })
            kwargs.update({'company': None })
        return func(*args, **kwargs)
    return wrapper
