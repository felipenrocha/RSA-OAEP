#  https://www.inf.pucrs.br/~calazans/graduate/TPVLSI_I/RSA-oaep_spec.pdf

import base64

def tostr(bs):
    return bs.decode("latin-1")
    
def i2osp(x: int, l: int):
    """
     Integer-to-Octet-String
    Input: 
        1. x -  nonnegative integer to be converted
        2. l  - intended length of the resulting octet string

    Output: 
        1. X - corresponding octet string of length l

    Errors: integer too large
    """

    # 2.  Write the integer x in its unique l-digit representation base 256:
    # 3. Let the octet Xi have the integer value xl−1 for 1 ≤ i ≤ l.
    #  Output the octet string X = X1X2 . . . Xl

    return x.to_bytes(l, byteorder='big')
   


def os2ip(X):
    """
    Input: 
        1. X -  octet string to be converted
    Output: 
        1. x  - corresponding nonnegative integer
    """
    # 1. Let X1X2 . . . Xn be the octets of X from first to last,
    #   and let Xi have the integer value xl−i for 1 ≤ i ≤ l.
    # 2. Let x = x_{l−1}256^(l−1) + x+{l−2}256^(l−2) + . . . + x1256 + x0.
    # 3. output x
    return int.from_bytes(X, byteorder='big')

def xor(x: bytes, y: bytes) -> bytes:
    '''Byte-by-byte XOR of two byte arrays'''
    return bytes(a ^ b for a, b in zip(x, y))

def tobytes(s, encoding="latin-1"):
        if isinstance(s, bytes):
            return s
        elif isinstance(s, bytearray):
            return bytes(s)
        elif isinstance(s,str):
            return s.encode(encoding)
        elif isinstance(s, memoryview):
            return s.tobytes()
        else:
            return bytes([s])


        
def toBase64(string):
    
    string_bytes = string.encode("ascii")
    base64_bytes = base64.b64encode(string_bytes)
    base64_string = base64_bytes.decode("ascii")
    return base64_string

def fromBase64(string):
   
    base64_bytes = string.encode("ascii")
    string_bytes = base64.b64decode(base64_bytes)
    string = string_bytes.decode("ascii")
    return string


# TODO: implement this functions myself
def BASE64Encode(data, key_type):
    out = "-----BEGIN " + key_type + "-----\n "
    out += toBase64(str(data))+ "\n"
    out += "-----END "+ key_type + "-----" 
    return out

def BASE64Decoding(data, key_type):
    data = tostr(data)
    data = data.split("\n")
    data = data[1:-1][0]
    return fromBase64(data)
    


def totuple(text):
    """Convert texting into Tuple"""
    #  remove ( and ):
    text = text[1:-1]
    text = text.split(",")
    return (int(text[0]), int(text[1]))