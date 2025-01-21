# Data Conversion & Luhn's Algorithm
import hashlib
import array

h = hashlib.new('sha256')

# done
def int_to_hex(arg):
    print("int to hex", arg)
    ar = array.array('B', arg.to_bytes(4, byteorder='big'))
    h.update(ar)
    hex_string = h.hexdigest() 
    print("result:", hex_string)

# done
def int_to_byte(arg):
    print("int to byte", arg)
    ar = array.array('B', arg.to_bytes(4, byteorder='big')) 
    hex_string = ''.join(format(x, '02x') for x in ar) # 02x is a specificer that converts the integer to a two digit hex string
    print("result:", hex_string)

# wip
def byte_to_int(arg):
    print("byte to int", arg)
    h.update(arg.encode())
    hex_string = h.hexdigest()
    result = int(hex_string, 16)
    print("result:", result)

# def byte_to_hex(arg):
#     print("byte_to_hex", arg)
#     ar = array.array('B', arg.to_bytes(8, byteorder='big')) 
 
# def hex_to_int(arg):

# def hex_to_byte():

def main():
    # int_to_byte(8888)
    # int_to_hex(8888)
    byte_to_int('0123456789abcdef')


if __name__ == "__main__":
    main()