from src.prime_generation import get_prime, BITS
import random
import src.modular_math as mod
# inspired by: https://www.youtube.com/watch?v=oOcTVTpUsPQ
 

class KeyGen:
    def __init__(self,p=0, q=0):
        #  from: https://en.wikipedia.org/wiki/RSA_(cryptosystem)
        # 1) Choose two large prime numbers p and q
        self.p=p 
        self.q = q
        if p == 0 and q == 0:
            self.p = get_prime()
            self.q = get_prime()
        
        # 2) Compute n = pq
        self.n = self.p * self.q
        # 3) compute phi(n)
        self.phi = (self.p - 1) * (self.q-1)
        # 4) Choose an integer e such that 2 < e < phi(n) and gcd(e, phi(n)) = 1; that is, e and phi(n) are coprime
        e = self.__generate_e()
        self.public_key = (e, self.n)
        # print('public_key = ',self.public_key)
        # 5) Determine d as d ≡ e−1 (mod phi(n)); that is, d is the modular multiplicative inverse of e modulo phi(n)
        d = self.__generate_d(e)

        self.__private_key = (d, self.n)
        # public key: (e, n)

        # private key: (d, n)
        # print('private_key =', self.private_key)

    def get_public_key(self):
        return self.public_key

    def get_private_key(self):
        return self.__private_key
    
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
            