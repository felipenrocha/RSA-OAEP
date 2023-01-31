
from src.rsaes_oaep import basic_encryption, basic_decryption, oaep_encrypt, oaep_decrypt
from src.signature import sign, verify

from src.rsa import RSAKey, import_key

def verification(pub_key:RSAKey, prv_key:RSAKey):
    print('--------------------------------------Signature/Verification Section--------------------------------------')

    s = input("Enter your signature: ")
    signature = sign(s, prv_key)
    message = input("Enter your signature again: ")

    if verify(message, signature, pub_key):
        print("Verification successfull\n\n")
    else:
        print("Verification failed\n\n")


def rsaoaep(pub_key:RSAKey, prv_key:RSAKey):
    print('--------------------------------------OAEP Encryption Section--------------------------------------')
    message = input("Message to encrypt: ")

    print("Original Message: ", message)

    print("Original Message: ", message)

    EM = oaep_encrypt(M=message, pub_key=pub_key)

    print("OAEP Encrypted Message: ", EM)


    DM = oaep_decrypt(C=EM, prv_key=prv_key)
    
    print("OAEP Decrypted Message: ",DM)

def basicEncryption(pub_key:RSAKey, prv_key:RSAKey):
    print('--------------------------------------Basic Encryption Section--------------------------------------')
    message = input("Message to encrypt: ")
    print("Original Message: ", message)

    em = basic_encryption(pub_key=pub_key, M=message)
    print("Basic Encrypted Message: ", em)
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

    # importing keys:
    with open('pub_key.pem', 'r') as f:
        imported_pub_key = import_key(f.read())
        # use as key object from here ...
    with open('prv_key.pem', 'r') as f:
        imported_prv_key = import_key(f.read())
        # use as key object from here ...

def wait_input():
    print(SEPARATE_MODULES)
    c = input()

def print_menu():
    print("1) Gerador de chave")
    print("2) Exportador/importador de chave")
    print("3) Cifração Básica")
    print("4) Assinatura e Verificação")
    print("5) Cifração/Decifração OAEP")
    print("6) Sair")
















SEPARATE_MODULES = "\n\n Enter to continue \n\n"

