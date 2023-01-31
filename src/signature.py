from src.rsa import RSAKey
from hashlib import sha512
import base64
from src.primitives import tobytes
# https://cryptobook.nakov.com/digital-signatures/rsa-sign-verify-examples



def sign(message, private_key: RSAKey) -> int:
    """Returns a signature of the message with the privat key"""
    message = message.encode('ascii')
    hash = int.from_bytes(sha512(message).digest(), byteorder='big')
    signature = pow(hash, private_key.d, private_key.n)
    return signature

def verify(message, signature, public_key:RSAKey) -> bool:
    """Check if the signature and the messages are equal using the public key"""
    message = message.encode('ascii')
    hash = int.from_bytes(sha512(message).digest(), byteorder='big')
    hashFromSignature = pow(signature, public_key.e, public_key.n)
    return hash == hashFromSignature
