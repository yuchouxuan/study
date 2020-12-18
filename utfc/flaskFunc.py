import sys
import zlib
from flask.sessions import session_json_serializer
from itsdangerous import base64_decode
import ast
import jwt


def CreateJwt(pl, key='', alg='HS256', headers={"alg": "HS256", "typ": "JWT"}):
    return jwt.encode(pl, key, alg, headers=headers).decode()


def Session(payload):
    payload, sig = payload.rsplit(b'.', 1)
    payload, timestamp = payload.rsplit(b'.', 1)

    decompress = False
    if payload.startswith(b'.'):
        payload = payload[1:]
        decompress = True
    try:
        payload = base64_decode(payload)
    except Exception as e:
        raise Exception('Could not base64 decode the payload because of '
                        'an exception')
    if decompress:
        try:
            payload = zlib.decompress(payload)
        except Exception as e:
            raise Exception('Could not zlib decompress the payload before '
                            'decoding the payload')
    return session_json_serializer.loads(payload)


def Cookie(val='', key='', enc=False):
    if sys.version_info[0] < 3:  # < 3.0
        raise Exception('Must be using at least Python 3')
    elif sys.version_info[0] == 3 and sys.version_info[1] < 4:  # >= 3.0 && < 3.4
        from abc import ABCMeta, abstractmethod
    else:  # > 3.4
        from abc import ABC, abstractmethod

    # Lib for argument parsing
    import argparse

    # external Imports
    from flask.sessions import SecureCookieSessionInterface

    class MockApp(object):

        def __init__(self, secret_key):
            self.secret_key = secret_key

    if sys.version_info[0] == 3 and sys.version_info[1] < 4:  # >= 3.0 && < 3.4
        class FSCM(metaclass=ABCMeta):
            def encode(secret_key, session_cookie_structure):
                """ Encode a Flask session cookie """
                try:
                    app = MockApp(secret_key)

                    session_cookie_structure = dict(ast.literal_eval(session_cookie_structure))
                    si = SecureCookieSessionInterface()
                    s = si.get_signing_serializer(app)

                    return s.dumps(session_cookie_structure)
                except Exception as e:
                    return "[Encoding error] {}".format(e)
                    raise e

            def decode(session_cookie_value, secret_key=None):
                """ Decode a Flask cookie  """
                try:
                    if (secret_key == None):
                        compressed = False
                        payload = session_cookie_value

                        if payload.startswith('.'):
                            compressed = True
                            payload = payload[1:]

                        data = payload.split(".")[0]

                        data = base64_decode(data)
                        if compressed:
                            data = zlib.decompress(data)

                        return data
                    else:
                        app = MockApp(secret_key)

                        si = SecureCookieSessionInterface()
                        s = si.get_signing_serializer(app)

                        return s.loads(session_cookie_value)
                except Exception as e:
                    return "[Decoding error] {}".format(e)
                    raise e
    else:  # > 3.4
        class FSCM(ABC):
            def encode(secret_key, session_cookie_structure):
                """ Encode a Flask session cookie """
                try:
                    app = MockApp(secret_key)

                    session_cookie_structure = dict(ast.literal_eval(session_cookie_structure))
                    si = SecureCookieSessionInterface()
                    s = si.get_signing_serializer(app)

                    return s.dumps(session_cookie_structure)
                except Exception as e:
                    return "[Encoding error] {}".format(e)
                    raise e

            def decode(session_cookie_value, secret_key=None):
                """ Decode a Flask cookie  """
                try:
                    if (secret_key == None):
                        compressed = False
                        payload = session_cookie_value

                        if payload.startswith('.'):
                            compressed = True
                            payload = payload[1:]

                        data = payload.split(".")[0]

                        data = base64_decode(data)
                        if compressed:
                            data = zlib.decompress(data)

                        return data
                    else:
                        app = MockApp(secret_key)

                        si = SecureCookieSessionInterface()
                        s = si.get_signing_serializer(app)

                        return s.loads(session_cookie_value)
                except Exception as e:
                    return "[Decoding error] {}".format(e)
                    raise e

    ret = ""
    if (enc):
        ret = FSCM.encode(key, val)
    else:
        if (key == ''):
            ret = FSCM.decode(val)
        else:
            ret = FSCM.decode(val, key)
    return ret;
