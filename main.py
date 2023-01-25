

from src.key_gen import KeyGen
from src.encryption import encrypt, decrypt


import time

def main():
    

    bob = KeyGen()
    m = 'Hello World!'


    public_key = bob.get_public_key()
    private_key = bob.get_private_key()

    print('Public Key:', public_key)
    print('Private Key:', private_key)
    print('Original Message:', m)
    c = encrypt(m, public_key)
    print('Criptogram:', c)
    m = decrypt(c, private_key)
    print('Message Decrypted', m)



if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s Total seconds ---" % (time.time() - start_time))
