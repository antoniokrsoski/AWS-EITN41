# Part 2 Full node
import hashlib


def merkle_concat(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

    i = int(lines[0].strip())
    j = int(lines[1].strip())
    leaves = [bytes.fromhex(line.strip()) for line in lines[2:]]

    def compute_merkle_root(leaves):
        while len(leaves) > 1:
            if len(leaves) % 2 != 0:
                leaves.append(leaves[-1])
            leaves = [
                hashlib.sha1(leaves[k] + leaves[k + 1]).digest()
                for k in range(0, len(leaves), 2)
            ]
        return leaves[0]

    def get_merkle_path(leaves, index):
        path = []
        while len(leaves) > 1:
            if len(leaves) % 2 != 0:
                leaves.append(leaves[-1])
            new_level = []
            for k in range(0, len(leaves), 2):
                if k == index or k + 1 == index:
                    sibling_index = k + 1 if k == index else k
                    direction = "L" if k == index else "R"
                    path.append(direction + leaves[sibling_index].hex())
                new_level.append(hashlib.sha1(leaves[k] + leaves[k + 1]).digest())
            index //= 2
            leaves = new_level
        return path

    merkle_path = get_merkle_path(leaves, i)
    merkle_root = compute_merkle_root(
        [bytes.fromhex(line.strip()) for line in lines[2:]]
    ).hex()
    merkle_path_node_at_depth_j = merkle_path[j - 1] if j - 1 < len(merkle_path) else ""

    return merkle_path_node_at_depth_j + merkle_root


file_path = "p2-2input.txt"
result = merkle_concat(file_path)
print("\nresult:", result)
