import os

from src.controller.toml import toml
from jose import jwt

config = toml(f'{os.getcwd()}/config/config.toml')
__service_account = toml(config.get('service_account.path'))


# TODO: Replace HS256 with RS256

def encode(payload: dict) -> str:
    return jwt.encode(payload, 'kappa', algorithm='HS256')


def decode(token: str) -> dict:
    # TODO: Add error exception with return it
    return jwt.decode(token, 'kappa', algorithms=['HS256'])

# TODO: Save token to logs when the signature is invalid
