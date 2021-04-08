import datetime
from pathlib import Path

import json
import jwt
import socket

CONFIG_FILE = 'jwt_config.json'
CONFIG_PATH = f'{str(Path.home())}/.m2ag-labs/secrets'
OPTIONS = {
        'enable': True,
        'secret_key': '',
        'auth_header': 'Authorization',
        'auth_param': 'jwt',
        'auth_error_code': 401,
        'auth_error_thing': {
            "id": "urn:m2ag:security:authorization-required",
            "title": f"{socket.gethostname()} is a secure thing. See https://{socket.gethostname()}.local:8443/auth.html",
            "@context": "https://webthings.io/schemas",
            "description": "Bearer tokens are required for this device",
            "securityDefinitions": {
                "bearer_sc": {
                    "scheme": "bearer",
                    "alg": "HS256",
                    "description": "Security is required for this thing.",
                    "authorization": f"https://{socket.gethostname()}.local:8443/auth.html"
                }
            },
            "security": ["bearer_sc"]
        },
        'jwt_options': {
            'verify_signature': True,
            'verify_exp': False,  # JWTs will never expire for this device if False
            'verify_nbf': False,
            'verify_iat': True,
            'verify_aud': False
        }
    }

# secret key in config
# if file read fails, create a file with a random string in it. (thing uses same file)
# secret can be any string
# enable false will bypass auth checks'''
# TODO: do I need all the config options here?
try:
    with open(f'{str(Path.home())}/.m2ag-labs/secrets/jwt_config.json', 'r') as file:
        opts = json.loads(file.read().replace('\n', ''))
        for i in opts:
            OPTIONS[i] = opts[i]
        del opts  # clean up
except FileNotFoundError:
    import string
    import random
    import socket

    rando = string.ascii_lowercase + string.digits
    OPTIONS['secret_key'] = ''.join(random.choice(rando) for i in range(100))

    with open(f'{str(Path.home())}/.m2ag-labs/secrets/jwt_config.json', 'w') as file:
        file.write(json.dumps(OPTIONS))

AUTH_TTL = 315360000  # 10 years


class Auth:
    """
        Handle to auth method.
        This method aim to provide a new authorization token
        What should the payload be? Just a key for now.
    """

    @staticmethod
    def get_token():
        """
            Encode a new token with JSON Web Token (PyJWT)
        """
        encoded = jwt.encode({
            'context': 'reserved',
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=AUTH_TTL)},
            OPTIONS['secret_key'],
            algorithm='HS256'
        )
        # raspian desktop full -- this returns a buffer and needs to be decoded - currently pyjwt 1.7.0
        # raspian lite -- returns a string -- version pyjwt 2.0.0
        if isinstance(encoded, str):
            return {'token': encoded}
        else:
            return {'token': encoded.decode('ascii')}
