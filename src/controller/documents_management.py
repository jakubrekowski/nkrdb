import json
import logging
import os
import shortuuid

from src.controller.toml import toml
from json import JSONDecodeError

config = toml(f'{os.getcwd()}/config/config.toml')


def input_security(string: str) -> bool: return not {'.', '/', '\\', '~'}.isdisjoint(string)


class ProhibitedCharactersInTheRequest(Exception):
    pass


class Document:
    def __init__(self, collection: str, document: str, jit: str, transaction_id: str):

        if input_security(collection) or input_security(document):
            logging.warning(f'{transaction_id}:(400) The symbols from blacklist in request. Rejection.')
            raise ProhibitedCharactersInTheRequest(f'(400) - The symbols from blacklist in request. Rejection.')

        collection_path = f'{config.get("database.dir")}/collections/{collection}'
        self.collection = collection

        if document == '' or document is None:
            self.document = shortuuid.uuid()
        else:
            self.document = document
        self.document_path = f'{collection_path}/{self.document}.json'

        if not os.path.isdir(collection_path):
            os.makedirs(collection_path)
            if os.path.isdir(collection_path):
                logging.info(f'{transaction_id}:(201) A new collection {collection} was successfully created.')
            else:
                logging.info(f'{transaction_id}:(500) The collection {collection} couldn\'t be created.')
                raise Exception(f'The collection {collection} couldn\'t be created in {collection_path}.')

        self.document_exists = os.path.isfile(self.document_path)
        self.transaction_id = transaction_id

    def get(self) -> dict:
        if self.document_exists:
            logging.error(f'{self.transaction_id}:GET(200) - The document {self.collection}/'
                          f'{self.document} already exists.')
            return json.load(open(self.document_path, 'r'))
        else:
            logging.error(f'{self.transaction_id}:GET(404) - The document {self.collection}/'
                          f'{self.document} doesn\'t exist.')
            return {
                '_db_status': 404,
                '_db_message': 'Document doesn\'t exist.'
            }

    def post(self, content: str) -> dict:
        if not self.document_exists:
            open(self.document_path, 'w').write(json.dumps(json.loads(content)))
            logging.error(f'{self.transaction_id}:POST(201) - The document {self.collection}/'
                          f'{self.document} are created.')
            doc = json.load(open(self.document_path, 'r'))
            doc['_key'] = self.document
            return doc
        else:
            logging.error(f'{self.transaction_id}:POST(409) - The document {self.collection}/'
                          f'{self.document} already exists.')
            return {
                '_db_status': 409,
                '_db_message': 'The document already exists. Wasn\'t that the type of PUT request for an update?'
            }

    def put(self, content: str) -> dict:
        if self.document_exists:
            try:
                old = json.loads(open(self.document_path, 'r').read())
                old.update(json.loads(content))
                doc = open(self.document_path, 'w')
                doc.write(json.dumps(old))

                logging.error(f'{self.transaction_id}:PUT(200) -  The document {self.collection}/'
                              f'{self.document} are updated.')
                return old
            except JSONDecodeError:
                logging.error(f'{self.transaction_id}:PUT(501) - The document {self.collection}/'
                              f'{self.document} are damaged.')
                return {
                    '_db_status': 500,
                    '_db_message': 'The document are damaged.'
                }
        else:
            logging.error(f'{self.transaction_id}:PUT(404 - The document {self.collection}/'
                          f'{self.document} doesn\'t exist.')
            return {
                '_db_status': 404,
                '_db_message': 'The document doesn\'t exist. '
                               'Wasn\'t that the type of POST request for creating a new one?'
            }

    def delete(self) -> dict:
        if self.document_exists:
            os.remove(self.document_path)
            logging.error(f'{self.transaction_id}:DELETE(200) - The document {self.collection}/'
                          f'{self.document} was deleted.')
            return {
                '_db_status': 200,
                '_db_message': 'The document was successfully deleted.'
            }
        else:
            logging.error(f'{self.transaction_id}:DELETE(200) - The document {self.collection}/'
                          f'{self.document} doesn\'t exist.')
            return {
                '_db_status': 200,
                '_db_message': 'The document doesn\'t exist, so work is done?'
            }
