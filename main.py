

from src.rsa import RSAKey, import_key
from src.primitives import i2osp
from src.rsaes_oaep import oaep_encode, oaep_decode


import time

def main():
    

    bob = RSAKey()
    pub_key = bob.public_key
    prv_key = bob.private_key
    message = "Hello World".encode('ascii')
   
    key_size = pub_key._size_in_bytes()
    EM = oaep_encode(M=message, emLen=key_size)








if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s Total seconds ---" % (time.time() - start_time))
