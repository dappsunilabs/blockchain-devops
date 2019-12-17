import json
from datetime import datetime
from flask import jsonify
import requests

#Main chatbot function, receives input question
class bot_responder:
    def make_data(sender,recipient,amount):
        return {'sender':sender,'recipient': recipient, 'amount': amount }

    def respond(blockchain,question,API_ENDPOINT):
        print([s for s in question.split() if s=='get'])

        #Help
        if (all(x in question for x in ['help'])):
            #response= 'You can ask me questions like:' +'how many block ,' + 'when was last block ,' + 'get chain stats ,' + 'create new transactions "sender " "receiver "' + 'amount ,' + '/chain ,' + '/mine ,'
            help= { "help": "You can ask me questions like: ", "how_many_blocks":"how many blocks? ", "when_was_last_block":"when was last block? ", "get_chain_stats": "get chain stats ", "create_new_transactions": "create new transactions sender receiver amount ","get_chain": "/chain ", "mine":"/mine "}
            return jsonify({'status':'OK','answer':json.dumps({"help":help})})


        #How many blocks on the chain?
        
        #Look for the words in the list [ ] if they match the question
        if (all(x in question for x in ['how', 'many', 'blocks'])):
            print('true it is')
            response = 'There are ' + str(len(blockchain.chain)) + ' blocks on the chain'
            return jsonify({'status':'OK','answer':json.dumps(response)})
        #How when was last block mined?
        if (all(x in question for x in ['when','was', 'last', 'block'])):
            print('true it is')
            last_block=blockchain.chain[len(blockchain.chain)-1]
            timestamp=last_block['timestamp']
            date_time = datetime.fromtimestamp(timestamp)
            response = 'Last block was mined ' + date_time.strftime("%m/%d/%Y, %H:%M:%S")
            return jsonify({'status':'OK','answer':json.dumps(response)})

        if (all(x in question for x in ['get', 'chain', 'stats'])):
            sender_receivers=set()
            total_tx=0
            total_value=0
            total_per_block=0
            value_per_block=[]
            time_block_created=[]
            tx=[]
            for block in blockchain.chain:

                transactions=block['transactions']
                for transaction in transactions:
                    print(transaction)
                    total_tx+=1
                    tx.append(transaction)
                    #response=tx
                    sender_receivers.add(transaction['sender'])
                    sender_receivers.add(transaction['recipient'])
                    total_value = total_value + transaction['amount']
                    total_per_block=total_per_block+ transaction['amount']
                value_per_block.append({str(block['index']):str(total_per_block)} )
                total_per_block=0
            #response = 'There are ' + str(len(blockchain.chain)) + ' blocks on the chain'
            stats= { "total_transactions": total_tx, "number_of_blocks": len(blockchain.chain), "transactions_total_value": total_value}
            return jsonify({'status':'OK','answer':json.dumps({"stats":stats})})

        if (all(x in question for x in ['/chain'])):
            response = requests.get(API_ENDPOINT+"chain")
            print(response.json())
            return jsonify({'status':'OK','answer':json.dumps(response.json())})

        if (all(x in question for x in ['/mine'])):
            response = requests.get(API_ENDPOINT+"mine")
            print(response.json())
            return jsonify({'status':'OK','answer':json.dumps(response.json())})

        if (all(x in question for x in ['/transactions/new'])):
            parameters= question.split()
            print(parameters[1])
            sender= parameters[1]
            recipient = parameters[2]
            amount = int(parameters[3]) 


        if  all(x in question for x in ['create', 'new', 'transactions']): 
            parameters= question.split()
            sender= parameters[3]
            recipient = parameters[4]
            amount = int(parameters[5]) 

        if (all(x in question for x in ['/transactions/new'])) or all(x in question for x in ['new', 'transactions']):

            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json',
            }
            data=json.dumps(bot_responder.make_data(sender,recipient,amount))
            print(data)
            response = requests.post(API_ENDPOINT+ 'transactions/new', headers=headers, data=data)
            print(response.json())
            return jsonify({'status':'OK','answer':json.dumps(response.json())})

        return jsonify({'status':'OK','answer':json.dumps("OK")})