# Data Conversion & Luhn's Algorithm
import hashlib
import array

# Integer -> hexadecimal
def int_to_hex(arg):
    print("int to hex", arg)
    ar = array.array('B', arg.to_bytes(4, byteorder='big'))
    h = hashlib.new('sha256')
    h.update(ar)
    hex_string = h.hexdigest()
    print("result:", hex_string, "\n")

# integer -> byte
def int_to_byte(arg):
    print("int to byte", arg)
    ar = array.array('B', arg.to_bytes(4, byteorder='big'))
    hex_string = ''.join(format(x, '02x') for x in ar)  # 02x is a specifier that converts the integer to a two-digit hex string
    print("result:", hex_string, "\n")

# hexadecimal string -> int
def byte_to_int(arg):
    print("byte to int", arg)
    ar = array.array('B', bytes.fromhex(arg))
    result = int.from_bytes(ar, byteorder='big')
    print("result:", result, "\n")

def byte_to_hex(arg):
    print("byte_to_hex", arg)
    ar = array.array('B', arg)
    h = hashlib.new('sha256')
    h.update(ar)
    hex_string = h.hexdigest()
    print("result", hex_string, "\n")

def hex_to_int(arg):
    print("hex to int", arg)
    result = int(arg, 16)
    print("result:", result, "\n")

def hex_to_byte(arg):
    print("hex_to_bytes", arg)
    result = bytes.fromhex(arg)
    print("result:", result, "\n")

# this was just in the quiz?
def byte_to_hash_to_int(arg):
    print("byte_to_hash_to_int", arg)
    h = hashlib.new('sha256')
    ar = array.array('B', bytes.fromhex(arg))
    h.update(ar)
    hash_bytes = h.digest()
    result = int.from_bytes(hash_bytes, byteorder='big')
    print("result", result, "\n")

def luhns(card_nbr):
    def luhn_sum(digits):
        sum = 0
        for index, digit in enumerate(reversed(digits)):
            if index % 2 == 0: #even
                sum += digit
            else: 
                doubled = digit * 2
                sum += doubled if doubled < 10 else doubled - 9 # we just count digits not the numbers 
        return sum
    
    x_index = card_nbr.index('X')

    digits = [int(d) if d.isdigit() else 0 for d in card_nbr]

    for x in range(10):
        digits[x_index] = x
        if luhn_sum(digits) % 10 == 0:
            return x

def find_x_in_cards(card_numbers):
    print("luhns algorithm with:\n")
    for i in card_numbers:
        print(i)
    result = ""
    for card_number in card_numbers:
        censored_digit = luhns(card_number)
        result += str(censored_digit)
    print("\nresult:", result, "\n")
    return result

def main():
    # 1 in quiz
    int_to_byte(8888)

    # 2 in quiz
    int_to_hex(8888)

    # 3 in quiz
    byte_to_hash_to_int('0123456789abcdef')

    # 4 in quiz
    byte_to_int('0123456789abcdef')

    # luhns 
    card_numbers = [
        "12774212857X4109",
        "586604X108627571",
        "7473X86953606632",
        "4026467X45830632",
        "20X3092648604969"
    ]
    find_x_in_cards(card_numbers)

if __name__ == "__main__":
    main()