
separator = '#'


def encrypt(message, key):
    criptogram = ''
    for letter in message:
        m = ord(letter)
        criptogram += str(encrpyt_letter(m, key)) + separator
    return criptogram
def decrypt(criptogram, key):
    message = ''
    criptogram = criptogram.split(separator)
    for letter in criptogram: 
        if letter != '':
            c = int(letter)
            c = encrpyt_letter(c,key)
            message +=chr(c) 
    return message

def encrpyt_letter(m,key):
    # Encryption c = (letter ^ e/d) % n:
    a = int(key[0])
    n = int(key[1])
    return pow(m, a, n)

