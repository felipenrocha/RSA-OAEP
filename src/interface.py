
from src.rsaes_oaep import basic_encryption, basic_decryption, oaep_encrypt, oaep_decrypt
from src.signature import sign, verify
from src.primitives import tobytes

from src.rsa import RSAKey, import_key

def verification():
    print('--------------------------------------Signature/Verification Section--------------------------------------')
    c = True
    while c:
        c = input("1) Generate signature\n2) Verify signature \n3) Go back ")
        if int(c) == 1:
            path = input("Type the path to your Private key: ")
            prv_key = import_key(path)
            s = input("Enter your message to be signed: ")
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
            s = input("Type the original Message: ")
            if verify(s, signature, pub_key):
                print("\n\nVerification was successuful.\n\n")
            else: 
                print("\n\nVerification failed.\n\n")
        elif int(c) == 3:
            break
        else: 
            print('Invalid option;')            
def rsaoaep():
    print('--------------------------------------OAEP Encryption Section--------------------------------------')
    inpt  = True
    while inpt:
        inpt = input("1) Encryption\n2) Decryption\nSelect one option: ")
        if int(inpt) == 1:
            path = input("Type the path to your Public key: ")
            pub_key = import_key(path)
            message = input("Message to encrypt: ")
            EM = oaep_encrypt(M=message, pub_key=pub_key)
            print("OAEP Encrypted Message: ",EM)
            export = input("1)Export\n2) Go back ")
            if int(export) == 1:
                with open('encrypted.txt', 'wb') as f:
                    f.write(EM)
        elif int(inpt) == 2:
            path = input("Type the path to your Private key: ")
            prv_key = import_key(path)
            path = input("Type the path to the encrypted file: ")
            with open(path, "rb") as f:
                 EM = f.read()
 

            DM = oaep_decrypt(C=EM, prv_key=prv_key)
            print("OAEP Decrypted Message: ",DM)
        else:
            break
def basicEncryption():
    print('--------------------------------------Basic Encryption Section--------------------------------------')
    
    
    inpt  = True
    while inpt:
        inpt = input("1) Encryption\n2) Decryption\nSelect one option: ")
        if int(inpt) == 1:
            path = input("Type the path of the signer's Public key: ")
            pub_key = import_key(path)
            message = input("Message to encrypt: ")
            em = basic_encryption(pub_key=pub_key, M=message)
            print("Basic Encrypted Message: ", em)
            export = input("1)Export\n2) Go back ")
            if int(export) == 1:
                with open('encrypted.txt', 'w') as f:
                    f.write(str(em))
                    
        if int(inpt) == 2:
            path = input("Type the path to your Private key: ")
            prv_key = import_key(path)
            em = int(input("Type the encrypted Message: "))
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
    print("2) Export last generated key")
    print("3) OAEP Encryption")
    print("4) Signing/Verifying")
    print("5) Basic Encryption")
    print("6) Import/Interact with key")
    print("7) Exit")
















SEPARATE_MODULES = "\n\n Enter to continue \n\n"

