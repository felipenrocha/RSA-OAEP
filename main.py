

from src.rsa import RSAKey
from src.import_file import import_key
from src.rsa_oaep import oaep_encode, oeaep_decode

import time

def main():
    

    bob = RSAKey()
    pub_key = bob.public_key
    # prv_key = bob.private_key
    exported = pub_key.export_key(format="BASE64")
    print('key: ', exported)


    m = 'Hello World!'





if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s Total seconds ---" % (time.time() - start_time))
