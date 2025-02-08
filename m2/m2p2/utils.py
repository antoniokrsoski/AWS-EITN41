from hashlib import sha256

def intToHexa(i: int, len: int = 4) -> str:
    """Convert the int i into a hexadecimal string"""
    return f"{i:0>{len}x}"

def intToBytArr(i: int, len: int = 4) -> bytes:
    """Convert the int i into a byte array of len"""
    return i.to_bytes(len, "big")

def hexaToBytArr(h: str) -> bytes:
    """Convert this hex string h into a byte array"""
    return bytes.fromhex(h)

def bytToInt(b: bytes) -> int:
    """Convert ths bytes b into a integer"""
    return int.from_bytes(b, "big")

def bytToHexa(b: bytes) -> str:
    """Turn the bytes b into a hex string"""
    return b.hex()

def sha(b: bytes) -> bytes:
    """Sha256 the given bytes and return the digest"""
    return sha256(b).digest()

def luhn(n: str) -> bool:
    r = [int(ch) for ch in str(n)][::-1]
    return (sum(r[0::2]) + sum(sum(divmod(d*2,10)) for d in r[1::2])) % 10 == 0

def luhnMissing(n: str) -> str:
    """Get the missing number indicated by a X in the str n using luhn algorithm"""
    for i in range(0, 10):
        if luhn(n.replace("X", f"{i}")):
            return f"{i}"

def readFile(file: str) -> list[str]:
    """Helper to readin all lines from a file (striped)"""
    with open(file, "r") as f:
        return [l.strip() for l in f.readlines()]

def missingNbrFromFile(file: str) -> str:
    return "".join([luhnMissing(n) for n in readFile(file)])
