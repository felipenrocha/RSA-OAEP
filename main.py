

from src.rsa import RSAKey, import_key


import time

def main():
    

    bob = RSAKey()
    pub_key = bob.public_key
    # prv_key = bob.private_key
    exported = pub_key.export_key()
    print('exported key: ', pub_key.e)
    imported = import_key(exported)
    print('imported key = ', imported.e)
    m = 'Hello World!'





if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s Total seconds ---" % (time.time() - start_time))
