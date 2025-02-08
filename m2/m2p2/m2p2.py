import hashlib
import math

import utils

K = 128
H_LEN = 20
L_HASH = hashlib.sha1("".encode("utf-8")).digest()


def i2osp(x: int, x_len: int) -> bytes:
    if x >= 256 ** x_len:
        raise ValueError("integer too large and stop")

    return x.to_bytes(x_len, byteorder='big')


def xor_bytes(bytes1: bytes, bytes2: bytes) -> bytes:
    return bytes([b1 ^ b2 for b1, b2 in zip(bytes1, bytes2)])


def mgf1(mgf_seed: str, mask_len: int) -> str:
    if mask_len > (2 ** 32) * H_LEN:
        raise ValueError("mask to long")

    t = b""
    iterations = math.ceil(mask_len / H_LEN)
    for counter in range(iterations):
        c = i2osp(counter , 4)
        t += hashlib.sha1(utils.hexaToBytArr(mgf_seed) + c).digest()
    return utils.bytToHexa(t[:mask_len])


def encode(m: str, seed: str) -> str:
    ps = (K - len(utils.hexaToBytArr(m)) - 2 * H_LEN - 2) * b"\x00"

    db = L_HASH + ps + b"\x01" + utils.hexaToBytArr(m)

    db_mask = utils.hexaToBytArr(mgf1(seed, K - H_LEN - 1))
    masked_db = xor_bytes(db, db_mask)
    seed_mask = utils.hexaToBytArr(mgf1(utils.bytToHexa(masked_db), H_LEN))
    masked_seed = xor_bytes(utils.hexaToBytArr(seed), seed_mask)

    return utils.bytToHexa(b"\x00" + masked_seed + masked_db)


def decode(m: str) -> str:
    hm = utils.hexaToBytArr(m)
    masked_seed, masked_db = hm[1:H_LEN + 1], hm[1 + H_LEN:]
    seed_mask = mgf1(utils.bytToHexa(masked_db), H_LEN)
    seed = xor_bytes(masked_seed, utils.hexaToBytArr(seed_mask))
    db_mask = mgf1(utils.bytToHexa(seed), K - H_LEN - 1)
    db = xor_bytes(masked_db, utils.hexaToBytArr(db_mask))
    return utils.bytToHexa(db.split(b"\x01")[-1])


def main() -> None:



    l = 24 
    seed = "46dad84c7fa3460344bda67c31e8f948addb0649f13b7509"
    r = mgf1(seed, l)
    print(r)
    print("--------")
    m = "0d4413b8823db607b594f3d7e86c4db168a4a17eb4fffd97bb71"
    seed = "e1683401d63da920ccced24b47c53cca7479f0ec"
    enc = encode(m, seed)
    print(enc)

    print("--------")
    em = "00581bc2381cf79218566065eb1def452262df368e129de319b5c2bb66e84df6be244fc653a9468c6aafbe715fe366526e9596c452cdf7a42ddcec8d8005724dc7d9450b769aa0fe6f58e8949e503294de3106a7a3b0254eac2b94d245421e610ca70466137c29e7ff5ccd41dda83a44457ea3c820d0f360599833d34ec82e3b"
    dm = decode(em)
    print(dm)


if __name__ == "__main__":
    main()