from common import EITN41Client
import json
from hashlib import sha256
from datetime import datetime
import urllib.parse

SEED = "beef"


def calc_hash(index, timestamp, data, prevhash, nonce):
    text = f"{index}-{timestamp}-{data}-{prevhash}-{nonce}"
    return sha256(text.encode("utf-8")).hexdigest()


def block(index, timestamp, data, prevhash, nonce, currhash):
    return {
        "block_id": index,
        "time_stamp": timestamp,
        "metadata": data,
        "prev_hash": prevhash,
        "nonce": nonce,
        "curr_hash": currhash,
    }


def mine(block_number, transaction, previous_hash, prefix_zeros, timestamp):
    prefix_str = "0" * prefix_zeros
    nonce = 0
    while True:
        curr_hash = calc_hash(
            block_number,
            timestamp,
            transaction,
            previous_hash,
            nonce,
        )
        if curr_hash.startswith(SEED):
            print("Bitcoin mined with nonce value:", nonce)
            return nonce, curr_hash
        else:
            nonce += 1


host = "igor.eit.lth.se"
client = EITN41Client(host, 6001, "POST", "/M1P3")
seed = "beef"
client.send("generate?seed=" + seed)
response = client.receive()

response_json = json.loads(response)
print(json.dumps(response_json, indent=4))

blockchain = response_json
prefix_zeros = 4

for i in range(2, 5):
    previous_block = blockchain[-1]
    print("Previous block:", previous_block)
    block_number = previous_block["block_id"] + 1
    timestamp = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
    transaction = f"block{block_number}"
    previous_hash = previous_block["curr_hash"]

    nonce, curr_hash = mine(
        block_number, transaction, previous_hash, prefix_zeros, timestamp
    )
    if nonce is not None:
        new_block = block(
            block_number, timestamp, transaction, previous_hash, nonce, curr_hash
        )
        blockchain.append(new_block)
    else:
        print("Mining failed for block", block_number)
        break

print("Final blockchain:", json.dumps(blockchain, indent=4))

chain_json = json.dumps(blockchain)
submit_url = f"http://igor.eit.lth.se:6001/M1P3/submit?seed={seed}"
print("Submission URL:", submit_url)


client.send(f"submit?seed={seed}&chain={chain_json}")
response = client.receive()
print("Submission response:", response)

client.close()
