import os
import socket

from src.controller.toml import toml
from src.model.package_cryptography import encode

config = toml(f'{os.getcwd()}/config/config.toml')


if __name__ == '__main__':
    print(f'nkrdb@{config.get("version")}::tcp_conn_client | {config.get("build.type")}\n')

    payload = {
        "iss": "KXWNicgJWZg8QfDZeuY59q",
        "sub": "cHRZ3vxzJiZJbm9vPTuZbE",
        "jit": "ZfTCQtiGi4akYG584n2vxZ",
        "type": "POST",
        "collection": "/home/req/locomotiveModels",
        "document": "VaKRmf7kYNW5DfDEJ4N6HL",
        "content": "{\"key\":\"value\"}",
        "iat": 1516239022
    }

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((config.get('database.ip'), config.get('database.port')))
    req = s.send(bytes(encode(payload).encode('utf-8')))
    data = s.recv(1024)
    s.close()
    print(data.decode('utf-8'))
