

from src.rsa import RSAKey, import_key
from src.primitives import i2osp
from src.rsaes_oaep import basic_encryption, basic_decryption


import time

def main():
    
    # generate new key:
    bob = RSAKey()

    # generate public key
    pub_key = bob.public_key
    # generate private key
    prv_key = bob.private_key


    # exporting keys:
    exported_pub_key = pub_key.export_key()
    with open('pub_key.pem', 'w') as f:
        f.write(exported_pub_key)
    exported_prv_key = prv_key.export_key()
    with open('prv_key.pem', 'w') as f:
        f.write(exported_prv_key)


    # importing keys:
    with open('pub_key.pem', 'r') as f:
        imported_pub_key = import_key(f.read())
        # use as key object from here ...
    

    with open('prv_key.pem', 'r') as f:
        imported_prv_key = import_key(f.read())
        # use as key object from here ...
    

    # encrypting and decrypting messages:
    message = "Hello World!"
    em = basic_encryption(pub_key=pub_key, M=message)
    print("Encrypted Message: ", em)
    dm = basic_decryption(prv_key=prv_key ,C=em)
    print("Decrypted Message: ", dm)

    
    # oaep section not working

    # EM = oaep_encode(M=message, emLen=emLen)
    # print("Encrypted Message: ", EM)
    # DM = oaep_decode(EM=EM)
    # print("Decrypted Message: ",DM)









if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s Total seconds ---" % (time.time() - start_time))
