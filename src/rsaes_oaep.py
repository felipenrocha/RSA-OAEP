
from typing import Callable
from src.primitives import xor,i2osp, os2ip, mask, remove_mask, sha256, mgf1
import os, math,hashlib, random
from src.rsa import RSAKey



# Author: Felipe Nascimento Rocha
# Based on: https://www.inf.pucrs.br/~calazans/graduate/TPVLSI_I/RSA-oaep_spec.pdf
# Brasilia, Brazil, 2023


def basic_encryption(pub_key: RSAKey, M):
    m  =  M.encode("ascii")
    mLen = len(m)
    if mLen > pub_key._size_in_bytes():
        raise ValueError("Message to long")
    
    masked  = mask(m, pub_key)
    new_message = masked+m
    encoded_int = int.from_bytes(new_message, byteorder='big')
    em = rsaep(encoded_int, pub_key)
    return em
  
def basic_decryption(prv_key, C):
    encoded_int = rsadp(c=C, prv_key=prv_key)
    maskSize = prv_key._size_in_bytes()
    decoded_int = encoded_int.to_bytes(length=maskSize, byteorder='big')
    dm = remove_mask(decoded_int)
    return dm.decode('ascii')



# EME- OAEP ENCONDING:

# RSAES - OAEP Encryption process:

# NOT WORKING

def oaep_encrypt(pub_key:RSAKey, M, P = b""):
    """
    RSAES-OAEP-Encrypt((n, e), M, P)
    Input:
        1.  Public Key - (e, n) recipients RSA public key
        2.  M - message to be encrypted, an octet string of length at most k - 2 - 2*hLen, where k is the length in 
        octets of the modulus n and hLen is the length in octets of the hash function output for EME-OAEP.
        3.  P -  encoding parameters, an octet string that may be empty
    Output:
         1. C - ciphertext, an octet string of length k
    Errors: 1. message too long
    Assumption: public key (n, e) is valid
    """
    # steps:

    # 1.Apply the EME-OAEP encoding operation to the message M and the
    # encoding parameters P to produce an encoded message EM of length k - 1 octets:
    # k = the length in octets of the modulus n
    k = pub_key._size_in_bytes()
    EM = oaep_encode(M, k-1, P)
    # 2. Convert the encoded message EM to an integer message representative m
    m = os2ip(EM)
    # 3.Apply the RSAEP encryption primitive to the public key (n, e) 
    # and the message representative m to produce an integer ciphertext representative c:
    c = rsaep(pub_key=pub_key, m=m)
    # 5. Convert the ciphertext representative c to a ciphertext C of length k octet
    C = i2osp(c, k)
    # 5. Output the ciphertext C.
    return C
def oaep_encode(M, emLen, label= b"", hash=sha256, mgf=mgf1):
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
    # (2^61 - 1 octets for SHA-1) then output ‘‘parameter string too long’’ and stop.
    if  len(label) > (pow(2,61) - 1):
        raise ValueError("Parameter String too large")
    
    # 2. let pHash = Hash(P), an octet string of length hLen.
    lHash = hash(label)
    hLen = len(lHash)
    mLen = len(M)    
    # 4. Generate an octet string PS consisting of (emLen − mLen − 2hLen − 1) zero octets. 
    # The length of PS may be 0.
    # PADDING:
    zero_octet = b'\x00'
    PS = zero_octet * (emLen - mLen - 2*hLen - 2)
    # 5. Concatenate lHash, PS, the message M, and other padding to form a data block DB as
    #  DB = lHash + PS + 01 + M.
    DB = lHash + PS + b'\x01' + M
    # 6. Generate a random octet string seed of length hLen.
    seed = os.urandom(hLen)

    # 7. Let dbMask = MGF(seed , emLen − hLen)
    dbMask = mgf(seed, emLen - hLen)
    #8.  Let maskedDB = DB xor dbMask.
    maskedDB = xor(DB, dbMask)
    # 9. Let seedMask = MGF(maskedDB, hLen).
    seedMask = mgf(maskedDB, hLen)
    # 10. Let maskedSeed = seed xor seedMask.
    maskedSeed = xor(seed, seedMask)
    # 11. Let EM = maskedSeed + maskedDB.
    EM = maskedSeed + maskedDB

    # 12. Output EM.

    return EM
