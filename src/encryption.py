
from typing import Callable
import src.primitives as primitives
import os, math,hashlib

def rsaep(m, pub_key):
    """ 
    Rsa encryption process
    Public Key = (e, n)
    """
    # assume pub key is valid in the form (e,n)
    e, n = pub_key
    c = pow(m, e, n)
    if c > n - 1 or c < 0:
        raise ValueError("Message representative out of range")
    return c

#rsa decryption process
def rsadp(c, prv_key):
    """ 
    Rsa decryption process
    Private Key = (d, n)
    """

    d, n = prv_key
    m = pow(c, d, n)
    if m > n - 1 or m < 0:
        raise ValueError("Ciphertext representative out of range")
    return m



def sha3(m: bytes) -> bytes:
    '''SHA-3 hash function'''
    hasher = hashlib.sha1()
    hasher.update(m)
    return hasher.digest()


def mgf(seed: bytes, mlen: int, f_hash: Callable = sha3):
    """MGF function"""
    t = b""
    hlen = len(f_hash(b''))
    for c in range(0, math.ceil(mlen / hlen)):
        _c = primitives.i2osp(c, 4)
        t += f_hash(seed + _c)
    return t[:mlen]




# https://www.inf.pucrs.br/~calazans/graduate/TPVLSI_I/RSA-oaep_spec.pdf
# EME- OAEP ENCONDING:
def oaep_encode(M, emLen, P= b"", hash=sha3, mgf=mgf):
    """
    OAEP encoding operation:

    Inputs:
        - M: message to be encoded, an octet string of length at most (emLen - 1 - 2hLen)
        (mLen denotes the length in octets of the message)  
        - P: Encoding Parameters, an octet string
        -emLen: intended length in octets of the encoded message, at least 2hLen + 1
    Options: 
        - Hash hash function (hLen denotes the length in octets of the hash function output)
        - MGF mask generation function
    Output:
        - EM: encoded message, an octet string of length emLen
    Exceptions:
         -Message too long; Parameter string too long
    """
    # 1. If the length of P is greater than the input limitation for the hash function
    # (2^61 − 1 octets for SHA-1) then output ‘‘parameter string too long’’ and stop.
    if  len(P) > (pow(2,61) - 1):
        raise ValueError("Parameter String too large")
    
    # 2. let pHash = Hash(P), an octet string of length hLen.
    pHash = hash(P)
    hLen = len(pHash)
    print(hLen)
    print(emLen)
    mLen = len(M)    
    # 4. Generate an octet string PS consisting of (emLen − mLen − 2hLen − 1) zero octets. 
    # The length of PS may be 0.
    zero_octet = b'\x00'
    PS = zero_octet * (emLen - mLen - 2*hLen - 1)

    # 5. Concatenate pHash, PS, the message M, and other padding to form a data block DB as
    #  DB = pHash + PS + 01 + M.
    DB = pHash + PS + b'\x01' + M

    # 6. Generate a random octet string seed of length hLen.
    seed = os.urandom(hLen)

    # 7. Let dbMask = MGF(seed , emLen − hLen)
    dbMask = mgf(seed, emLen - hLen)

    #8.  Let maskedDB = DB xor dbMask.
    maskedDB = primitives.xor(DB, dbMask)

    # 9. Let seedMask = MGF(maskedDB, hLen).
    seedMask = mgf(maskedDB, hLen)

    # 10. Let maskedSeed = seed xor seedMask.
    maskedSeed = primitives.xor(seed, seedMask)
    # 11. Let EM = maskedSeed + maskedDB.
    EM = maskedSeed + maskedDB

    # 12. Output EM.

    return EM

def oeaep_decode(EM, k,P= b"", hash=sha3, mgf=mgf):
    """
 

    """
    emLen = len(EM)
    pHash = hash(P)
    hLen = len(pHash)

    _, masked_seed, masked_db = EM[:1], EM[1:1 + hLen], EM[1 + hLen:]
    seed_mask = mgf(masked_db, hLen, hash)
    seed = primitives.xor(masked_seed, seed_mask)
    db_mask = mgf(seed, k - hLen - 1, hash)
    db = primitives.xor(masked_db, db_mask)
    _pHash = db[:hLen]
    assert pHash == _pHash
    i = hLen
    while i < len(db):
        if db[i] == 0:
            i += 1
            continue
        elif db[i] == 1:
            i += 1
            break
        else:
            raise Exception()
    m = db[i:]
    return m


    return M
