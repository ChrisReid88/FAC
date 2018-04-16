import hashlib as hasher
import json
import requests
import datetime
from uuid import uuid4
from flask import Flask, jsonify, request
from urllib.parse import urlparse
import pickle
import os.path


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
        dt = str(datetime.datetime.now())
        block = {
            'index': len(self.chain)+1,
            'timestamp': dt,
            'data': self.data,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.data = []
        self.chain.append(block)
        return block

    def transaction(self, licence_no, trans_no, serial_no, firearm_model, store_id, emp_id):
        # Adds a transaction that will need to be mined/added
        # TODO: change to match the updated GUI
        self.data.append({
            'licence_no': licence_no,
            'trans_no': trans_no,
            'serial_no': serial_no,
            'firearm_model': firearm_model,
            'store_id': store_id,
            'emp_id': emp_id,
        })
        return self.last_block['index']+1

    def hash(self, block):
        # Hashes the block
        block_string = json.dumps(block, sort_keys=True).encode()
        return hasher.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        # Retreives the last block in the chain
        return self.chain[-1]

    def consensus(self):
        # Consensus algorithm. compares length of our  chain with all other nodes
        # in the sets chains. Replaces ours with the longest chain.
        nodes = self.nodes
        our_chain = len(self.chain)
        new_chain = []

        for node in nodes:
            other_chain = requests.get('http://{}/chain'.format(node))

            if other_chain.status_code == 200:
                size = other_chain.json()['length']
                chain = other_chain.json()['chain']

                if size > our_chain:
                    our_chain = size
                    new_chain = chain
        if new_chain:
            self.chain = new_chain
            return True
        return False

    def add_node(self, addr):
        # Add the netloc(address and port) to the set.
        url = urlparse(addr)
        self.nodes.add(url.netloc)


def save_blockchain(obj, filename):
    # Stores the blockchain object using pickle
    with open(filename, 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

def load_blockchain(filename):
    with open(filename, 'rb') as input:
        blockchain = pickle.load(input)
    return blockchain

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

@app.route('/new', methods=['POST'])
def new():
    # Create new data that will be added to the blocks/
    values = request.get_json()
    index = blockchain.transaction(values['licence_no'],
                                   values['trans_no'],
                                   values['serial_no'],
                                   values['firearm_model'],
                                   values['store_id'],
                                   values['emp_id'])

    # Add new block to the blockchain.
    last_block = blockchain.last_block
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(previous_hash)
    save_blockchain(blockchain, file_path)

    return "Transaction added to Block {} which has been added to blockchain".format(block['index'])


@app.route('/chain', methods=['GET'])
def full_chain():
    # Return the full blockchain
    chain = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(chain)

@app.route('/node/new', methods=['POST'])
def new_node():
    # Register new nodes in our set/network.
    req = request.get_json()
    nodes = req.get('nodes')
    for node in nodes:
        blockchain.add_node(node)

    resp = {
        'message': "Nodes added",
        'nodes': list(blockchain.nodes),
    }
    return jsonify(resp)

@app.route('/node/consensus',methods=['GET'])
def consensus():
    # Use the consensus algorithm to ensure we have the longest chain.
    updated = blockchain.consensus()
    print(jsonify(blockchain))
    if not updated:
        resp = {
            'message': 'Our chain is up to date.'
        }
    else:
        resp = {
            'message': 'Chain updated'
        }
    return jsonify(resp)

# Get the users file path to their documents folder
file_path = os.path.expanduser('~/Documents/blockchain.pkl')

# Check if the blockchain has been stored. If so, use it as the blockchain
# Else instantiate a new one
if os.path.isfile(file_path):
    blockchain = load_blockchain(file_path)
    print("Blockchain already existed")
else:
    blockchain = Blockchain()
    print("New blockchain created")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
