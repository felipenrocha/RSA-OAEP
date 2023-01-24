from src.prime_generation import get_prime, BITS
import random
import src.modular_math as mod
# inspired by: https://www.youtube.com/watch?v=oOcTVTpUsPQ


 

class KeyGen:
    def __init__(self):
        #  from: https://en.wikipedia.org/wiki/RSA_(cryptosystem)
        # 1) Choose two large prime numbers p and q
        self.p = get_prime()
        self.q = get_prime()
        # 2) Compute n = pq
        self.n = self.p * self.q
        # 3) compute phi(n)
        self.phi = (self.p - 1) * (self.q-1)
        print("Done step 3")
        # 4) Choose an integer e such that 2 < e < phi(n) and gcd(e, phi(n)) = 1; that is, e and phi(n) are coprime
        self.e = self.__generate_e()
        print("Done step 4")
        self.public_key = (self.e, self.n)
        print('Public Key: ',self.public_key)
        # 5) Determine d as d ≡ e−1 (mod phi(n)); that is, d is the modular multiplicative inverse of e modulo phi(n)
        self.d = self.__generate_d()
        print("Done step 5")

        self.private_key = (self.d, self.n)
        # public key: (e, n)

        # private key: (d, n)
        print('Private Key: ', self.private_key)



    def __generate_e(self):
        # choose e
        # 1) 2 < e < phi(n)
        # 2) has to be coprime with n and phi(n)
        while True:
            e = random.randrange(2 ** (BITS - 1), 2 ** (BITS))
            if mod.is_coprime(e, self.phi) and mod.is_coprime(e, self.n):
                return e

    def __generate_d(self):
        # choose d :
        # 1) d * e (mod phi(n)) == 1    or d = modular inverse of e and phi(n)    
        return mod.find_mod_inverse(self.e, self.phi)
            
        