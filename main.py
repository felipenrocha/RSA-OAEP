

from src.key_gen import KeyGen
from src.encryption import oaep_encode, oeaep_decode

import time

def main():
    

    bob = KeyGen()
    m = 'Hello World!'


    public_key = bob.get_public_key()
    prv_key = bob.get_private_key()

    message = m.encode("utf-8")
    emLen = public_key[1].bit_length() // 8
    a = oaep_encode(message, emLen)
    print(message,a)
    b = oeaep_decode(a, emLen)
    




if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s Total seconds ---" % (time.time() - start_time))
