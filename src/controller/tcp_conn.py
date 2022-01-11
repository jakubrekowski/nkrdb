import os
import socket

from src.controller.toml import toml
from src.model.handle_requests import Request

config = toml(f'{os.getcwd()}/config/config.toml')


def tcp_conn():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((config.get('database.ip'), config.get('database.port')))

    print(f'🚀 handler listening on {config.get("database.ip")}:{config.get("database.port")}!')

    s.listen()
    while True:
        conn, adr = s.accept()

        data = conn.recv(1024)
        if not data:
            continue

        Request(data, conn)
    conn.close()
