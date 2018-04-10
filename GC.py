import hashlib as hasher
import json
import requests
import datetime
from uuid import uuid4
from flask import Flask, jsonify, request
from urllib.parse import urlparse


class Blockchain:
    '''
    Class for creating the block chain and updating the blockchain.
    Removed proof of work. Needs to be validated through the GUI
    '''

    def __init__(self):
        self.chain = []
        self.data = []
        self.nodes = set()
        self.new_block(previous_hash=1)

    def new_block(self, previous_hash=None):
        # Creates a new block to be added to the blockchain
        block = {
            'index': len(self.chain)+1,
            'timestamp': datetime.datetime.now(),
            'data': self.data,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.data = []
        self.chain.append(block)
        return block

    def transaction(self, first_name, surname, serial_no):
        # Adds a transaction that will need to be mined/added
        # TODO: change to match the updated GUI
        self.data.append({
            'first_name': first_name,
            'surname': surname,
            'serial_no': serial_no,
        })
        return self.last_block['index']+1

    def hash(self, block):
        # Hashes the block
        block_string = json.dumps(block, sort_keys=True).encode()
        return hasher.sha256(block_string).hexdigest()

    def last_block(self):
        # Retreives the last block in the chain
        return self.chain[-1]

    def consensus(self):
        nodes = self.nodes
        our_chain = len(self.chain)
        new_chain = []

        for node in nodes:
            other_chain = requests.get('https://{}'.format(node))

            if other_chain.status_code == 200:
                size = other_chain.json()['length']
                chain = other_chain.json()['chain']

                if size > our_chain:
                    our_chain = size
                    new_chain = chain
        if new_chain:
            self.chain = new_chain


'''TODO: add a consensus algorithm'''
# def new_chains():
#     # Retrieves Blockchains from the other registered nodes
#     chains = []
#     for node in nodes:
#         block = request.get(node + "/chain").content
#         block = json.loads(block)
#         chains.append(block)
#     return chains
#
#
# def consensus():
#     # Returns the largest chain out of the returned new chains.
#     chains = new_chains()
#     temp_chain = []
#     if chains:
#         for chain in chains:
#             if len(temp_chain) < len(chain):
#                 temp_chain = chain
#     return temp_chain


# nodes = [
#     "http://localhost:5000"
#     ]

""" FLASK ROUTES USED TO ADD AND RETRIEVE BLOCKS"""
app = Flask(__name__)


@app.route('/add', methods=['GET'])
def add_txion():
    last_block = blockchain.last_block
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(previous_hash)

    return "Block {} createrd".format(block['index'])


@app.route('/new', methods=['POST'])
def new():
    values = request.get_json()

    index = blockchain.transaction(values['first_name'], values['surname'], values['serial_no'])

    message = {'message': 'New transaction successfully added. It will be added to block {index}'}
    return jsonify(message),


@app.route('/chain', methods=['GET'])
def full_chain():
    chain = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(chain)


blockchain = Blockchain()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
