import sys
import json

from sawtooth_sdk.processor.core import TransactionProcessor
from sawtooth_sdk.processor.handler import TransactionHandler

from transaction_family import TransactionPayload, State, InvalidAction, \
    NAMESPACE, NAME, VERSION

import logging

logger = logging.getLogger(__name__)

# Defines a custom transaction handler class that inherits from the TransactionHandler class
class CustomTransactionHandler(TransactionHandler):

    @property
    def family_name(self):
        return NAME

    @property
    def family_versions(self):
        return [VERSION]

    @property
    def namespaces(self):
        return [NAMESPACE]

    # When a new transaction arrives, the Sawtooth processor calls this method method, 
    # which inserts the data type and value extracted from the transaction 
    # into the state of the blockchain for subsequent querying and processing.
    def apply(self, transaction, context):
        logger.error("inside apply")
        header = transaction.header
        signer = header.signer_public_key

        transaction = TransactionPayload.from_bytes(transaction.payload)  # Parsing out the payload of a transaction
        
        if transaction.datatype not in ['hash', 'tuple', 'record']:
            raise InvalidAction(transaction.datatype)  # Checked the data type of the transaction
        
        state = State(context)  # A blockchain state object is created
        val = json.dumps({transaction.datatype: transaction.value})  # Combine the transaction's data type and value into a JSON string
        state.insert(transaction.id, val)  # Inserts the transaction's ID and corresponding value into the blockchain's state


def main():
    processor = TransactionProcessor(url=sys.argv[1])  # Create processor instances
    processor.add_handler(CustomTransactionHandler())
    processor.start()


if __name__ == '__main__':
    logging.basicConfig(filename='example.log',
                        level=logging.DEBUG)
    logger.setLevel(logging.INFO)
    logger.info("hello")
    main()
