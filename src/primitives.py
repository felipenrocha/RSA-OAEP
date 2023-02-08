#  https://www.inf.pucrs.br/~calazans/graduate/TPVLSI_I/RSA-oaep_spec.pdf

import base64, hashlib, math, random
from decimal import Decimal


def sha256(m):
    """Hasher for our OAEP and Signing function"""
    hasher = hashlib.sha1()
    hasher.update(m)
    return hasher.digest()

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
    return x.to_bytes(l, byteorder='big')
   

def os2ip(X):
    """
    Octet String to Integer positive
    Input: 
        1. X -  octet string to be converted
    Output: 
        1. x  - corresponding nonnegative integer
    """
    return int.from_bytes(X, byteorder='big')

def mgf1(seed, emLen, hash=hashlib.sha256):
    """MGF1 is a Mask Generation Function based on a hash function.

        Inputs  1. Z - seed from which mask is generated, an octet string
                2. emLen -  intended length in octets of the mask, at most 2^32(hLen)
                Output:
                    1. mask -  an octet string of length l; or "mask too long"
    """
    #    Steps:
    # 1  If emLen > 2^{32}*hLen, output mask too long and stop
    hLen = hash().digest_size
    if emLen > pow(2,32) * hLen:
        raise ValueError("mask too long")

    # 2. Let T be the empty octet string
    T = b""
    # 3. For i = 0 to ceiling(emLen/hLen), do
        # 3.1 Convert i to an octet string C of length 4 with the primitive I2OSP:
        # C = I2OSP(i, 4).
        # 3.2 Concatenate the hash of the seed Z and C to the octet string T:
        # T = T + Hash(Z + C)
    for i in range(math.ceil(emLen / hLen)):
        c = i2osp(i, 4)
        hash().update(seed + c)
        T = T + hash().digest()
    assert(len(T) >= emLen)
    #4. Output the leading l octets of T as the octet string mask.
    return T[:emLen]


def xor(x: bytes, y: bytes) -> bytes:
    '''Byte-by-byte XOR of two byte arrays'''
    return bytes(a ^ b for a, b in zip(x, y))

def tobytes(s, encoding="latin-1"):
        """Transform instances of data types to bytes"""
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
    """Encode String to base64"""
    string_bytes = string.encode("ascii")
    base64_bytes = base64.b64encode(string_bytes)
    base64_string = base64_bytes.decode("ascii")
    return base64_string

def fromBase64(string):
    """Decode string from base64 to  normal string"""
    base64_bytes = string.encode("ascii")
    string_bytes = base64.b64decode(base64_bytes)
    string = string_bytes.decode("ascii")
    return string



def BASE64Encode(data, key_type):
    """generate string for key exportion with base64"""
    out = "-----BEGIN " + key_type + "-----\n "
    out += toBase64(str(data))+ "\n"
    out += "-----END "+ key_type + "-----" 
    return out

def BASE64Decoding(data, key_type):
    """generate string of pairs from key exportion"""
    data = data.split("\n")
    data = data[1:-1][0]
    return fromBase64(data)
    


def totuple(text):
    """Convert text into Tuple
        Ex.: "(1,2)" -> (1,2)
    """
    #  remove ( and ):
    text = text[1:-1]
    text = text.split(",")
    return (int(text[0]), int(text[1]))


def tostr(bs):
    """Return a string from a bytestring"""
    return bs.decode("ascii")

    
def mask(message, pub_key):
    """Function that extends zero octets of message until it reaches pub_key.n length"""
    mLen = len(message)
    return b'\x00' * (pub_key._size_in_bytes() - mLen)


def remove_mask(octet_string: bytes):
    """Function that remove zero octets of message"""

    i = 0
    while octet_string[i] == 0:
        i+=1
    return octet_string[i:]

