import random
import time
import requests
from hashlib import sha512
import cbor2
from sawtooth_sdk.protobuf.batch_pb2 import BatchHeader, Batch, BatchList
from sawtooth_sdk.protobuf.transaction_pb2 import TransactionHeader, Transaction
from sawtooth_signing import create_context
from sawtooth_signing import CryptoFactory
from transaction_family import generate_address, NAME, VERSION
import secrets

Txn_Numbers = 500
Batches = 10

context = create_context('secp256k1')
private_key = context.new_random_private_key()
signer = CryptoFactory(context).new_signer(private_key)

def createTxns(i):
    txns = []
    address = generate_address(i)

    for _ in range(Txn_Numbers):
       txn_header_bytes = TransactionHeader(
            family_name=NAME,
            family_version=VERSION,
            inputs=[address],
            outputs=[address],
            signer_public_key=signer.get_public_key().as_hex(),
            batcher_public_key=signer.get_public_key().as_hex(),
            dependencies=[],
            payload_sha512=sha512(payload_bytes).hexdigest(),
            nonce=secrets.token_hex(16)
        ).SerializeToString()
        
        signature = signer.sign(txn_header_bytes)
        
        value = [random.getrandbits(256), {
            "MID": random.getrandbits(256),
            "B": random.getrandbits(256)
        }, {
            "Omega": random.getrandbits(256),
            "m": random.getrandbits(256),
            "Id": random.getrandbits(256),
            "Sig": random.getrandbits(256)
        }]
        datatype = ["hash", "tuple", "record"]
        value, datatype = random.choice(list(zip(value, datatype)))
        payload_bytes = cbor2.dumps([datatype, i, value])
        
        txn = Transaction(header=txn_header_bytes,
                          header_signature=signature,
                          payload=payload_bytes)
        txns.append(txn)
    return txns
    

def sendTxns(txns):
    batch_header_bytes = BatchHeader(
        signer_public_key=signer.get_public_key().as_hex(),
        transaction_ids=[txn.header_signature for txn in txns]
    ).SerializeToString()
    
    signature = signer.sign(batch_header_bytes)
    
    batch = Batch(
        header=batch_header_bytes,
        header_signature=signature,
        transactions=txns,
        trace=True
    )

    batch_list_bytes = BatchList(batches=[batch]).SerializeToString()

    resp = requests.post(
        'http://localhost:8008/batches',
        headers={'Content-Type': 'application/octet-stream'},
        data=batch_list_bytes)
        
    if resp.status_code == 202:
        print(len(txns), "Added successfully!")
    else:
        print(resp.status_code)


def main():
    i = 1
    startTime = time.time()
    for i in range(Batches):
        txs = createTxns(i)
        sendTxns(txs)
        time.sleep(3)
    endTime = time.time()
    print(endTime - startTime - 3 * Batches)


if __name__ == '__main__':
    main()
