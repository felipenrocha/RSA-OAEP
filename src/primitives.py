#  https://www.inf.pucrs.br/~calazans/graduate/TPVLSI_I/RSA-oaep_spec.pdf

import base64, hashlib, math

def tostr(bs):
    return bs.decode("ascii")
    
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

def mgf1(z, emLen, hash=hashlib.sha1):
    """MGF1 is a Mask Generation Function based on a hash function.

        Inputs  1. Z - seed from which mask is generated, an octet string
                2. emLen -  intended length in octets of the mask, at most 2^32(hLen)
                Output:
                    1. mask -  an octet string of length l; or "mask too long"
    """
#    Steps:

#    1.If l > 2^32(hLen), output "mask too long" and stop.
    hLen = hash().digest_size # size of sha1 hash
    if emLen > pow(2, (32*hLen)):
        raise ValueError("Mask too long")
#    2.Let T  be the empty octet string.
    T = b''
#    3.For counter from 0 to \lceil{l / hLen}\rceil-1, do the following:
    for i in range(0, math.ceil(emLen / hLen)):

#       a.Convert counter to an octet string C of length 4 with the primitive
#           I2OSP: C = I2OSP (counter, 4)
            c =  i2osp(i, 4)
            T += hash(z + c).digest()
#       b.Concatenate the hash of the seed Z and C to the octet string T: T =
#               T || Hash (Z || C)

#    4.Output the leading l octets of T as the octet string mask.
    #  FIRST ONE IS
    return T[:emLen]


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