

from src.rsa import RSAKey, import_key
from src.primitives import i2osp
from src.rsaes_oaep import basic_encryption, basic_decryption, oaep_encrypt, oaep_decrypt


import time

def main():
    print('--------------------------------------Key Generator Module--------------------------------------')
    # generate new key 1024 bits:
    bob = RSAKey(1024)


    # generate public key
    pub_key = bob.public_key
    # generate private key
    prv_key = bob.private_key
    print('Public Key: ', pub_key.get_key())
    print('Private Key: ', prv_key.get_key())

    print(SEPARATE_MODULES)
    print('--------------------------------------Export/Import Key Module--------------------------------------')

    # exporting keys:
    exported_pub_key = pub_key.export_key()
    with open('pub_key.pem', 'w') as f:
        f.write(exported_pub_key)
    exported_prv_key = prv_key.export_key()
    with open('prv_key.pem', 'w') as f:
        f.write(exported_prv_key)
    print('Exported Public Key: ', exported_pub_key)

    print(SEPARATE_MODULES)
    # importing keys:
    with open('pub_key.pem', 'r') as f:
        imported_pub_key = import_key(f.read())
        # use as key object from here ...
    with open('prv_key.pem', 'r') as f:
        imported_prv_key = import_key(f.read())
        # use as key object from here ...
    
    print(SEPARATE_MODULES)

    # encrypting and decrypting messages:
    print('--------------------------------------Basic Encryption Section--------------------------------------')

    message = "Hello World!"
    em = basic_encryption(pub_key=pub_key, M=message)
    print("Basic Encrypted Message: ", em)
    dm = basic_decryption(prv_key=prv_key ,C=em)
    print("Basic Decrypted Message: ", dm)


    print(SEPARATE_MODULES )
    

    print('--------------------------------------OAEP Encryption Section--------------------------------------')
    EM = oaep_encrypt(M=message, pub_key=pub_key)
    print("OAEP Encrypted Message: ", EM)
    DM = oaep_decrypt(C=EM, prv_key=prv_key)
    print("OAEP Decrypted Message: ",DM)





SEPARATE_MODULES = "-----------------------------------------------------------------------------------------------------------------------"


if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s Total seconds ---" % (time.time() - start_time))
