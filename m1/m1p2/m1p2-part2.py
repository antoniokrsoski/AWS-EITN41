from __future__ import annotations

import hashlib
import math
from dataclasses import dataclass


def read_file(file_path):
    with open(file_path, "r") as f:
        lines = f.readlines()
    i = int(lines[0].strip())
    j = int(lines[1].strip())
    leaves = [line.strip() for line in lines[2:]]
    return i, j, leaves


@dataclass
class Node:
    val: str
    left: Node = None
    right: Node = None
    parent: Node = None
    depth: int = -1

    def copy(self) -> Node:
        if self.left and self.right:
            return Node(
                self.val, self.left.copy(), self.right.copy(), self.parent, self.depth
            )
        return Node(self.val, self.left, self.right, self.depth)


def compute_merkle_root(leaf: str, path: list[str]) -> str:
    current_hash = bytes.fromhex(leaf)
    for node in path:
        direction = node[0]
        sibling_hash = bytes.fromhex(node[1:])
        if direction == "L":
            current_hash = hashlib.sha1(sibling_hash + current_hash).digest()
        elif direction == "R":
            current_hash = hashlib.sha1(current_hash + sibling_hash).digest()
    return current_hash.hex()


def create_tree(leaves: list[str]) -> tuple[Node, list[Node]]:
    if len(leaves) % 2:
        leaves.append(leaves[-1])
    depth = math.ceil(math.log2(len(leaves)))
    leafs = [Node(h, depth=depth) for h in leaves]
    curr = leafs[:]

    for d in range(depth - 1, -1, -1):
        tmp = []
        if len(curr) % 2:
            curr.append(curr[-1].copy())
        for i in range(0, len(curr), 2):
            l, r = curr[i], curr[i + 1]
            n = Node(
                hashlib.sha1(bytes.fromhex(l.val) + bytes.fromhex(r.val)).hexdigest(),
                l,
                r,
                depth=d,
            )
            l.parent = n
            r.parent = n
            tmp.append(n)
        curr = tmp

    return (curr[0], leafs)


def path(n: Node) -> list[str]:
    r = []
    tmp = n.parent
    while tmp != None:
        if tmp.left == n:
            r.append(f"R{tmp.right.val}")
        else:
            r.append(f"L{tmp.left.val}")
        n = tmp
        tmp = tmp.parent
    return r


def main(file_path):
    i, j, leaves = read_file(file_path)
    root, leaf_nodes = create_tree(leaves)
    merkle_path = path(leaf_nodes[i])
    result = merkle_path[-j] + root.val
    print(result)

    leaf = "a4415e3de446f3bf1a9a27db5f994f54e8b74de8"
    m_path = [
        "R8e88f127a85ce720b6cafb1b7ceb57b1c47fd557",
        "L2bd77796f4124c9f4dfd78781660e19df13e8088",
        "L4a173b17b11da98bf1558019865e90e23a12c183",
        "R2ec0c786a0c3bad8904fd97dca9642c4012a1cb3",
        "R519905a731382c6cf3e7b62d52e0f1888a9bcc68",
        "R4b853260a7a038c282cbe146e2bc1413a472bdf9",
        "L813bc004fc4f17233dc697a65c0072c09fe29737",
        "R6795ddb5c1d55faf2e6f5cf3b7df80d7643db179",
        "Rbdf9adcca851173f1b102c96ea953f7f8fa5e024",
        "Raf7f32b6d48cb58c90e7359e8ba198b511c358b4",
    ]

    merkle_root = compute_merkle_root(leaf, m_path)
    print(f"Merkle root: {merkle_root}")


if __name__ == "__main__":
    main("leaves1.txt")
