from src.prime import get_prime, BITS
import src.modular_math as mod
from src.primitives import BASE64Decoding, BASE64Encode, tobytes, totuple, tostr
import random, os, sys


# Author: Felipe Nascimento Rocha - Brasilia, Brazil, 2023


# inspired by: https://www.youtube.com/watch?v=oOcTVTpUsPQ and https://en.wikipedia.org/wiki/RSA_(cryptosystem)

class RSAKey:
    def __init__(self, p=0, q=0, e= 0, d = 0, modulus=0):
        #  setup key with params fixed
     
        self._e = 0
        self._d = 0
        # create new key
        if e == 0 and d == 0:
            # 1) Choose two large prime numbers p and q
            self.p = get_prime()
            self.q = get_prime()
            # 2) Compute n = pq
            self._n = self.p * self.q
            # 3) compute phi(n)
            self.phi = (self.p - 1) * (self.q-1)
            # 4) Choose an integer e such that 2 < e < phi(n) and gcd(e, phi(n)) = 1; that is, e and phi(n) are coprime
            self._e = self.__generate_e()
            # 5) Determine d as d ≡ e−1 (mod phi(n)); that is, d is the modular multiplicative inverse of e modulo phi(n)
            self._d = self.__generate_d(self._e)
        


        # private key case:
        elif e == 0 and ((d and modulus) != 0):
            self._d = d
            self._n = modulus
        # public key case:
        elif d == 0 and ((e and modulus) !=0):
            self._e = e
            self._n = modulus
        

    @property
    def n(self):
        return int(self._n)

    @property
    def e(self):
        return int(self._e)
    @property
    def d(self):
        return int(self._d)

    @property 
    def public_key(self):
        if self._e != 0:
            return RSAKey(e=self._e, modulus=self._n, d =0)
        else:
            raise ValueError("This is a private key, you cant get the public one.")  

    @property 
    def private_key(self):
        if self._d != 0:
            return RSAKey(d=self._d, modulus=self._n, p = self.p, q = self.q, e =0) 
        else:
            raise ValueError("This is a public key, you cant get the private one.")  
 

    def get_key(self):
        """Returns tuple of key (e, modulus) for public and (d, modulus) for private"""
        if self.isPublic():
            return (self.e, self.n)
        elif self.isPrivate():
            return (self.d, self.n)
        else:
            # return both
            return ((self.e, self.n), (self.d, self.n))
    def isPublic(self):
        """True if current key is a public one"""
        if self._d == 0:
            return True
        return False
 
    def isPrivate(self):
        """True if current key is a private one"""
        if self._e == 0:
            return True
        return False
    
    def _size_in_bits(self):
        """Size of the RSA modulus in bits"""
        return self._n.bit_length()

    def _size_in_bytes(self):
        """The minimal amount of bytes that can hold the RSA modulus"""
        return (self._n.bit_length()) // 8   

    
        

    def _encrypt(self, text):
        return pow(text, self.c, self.n)
    def _decrypt(self, cipher):
        if cipher > self.n:
            raise ValueError("Cipher too large")
        return pow(cipher, self.d, self.n)
    
    
    # calculating new keys
    def __generate_e(self):
        """ 
        Gera um valor para e
        # 1) 2 < e < phi(n)
        # 2) has to be coprime with n and phi(n)
        # """
        while True:
            e = random.randrange(2**(BITS - 1), 2**(BITS))
            if mod.is_coprime(e, self.phi):
                return e
    def __generate_d(self, e):
        """
        Gera um valor para d
        # choose d :
        # 1) d * e (mod phi(n)) == 1    or d = modular inverse of e and phi(n)
        #   """  
        return mod.find_mod_inverse(e, self.phi)

    def export_key(self):
        """
        Export this key
        Output:
            Byte string: A chave cifrada.

            Formato: 
            ----------- BEGIN KEY_TYPE KEY ---------------
                    (e,n)/(d,n) converted to base64
            ------------ END KEY_TYPE KEY ----------------
        """

        if not self.isPublic():            
            key_type = 'PRIVATE KEY'
            str = BASE64Encode(self.get_key(), key_type)
        else:
            key_type = "PUBLIC KEY"
            str = BASE64Encode(self.get_key(), key_type)
            

        return tobytes(str).decode('ascii')



def import_key(extern_key):
    """
    Import an RSA key (public or private). 
        that has this format:
        
            ----------- BEGIN KEY_TYPE KEY ---------------
                    (e,n)/(d,n) converted to base64
            ------------ END KEY_TYPE KEY ----------------
    """
    print(extern_key)
    # extern_key.encode('ascii')
    key_type = get_key_type(extern_key)
    keys_string = BASE64Decoding(extern_key, key_type) 
    key = totuple(keys_string)
    if key_type == "PUBLIC KEY":
        e, modulus = key
        return RSAKey(e=e, modulus=modulus)
    else:
        d, modulus = key
        return RSAKey(d=d, modulus=modulus)

def get_key_type(extern_key):
    if "PUBLIC KEY" in extern_key:
        return "PUBLIC KEY"
    else:
        return "PRIVATE KEY"