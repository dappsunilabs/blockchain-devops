# To run, env FLASK_APP=main.py flask run --port 5001
#curl -F "messageText=help" -X POST  http://localhost:5001/ask
#curl -F "messageText=how many blocks" -X POST  http://localhost:5001/ask

import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4
import os
from datetime import datetime
from blockchain_core import Blockchain
import requests
from flask import Flask, jsonify, request,render_template, request
from flask_cors import CORS

import flask_apscheduler 
from flask_apscheduler import APScheduler
from bot_responder import bot_responder

# Instantiate the Blockchain
blockchain = Blockchain()

#def fill_faucet(a, b):

class Config(object):
    JOBS = [
        {
            'id': 'mining',
            'func': 'main:mining',
            #'args': (1, 2),
            'trigger': 'interval',
            'seconds': 10
        }
    ]

SCHEDULER_API_ENABLED = True
port=5001
API_ENDPOINT= "http://127.0.0.1:"+ str(port)+ "/"
MINE_ENDPOINT= API_ENDPOINT+ "mine"

def mining():

    response=requests.get(MINE_ENDPOINT)
    print('background mining to fill faucet')



# Instantiate the Node
app = Flask(__name__)
CORS(app)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')



def find_filter(blocks, value):
    return filter(lambda s: len(s['transactions'])>1 , blocks) 

@app.route("/")
def hello():
    return render_template('chat.html')


@app.route("/ask", methods=['POST'])
def ask():
    # @chain get stats
    # No of blocks, Total No of transactions, blocks in last hour
    # @
    #message = request.form['messageText'].encode('utf-8').strip()
    question = request.form['messageText'].encode('utf-8').strip()
    question=str(question.decode('utf-8'))
    print("message is x ", question)

    return bot_responder.respond(blockchain,question,API_ENDPOINT)

        
@app.route('/info', methods=['GET'])
def chain_info():
    response = {
        'owner': 'DappsUni',
        'User': 'Nilesh',
    }
    return jsonify(response), 200

@app.route('/mine', methods=['GET'])
def mine():
    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block)

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Mined",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index} after block is mined with /mine'}
    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5001, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.config.from_object(Config())
    app.config['SCHEDULER_TIMEZONE']='utc'
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()


    #In debug mode, Flask's reloader will load the flask app twice, so set use_reloader=False
    app.run(host='0.0.0.0', port=port,use_reloader=False, use_debugger=True, use_evalex=True)
