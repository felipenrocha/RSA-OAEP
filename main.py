

from src.rsa import RSAKey, import_key
from src.primitives import i2osp
import src.interface as interface


import time

def main():
    start_time = time.time()
    bit_size = 1024

    print("generating new key with primes of size " + str(bit_size)+ " bits... (this can take a while)")
    key_pairs = RSAKey(bit_size)
    print("--- %s Total seconds ---" % (time.time() - start_time))

    pub_key = key_pairs.public_key
    # get private key
    prv_key = key_pairs.private_key
    print('Public Key: ', pub_key.get_key())
    print('Private Key: ', prv_key.get_key())
    interface.wait_input()

    # menu
    c = ''
    while c != '6':
        interface.print_menu()
        c = input("Selecione uma opção: ")
        if c == '1':
           
            print('--------------------------------------Key Generator Module--------------------------------------')
                    # generate new key 1024 bits:
                    
            print("generating new key with primes of size " + str(bit_size)+ " bits... (this can take a while)")

            key_pairs = RSAKey(bit_size)
            # get public key
            pub_key = key_pairs.public_key
            # get private key
            prv_key = key_pairs.private_key
            print('Public Key: ', pub_key.get_key())
            print('Private Key: ', prv_key.get_key())
        elif c == '2':
        # importing/exporting keys section:
            interface.import_export(pub_key=pub_key, prv_key=prv_key)   

        elif c == '3':
        # Basic Encrypting Section:
            interface.basicEncryption(pub_key=pub_key, prv_key=prv_key)
            
        elif c == '4':
            interface.verification(pub_key=pub_key, prv_key=prv_key)

        elif c == '5':
        # oaep section
            try:
                interface.rsaoaep(pub_key=pub_key, prv_key=prv_key)
            except:
                print("An error ocurred, int too big to convert.")
        elif c == '':
            continue     
        else:
            interface.print_menu()
            c = input("Selecione uma opção: ")






if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s Total seconds ---" % (time.time() - start_time))
