

from src.rsa import RSAKey, import_key


import time

def main():
    

    bob = RSAKey()
    pub_key = bob.public_key
    prv_key = bob.private_key
    exported_pub = pub_key.export_key()
    print('exported public key: ', exported_pub)
    exported_prv = prv_key.export_key()
    print('exported private key: ', exported_prv)





if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s Total seconds ---" % (time.time() - start_time))
