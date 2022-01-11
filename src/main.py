import os
import logging

from controller.toml import toml
from controller.tcp_conn import tcp_conn

config = toml(f'{os.getcwd()}/config/config.toml')


def self_initialization():
    print(f'nkrdb@{config.get("version")}::server | {config.get("build.type")}\n')

    logging.basicConfig(filemode='a',
                        filename='nkrdb.log',
                        format='%(asctime)s:%(msecs)d %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)

    # try:
    tcp_conn()
    # except Exception as e:
    #     print(f'err:\n{e}')


if __name__ == '__main__':
    self_initialization()
