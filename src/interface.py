
from src.rsaes_oaep import basic_encryption, basic_decryption, oaep_encrypt, oaep_decrypt
from src.signature import sign, verify

from src.rsa import RSAKey, import_key

def verification():
    print('--------------------------------------Signature/Verification Section--------------------------------------')
    c = True
    while c:
        c = input("1) Generate signature\n 2) Verify signature \n 3) Go back")
        if int(c) == 1:
            path = input("Type the path to your Private key: ")
            prv_key = import_key(path)
            s = input("Enter your signature: ")
            print("generating signature...")       
            signature = sign(s, prv_key)
            print("Signature generated: ", signature)
            with open('signature.txt', 'w') as f:
                f.write(signature)
            print("Exported signature to file signature.txt")
        elif int(c) == 2:
            path = input("Type the path of the signer's Public key: ")
            pub_key = import_key(path)
            path = input("Type the path to the signers signature: ")
            with open(path, 'r') as f:
                signature = f.read()
            s = input("Type the original signature: ")
            if verify(s, signature, pub_key):
                print("Verification was successuful.")
            else: 
                print("Verification failed.")
        elif int(c) == 3:
            break
        else: 
            print('Invalid option;')            
def rsaoaep():
    print('--------------------------------------OAEP Encryption Section--------------------------------------')
    path = input("Type the path to your Public key: ")
    pub_key = import_key(path)
    message = input("Message to encrypt: ")
    print("Original Message: ", message)
    EM = oaep_encrypt(M=message, pub_key=pub_key)
    print("OAEP Encrypted Message: ", EM)


    path = input("Type the path to your Private key: ")
    prv_key = import_key(path)
    DM = oaep_decrypt(C=EM, prv_key=prv_key)
    print("OAEP Decrypted Message: ",DM)
def basicEncryption():
    print('--------------------------------------Basic Encryption Section--------------------------------------')
    path = input("Type the path of the signer's Public key: ")
    pub_key = import_key(path)
    message = input("Message to encrypt: ")
    print("Original Message: ", message)
    em = basic_encryption(pub_key=pub_key, M=message)
    print("Basic Encrypted Message: ", em)


    path = input("Type the path to your Private key: ")
    prv_key = import_key(path)

    dm = basic_decryption(prv_key=prv_key ,C=em)
    print("Basic Decrypted Message: ", dm)
def import_export(pub_key:RSAKey, prv_key:RSAKey):
    print('--------------------------------------Export/Import Key Module--------------------------------------')

    exported_pub_key = pub_key.export_key()
    with open('pub_key.pem', 'w') as f:
        f.write(exported_pub_key)
    exported_prv_key = prv_key.export_key()
    with open('prv_key.pem', 'w') as f:
        f.write(exported_prv_key)
    print('Exported Public Key: \n', exported_pub_key)
    print('Exported Private Key: \n', exported_prv_key)

def key_values():
    path = input("Type the path of the key you want to see: ")
    key = import_key(path)
    c = True
    while c:
        print("1) See key pair values\n2) See Modulus\n3) See if its private or Public\n4) Go back")
        c = input("Select an option:")
        if int(c) == 1:
            print(key.get_key())
        elif int(c) == 2:
            print(key.n)
        elif int(c) == 3:
            if key.isPrivate():
                print("This is a private key")
            else:
                print("This is a public key")
        elif int(c) == 4:
            break
        else:
            print('Invalid option.')



def wait_input():
    print(SEPARATE_MODULES)
    c = input()
def print_menu():
    print("1) Key generator")
    print("2) Export Key")
    print("3) Basic Encryption")
    print("4) Signing/Verifying")
    print("5) OAEP Encryption")
    print("6) Interact with your key (read only)")
    print("7) Exit")
















SEPARATE_MODULES = "\n\n Enter to continue \n\n"