def rsaep(m, pub_key: RSAKey):
    """ 
    Rsa encryption process
    Public Key = (e, n)
    """
    # assume pub key is valid in the form (e,n)
    e, n = pub_key.get_key()
    c = pow(m, e, n)
    if c > n - 1 or c < 0:
        raise ValueError("Message representative out of range")
    return c

# RSAES - OAEP Decryption process:

def oaep_decrypt(prv_key:RSAKey, C, P=b""):
    """RSAES-OAEP-Decrypt(K, C, P)
        Inputs: 
            1. K - recipients RSA private key
            2. C - ciphertext to be decrypted, an octet string of length k
            3. P - encoding parameters, an octet string that may be empty

        Output:
            1. M -  message, an octet string of length at most k - 2 - 2hLen, where hLen is the length in octets
            of the hash function output for EME-OAEP
        Errors:
            1. Decryption error
    """
    # steps:
    k = prv_key._size_in_bytes()
    # 1. If the length of the ciphertext C is not k octets, output decryption error and stop.
    cLen = len(C)
    if cLen != k:
        raise ValueError("Decryption error, different number of octets")
    # 2. Convert the ciphertext C to an integer ciphertext representative c
    c = os2ip(C)
    # 3. Apply the RSADP decryption primitive  to the private key K and the ciphertext
    # representative c to produce an integer message representative m:
    m = rsadp(prv_key=prv_key, c=c)
    # 4. Convert the message representative m to an encoded message EM of length k − 1 octets
    EM =i2osp(m, k - 1)
    # 5. Apply the EME-OAEP decoding operation to the encoded message EM and
    # the encoding parameters P to recover a message M:
    M = oaep_decode(EM, P)
    # 6. Output the message M
    return M
def oaep_decode(EM, label = b'', hash=sha256, mgf=mgf1):
        """ EME-OAEP-Decode(EM, P)
        Options: 
            1. Hash - hash function (hLen denotes the length in octets of the hash function output)
            2. MGF - mask generation function
        Input: 
            1. EM - encoded message, an octet string of length at least 2hLen + 1 (emLen denotes the length in
            octets of EM)
            2. P - Encoding parameters, an octet string
        Output:
            1. M - recovered message, an octet string of length at most emLen - 1 - 2hLen

        Errors:
            1. Decoding error
        """
        # steps:
        # 1. If the length of P is greater than the input limitation then output ‘‘decoding error’’ and stop.
        # SHA1: 2^61 - 1
        if len(label) > (pow(2, 61) - 1):
            raise ValueError("Decoding error, parameter too large")
        # 2. If emLen < 2hLen + 1, output ‘‘decoding error’’ and stop.
        emLen = len(EM) 
        lHash = hash(label)
        hLen = len(lHash)
        
        # if emLen < ((2*hLen) + 1):
        #     raise ValueError("Decoding error, parameter too large")
        # 3. Let maskedSeed be the first hLen octets of EM and let maskedDB be the remaining emLen-hLen octets.
        maskedSeed = EM[0:hLen]
        print("Masked seed: ", maskedSeed)
        maskedDB = EM[hLen+1:-1]
        # 4.  Let seedMask = MGF(maskedDB, hLen).
        seedMask =  mgf(maskedDB, hLen)
        # 5. Let seed = maskedSeed xor seedMask.
        seed = xor(maskedSeed,seedMask) 
        # 6. Let dbMask = MGF(seed , emLen - hLen)
        dbMask = mgf(seed, emLen - hLen)
        # 7. Let DB = maskedDB xor dbMask.
        DB = xor(maskedDB, dbMask)
        # 8. Let pHash = Hash(P), an octet string of length hLen.
        print("pHash: ", lHash)
        # 9. Separate DB into an octet string pHash’ || PS || 01 || M
        print("DB: ", DB)
        return DB
def rsadp(c, prv_key: RSAKey) -> int:
    """ 
    Rsa decryption process
    Private Key = (d, n)
    """

    d, n = prv_key.get_key()
    m = pow(c, d, n)
    if m > n - 1 or m < 0:
        raise ValueError("Ciphertext representative out of range")
    return m




