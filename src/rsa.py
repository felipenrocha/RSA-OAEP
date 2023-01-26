from src.prime import get_prime, BITS
import src.modular_math as mod
import src.primitives as primitives
import random, os


# todo: remove this imports and do it myself
from Crypto.Math.Numbers import Integer
from Crypto.Util.asn1 import DerSequence, DerNull
from Crypto.PublicKey import (_create_subject_public_key_info)



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
        return self._n.size_in_bits()

    def _size_in_bytes(self):
        """The minimal amount of bytes that can hold the RSA modulus"""
        return (self._n.size_in_bits() - 1) // 8 + 1    

    
        

    def _encrypt(self, text):
        return pow(text, self.c, self.n)
    def _decrypt(self, cipher):
        if cipher > self.n:
            raise ValueError("Cipher too large")
        return pow(cipher, self.d, self.n)
    
    
    # calculating new keys
    def __generate_e(self):
        # choose e
        # 1) 2 < e < phi(n)
        # 2) has to be coprime with n and phi(n)
        while True:
            e = random.randrange(2**(BITS - 1), 2**(BITS))
            if mod.is_coprime(e, self.phi):
                return e
    def __generate_d(self, e):
        # choose d :
        # 1) d * e (mod phi(n)) == 1    or d = modular inverse of e and phi(n)    
        return mod.find_mod_inverse(e, self.phi)

    #  export function, TODO: write those functions myself
    def export_key(self, format='PEM', passphrase=None, randfunc=None):
        """
        Export this key
        Inputs:
            1. Format (String):
                - "PEM" - cifracao de texto
            2. Passphrase (string) (para chaves privadas): 
                - Chave usada para proteger a saída
            3. randfunc:
                Uma função de bytes aleatorios. Usado para exportação PEM
            
        Output:
            Byte string: A chave cifrada.
        """
        # check if using passphrase:
        if passphrase:
            passphrase = primitives.primitives.tobytes(passphrase)
        #  check randfunc

        if not randfunc:
            randfunc = os.urandom
            

        # obs.: couldnt do this function by myself= DerSequence, PCKS8 encoding, PEM encoding

        if not self.isPublic():
            binary_key = DerSequence([0,
                                      self.n,
                                      self.e,
                                      self.d,
                                      self.p,
                                      self.q,
                                      self.d % (self.p-1),
                                      self.d % (self.q-1),
                                      Integer(self.q).inverse(self.p)
                                      ]).encode()
            
            key_type = 'RSA PRIVATE KEY'
           
            # PKCS#8
            # TODO: this function
            from Crypto.IO import PKCS8

            if format == 'PEM':
                key_type = 'PRIVATE KEY'
                binary_key = PKCS8.wrap(binary_key, oid, None,
                                            key_params=DerNull())
            else:
                key_type = 'ENCRYPTED PRIVATE KEY'
                if not protection:
                    protection = 'PBKDF2WithHMAC-SHA1AndDES-EDE3-CBC'
                    binary_key = PKCS8.wrap(binary_key, oid,
                                            passphrase, protection,
                                            key_params=DerNull())
                    passphrase = None
        else:
            key_type = "PUBLIC KEY"
            binary_key = _create_subject_public_key_info(oid,
                                                         DerSequence([self.n,
                                                                      self.e]),
                                                         DerNull()
                                                         )

        if format == 'PEM':
            from Crypto.IO import PEM
            
            
            # no time to implement PEM Encode
            pem_str = PEM.encode(binary_key, key_type, passphrase, randfunc)
            return primitives.tobytes(pem_str)

oid = "1.2.840.113549.1.1.1"
