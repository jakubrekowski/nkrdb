import json
import os
import socket
import uuid

from src.controller.toml import toml
from src.model.package_cryptography import decode
from src.controller.documents_management import Document

config = toml(f'{os.getcwd()}/config/config.toml')


class Request:

    def __init__(self, arr: bytes, conn: socket):
        request = decode(arr.decode('utf-8'))
        # logging.info(f'{request.get("iss")} requested for {request.get("type")}')

        doc = Document(request.get('collection'), request.get('document'), request.get('jit'), str(uuid.uuid4()))

        match request.get('type'):
            case 'GET':
                print('GET:', doc.get())
                conn.sendall(bytes(json.dumps(doc.get()).encode('utf-8')))
            case 'POST':
                print('POST:', doc.post(request.get('content')))
                conn.sendall(bytes(json.dumps(doc.post(request.get('content'))).encode('utf-8')))
            case 'PUT':
                print('PUT:', doc.put(request.get('content')))
                conn.sendall(bytes(json.dumps(doc.put(request.get('content'))).encode('utf-8')))
            case 'DELETE':
                print('DELETE:', doc.delete())
                conn.sendall(bytes(json.dumps(doc.delete()).encode('utf-8')))
            case _:
                print('Token\'s type not matched!')
                conn.sendall(bytes(json.dumps({
                    '_db_status': 'error',
                    '_db_message': 'Token\'s type not matched!'
                }).encode('utf-8')))