import logging
import os
from typing import Set

from src.controller.toml import toml
from jose import jwt

config = toml(f'{os.getcwd()}/config/config.toml')
__service_account = toml(config.get('service_account.path'))


# TODO: Replace HS256 with RS256

def encode(payload: dict) -> str:
    return jwt.encode(payload, 'kappa', algorithm='HS256')


def decode(token: str) -> dict:
    try:
        return jwt.decode(token, 'kappa', algorithms=['HS256'])
    except jwt.JWTError as e:
        logging.warning(f'PACKAGE_CRYPTOGRAPHY:(401) {e} token({token})')
        return {
            '_db_status': 403,
            '_db_message': str(e)
        }
