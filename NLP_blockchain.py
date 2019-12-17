#Inspiration for service: https://aleth.io/block/8901150

import hashlib
import json
from time import time

chain = []

for i in range(0,10):
  block = {
              'index': i,
              'timestamp': time(),
              'transactions': " get block "+str(i),
          }

  chain.append(block)
chain=[
    {
      "index": 1, 
      "previous_hash": "1", 
      "proof": 100, 
      "timestamp": 1573188743.440402, 
      "transactions": []
    }, 
    {
      "index": 2, 
      "previous_hash": "d9fbfa4e679bd06d9fdcbeed459fb53e4446c658b1220b54c2515a683461e5a1", 
      "proof": 69658, 
      "timestamp": 1573191294.7991657, 
      "transactions": [
        {
          "amount": 2000, 
          "recipient": "d", 
          "sender": "c"
        }, 
        {
          "amount": 1, 
          "recipient": "e74b729bf1754e588825670e03a5a02d", 
          "sender": "0"
        }
      ]
    }, 
    {
      "index": 3, 
      "previous_hash": "1c61b1bf759278b381e98ca657649e72c7934bb96f13cafbc42a780a797995cf", 
      "proof": 9348, 
      "timestamp": 1573191316.1841822, 
      "transactions": [
        {
          "amount": 2000, 
          "recipient": "d", 
          "sender": "sc"
        }, 
        {
          "amount": 2400, 
          "recipient": "ddd", 
          "sender": "sc"
        }, 
        {
          "amount": 1, 
          "recipient": "e74b729bf1754e588825670e03a5a02d", 
          "sender": "0"
        }
      ]
    }, 
    {
      "index": 4, 
      "previous_hash": "6c2c2e28fe39ceb551167548c240117b097813ed1bc0bf9289a1bf7c32733ee4", 
      "proof": 41265, 
      "timestamp": 1573231943.0867221, 
      "transactions": [
        {
          "amount": 1, 
          "recipient": "e74b729bf1754e588825670e03a5a02d", 
          "sender": "0"
        }
      ]
    }, 
    {
      "index": 5, 
      "previous_hash": "8921295552fb80af2824e028189e522914c3365b4a2a089fd885bb3197ec7b12", 
      "proof": 19343, 
      "timestamp": 1573231943.5458143, 
      "transactions": [
        {
          "amount": 1, 
          "recipient": "e74b729bf1754e588825670e03a5a02d", 
          "sender": "0"
        }
      ]
    }
  ]
#print(chain)
sender=set()
total_value=0
total_per_block=0
value_per_block=[]

for block in chain:
 # print(item['transactions'].split(' '))
 #print(item['transactions'])
  transactions=block['transactions']
  for transaction in transactions:
    #print(transaction['sender'])
    sender.add(transaction['sender'])
    total_value = total_value + transaction['amount']
    total_per_block=total_per_block+ transaction['amount']
  value_per_block.append({str(block['index']):str(total_per_block)} )
print(sender)
print("Total transaction value is " + str(total_value))
print(value_per_block)

test_string= 'get all senders 10 e74b729bf1754e588825670e03a5a02d'
test_string= 'how many total senders'

#x=test_string.split()
#print(x)
print([int(s) for s in test_string.split() if s.isdigit()])
print([s for s in test_string.split() if s=='get'])
print(all(x in test_string for x in ['get', 'sender']))
if (all(x in test_string for x in ['total', 'senders'])):
  print('true it is')

#print(all(x in test_string for x in ['get', 'sender']))


def hash(block):
        """
        Creates a SHA-256 hash of a Block
        :param block: Block
        """

        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

print(chain[2]['previous_hash'])
print(hash(chain[1]))