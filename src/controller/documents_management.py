import json
import logging
import os
import shortuuid

from src.controller.toml import toml

config = toml(f'{os.getcwd()}/config/config.toml')


class Document:
    def __init__(self, collection: str, document: str, jit: str, transaction_id: str):
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
                pass
                # TODO: add exception
                # print(f'Collection {collection} now exists')
            logging.info(f'service_account({jit}) sent a request to create new collection named '
                         f'{collection}. Result: SUCCESS!')

        self.document_exists = os.path.isfile(self.document_path)
        self.transaction_id = transaction_id

    def get(self) -> dict:
        if self.document_exists:
            logging.error(f'{self.transaction_id}:GET - The document {self.collection}/'
                          f'{self.document} already exists!')
            return json.load(open(self.document_path, 'r'))
        else:
            logging.error(f'{self.transaction_id}:GET - The document {self.collection}/{self.document} doesn\'t exist!')
            return {
                '_db_status': 'error',
                '_db_message': 'Document doesn\'t exist!'
            }

    def post(self, content: str) -> dict:
        if not self.document_exists:
            open(self.document_path, 'w').write(json.dumps(json.loads(content)))
            logging.error(f'{self.transaction_id}:POST - The document {self.collection}/{self.document} are created!')
            doc = json.load(open(self.document_path, 'r'))
            doc['_key'] = self.document
            return doc
        else:
            logging.error(f'{self.transaction_id}:POST - The document {self.collection}/'
                          f'{self.document} already exists!')
            return {
                '_db_status': 'error',
                '_db_message': 'The document already exists! Wasn\'t that the type of PUT request for an update?'
            }

    def put(self, content: str) -> dict:
        if self.document_exists:
            # TODO: do that
            logging.error(f'{self.transaction_id}:PUT - The request was received, '
                          f'but I still didn\'t write this function')
            return {
                '_db_status': 'info',
                '_db_message': 'I didn\'t write this yet! Please try again later.'
            }
        else:
            logging.error(f'{self.transaction_id}:PUT - The document {self.collection}/{self.document} doesn\'t exist!')
            return {
                '_db_status': 'error',
                '_db_message': 'The document doesn\'t exist! '
                               'Wasn\'t that the type of POST request for creating a new one?'
            }

    def delete(self) -> dict:
        if self.document_exists:
            os.remove(self.document_path)
            logging.error(f'{self.transaction_id}:DELETE - The document {self.collection}/{self.document} was deleted.')
            return {
                '_db_status': 'info',
                '_db_message': 'The document was successfully deleted! '
            }
        else:
            logging.error(f'{self.transaction_id}:DELETE - The document {self.collection}/'
                          f'{self.document} doesn\'t exist!')
            return {
                '_db_status': 'error',
                '_db_message': 'The document doesn\'t exist, so work is done?'
            }
