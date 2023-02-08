# RSA Signature Generator/Verifier (no Crypto packages)

Author: Felipe Nacimento Rocha

#### Execução:
Python >=3.10


```
        python main.py
```

#### Modules:
        1. Key Generation
        2. Key Exporting
        3. OAEP Encryption
        4. Signing/Verifyng
        5. Basic Encryption (Created by me i guess)
        6 . Interact with the key


#### Observation:

        Sometimes the OAEP Encryption/Decryption doesnt work with the generated key, i still
        haven't discovered what is causing this bug, so when this happen just generate another key,
        please.

         
#### Usage:
        Remember to export the key to use the other modules (Generate first to export it) and 
        then use it later to encrypt it or sign it. when exported the key is stored in a file 
        name "TYPE_KEY_key.pem".

        The RSA Key class uses a prime module to generate the primes p and q,
        to generate the primes we're using a low prime lists (primes up to 1000)
        to use with the miller rabin test.

        The Key exported is just a BASE64 encoding of the tuple that defines
        the key with"---BEGIN PUBLIC/PRIVATE KEY -----" in the beggining and
        "----- END KEY -----"  in the end.

        The OAEP was mainly developed following this: 
        https://www.inf.pucrs.br/~calazans/graduate/TPVLSI_I/RSA-oaep_spec.pdf.

        We're using SHA256 from hashlib as the hash function to the OAEP and sigining stage.

        The Signing/Veryfing was developed following the wikipedia page.


#### TODO Stuff:
        1. Parte I: Geração de chaves e cifra
        
                a. Geração de chaves (p e q primos com no mínimo de 1024 bits) (DONE)
                b. Cifração/decifração assimétrica RSA usando OAEP.  (DONE)    
        2.  Parte II: Assinatura
                a. Cálculo de hashes da mensagem em claro (função de hash SHA-3) (DONE)
                b. Assinatura da mensagem (cifração do hash da mensagem) (DONE)
                c. Formatação do resultado (caracteres especiais e informações para verificação em BASE64) (DONE)        
        3. Parte III: Verificação:
                a. Parsing do documento assinado e decifração da mensagem (de acordo com a formatação usada, no caso BASE64)  (DONE)
                b. Decifração da assinatura (decifração do hash) (DONE)
                c. Verificação (cálculo e comparação do hash do arquivo) (DONE)


