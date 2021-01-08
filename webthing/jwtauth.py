"""
    JSON Web Token auth for Tornado
    Modified by marc at m2ag-labs (marc@m2ag.net) from files found here:
    https://github.com/paulorodriguesxv/tornado-json-web-token-jwt
    Added configuration from file, errors as dict, added a check for
    websocket upgrade (wss add auth parameter to connect string --
    ?Authorization=Bearer <token>)
"""
import jwt
import json
import socket
from pathlib import Path

AUTHORIZATION_HEADER = 'Authorization'
AUTHORIZATION_PARAM = 'jwt'  # for web socket
AUTHORIZATION_ERROR_MESSAGE = {
        'id': "urn:dev:ops:m2ag-security-required",
        "title": f"{socket.gethostname()} is a secure thing. See https://{socket.gethostname()}.local/auth",
        "@context": "https://iot.mozilla.org/schemas",
        "description": "Bearer tokens are required for this device",
        "securityDefinitions": {
            "nosec_sc": {
                "scheme": "nosec"
            },
            "bearer_sc": {
                "scheme": "bearer",
                "description": "Security is required for this thing.",
                "authorization": f"https://{socket.gethostname()}.local"
            }
        }
    }
AUTHORIZATION_ERROR_CODE = 401
ENABLE = False
SECRET_KEY = ''
CONFIG_PATH = f'{str(Path.home())}/.m2ag-labs/secrets/jwt_secret.json'
# secret can be any string
# enable false will signal the thing to bypass auth checks
# example jwt_secret.json:
'''{"secret": "57%17p}\"7n0<x4d?qn<9ech<qkp*i.hb]>45s3ux=qilds?e2p$fcax\"}<p-0y!4#)osj;v2xr(|ul'2/)<o+65}|h$+!z&a;2^+", 
 "enable": true,
 "auth_thing":{
        "id": "urn:dev:ops:m2ag-security-required",
        "title": "raspib is a secure thing. See https://raspib.local/auth",
        "@context": "https://iot.mozilla.org/schemas",
        "description": "Bearer tokens are required for this device",
        "securityDefinitions": {
            "nosec_sc": {
                "scheme": "nosec"
            },
            "bearer_sc": {
                "scheme": "bearer",
                "description": "Security is required for this thing.",
                "authorization":"https://raspib.local"
            }
        },
        "security": "bearer_sc"
    }
}
 '''
try:
    with open(CONFIG_PATH, 'r') as file:
        opts = json.loads(file.read().replace('\n', ''))
        for i in opts:
            if i == 'secret':
                SECRET_KEY = opts[i]
                continue
            if i == 'enable':
                ENABLE = opts[i]
                continue
            if i == 'auth_thing':
                AUTHORIZATION_ERROR_MESSAGE = opts[i]
                continue
        del opts  # clean up

except FileNotFoundError:
    pass  # go with defaults if no file found -- disable checking.

# TODO: add these to the config file
jwt_options = {
    'verify_signature': True,
    'verify_exp': True,
    'verify_nbf': False,
    'verify_iat': True,
    'verify_aud': False
}


def return_auth_error(handler, message):
    """
        Return authorization error
    """
    handler._transforms = []
    handler.set_status(AUTHORIZATION_ERROR_CODE)
    handler.write(AUTHORIZATION_ERROR_MESSAGE)
    handler.finish()


def return_header_error(handler):
    """
        Returh authorization header error
    """
    return_auth_error(handler, AUTHORIZATION_ERROR_MESSAGE)


def jwtauth(handler_class):
    """
        Tornado JWT Auth Decorator
    """

    def wrap_execute(handler_execute):
        def require_auth(handler):
            # configure the jwt with a config file
            if not ENABLE:
                return True
            auth = handler.request.headers.get(AUTHORIZATION_HEADER)
            if auth:
                parts = auth.split()
                try:
                    jwt.decode(
                        parts[1],
                        SECRET_KEY,
                        algorithms=["HS256"],
                        options=jwt_options
                    )
                except Exception as err:
                    print(str(err))
                    return_auth_error(handler, AUTHORIZATION_ERROR_MESSAGE)

            else:
                # is this websocket upgrade? if so look for auth header in
                # params
                upgrade = handler.request.headers.get("Upgrade")
                if upgrade == 'websocket':
                    # broken up for length issue (flake8)
                    handle = handler.request.query_arguments
                    auth = handle.get(AUTHORIZATION_PARAM)
                    if auth:
                        try:
                            jwt.decode(
                                auth[0].decode('UTF-8'),
                                SECRET_KEY,
                                options=jwt_options
                            )
                        except Exception as err:
                            print(str(err))
                            return_auth_error(handler, AUTHORIZATION_ERROR_MESSAGE)
                            # return_auth_error(handler, str(err))
                        return True

                handler._transforms = []
                handler.write(AUTHORIZATION_ERROR_MESSAGE)
                handler.finish()

            return True

        def _execute(self, transforms, *args, **kwargs):

            try:
                require_auth(self)
            except Exception:
                return False

            return handler_execute(self, transforms, *args, **kwargs)

        return _execute

    handler_class._execute = wrap_execute(handler_class._execute)
    return handler_class
