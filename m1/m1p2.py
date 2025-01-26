# SPV Node

import hashlib


def compute_merkle_root(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

    print("input: \n")
    for line in lines:
        print(line)

    # take out the leaf node, first line in the list
    leaf_node = lines[0].strip()

    # parse each line remaining in the file as the merkle path
    merkle_path = [line.strip() for line in lines[1:]]

    # compute the has of the leaf node that we will concat with
    current_hash = bytes.fromhex(leaf_node)

    for node in merkle_path:
        # extract the first char from the hash to see what sibiling
        direction = node[0]
        # hash everything to the right of the first char
        sibling_hash = bytes.fromhex(node[1:])

        if direction == "L":
            # concat the sibling hash to the left of the curr
            current_hash = hashlib.sha1(sibling_hash + current_hash).digest()
        elif direction == "R":
            # vice versa
            current_hash = hashlib.sha1(current_hash + sibling_hash).digest()

    # return the final after traversing all the nodes
    return current_hash.hex()


file_path = "p2input.txt"
merkle_root = compute_merkle_root(file_path)
print("\nresult:", merkle_root)
