import json
import os
import socket
import uuid

from src.controller.toml import toml
from src.model.package_cryptography import decode
from src.controller.documents_management import Document, ProhibitedCharactersInTheRequest

config = toml(f'{os.getcwd()}/config/config.toml')


class Request:

    def __init__(self, arr: bytes, conn: socket):
        request = decode(arr.decode('utf-8'))

        if request.get('_db_status') == 403:
            conn.sendall(json.dumps(request).encode('utf-8'))
            return

        try:
            doc = Document(request.get('collection'), request.get('document'), request.get('jit'), str(uuid.uuid4()))

            match request.get('type'):
                case 'GET':
                    print('GET:', doc.get())
                    conn.sendall(json.dumps(doc.get()).encode('utf-8'))
                case 'POST':
                    print('POST:', doc.post(request.get('content')))
                    conn.sendall(json.dumps(doc.post(request.get('content'))).encode('utf-8'))
                case 'PUT':
                    print('PUT:', doc.put(request.get('content')))
                    conn.sendall(json.dumps(doc.put(request.get('content'))).encode('utf-8'))
                case 'DELETE':
                    print('DELETE:', doc.delete())
                    conn.sendall(json.dumps(doc.delete()).encode('utf-8'))
                case _:
                    print(f'{request.get("type")}: The request type not matched.')
                    conn.sendall(json.dumps({
                        '_db_status': 405,
                        '_db_message': 'The request type not matched.'
                    }).encode('utf-8'))
        except ProhibitedCharactersInTheRequest:
            print('SECURITY: Prohibited characters in the request.')
            conn.sendall(json.dumps({
                '_db_status': 400,
                '_db_message': 'Prohibited characters in the request.'
            }).encode('utf-8'))
