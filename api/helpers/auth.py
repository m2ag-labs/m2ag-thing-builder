import datetime
from pathlib import Path

import json
import jwt

# secret key in config
# if file read fails, create a file with a random string in it. (thing uses same file)
# secret can be any string
# enable false will bypass auth checks'''
try:
    with open(f'{str(Path.home())}/.m2ag-labs/secrets/jwt_secret.json', 'r') as file:
        opts = json.loads(file.read().replace('\n', ''))
        for i in opts:
            if i == 'secret':
                SECRET = opts[i]
except FileNotFoundError:
    import string
    import random
    rando = string.ascii_lowercase + string.punctuation + string.digits
    SECRET = ''.join(random.choice(rando) for i in range(100))
    default = {
        "secret": SECRET,
        "enable": True
    }
    with open(f'{str(Path.home())}/.m2ag-labs/secrets/jwt_secret.json', 'w') as file:
        file.write(json.dumps(default))


AUTH_TTL = 31104000  # this is super long for development


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
            'some': 'payload',
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=AUTH_TTL)},
            SECRET,
            algorithm='HS256'
        )

        return {'token': encoded.decode('ascii')}
