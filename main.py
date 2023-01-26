

from src.rsa import RSAKey
from src.rsa_oaep import oaep_encode, oeaep_decode

import time

def main():
    

    bob = RSAKey()
    pub_key = bob.public_key
    # prv_key = bob.private_key
    print(pub_key.export_key())

    m = 'Hello World!'





if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s Total seconds ---" % (time.time() - start_time))
